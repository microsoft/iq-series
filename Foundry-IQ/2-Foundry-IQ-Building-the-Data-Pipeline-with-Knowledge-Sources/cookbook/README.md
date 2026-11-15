# Episode 2 Cookbook: Building the Data Pipeline with Knowledge Sources

This folder contains the hands-on cookbook for Episode 2 of The Foundry IQ Series.

## 📋 Prerequisites

- **Azure Subscription** with permissions to create resources and assign roles
- **Azure CLI** installed and configured ([Install guide](https://learn.microsoft.com/cli/azure/install-azure-cli))
- **Python 3.10+** installed
- A region that supports [agentic retrieval](https://learn.microsoft.com/azure/search/search-region-support) (default: `eastus2`)

## 🚀 Deploy Azure Resources

> **Note:** This deployment is shared across all Foundry IQ episodes. You only need to deploy once — if you've already deployed for another episode, skip this step and reuse your existing resources.

Deploy all required Azure resources with one click — this creates AI Search, Azure OpenAI, AI Services, a Foundry project, an AI Search connection, Azure Blob Storage, model deployments, and RBAC roles:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://aka.ms/iq-series/deploytoazure)

> **Automatic sample-data setup**
>
> The deployment seeds the NASA "Earth at Night" data and creates its knowledge source and knowledge base using a managed-identity Container Apps runner, without a shared-key storage mount. The runner becomes ready only after setup succeeds and scales to zero when idle. If setup fails, inspect the runner's console and system logs; see [deployment troubleshooting](../../../infra/README.md#one-click-deploy).

In the deployment form:

- **Create a new resource group** (e.g., `iq-series-rg`) — click **Create new** under the Resource group field. If you've already created one for a previous episode, select it instead
- Enter your **User Object ID** (see below)
- Customize the resource prefix, location, and SKUs

**How to get your User Object ID:** Open a terminal and run:

```bash
az ad signed-in-user show --query id -o tsv
```

This returns your Microsoft Entra ID unique identifier — paste it into the deployment form. It's needed to assign proper RBAC roles to your account.

After deployment, create a `.env` file **in this folder** (`2-Foundry-IQ-Building-the-Data-Pipeline-with-Knowledge-Sources/cookbook/.env`) with your values from the deployment outputs:

```env
SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AOAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com
AOAI_EMBEDDING_MODEL=text-embedding-3-large
AOAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AOAI_GPT_MODEL=gpt-5.4-mini
AOAI_GPT_DEPLOYMENT=gpt-5.4-mini
BLOB_CONNECTION_STRING=<your-blob-connection-string>
BLOB_CONTAINER_NAME=<your-container-name>
```

**Where to find these values:** All values are available in the deployment **Outputs** tab in the Azure portal. Copy `searchEndpoint`, `openAiEndpoint`, `blobConnectionString`, and `blobContainerName` directly from the outputs.

For CLI deployment and cleanup instructions, see the [Infrastructure Guide](../../../infra/README.md).

## 📓 Cookbook Notebook

The [**Foundry IQ Cookbook**](./foundry-iq-cookbook.ipynb) walks you through building the data pipeline with Knowledge Sources, step by step:

1. Understanding Knowledge Source types (indexed vs. remote)
2. Creating a search index and uploading sample product data
3. Creating an indexed Knowledge Source (Azure AI Search)
4. Creating a Blob Storage Knowledge Source (automated ingestion pipeline)
5. Creating a Web Knowledge Source (real-time public information)
6. Combining multiple sources in a single Knowledge Base
7. Querying across sources and inspecting the activity log
8. Security and governance considerations

### Quick Start

1. Install dependencies: `pip install -U azure-search-documents==12.1.0b1 azure-identity python-dotenv`
2. Sign in to Azure: run `az login` in a terminal
3. Create a `.env` file with your endpoint values (see the notebook for details)
4. Open `foundry-iq-cookbook.ipynb` in VS Code and run the cells

> **Running in GitHub Codespaces?** The devcontainer already installs all dependencies and the VS Code Jupyter extension automatically. Just open the `.ipynb` file directly in the VS Code editor — no need to install or launch a standalone Jupyter server. The notebook renders and runs natively inside VS Code.

## Additional Resources

- [Episode 2 README](../README.md)
- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Knowledge Sources Overview](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-source)
