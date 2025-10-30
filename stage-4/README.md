# Multi-modal LLMs
Large Language Models (LLMs) are evolving to handle multiple modalities beyond just text, such as images, audio, and video. This stage focuses on leveraging these multi-modal capabilities to build applications that can process input with different formats.

Azure OpenAI models like GPT-4o, GPT-4.1, GPT-5 etc can handle multi-modal inputs. You can follow the tutorial here to get started: [Use vision-enabled chat models](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/gpt-with-vision?tabs=python).

As the request is coming in as a image_url, you don't need to handle the image processing part. The model will take care of it. You just need to pass the image URL in the message content.

Inspect the instruction carefully. You can either use pro-code or low-code approach to build the solution. For pro-code approach, you can use Azure AI Foundry Python SDK to create the agent, just like previous stages. For low-code approach, you can consider to use Azure Logic Apps to create the REST API that invokes HTTP request to models in Azure AI Foundry. 