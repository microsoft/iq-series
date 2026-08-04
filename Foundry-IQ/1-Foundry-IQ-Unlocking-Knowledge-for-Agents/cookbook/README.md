# Episode 1 Cookbook: Unlocking Knowledge for your Agents

This folder contains the hands-on cookbook for Episode 1 of The Foundry IQ Series.

## 📋 Prerequisites

- **Azure Subscription** with permissions to create resources and assign roles
- **Azure CLI** installed and configured ([Install guide](https://learn.microsoft.com/cli/azure/install-azure-cli))
- **Python 3.10+** installed
- A region that supports [agentic retrieval](https://learn.microsoft.com/azure/search/search-region-support) (default: `eastus2`)

## 🚀 Deploy Azure Resources

> **Note:** This deployment is shared across all Foundry IQ episodes. You only need to deploy once — if you've already deployed for another episode, skip this step and reuse your existing resources.

Deploy all required Azure resources with one click — this creates AI Search, Azure OpenAI, AI Services, a Foundry project, an AI Search connection, Azure Blob Storage, model deployments, and RBAC roles:

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://aka.ms/iq-series/deploytoazure)

> **⚠️ Troubleshooting: Deployment script failed?**
>
> Some Azure tenants enforce policies that block key-based access on storage accounts. This can cause the **data seeding script** to fail while all other resources deploy successfully. If this happens, your Azure resources are fully deployed — only the sample data and knowledge base setup is missing. You can seed the data manually using either of these alternatives:
>
> 1. **Run this cookbook**: Run this notebook end-to-end — it indexes the same NASA "Earth at Night" sample data to your AI Search and creates the knowledge source and knowledge base.
> 2. **Seed via Foundry IQ UI**: Create an index in AI Search manually using the [NASA Earth at Night dataset](https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/main/nasa-e-book/earth-at-night-json/documents.json), then create a knowledge source and knowledge base pointing to it through the Foundry IQ portal.

In the deployment form:

- **Create a new resource group** (e.g., `iq-series-rg`) — click **Create new** under the Resource group field. If you've already created one for a previous episode, select it instead
- Enter your **User Object ID**: run the following in a terminal to get it:

```bash
az login
az ad signed-in-user show --query id -o tsv
```
This returns your Microsoft Entra ID unique identifier — paste it into the deployment form. It's needed to assign proper RBAC roles to your account.

- Customize the resource prefix, location, and SKUs

After deployment, create a `.env` file **in this folder** (`1-Foundry-IQ-Unlocking-Knowledge-for-Agents/cookbook/.env`) with your values from the deployment outputs:

```env
SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AOAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com
AOAI_EMBEDDING_MODEL=text-embedding-3-large
AOAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AOAI_GPT_MODEL=gpt-5-mini
AOAI_GPT_DEPLOYMENT=gpt-5-mini
FOUNDRY_PROJECT_ENDPOINT=https://<your-ai-services>.services.ai.azure.com/api/projects/<your-project>
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-5-mini
AZURE_AI_SEARCH_CONNECTION_NAME=iq-series-search-connection
FOUNDRY_PROJECT_RESOURCE_ID=/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.MachineLearningServices/workspaces/<workspace>/projects/<project>
```

**Where to find these values:** All values except `FOUNDRY_PROJECT_RESOURCE_ID` are available in the deployment **Outputs** tab in the Azure portal. To find the project resource ID, go to [Microsoft Foundry](https://ai.azure.com) → your project → **Overview** → **Properties** and copy the full ARM resource ID.

For CLI deployment and cleanup instructions, see the [Infrastructure Guide](../../../infra/README.md).

## 📓 Cookbook Notebook

The [**Foundry IQ Cookbook**](./foundry-iq-cookbook.ipynb) walks you through Foundry IQ end-to-end, step by step:

1. Creating a knowledge source backed by an Azure AI Search index
2. Creating a knowledge base that pairs your data with an LLM for agentic retrieval
3. Querying the knowledge base and inspecting synthesized answers with citations
4. Connecting Foundry IQ to the Foundry Agent Service so an agent can ground its responses in your data

### Quick Start

1. Install dependencies: `pip install -U azure-search-documents==12.1.0b1 azure-ai-projects azure-identity python-dotenv`
2. Sign in to Azure: run `az login` in a terminal
3. Create a `.env` file with your endpoint values (see above)
4. Open `foundry-iq-cookbook.ipynb` in VS Code and run the cells

### Learn with Copilot

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://aka.ms/iq-series/learnwithcopilot)

Launch a Codespace and start exploring Foundry IQ with GitHub Copilot. Copilot connects to your deployed knowledge base via MCP. Ask questions about your data and get grounded, cited answers.

1. Click the button above to open a Codespace
2. Open `.vscode/mcp.json` and replace the two placeholders with your values from the deployment **Outputs** tab:
   - `<your-search-service>` → your AI Search service name
   - `<your-search-api-key>` → your AI Search admin API key
3. **Enable the foundry-iq tool (important!):** Open **Copilot Chat**, click the **🔧 Tools** icon at the top of the chat panel. Scroll through the tool list and find **foundry-iq** — toggle it **on**. If you skip this step, Copilot won't be able to query your knowledge base.
4. Ask Copilot questions about your knowledge base, try these:

   - *"What does Earth look like at night from space?"*
   - *"How do scientists use nighttime lights to study urbanization?"*
   - *"What are the brightest regions on Earth at night and why?"*

5. Open any cookbook notebook and use Copilot to help you learn and experiment:

   - *"Explain what this notebook does step by step"*
   - *"What is a knowledge source vs a knowledge base?"*
   - *"Help me create a new knowledge base with a different index"*

> You can also use the repo locally. Clone the repo, open in VS Code, update `.vscode/mcp.json` with your values, and the MCP server appears in Copilot Chat Tools.

## Additional Resources

- [Episode 1 README](../README.md)
- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Agentic Retrieval Quickstart](https://learn.microsoft.com/azure/search/search-get-started-agentic-retrieval)
