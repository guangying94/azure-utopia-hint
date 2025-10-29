# Azure Utopia Hint
Getting stuck in Azure Utopia? Here are some hints to help you navigate through the challenges.

## General Guidelines
The tasks are about building an API with LLMs. Building the API is not the main challenge; the main challenge is to figure out how to expose the LLM capabilities through the API effectively in Azure.

A simple and effective solution is often better than a complex one. Leverage Azure native Platform-As-A-Service (PaaS) offerings wherever possible to minimize infrastructure management overhead.

Containers is a good candidate for hosting the API. One way to do this is to use Azure Container Apps, which allows you to deploy containerized applications without managing the underlying infrastructure.

General steps to follow:
1. Write the API code.
2. Containerize the application using Docker - create a Dockerfile and build the image.
3. Push the Docker image to a container registry like Azure Container Registry (ACR).
4. Deploy the container to Azure Container Apps. Configure the right settings, such as environment variables, scaling options, and networking.
5. Azure Container Apps provides a public URL for the deployed API. Test the deployed API to ensure it works as expected.

## Specific Hints for Each Task
### Azure Resource Creation
- Use Azure CLI or Azure Portal to create resources.
- You can launch Azure Cloud Shell directly to write and execute Azure CLI commands. Here is the link: [Azure Cloud Shell](https://shell.azure.com/).
- Refer to [./setup/README.md](./setup/README.md) for detailed instructions on setting up the required Azure resources.

### Stage 1
This stage is about creating an image using Generative AI. There are plenty of free tools available online that can help you generate images using AI models. Refer to [./stage1/README.md](./stage1/README.md) for more details.

### Stage 2
This stage is about creating a RAG (Retrieval-Augmented Generation) application. RAG is getting popular and there are many tools out that provide out of the box solutions. Refer to [./stage2/README.md](./stage2/README.md) for more details.

### Stage 3
This stage is about creating a machine learning model, and expose the trained model as a tool for LLMs. This is an interesting approach where statistical machine learning meet Generative AI. Refer to [./stage3/README.md](./stage3/README.md) for more details.

### Stage 4
This stage is about leveraging multi-modal capabilities of LLMs. Multi-modal models can process and generate content in multiple formats, such as text, images, and audio. Refer to [./stage4/README.md](./stage4/README.md) for more details.

### Stage 5
This stage is about leveraging LLM to connect to database and perform operations. Refer to [./stage5/README.md](./stage5/README.md) for more details.