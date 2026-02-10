# Foundry IQ End-to-End Cookbook

## Overview

A concise, hands-on cookbook that walks you through the entire Foundry IQ lifecycle in a single Jupyter notebook — from creating a search index to querying a knowledge base to grounding a Foundry agent in your data. This cookbook complements the [IQ Series episodes](../README.md#learning-episodes) by combining all the concepts into one runnable guide.

* **🚀 [Run the cookbook](./sample/foundry-iq-cookbook.ipynb)**

## What You'll Learn

- Create a **knowledge source** backed by an Azure AI Search index
- Create a **knowledge base** that pairs your data with an LLM for agentic retrieval
- **Query the knowledge base** and inspect synthesized answers with citations
- Connect Foundry IQ to the **Foundry Agent Service** so an agent can ground its responses in your data

## Getting Started

1. Copy `sample/sample.env` to `sample/.env` and fill in your Azure endpoints.
2. Install dependencies:
   ```bash
   pip install -r sample/requirements.txt
   ```
3. Open `sample/foundry-iq-cookbook.ipynb` and run cells top to bottom.

See the notebook's **Prerequisites** section for detailed Azure setup instructions.

## 📂 Sample Code

Explore the implementation in the 📂 [Cookbook Sample](./sample/) folder.

## 🔗 Additional Learning Resources

- 📚 Microsoft Foundry Documentation: [Learn more](https://learn.microsoft.com/azure/ai-foundry/)
- 📚 Agentic Retrieval Quickstart: [Get started](https://learn.microsoft.com/azure/search/search-get-started-agentic-retrieval)
- 📚 Foundry Agent Service: [Build agents](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/ai-search)
- 💬 Join the Discussion: Ask your questions on our [Discord channel](https://discord.gg/REmjGvvFpW)

### 🚀 Dive deeper with the IQ Series episodes: [Episode 1: Unified Knowledge Layer](../1-Foundry-IQ-Unified-Knowledge-Layer-for-Agents/), [Episode 2: Data Pipelines](../2-Foundry-IQ-Building-the-Data-Pipeline-with-Knowledge-Sources/), and [Episode 3: Multi-Source Queries](../3-Foundry-IQ-Querying-the-Multi-Source-AI-Knowledge-Bases/)!
