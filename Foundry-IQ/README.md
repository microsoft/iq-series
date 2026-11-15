<h1 align="center">Foundry IQ</h1>

**Foundry IQ** is about Unlocking Knowledge for your Agents; connecting structured and unstructured data across Azure, SharePoint, OneLake, and the web so agents can access permission-aware knowledge.

This folder contains the Foundry IQ episodes of The Microsoft IQ Series, including hands-on Jupyter notebook cookbooks with step-by-step guidance.

> **👉 New here? Start with Episode 1.** Follow the [Get Started](#-get-started) steps below to deploy your Azure resources, then open the [Episode 1 cookbook](./1-Foundry-IQ-Unlocking-Knowledge-for-Agents/cookbook/) and run it end-to-end. Episodes build on each other, so working through them in order (1 → 2 → 3) gives you the smoothest learning path.

## 📚 Episodes

| **Episode**                                                                                                                          | **Description**                                                                    | **Video**       | **Cookbook**                                                                         |
|--------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-----------------|-------------------------------------------------------------------------------------|
| [Foundry IQ: Unlocking Knowledge for your Agents](./1-Foundry-IQ-Unlocking-Knowledge-for-Agents/README.md)                                    | Understand Foundry IQ's core components and how it fits into the agent architecture | [Watch Now 🎥](https://aka.ms/iq-series/episode1)     | [Cookbook](./1-Foundry-IQ-Unlocking-Knowledge-for-Agents/cookbook/)                |
| [Foundry IQ: Building the Data Pipeline with Knowledge Sources](./2-Foundry-IQ-Building-the-Data-Pipeline-with-Knowledge-Sources/README.md)      | Learn how different content enters Foundry IQ from various sources                 | [Watch Now 🎥](https://aka.ms/iq-series/episode2)     | [Cookbook](./2-Foundry-IQ-Building-the-Data-Pipeline-with-Knowledge-Sources/cookbook/) |
| [Foundry IQ: Querying the Multi-Source AI Knowledge Bases](./3-Foundry-IQ-Querying-the-Multi-Source-AI-Knowledge-Bases/README.md)                | Dive into Knowledge Bases and multi-source query paths                             | [Watch Now 🎥](https://aka.ms/iq-series/episode3)     | [Cookbook](./3-Foundry-IQ-Querying-the-Multi-Source-AI-Knowledge-Bases/cookbook/)      |

## 🚀 Get Started

### 1. Deploy to Azure

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://aka.ms/iq-series/deploytoazure)

Click the button above to deploy all required Azure resources: AI Search, Azure OpenAI, a Foundry project, Azure Blob Storage, and seeded sample data with a ready-to-use knowledge base.

In the deployment form:

- **Create a new resource group** (e.g., `iq-series-rg`): click **Create new** under the Resource group field
- Enter your **User Object ID**: run the following in a terminal to get it:

```bash
az login
az ad signed-in-user show --query id -o tsv
```

- Customize the resource prefix, location, and SKUs as needed, then click **Review + create**

Once deployment completes, copy the **Azure AI Search endpoint** and **API key** from the deployment **Outputs** tab. You'll need them in the next step.

> **Automatic sample-data setup**
>
> The deployment seeds the NASA "Earth at Night" data and creates its knowledge source and knowledge base using a managed-identity Container Apps runner, without a shared-key storage mount. The runner becomes ready only after setup succeeds and scales to zero when idle. If setup fails, inspect the runner's console and system logs; see [deployment troubleshooting](../infra/README.md#one-click-deploy).

### 2. Learn with Copilot

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

### 3. Run the Cookbooks

The cookbook notebooks **reuse the same Azure resources** you deployed in Step 1 — you do **not** need to redeploy for each episode. Each cookbook folder needs its own `.env` file with your endpoint values:

1. Go to the Azure portal → your deployment → **Outputs** tab
2. Create a `.env` file inside the episode's `cookbook/` folder (e.g., `1-Foundry-IQ-Unlocking-Knowledge-for-Agents/cookbook/.env`)
3. Paste the values from the Outputs tab — see each cookbook's README for the exact variables needed

> **📍 Where does the `.env` file go?** Each episode's `cookbook/` folder expects its own `.env` file. The notebooks load it with `dotenv` relative to the notebook's location.
