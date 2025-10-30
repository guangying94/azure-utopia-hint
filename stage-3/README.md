# How to expose custom ML model as a tool for LLMs
An agent consists of 3 things to derive the output.
1. An LLM model - the brain
2. A set of tools - the actions
3. knowledge base - the context, conversation history etc

With the above in mind, an agent can then be invoked to perform tasks that require reasoning and tool usage, whether it's autonomously or with user input.

# How to train the machine learning model
Before exposing your custom ML model as a tool for LLMs, you need to train and deploy your ML model. As the dataset is not huge, you can train the model locally using popular ML frameworks like Scikit-learn, TensorFlow, PyTorch etc. For larger dataset, you can use Azure Machine Learning service to train and deploy your ML model at scale. Here's a [tutorial](https://learn.microsoft.com/en-us/azure/machine-learning/overview-what-is-azure-machine-learning?view=azureml-api-2) to get started with Azure Machine Learning.

If you plan to train the model locally, leverage the code assistant to write the training code for you. A typical machine learning project follows the steps below:
1. Understand the dataset and define the problem statement (what to predict).
2. Identify the features and label/target column.
3. Identify the suitable machine learning algorithm (classification, regression etc).
4. Preprocess the data (handle missing values, categorical variables, scaling etc).
5. Split the dataset into training and testing sets.
6. Train the model using the training set.
7. Evaluate the model performance using the testing set.
8. Save the trained model to a file for deployment.

Here's an example prompt you can use:

```text
I have a dataset in CSV format for a classification problem. Write me a sample code using Python and Scikit-learn to train a machine learning model, evaluate its performance, and save the trained model to a file using joblib.
```

There are few ways to expose your custom ML model as a tool for LLMs.

### Option 1: Expose the model as an API endpoint using Low Code approach
You can deploy your custom ML model as a HTTP REST API, using services like Azure Container Apps, and enable tool usage in Azure AI Foundry agent by using [OpenAPI defined tools](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/openapi-spec).

Another option is to use Azure Logic Apps to expose your custom ML model as an API endpoint, and then integrate it with Azure AI Foundry agent using [Azure AI Foundry Agent Service Logic App Connector](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/logic-apps?pivots=portal).

### Option 2: Expose the model as an API endpoint using Pro Code approach
If pro-code is preferred, you can use Azure AI Foundry Python SDK to create a custom tool that invokes your custom ML model. Here's a [tutorial](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/function-calling?pivots=python) on how to create a custom tool using Python SDK.