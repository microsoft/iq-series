# Copilot Instructions for The IQ Series

## Project Overview

This repository is **The IQ Series** — a hands-on learning series for Microsoft IQ, Microsoft's unified intelligence layer for the enterprise. It covers three intelligence services:

- **Foundry IQ**: A managed knowledge layer for enterprise data (Azure AI Search + Foundry Agent Service)
- **Work IQ**: Intelligence layer for Microsoft 365 Copilot (coming soon)
- **Fabric IQ**: Business semantics for intelligent agents and decisions (coming soon)

## Repository Structure

- `1-Foundry-IQ-Unlocking-Knowledge-for-Agents/` — Episode 1: Core concepts, knowledge sources, knowledge bases, agentic retrieval
- `2-Foundry-IQ-Building-the-Data-Pipeline-with-Knowledge-Sources/` — Episode 2: Data pipelines, indexed/remote/web knowledge sources
- `3-Foundry-IQ-Querying-the-Multi-Source-AI-Knowledge-Bases/` — Episode 3: Multi-source querying and knowledge base composition
- `infra/` — Bicep and ARM templates for deploying all Azure resources
- Each episode has a `cookbook/` folder with Jupyter notebooks

## Key Azure Services

- **Azure AI Search** — Provides the search index and agentic retrieval capabilities
- **Azure OpenAI** — Hosts embedding (`text-embedding-3-large`) and chat (`gpt-5-mini`) model deployments
- **Azure AI Services (Foundry)** — The parent resource for Foundry projects
- **Foundry Project** — Hosts agents and connections
- **RBAC Roles** — Search Service Contributor, Search Index Data Contributor, Search Index Data Reader, Cognitive Services User

## SDK & API Patterns

- **Authentication**: Always use `DefaultAzureCredential` — never hardcode API keys
- **Environment variables**: Loaded from `.env` files using `python-dotenv`
- **Key packages**: `azure-search-documents`, `azure-ai-projects`, `azure-identity`
- **Agentic retrieval**: Knowledge sources → Knowledge bases → `KnowledgeBaseRetrievalClient.retrieve()`
- **Agent integration**: Knowledge bases expose an MCP endpoint at `{search_endpoint}/knowledgebases/{kb_name}/mcp`
- **Agent creation**: Use `AIProjectClient` with `MCPTool` pointing to the knowledge base MCP endpoint

## Foundry IQ Concepts

- **Knowledge Source**: A pointer to a search index — tells Foundry IQ *where* to find data
- **Knowledge Base**: Wraps knowledge sources with an LLM config — defines *how* queries are planned, executed, and synthesized
- **Agentic Retrieval**: Query planning → parallel sub-queries → semantic reranking → answer synthesis with citations
- **MCP Endpoint**: Each knowledge base exposes a Model Context Protocol endpoint for tool-based access by agents

## Conventions

- Markdown files use ATX-style headers (`#`, `##`, etc.)
- Code examples use Python 3.10+
- All Azure resource creation uses Bicep (not raw ARM templates)
- The ARM template (`azuredeploy.json`) is generated from Bicep via `az bicep build`
- Deploy to Azure button links use `https://aka.ms/iq-series/deploytoazure`
