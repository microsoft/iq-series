<h1 align="center">Web IQ</h1>

**Microsoft Web IQ** is Microsoft's agent-native grounding service for the public web. It's a suite of AI-native APIs that give agents and applications **ranked, citation-ready context** from across the web — web pages, news, images, and videos — designed for direct injection into an LLM's context window. Web IQ is built on 20+ years of Bing search infrastructure and re-architected for LLMs and multi-step agents.

Where **Foundry IQ** unlocks your organization's curated knowledge, **Work IQ** brings in how people work, and **Fabric IQ** adds business semantics, **Web IQ** grounds agents in fresh, real-world information from *outside* your enterprise — today's news, the latest product release, the current version of a public doc page.

This folder contains the Web IQ episodes of The Microsoft IQ Series, including hands-on Jupyter notebook cookbooks with step-by-step guidance.

> **👉 New here? Start with Episode 1.** Follow the [Get Started](#-get-started) steps below to get an API key, then open the [Episode 1 cookbook](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) and run it end-to-end.

## Passage-only learning path

For users with passage-only Web IQ access, the [passage-only learning path](./Passage-Only/README.md) provides a separate, standalone [Python cookbook](./Passage-Only/cookbook/web-iq-passage-only-cookbook.ipynb). It covers Web Search with `contentFormat: "passage"`, Images, Videos, and grounded answers with citations. Images and Videos use their native metadata responses rather than a content format.

This path leaves the broader Episode 1 cookbook unchanged.

## 📚 Episodes

| **Episode**                                                                                                          | **Description**                                                                 | **Video**     | **Cookbook**                                                                              |
|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|---------------|--------------------------------------------------------------------------------------------|
| [Web IQ: Grounding Agents with Real-Time Web Search](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/README.md) | Explore every Web IQ API — Web, News, Images, Videos, Browse, and Auto — then ground a model's answer in live sources with citations and connect Web IQ as an MCP server | Coming soon 🎥 | [Cookbook](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) |

## ✨ Why Web IQ

| | |
|---|---|
| ⚡ **Speed** | **164 ms P95** latency — about 2.5× faster than today's best alternative — so multi-step agent chains stay responsive |
| 🎯 **Quality** | Highest grounding satisfaction, validated against benchmarks including DeepSearchQA, grounding satisfaction, and freshness. Results are ranked for relevance, freshness, and authority — not just a list of links |
| 🪙&nbsp;**Efficiency** | Passage-level retrieval surfaces only the most relevant text, so you send **fewer tokens per query** and lower the cost of every call |
| 📚 **Content** | Combines **licensed sources, structured data, and the open web** — not SERP scraping |
| 🌍 **Global** | Coverage across **100+ languages and markets** |
| 🔌 **Open** | REST, **MCP** (JSON-RPC 2.0), and SDKs — model-agnostic, with no inference lock-in |

## 🧰 What's in Web IQ

| API | Endpoint | What it returns |
|---|---|---|
| **Web Search** | <code>POST&nbsp;/search/web</code> | Ranked passages with freshness signals (`crawledAt`, `lastUpdatedAt`). Full-document formats (`text`, `html`, `markdown`) require full-document access. Supports `site:` operators, language/region, and location |
| **News Search** | <code>POST&nbsp;/search/news</code> | Trusted news from the **last 14 days**, with publisher, content, and thumbnail |
| **Images Search** | <code>POST&nbsp;/search/images</code> | Images with generated captions and host pages; filter by aspect ratio, size, color, and watermark |
| **Videos Search** | <code>POST&nbsp;/search/videos</code> | Videos with AI summaries, embeddable players, and optional **moments** that deep-link to the most relevant segment |
| **Browse** | <code>POST&nbsp;/browse</code> | Extracted content from a specific URL, with **on-demand live crawl** for pages not yet indexed. Requires full-document access |
| **Auto (Beta)** | <code>POST&nbsp;/auto</code> | Typed evidence (text, images, videos, weather, time zones, and more) with **result-scoped citations** in a single call |

All endpoints live at `https://api.microsoft.ai/v3/`, share one error schema, and are also available as tools on the **Web IQ MCP server** at `https://api.microsoft.ai/v3/mcp`.

## 🔌 Ways to Integrate

- **REST API** — `POST` a JSON body with an `x-apikey` header (or an Entra ID bearer token). Works from any language.
- **MCP server** — Plug Web IQ into VS Code, GitHub Copilot, or any MCP-compatible agent framework over Streamable HTTP.
- **SDKs** — See [SDKs and Libraries](https://webiq.microsoft.ai/documentation/sdk/?view=md) for official packages.
- **Playground** — Build requests interactively in the [Web IQ Playground](https://webiq.microsoft.ai/playground/) and copy generated code in cURL, Python, JavaScript, C#, Java, Go, or Ruby.

## 🤔 Web IQ vs. Grounding with Bing

**Grounding with Bing** is designed for integrated web augmentation experiences inside Microsoft Foundry Agent Service, and remains available for existing customers as an accessible entry point.

**Web IQ** is purpose-built for AI agents and multi-step workflows. It returns structured, citation-ready, passage-level content **directly to the developer**, giving you fine-grained control over retrieval, orchestration, and how results are used in your LLM workflow.

## 🚀 Get Started

### 1. Prerequisites

- **A paid Azure subscription and a Web IQ resource** — Passage-only access is publicly available. [Create a Web IQ billing resource in the Azure portal](https://learn.microsoft.com/en-us/web-iq/get-started/deploy-azure-portal), then connect it in the [Web IQ portal](https://webiq.microsoft.ai/) to get an App ID. Azure credits cannot be used for Web IQ.
- **An API key** — In the [Web IQ Portal → Profile Management](https://webiq.microsoft.ai/profiles/), select **Create API Key**. The same page shows your per-second quota (default: **15 QPS**) and which services your profile can call.
- **Python 3.10+** installed
- *(Optional)* **Full-document access** for the format comparison and Browse examples. See [Passages and content formats](https://learn.microsoft.com/en-us/web-iq/concepts/content-formats) for defaults, limits, and how to request access. The grounded-answer step can optionally use a model in a Microsoft Foundry project.

### 2. Run the Cookbook

The cookbook notebook lives in the [`1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/`](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) folder and includes prerequisites, setup, and step-by-step instructions:

1. [Episode 1 cookbook](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) — Grounding Agents with Real-Time Web Search

## 🔗 Learn More

- 🌐 [Microsoft Web IQ](https://webiq.microsoft.ai/)
- 📖 [Documentation overview](https://webiq.microsoft.ai/documentation/overview/)
- 📖 [Quick Start](https://webiq.microsoft.ai/documentation/quick-start/?view=md)
- 📖 [Authentication](https://webiq.microsoft.ai/documentation/authentication/?view=md)
- 📖 [MCP Server](https://webiq.microsoft.ai/documentation/mcp/?view=md)
- 📖 [Error Handling](https://webiq.microsoft.ai/documentation/error-handling/?view=md)
- 📖 [Supported Languages and Regions](https://webiq.microsoft.ai/documentation/supported-languages-and-regions/?view=md)
- 📖 [Instrumentation](https://webiq.microsoft.ai/documentation/instrumentation/?view=md)
- 📖 [FAQ](https://webiq.microsoft.ai/documentation/faq/?view=md)
- 🧾 [OpenAPI specification](https://webiq.microsoft.ai/documentation/openapi.json)
- 🛟 [Web IQ Support](https://aka.ms/microsoft-webiq-support)
- 💬 Ask your questions in our [Discussions](https://aka.ms/iq/discussions)
