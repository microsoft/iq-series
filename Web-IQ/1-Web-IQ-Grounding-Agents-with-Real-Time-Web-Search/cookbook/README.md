# Episode 1 Cookbook: Grounding Agents with Real-Time Web Search

This folder contains the hands-on cookbook for Episode 1 of The Web IQ Series.

## 📋 Prerequisites

- **Azure subscription** with a [basic or standard Foundry Agent Service environment](https://learn.microsoft.com/azure/ai-foundry/agents/environment-setup)
- **Foundry User** role on the Foundry project to create and run agents
- **Python 3.10+** installed
- A **model deployment** that supports the web search tool (e.g., `gpt-5-mini`) — `gpt-4o-mini` and GPT-5 reasoning models are **not** supported for Grounding with Bing Search
- Azure CLI installed and signed in (`az login`), used by `DefaultAzureCredential`

> **💡 No new infrastructure needed.** Unlike Foundry IQ, the web search tool doesn't require an Azure AI Search index, a knowledge source, or a knowledge base. If you already deployed a Foundry project for the Foundry IQ episodes, reuse it here.

## 🔧 Setup

Create a `.env` file **in this folder** (`1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/.env`):

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-ai-services>.services.ai.azure.com/api/projects/<your-project>
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-5-mini
```

**Where to find these values:** In [Microsoft Foundry](https://ai.azure.com) → your project → **Overview**, copy the **Project endpoint**. `FOUNDRY_MODEL_DEPLOYMENT_NAME` is the name of a deployed chat model that supports the web search tool.

## 📓 Cookbook Notebook

The [**Web IQ Cookbook**](./web-iq-cookbook.ipynb) walks you through grounding an agent in the live web, step by step:

1. Creating a Foundry agent with the `WebSearchTool` attached
2. Asking the agent a time-sensitive question and streaming the response
3. Inspecting the inline URL citations returned alongside the answer
4. Restricting the web search to a location, and cleaning up the agent afterward

### Quick Start

1. Install dependencies: `pip install -U azure-ai-projects azure-identity python-dotenv`
2. Sign in to Azure: run `az login` in a terminal
3. Create a `.env` file with your endpoint values (see above)
4. Open `web-iq-cookbook.ipynb` in VS Code and run the cells

### Learn with Copilot

Open any cookbook notebook and use Copilot Chat to help you learn and experiment:

- *"Explain what this notebook does step by step"*
- *"What's the difference between the web search tool and Grounding with Bing Search?"*
- *"Help me restrict this agent's web search to a specific country"*

## Additional Resources

- [Episode 1 README](../README.md)
- [Web search tool documentation](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/web-search)
- [Grounding with Bing Search terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal)
