# Episode 3 Cookbook: Querying the Multi-Source AI Knowledge Bases

This folder contains the hands-on cookbook and MCP connection guides for Episode 3 of The IQ Series.

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

The [**Foundry IQ Cookbook**](./foundry-iq-cookbook.ipynb) walks you through querying multi-source Knowledge Bases, step by step:

1. Creating a multi-source Knowledge Base (indexed + web)
2. Querying with **minimal** reasoning effort (fastest, no LLM planning)
3. Querying with **low** reasoning effort (LLM query planning + source selection)
4. Querying with **medium** reasoning effort (iterative retrieval with refinement)
5. Comparing effort levels side by side
6. Answer synthesis with inline citations
7. Connecting via MCP (configuration examples below)

### Quick Start

1. Install dependencies: `pip install -U azure-search-documents==11.7.0b2 azure-identity python-dotenv`
2. Create a `.env` file with your endpoint values (see the notebook for details)
3. Open `foundry-iq-cookbook.ipynb` in VS Code or Jupyter and run the cells

---

## Connect to a Knowledge Base via MCP

Once you've created a [knowledge base](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base) on your Azure AI Search service, it exposes an **MCP (Model Context Protocol) endpoint** that any MCP-compatible client can connect to. The endpoint follows this pattern:

```
https://<your-search-service>.search.windows.net/knowledgebases/<your-kb-name>/mcp?api-version=2025-11-01-preview
```

The examples below show how to connect to a Foundry IQ knowledge base from popular MCP clients.

> **Note:** Replace `<your-search-service>`, `<your-kb-name>`, and `<your-query-key>` with your actual values. If your knowledge base includes a [remote SharePoint knowledge source](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-sharepoint-remote), you must also include the `x-ms-query-source-authorization` header with a valid bearer token scoped to `https://search.azure.com/.default`.

---

### Claude Desktop

Edit `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`).

Claude Desktop does not natively support remote SSE servers with custom headers. Use the [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) proxy to bridge the connection:

```json
{
  "mcpServers": {
    "my-kb": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://<your-search-service>.search.windows.net/knowledgebases/<your-kb-name>/mcp?api-version=2025-11-01-preview",
        "--header", "api-key: <your-query-key>"
      ]
    }
  }
}
```

Restart Claude Desktop after saving the file.

---

### GitHub Copilot in VS Code

Create or edit `.vscode/mcp.json` in your workspace root:

```json
{
  "servers": {
    "my-kb": {
      "type": "sse",
      "url": "https://<your-search-service>.search.windows.net/knowledgebases/<your-kb-name>/mcp?api-version=2025-11-01-preview",
      "headers": {
        "api-key": "<your-query-key>"
      }
    }
  }
}
```

> **Tip:** To avoid checking secrets into source control, use VS Code input variables for the API key:
>
> ```json
> {
>   "inputs": [
>     {
>       "type": "promptString",
>       "id": "search-api-key",
>       "description": "Azure AI Search query API key",
>       "password": true
>     }
>   ],
>   "servers": {
>     "my-kb": {
>       "type": "sse",
>       "url": "https://<your-search-service>.search.windows.net/knowledgebases/<your-kb-name>/mcp?api-version=2025-11-01-preview",
>       "headers": {
>         "api-key": "${input:search-api-key}"
>       }
>     }
>   }
> }
> ```

---

### GitHub Copilot CLI

Edit `~/.copilot/mcp-config.json` (user-level) or `.copilot/mcp-config.json` (repo-level):

```json
{
  "mcpServers": {
    "my-kb": {
      "url": "https://<your-search-service>.search.windows.net/knowledgebases/<your-kb-name>/mcp?api-version=2025-11-01-preview",
      "headers": {
        "api-key": "<your-query-key>"
      }
    }
  }
}
```

---

### Foundry Agent Service

To connect a knowledge base to an agent in the **Foundry Agent Service**, follow the official guide which covers creating a project connection, configuring the MCP tool, and invoking the agent:

📚 [Connect Foundry IQ to Foundry Agent Service](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/foundry-iq-connect?view=foundry&tabs=foundry%2Cpython)

---

## Additional Resources

- [Episode 3 README](../README.md)
- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Agentic Retrieval Quickstart](https://learn.microsoft.com/azure/search/search-get-started-agentic-retrieval)
- [Knowledge Base Overview](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base)
