# How to build RAG solution using Azure AI Foundry
An easy option is to build the RAG solution using Azure AI Foundry Agent Service file search tool. Here's the [tutorial](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/file-search-agent) to create a file search agent.

## How to expose the agent as an API
Invoking an agent is different from consuming a regular LLM endpoint. In high level, consuming an agent involves the following steps:
1. Create a thread (Conversation).
2. Insert message into this thread, both user message and system message.
3. Start a thread run to let the agent process the messages.
4. Poll the thread run status until it is completed.
5. Get the response message from the completed thread run.

### Pro Code
You can either use code to create agent in Azure AI Foundry, or simply use the Azure AI Foundry Portal to create the agent visually.

Refer to the sample code on how to invoke the agent using Python SDK. The code is written by GitHub Copilot, using GPT-5-Codex. The following example uses container, however, you are fre to use any services that can host API endpoints, such as Azure App Service, Azure Functions etc.

```text
Refer to microsoft learn documentation for sample code using microsoft learn MCP server (microsoft.docs.mcp). I have an agent created in Azure AI foundry. write me a sample code using python, which is an based on fast API, accept a post request, then it will invoke this agent in Azure ai foundry using the assistant ID, poll the result, get the response, and return the result. then, write me the dockerfile that allows me to deploy this as a container to azure container apps as external API service.
```

Here's the step to deploy the API as a container to Azure Container Apps:
1. Create the container image using the Dockerfile.
   ```bash
    docker build -t your-image-name:tag .
    ```
2. Push the container image to Azure Container Registry (ACR).
   ```bash
    docker login your-acr-name.azurecr.io -u your-username
    docker tag your-image-name:tag your-acr-name.azurecr.io/your-image-name:tag
    docker push your-acr-name.azurecr.io/your-image-name:tag
    ```
3. Create an Azure Container App using the container image from ACR, following the [quickstart guide](https://learn.microsoft.com/en-us/azure/container-apps/quickstart-portal).

### Low Code
Another option is to leverage Azure Logic Apps to expose the agent as an API. Here is a [tutorial](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/triggers) on how to integrate Azure AI Foundry agent with Logic Apps.

You can add a HTTP trigger to the Logic App to expose it as an API endpoint. Inside the Logic App workflow, you can add an action to invoke the Azure AI Foundry agent, passing in the necessary parameters from the HTTP request. Finally, you can return the agent's response as the HTTP response.