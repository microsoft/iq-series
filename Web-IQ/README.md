<h1 align="center">Web IQ</h1>

**Microsoft Web IQ** is Microsoft's agent-native grounding service for the public web. It's a suite of AI-native APIs that give agents and applications **ranked, citation-ready context** from across the web — web pages, news, images, and videos — designed for direct injection into an LLM's context window. Web IQ is built on 20+ years of Bing search infrastructure and re-architected for LLMs and multi-step agents.

Where **Foundry IQ** unlocks your organization's curated knowledge, **Work IQ** brings in how people work, and **Fabric IQ** adds business semantics, **Web IQ** grounds agents in fresh, real-world information from *outside* your enterprise — today's news, the latest product release, the current version of a public doc page.

This folder contains the Web IQ episodes of The Microsoft IQ Series, including hands-on Jupyter notebook cookbooks with step-by-step guidance.

> **👉 New here? Start with Episode 1.** Follow the [Get Started](#-get-started) steps below to get an API key, then open the [Episode 1 cookbook](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) and run it end-to-end.

## 📚 Episodes

| **Episode**                                                                                                          | **Description**                                                                 | **Video**     | **Cookbook**                                                                              |
|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|---------------|--------------------------------------------------------------------------------------------|
| [Web IQ: Grounding Agents with Real-Time Web Search](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/README.md) | Explore every Web IQ API — Web, News, Images, Videos, Browse, and Auto — then ground a model's answer in live sources with citations and connect Web IQ as an MCP server | Coming soon 🎥 | [Cookbook](./1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/cookbook/) |

## ✨ Why Web IQ

| | |
|---|---|
| ⚡ **Speed** | **164 ms P95** latency — about 2.5× faster than today's best alternative — so multi-step agent chains stay responsive |
| 🎯 **Quality** | Highest grounding satisfaction, validated against benchmarks including DeepSearchQA, grounding satisfaction, and freshness. Results are ranked for relevance, freshness, and authority — not just a list of links |
| 🪙 **Efficiency** | Passage-level retrieval surfaces only the most relevant text, so you send **fewer tokens per query** and lower the cost of every call |
| 📚 **Content** | Combines **licensed sources, structured data, and the open web** — not SERP scraping |
| 🌍 **Global** | Coverage across **100+ languages and markets** |
| 🔌 **Open** | REST, **MCP** (JSON-RPC 2.0), and SDKs — model-agnostic, with no inference lock-in |

## 🧰 What's in Web IQ

| API | Endpoint | What it returns |
|---|---|---|
| **Web Search** | `POST /search/web` | Ranked web pages as `passage`, `text`, `html`, or `markdown`, with freshness signals (`crawledAt`, `lastUpdatedAt`). Supports `site:` operators, language/region, and location |
| **News Search** | `POST /search/news` | Trusted news from the **last 14 days**, with publisher, snippet, and thumbnail |
| **Images Search** | `POST /search/images` | Images with generated captions and host pages; filter by aspect ratio, size, color, and watermark |
| **Videos Search** | `POST /search/videos` | Videos with AI summaries, embeddable players, and **moments** that deep-link to the most relevant segment |
| **Browse** | `POST /browse` | Extracted content from a specific URL, with **on-demand live crawl** for pages not yet indexed |
| **Auto (Beta)** | `POST /auto` | Typed evidence (text, images, videos, weather, time zones, and more) with **result-scoped citations** in a single call |

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

- **Web IQ access** — Web IQ is currently in **limited access** for select enterprise customers building AI agents and applications at scale, prioritized for organizations working with Microsoft account teams. Request access at [webiq.microsoft.ai](https://webiq.microsoft.ai/).
- **An API key** — In the [Web IQ Portal → Profile Management](https://webiq.microsoft.ai/profiles/), select **Create API Key**. The same page shows your quota and which services your profile can call.
- **Python 3.10+** installed
- No Azure subscription or infrastructure deployment is required — Web IQ is a standalone, hosted service. *(The cookbook's optional grounded-answer step can use a model in a Microsoft Foundry project.)*

> 💡 **Can't verify your invitation code?** The invitation is usually tied to a different address than the one you sign in with. Open [portal.azure.com](https://portal.azure.com), check the address shown under your name in the top-right corner, and reply to your invitation email with that address.

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
