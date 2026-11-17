# Episode 1: Web IQ: Grounding Agents with Real-Time Web Search

📂 [Try the cookbook](./cookbook/)

📺 [Watch the episode](https://youtu.be/5O7ZsSHhzpg)

## 🎯 What You'll Learn

Foundry IQ, Work IQ, and Fabric IQ ground agents in your organization's knowledge, work, and business data. But some questions can only be answered with information that changes by the hour — today's news, the latest product release, the current weather, the newest version of a public doc page. Models can't answer those from training data, and generic search results are noisy, unranked for LLMs, and expensive to stuff into a context window.

**Microsoft Web IQ** closes that gap with an agent-native grounding API that:

- Returns **ranked, citation-ready context** across web, news, images, and videos — ranked for relevance, freshness, and authority
- Uses **passage-level retrieval** so the tokens you send to your model are the ones that answer the question
- Responds in **164 ms at P95**, keeping multi-step agent chains fast
- Draws on **licensed sources, structured data, and the open web** — not SERP scraping — across 100+ languages and markets
- Is available over **REST** and an **MCP server** (JSON-RPC 2.0) — model-agnostic, with no inference lock-in

In this episode you'll explore Web IQ APIs available to your profile and learn how to turn their results into a grounded, cited answer.

## 🧠 Key Concepts

| Concept | What it means |
|---|---|
| **Grounding** | Building a model's answer from retrieved, current sources instead of its training memory — the most reliable way to reduce hallucinations |
| **Content format** | `passage` returns query-relevant paragraphs (up to 3,000 characters without full-document access); `text`, `markdown`, and `html` require full-document access. `maxLength` caps the characters per result — your token budget dial |
| **Freshness signals** | `crawledAt`, `lastUpdatedAt`, and `querySignals.freshness` tell your agent how current a source is and whether the query needs recent results |
| **Verticals** | Web, News (last 14 days), Images, Videos, and Places each return vertical-specific fields such as publisher, captions, video moments, and place addresses |
| **Browse and live crawl** | Read a specific URL as passages (any AppID) or as a full document (full-document access); with `liveCrawl="fallback"`, Web IQ crawls un-indexed pages on demand and returns `202` until content is ready |
| **Auto** | One call that returns typed evidence — text, media, weather, time zones, and more — each with its own citations |
| **Commerce (Private Preview)** | Optional Commerce Search, Offers, and Product Details APIs for product discovery and lookup; not available on all accounts |
| **MCP server** | The same capabilities as tools at `https://api.microsoft.ai/v3/mcp` for VS Code, GitHub Copilot, and any MCP client |
| **Instrumentation** | Optional citation and click telemetry that shows which results your model cited and which ones users opened |

## 🛠️ What You'll Build

1. Call **Web Search** and read the response anatomy — content, freshness, provenance, and query signals
2. Control your token budget with `maxLength` and optionally compare **content formats** with full-document access
3. Target results with **`site:` operators, language/region markets, and location**
4. Retrieve **News**, **Images** (with filters), **Videos** (with moments), and **Places** (with addresses and opening hours)
5. **Browse** a specific URL with on-demand live crawl
6. Try **Auto** for Web/News passage evidence with result-scoped citations
7. **Ground a model's answer** in numbered Web IQ sources with inline citations — optionally using a model deployed in Microsoft Foundry
8. Handle **errors, rate limits, and retries** with Web IQ's shared error schema
9. Connect Web IQ to VS Code as an **MCP server**, and call its tools directly over JSON-RPC
10. Understand **instrumentation** for citation and click telemetry
11. Optionally try **Commerce (Private Preview)**: search products, retrieve seller offers, and fetch product details using identifiers from the search response

> **Commerce is in Private Preview and is not available on all accounts.** Access is limited to select Azure customers and isn't guaranteed. Leave `COMMERCE_ACCESS = False` unless your AppID is enabled. See the [Commerce API reference](https://learn.microsoft.com/en-us/web-iq/reference/commerce) for supported markets, offer-link requirements, and how to request access.

## 📓 Try the Cookbook

Ready to get hands-on? Head to the [Episode 1 Cookbook](./cookbook/) for prerequisites and a step-by-step Jupyter notebook. You'll need a paid Azure subscription, a Web IQ billing resource, and a Web IQ API key.

## 🔗 Learn More

- 🌐 [Microsoft Web IQ](https://webiq.microsoft.ai/)
- 📖 [Quick Start](https://learn.microsoft.com/en-us/web-iq/get-started/quickstart)
- 📖 [API reference — Web](https://learn.microsoft.com/en-us/web-iq/reference/web-search) · [News](https://learn.microsoft.com/en-us/web-iq/reference/news-search) · [Images](https://learn.microsoft.com/en-us/web-iq/reference/image-search) · [Videos](https://learn.microsoft.com/en-us/web-iq/reference/video-search) · [Places](https://learn.microsoft.com/en-us/web-iq/reference/places) · [Browse](https://learn.microsoft.com/en-us/web-iq/reference/browse) · [Auto](https://learn.microsoft.com/en-us/web-iq/reference/auto)
- 📖 [MCP Server](https://learn.microsoft.com/en-us/web-iq/integrations/mcp)
- 📖 [Instrumentation](https://learn.microsoft.com/en-us/web-iq/guides/instrumentation)
- 📖 [FAQ](https://learn.microsoft.com/en-us/web-iq/resources/faq)
- 🧪 [Web IQ Playground](https://webiq.microsoft.ai/playground/)

## 💬 Community

- Ask your questions in our [Discussions](https://aka.ms/iq/discussions)

### 🚀 Back to [Web IQ overview](../README.md)
