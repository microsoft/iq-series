# Episode 1 Cookbook: Unlocking Knowledge for your Agents

This folder contains the hands-on cookbook for Episode 1 of The IQ Series.

## 📋 Prerequisites

- **Azure Subscription** with permissions to create resources and assign roles
- **Azure CLI** installed and configured ([Install guide](https://learn.microsoft.com/cli/azure/install-azure-cli))
- **Python 3.10+** installed
- A region that supports [agentic retrieval](https://learn.microsoft.com/azure/search/search-region-support) (default: `eastus2`)

## 🚀 Deploy Azure Resources

> **Note:** This deployment is shared across all Foundry IQ episodes. You only need to deploy once — if you've already deployed for another episode, skip this step and reuse your existing resources.

Deploy all required Azure resources with one click — this creates AI Search, Azure OpenAI, AI Services, a Foundry project, an AI Search connection, model deployments, and RBAC roles:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://aka.ms/iq-series/deploytoazure)

In the deployment form:

- **Create a new resource group** (e.g., `iq-series-rg`) — click **Create new** under the Resource group field. If you've already created one for a previous episode, select it instead
- Enter your **User Object ID** (see below)
- Customize the resource prefix, location, and SKUs

**How to get your User Object ID:** Open a terminal and run:

```bash
az ad signed-in-user show --query id -o tsv
```

This returns your Microsoft Entra ID unique identifier — paste it into the deployment form. It's needed to assign proper RBAC roles to your account.

After deployment, create a `.env` file in this folder with your values from the deployment outputs:

```env
SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AOAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com
AOAI_EMBEDDING_MODEL=text-embedding-3-large
AOAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AOAI_GPT_MODEL=gpt-4o-mini
AOAI_GPT_DEPLOYMENT=gpt-4o-mini
FOUNDRY_PROJECT_ENDPOINT=https://<your-ai-services>.services.ai.azure.com/api/projects/<your-project>
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_AI_SEARCH_CONNECTION_NAME=iq-series-search-connection
```

**Where to find these values:** All values are available in the deployment **Outputs** tab in the Azure portal. You can also find them in [Microsoft Foundry](https://ai.azure.com) → your project → **Overview**.

For CLI deployment and cleanup instructions, see the [Infrastructure Guide](../../infra/README.md).

## 📓 Cookbook Notebook

The [**Foundry IQ Cookbook**](./foundry-iq-cookbook.ipynb) walks you through Foundry IQ end-to-end, step by step:

1. Creating a knowledge source backed by an Azure AI Search index
2. Creating a knowledge base that pairs your data with an LLM for agentic retrieval
3. Querying the knowledge base and inspecting synthesized answers with citations
4. Connecting Foundry IQ to the Foundry Agent Service so an agent can ground its responses in your data

### Quick Start

1. Install dependencies: `pip install -U azure-search-documents==11.6.0b13 azure-ai-projects azure-identity python-dotenv`
2. Create a `.env` file with your endpoint values (see above)
3. Open `foundry-iq-cookbook.ipynb` in VS Code or Jupyter and run the cells

## Additional Resources

- [Episode 1 README](../README.md)
- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Agentic Retrieval Quickstart](https://learn.microsoft.com/azure/search/search-get-started-agentic-retrieval)
