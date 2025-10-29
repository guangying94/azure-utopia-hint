# Useful Azure Resources
The following Azure resources can be helpful as you work through the tasks in Azure Utopia:
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
- [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-intro)
- [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/overview)

The following guide uses Azure CLI, bash commands can be run in [Azure Cloud Shell](https://shell.azure.com/).

## Create Resource Group
### Azure CLI
```bash
# Variables - adjust as needed
RESOURCE_GROUP="utopia"
LOCATION="southeastasia"

# Create Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION
```

## Deploy Azure AI Foundry
### Azure CLI
```bash
# Variables - adjust as needed
FOUNDRY_NAME="gtutopiadev"
PROJECT_NAME="utopia-project"

# Create Azure AI Foundry account
az cognitiveservices account create -n $FOUNDRY_NAME -g $RESOURCE_GROUP --custom-domain $FOUNDRY_NAME --location $LOCATION --kind AIServices --sku S0

# List available models
az cognitiveservices account list-models -n $FOUNDRY_NAME -g $RESOURCE_GROUP | jq '.[] | { name: .name, format: .format, version: .version, sku: .skus[0].name, capacity: .skus[0].capacity.default }'

# Deploy GPT-4.1 model
az cognitiveservices account deployment create -n $FOUNDRY_NAME -g $RESOURCE_GROUP --deployment-name gpt-4.1 --model-name gpt-4.1 --model-version 2025-04-14 --model-format OpenAI --sku-capacity 1 --sku-name GlobalStandard

# Once done, navigate to Azure AI Foundry in Azure Portal (https://ai.azure.com) to create a project and add the deployed model to the project.
```


## Azure Container Registry
### Azure CLI
```bash
# Variables - adjust as needed
ACR_NAME="utopiaacr"

# Create Azure Container Registry
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# Get ACR credentials
az acr credential show \
    --name $ACR_NAME \
    --resource-group $RESOURCE_GROUP
```

## Azure Container Apps
### Azure CLI
```bash
# Ensure the Container Apps extension is available
az extension add --name containerapp --upgrade

# Variables - update as needed
RESOURCE_GROUP="utopia"
LOCATION="southeastasia"
LOG_ANALYTICS_WORKSPACE="utopia-law"
CONTAINERAPPS_ENVIRONMENT="utopia-env"
CONTAINERAPP_NAME="hello-aca"
INGRESS_PORT=8000

# Log Analytics (required for Container Apps diagnostics)
az monitor log-analytics workspace create \
  --resource-group $RESOURCE_GROUP \
  --workspace-name $LOG_ANALYTICS_WORKSPACE \
  --location $LOCATION

WORKSPACE_ID=$(az monitor log-analytics workspace show \
  --resource-group $RESOURCE_GROUP \
  --workspace-name $LOG_ANALYTICS_WORKSPACE \
  --query customerId -o tsv)

WORKSPACE_KEY=$(az monitor log-analytics workspace get-shared-keys \
  --resource-group $RESOURCE_GROUP \
  --workspace-name $LOG_ANALYTICS_WORKSPACE \
  --query primarySharedKey -o tsv)

# Container Apps environment
az containerapp env create \
  --name $CONTAINERAPPS_ENVIRONMENT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --logs-destination log-analytics \
  --logs-workspace-id $WORKSPACE_ID \
  --logs-workspace-key $WORKSPACE_KEY

# Hello-world container (simple Python HTTP server on port 8000)
az containerapp create \
  --name $CONTAINERAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINERAPPS_ENVIRONMENT \
  --image docker.io/library/python:3.9-slim \
  --ingress external \
  --target-port $INGRESS_PORT \
  --transport auto \
  --min-replicas 1 \
  --max-replicas 1 \
  --command '["python","-m","http.server","8000"]'

# Get the FQDN of the deployed Container App
az containerapp show \
  --name $CONTAINERAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  -o tsv
```