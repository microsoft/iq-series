<h1 align="center">The Microsoft IQ Series</h1>

<p align="center">
  <img src="./images/IQ-Banner-v2.jpg" alt="The IQ Series Banner" />
</p>

Master Microsoft IQ with The IQ Series! Microsoft IQ is Microsoft's unified intelligence layer for the enterprise, bringing together three core intelligence services:

- **Foundry IQ**: A managed knowledge layer for enterprise data; connecting structured and unstructured data across Azure, SharePoint, OneLake, and the web so agents can access permission-aware knowledge.
- **Work IQ**: The intelligence layer that personalizes Microsoft 365 Copilot; understanding context, relationships, and work patterns so agents can be faster, more accurate, and more secure.
- **Fabric IQ**: Unify business semantics across data, models, and systems to power intelligent agents and decisions grounded in a live, holistic view of the business.

Together, these IQs enable AI agents to reason, retrieve, and act with deep business context going beyond traditional RAG for true enterprise intelligence.

> **Note:** The series kicks off with **Foundry IQ** episodes. Work IQ and Fabric IQ content is coming soon!

📺 Foundry IQ episodes premiere **every Wednesday at 9 AM PT**, starting **March 18, 2026** on [Microsoft Developer YouTube](https://aka.ms/iq-series).

## 📚 Episodes

| **Episode**                                                                                                                          | **Description**                                                                    | **Video**       | **Cookbook**                                                                         |
|--------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-----------------|-------------------------------------------------------------------------------------| 
| [Foundry IQ: Unlocking Knowledge for your Agents](./1-Foundry-IQ-Unlocking-Knowledge-for-Agents/README.md)                                    | Understand Foundry IQ's core components and how it fits into the agent architecture | [Mar 18, 2026](https://aka.ms/iq-series/episode1)     | [Cookbook](./1-Foundry-IQ-Unlocking-Knowledge-for-Agents/cookbook/)                |
| [Foundry IQ: Building the Data Pipeline with Knowledge Sources](./2-Foundry-IQ-Building-the-Data-Pipeline-with-Knowledge-Sources/README.md)      | Learn how different content enters Foundry IQ from various sources                 | [Mar 25, 2026](https://aka.ms/iq-series/episode2)     | [Cookbook](./2-Foundry-IQ-Building-the-Data-Pipeline-with-Knowledge-Sources/cookbook/) |
| [Foundry IQ: Querying the Multi-Source AI Knowledge Bases](./3-Foundry-IQ-Querying-the-Multi-Source-AI-Knowledge-Bases/README.md)                | Dive into Knowledge Bases and multi-source query paths                             | [Apr 1, 2026](https://aka.ms/iq-series/episode3)     | [Cookbook](./3-Foundry-IQ-Querying-the-Multi-Source-AI-Knowledge-Bases/cookbook/)      |
| Work IQ                                                                                                                              | Coming soon!                                                                       |                 |                                                                                     |
| Fabric IQ                                                                                                                            | Coming soon!                                                                       |                 |                                                                                     |

### Episode Format

Each episode includes:

- **Introduction (1 min)**: Executive speech
- **Tech Talk (15 min)**: Interactive discussion with Product Group + Advocacy
- **Close-out (1 min)**: Doodle summary

Episode folders also include Jupyter notebook cookbooks with hands-on, step-by-step guidance.

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

### 2. Learn with Copilot

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://aka.ms/iq-series/learnwithcopilot)

Launch a Codespace and start exploring Foundry IQ with GitHub Copilot. Copilot connects to your deployed knowledge base via MCP. Ask questions about your data and get grounded, cited answers.

1. Click the button above to open a Codespace
2. Open `.vscode/mcp.json` and replace the two placeholders with your values from the deployment **Outputs** tab:
   - `<your-search-service>` → your AI Search service name
   - `<your-search-api-key>` → your AI Search admin API key
3. Open **Copilot Chat**, click the **🔧 Tools** icon — **foundry-iq** should now appear. Enable it
4. Ask Copilot questions about your knowledge base, try these:

   - *"What does Earth look like at night from space?"*
   - *"How do scientists use nighttime lights to study urbanization?"*
   - *"What are the brightest regions on Earth at night and why?"*

4. Open any cookbook notebook and use Copilot to help you learn and experiment:

   - *"Explain what this notebook does step by step"*
   - *"What is a knowledge source vs a knowledge base?"*
   - *"Help me create a new knowledge base with a different index"*

> You can also use the repo locally. Clone the repo, open in VS Code, update `.vscode/mcp.json` with your values, and the MCP server appears in Copilot Chat Tools.

## 🙏 Get Involved

We'd love to see you contributing to our repo and engaging with the experts with your questions!

- 🤔 Do you have suggestions or have you found spelling or code errors? [Raise an issue](https://github.com/microsoft/iq-series/issues) or [Create a pull request](https://github.com/microsoft/iq-series/pulls).
- 🚀 If you get stuck or have any questions about Microsoft IQ, join our [Discord](https://aka.ms/iq-series/discord).
- Check out [Contributing](./CONTRIBUTING.md) & [Trademarks](./TRADEMARKS.md) details.
