# Episode 1: Web IQ: Grounding Agents with Real-Time Web Search

📂 [Try the cookbook](./cookbook/)

> 📺 This episode's video premiere is **coming soon**. In the meantime, the cookbook below is fully hands-on and works today.

## 🎯 What You'll Learn

Foundry IQ, Work IQ, and Fabric IQ ground agents in your organization's knowledge, work, and business data. But some questions can only be answered with information that changes by the hour — today's news, the latest product release, the current weather, the newest version of a public doc page. Models can't answer those from training data, and generic search results are noisy, unranked for LLMs, and expensive to stuff into a context window.

**Microsoft Web IQ** closes that gap with an agent-native grounding API that:

- Returns **ranked, citation-ready context** across web, news, images, and videos — ranked for relevance, freshness, and authority
- Uses **passage-level retrieval** so the tokens you send to your model are the ones that answer the question
- Responds in **164 ms at P95**, keeping multi-step agent chains fast
- Draws on **licensed sources, structured data, and the open web** — not SERP scraping — across 100+ languages and markets
- Is available over **REST** and an **MCP server** (JSON-RPC 2.0) — model-agnostic, with no inference lock-in

In this episode you'll explore every Web IQ API and learn how to turn its results into a grounded, cited answer.

## 🧠 Key Concepts

| Concept | What it means |
|---|---|
| **Grounding** | Building a model's answer from retrieved, current sources instead of its training memory — the most reliable way to reduce hallucinations |
| **Content format** | `passage` returns query-relevant paragraphs; `text`, `markdown`, and `html` return the full document. `maxLength` caps the characters per result — your token budget dial |
| **Freshness signals** | `crawledAt`, `lastUpdatedAt`, and `querySignals.freshness` tell your agent how current a source is and whether the query needs recent results |
| **Verticals** | Web, News (last 14 days), Images, and Videos each return vertical-specific fields such as publisher, captions, and video moments |
| **Browse and live crawl** | Read a specific URL; with `liveCrawl="fallback"`, Web IQ crawls un-indexed pages on demand and returns `202` until content is ready |
| **Auto (Beta)** | One call that returns typed evidence — text, media, weather, time zones, and more — each with its own citations |
| **MCP server** | The same capabilities as tools at `https://api.microsoft.ai/v3/mcp` for VS Code, GitHub Copilot, and any MCP client |
| **Instrumentation** | Optional citation and click telemetry that shows which results your model cited and which ones users opened |

## 🛠️ What You'll Build

1. Call **Web Search** and read the response anatomy — content, freshness, provenance, and query signals
2. Compare **content formats** and control your token budget with `maxLength`
3. Target results with **`site:` operators, language/region markets, and location**
4. Retrieve **News**, **Images** (with filters), and **Videos** (with moments)
5. **Browse** a specific URL with on-demand live crawl
6. Try **Auto (Beta)** for typed evidence with result-scoped citations
7. **Ground a model's answer** in numbered Web IQ sources with inline citations — optionally using a model deployed in Microsoft Foundry
8. Handle **errors, rate limits, and retries** with Web IQ's shared error schema
9. Connect Web IQ to VS Code as an **MCP server**, and call its tools directly over JSON-RPC
10. Understand **instrumentation** for citation and click telemetry

## 📓 Try the Cookbook

Ready to get hands-on? Head to the [Episode 1 Cookbook](./cookbook/) for prerequisites and a step-by-step Jupyter notebook. All you need is a Web IQ API key.

## 🔗 Learn More

- 🌐 [Microsoft Web IQ](https://webiq.microsoft.ai/)
- 📖 [Quick Start](https://webiq.microsoft.ai/documentation/quick-start/?view=md)
- 📖 [API reference — Web](https://webiq.microsoft.ai/documentation/api-reference/web/?view=md) · [News](https://webiq.microsoft.ai/documentation/api-reference/news/?view=md) · [Images](https://webiq.microsoft.ai/documentation/api-reference/images/?view=md) · [Videos](https://webiq.microsoft.ai/documentation/api-reference/videos/?view=md) · [Browse](https://webiq.microsoft.ai/documentation/api-reference/browse/?view=md) · [Auto (Beta)](https://webiq.microsoft.ai/documentation/api-reference/auto/?view=md)
- 📖 [MCP Server](https://webiq.microsoft.ai/documentation/mcp/?view=md)
- 📖 [Instrumentation](https://webiq.microsoft.ai/documentation/instrumentation/?view=md)
- 📖 [FAQ — including how Web IQ differs from Grounding with Bing](https://webiq.microsoft.ai/documentation/faq/?view=md)
- 🧪 [Web IQ Playground](https://webiq.microsoft.ai/playground/)

## 💬 Community

- Ask your questions in our [Discussions](https://aka.ms/iq/discussions)

### 🚀 Back to [Web IQ overview](../README.md)
