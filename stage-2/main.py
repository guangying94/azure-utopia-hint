"""FastAPI proxy for invoking an Azure AI Foundry agent run.

This sample follows the Azure AI Foundry quickstart guidance:
https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart#configure-and-run-an-agent
"""

import os
import time
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.core.exceptions import HttpResponseError


POLL_DELAY_SECONDS = float(os.environ.get("RUN_POLL_DELAY_SECONDS", "1.0"))
MAX_WAIT_SECONDS = float(os.environ.get("RUN_MAX_WAIT_SECONDS", "120.0"))

# Mandatory environment configuration.
try:
	PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
	ASSISTANT_ID = os.environ["AZURE_AI_ASSISTANT_ID"]
except KeyError as exc:
	missing = exc.args[0]
	raise RuntimeError(
		f"Missing required environment variable: {missing}. "
		"Ensure the service is configured before starting."
	) from exc


credential = DefaultAzureCredential()
project_client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)

app = FastAPI(title="Azure AI Foundry Agent Proxy", version="0.1.0")


class InvokeRequest(BaseModel):
	prompt: str = Field(..., description="End-user prompt passed to the agent.")
	session_metadata: Optional[Dict[str, str]] = Field(
		default=None,
		description="Optional metadata (string key/value pairs) added to the thread.",
	)


class InvokeResponse(BaseModel):
	status: str
	run_id: str
	thread_id: str
	response_text: str


@app.get("/healthz", tags=["probes"])
def health_check() -> Dict[str, str]:
	return {"status": "ok"}


@app.post("/invoke", response_model=InvokeResponse, tags=["agent"])
def invoke_agent(request: InvokeRequest) -> InvokeResponse:
	try:
		metadata = (
			{key: str(value) for key, value in request.session_metadata.items()}
			if request.session_metadata
			else None
		)
		thread = project_client.agents.threads.create(metadata=metadata)

		project_client.agents.messages.create(
			thread_id=thread.id, role="user", content=request.prompt
		)

		run = project_client.agents.runs.create(
			thread_id=thread.id, agent_id=ASSISTANT_ID
		)

		elapsed = 0.0
		while run.status in {"queued", "in_progress", "requires_action"}:
			if elapsed >= MAX_WAIT_SECONDS:
				raise TimeoutError(
					f"Run {run.id} exceeded {MAX_WAIT_SECONDS} seconds without completing."
				)
			time.sleep(POLL_DELAY_SECONDS)
			elapsed += POLL_DELAY_SECONDS
			run = project_client.agents.runs.get(thread_id=thread.id, run_id=run.id)

		if run.status != "completed":
			raise RuntimeError(
				f"Run ended in status '{run.status}'. Last error: {run.last_error}"
			)

		messages: List = list(project_client.agents.messages.list(thread_id=thread.id))
		assistant_messages = [message for message in messages if message.role == "assistant"]
		if not assistant_messages:
			raise RuntimeError("Agent completed but returned no assistant messages.")

		final_message = assistant_messages[-1]
		text_chunks = []
		for content in getattr(final_message, "content", []):
			if getattr(content, "type", "") == "text" and getattr(content, "text", None):
				text_chunks.append(content.text.value)
		response_text = "\n\n".join(text_chunks)

		return InvokeResponse(
			status=run.status,
			run_id=run.id,
			thread_id=thread.id,
			response_text=response_text,
		)
	except (HttpResponseError, TimeoutError, RuntimeError) as exc:
		raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.on_event("shutdown")
def shutdown_event() -> None:
	project_client.close()
	credential.close()
