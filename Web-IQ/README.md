<h1 align="center">Web IQ</h1>

**Microsoft Web IQ** is Microsoft's agent-native grounding service for the public web. It's a suite of AI-native APIs that give agents and applications **ranked, citation-ready context** from across the web — web pages, news, images, and videos — designed for direct injection into an LLM's context window. Web IQ is built on 20+ years of Bing search infrastructure and re-architected for LLMs and multi-step agents.

Where **Foundry IQ** unlocks your organization's curated knowledge, **Work IQ** brings in how people work, and **Fabric IQ** adds business semantics, **Web IQ** grounds agents in fresh, real-world information from *outside* your enterprise — today's news, the latest product release, the current version of a public doc page.

This folder contains the Web IQ episodes of The Microsoft IQ Series, including hands-on Jupyter notebook cookbooks with step-by-step guidance.

> **👉 New here? Start with Episode 1.** Follow the [Get Started](#-get-started) steps below to get an API key, then open the [Episode 1 cookbook](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) and run it end-to-end.

## 📚 Episodes

| **Episode**                                                                                                          | **Description**                                                                 | **Video**     | **Cookbook**                                                                              |
|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|---------------|--------------------------------------------------------------------------------------------|
| [Web IQ: Grounding Agents with Real-Time Web Search](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/README.md) | Explore Web IQ APIs — Web, News, Images, Videos, Places, Browse, and Auto — then ground a model's answer in live sources with citations and connect Web IQ as an MCP server | [Watch Now 🎥](https://youtu.be/5O7ZsSHhzpg) | [Cookbook](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) |

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
| **Auto** | <code>POST&nbsp;/auto</code> | Typed evidence (text, images, videos, weather, time zones, and more) with **result-scoped citations** in a single call |
| **Web Search** | <code>POST&nbsp;/search/web</code> | Ranked passages with freshness signals (`crawledAt`, `lastUpdatedAt`). Full-document formats (`text`, `html`, `markdown`) require full-document access. Supports `site:` operators, language/region, and location |
| **News Search** | <code>POST&nbsp;/search/news</code> | Trusted news from the **last 14 days**, with publisher, content, and thumbnail |
| **Images Search** | <code>POST&nbsp;/search/images</code> | Images with generated captions and host pages; filter by aspect ratio, size, color, and watermark |
| **Videos Search** | <code>POST&nbsp;/search/videos</code> | Videos with AI summaries, embeddable players, and optional **moments** that deep-link to the most relevant segment |
| **Places Search** | <code>POST&nbsp;/search/places</code> | Structured place information, including addresses, opening hours, reviews, photos, and query-relevant passages. Does not require full-document access |
| **Browse** | <code>POST&nbsp;/browse</code> | Extracted content from a specific URL, with **on-demand live crawl** for pages not yet indexed. Passages for every AppID; full documents need full-document access |
| **Commerce Search (Private Preview)** | <code>POST&nbsp;/search/commerce/products</code> | Ranked products and seller offers for a product query |
| **Commerce Offers (Private Preview)** | <code>POST&nbsp;/fetch/commerce/products/offers</code> | Seller offers for product, SKU, or representative-offer identifiers returned by Commerce Search |
| **Commerce Product Details (Private Preview)** | <code>POST&nbsp;/fetch/commerce/products/details</code> | Product name, description, and aggregate rating for product or SKU identifiers returned by Commerce Search |

Places and Auto are generally available. All endpoints live at `https://api.microsoft.ai/v3/` and share one error schema. For the tools available on the **Web IQ MCP server** at `https://api.microsoft.ai/v3/mcp`, use `tools/list` with your profile.

> **Commerce is in Private Preview and is not available on all accounts.** Access is limited to select Azure customers, isn't guaranteed, and the API contract may change. The cookbook's three Commerce examples are optional and skipped unless you set `COMMERCE_ACCESS = True` after access is enabled for your AppID. See the [Commerce API reference and access-request guidance](https://learn.microsoft.com/en-us/web-iq/reference/commerce).

## 🔌 Ways to Integrate

- **REST API** — `POST` a JSON body with an `x-apikey` header (or an Entra ID bearer token). Works from any language.
- **MCP server** — Plug Web IQ into VS Code, GitHub Copilot, or any MCP-compatible agent framework over Streamable HTTP.
- **SDKs** — See [SDKs](https://learn.microsoft.com/en-us/web-iq/integrations/sdk) for official packages.
- **Playground** — Build requests interactively in the [Web IQ Playground](https://webiq.microsoft.ai/playground/) and copy generated code in cURL, Python, JavaScript, C#, Java, Go, or Ruby.

## 🤔 Web IQ vs. Grounding with Bing

**Grounding with Bing** is designed for integrated web augmentation experiences inside Microsoft Foundry Agent Service, and remains available for existing customers as an accessible entry point.

**Web IQ** is purpose-built for AI agents and multi-step workflows. It returns structured, citation-ready, passage-level content **directly to the developer**, giving you fine-grained control over retrieval, orchestration, and how results are used in your LLM workflow.

## 🚀 Get Started

### 1. Prerequisites

- **A paid Azure subscription and a Web IQ resource** — Passage-only access is publicly available. [Create a Web IQ billing resource in the Azure portal](https://learn.microsoft.com/en-us/web-iq/get-started/deploy-azure-portal), then connect it in the [Web IQ Developer Portal](https://webiq.microsoft.ai/) to get an App ID. Azure credits cannot be used for Web IQ.
- **An API key** — In the Web IQ Developer Portal's [Profile Management](https://webiq.microsoft.ai/profiles/), select **Create API Key**. The same page shows your per-second quota (default: **15 QPS**) and which services your profile can call.
- **Python 3.10+** installed
- *(Optional)* **Full-document access** for the format comparison and the full-document Browse example. See [Passages and content formats](https://learn.microsoft.com/en-us/web-iq/concepts/content-formats) for defaults, limits, and how to request access. The grounded-answer step can optionally use a model in a Microsoft Foundry project.

### 2. Run the Cookbook

The cookbook notebook lives in the [`1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/`](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) folder and includes prerequisites, setup, and step-by-step instructions:

1. [Episode 1 cookbook](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) — Grounding Agents with Real-Time Web Search

## 🔗 Learn More

- 🌐 [Microsoft Web IQ](https://webiq.microsoft.ai/)
- 📖 [Documentation overview](https://learn.microsoft.com/en-us/web-iq/overview)
- 📖 [Quick Start](https://learn.microsoft.com/en-us/web-iq/get-started/quickstart)
- 📖 [Authentication](https://learn.microsoft.com/en-us/web-iq/get-started/authentication)
- 📖 [MCP Server](https://learn.microsoft.com/en-us/web-iq/integrations/mcp)
- 📖 [Error Handling](https://learn.microsoft.com/en-us/web-iq/reference/error-handling)
- 📖 [Supported Languages and Regions](https://learn.microsoft.com/en-us/web-iq/reference/supported-languages-regions)
- 📖 [Instrumentation](https://learn.microsoft.com/en-us/web-iq/guides/instrumentation)
- 📖 [FAQ](https://learn.microsoft.com/en-us/web-iq/resources/faq)
- 🧾 [OpenAPI specification](https://webiq.microsoft.ai/documentation/openapi.json)
- 🛟 [Web IQ Support](https://aka.ms/microsoft-webiq-support)
- 💬 Ask your questions in our [Discussions](https://aka.ms/iq/discussions)
