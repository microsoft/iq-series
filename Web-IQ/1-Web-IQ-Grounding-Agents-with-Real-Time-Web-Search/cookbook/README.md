# Episode 1 Cookbook: Grounding Agents with Real-Time Web Search

This folder contains the hands-on cookbook for Episode 1 of The Web IQ Series.

## 📋 Prerequisites

- **Web IQ access** — Web IQ is currently in **limited access** for select enterprise customers. Request access and generate an API key at the [Microsoft Web IQ Portal](https://webiq.microsoft.ai/profiles/)
- **Python 3.10+** installed

> **💡 No Azure subscription or infrastructure needed.** Unlike Foundry IQ, Web IQ is a standalone, hosted REST/MCP service — there's no index, knowledge base, or Foundry project to provision. You only need an API key.

## 🔑 Authentication

Web IQ supports two authentication modes:

1. **API key** (used in this cookbook) — generate one in the [Web IQ Portal](https://webiq.microsoft.ai/profiles/) under **Profile Management**, then pass it in the `x-apikey` header.
2. **Entra ID OAuth 2.0 (client credentials)** — bind an app registration's Application (Client) ID in the portal, then acquire a token with scope `https://api.microsoft.ai/.default` and pass it as `Authorization: Bearer <token>`.

## 🔧 Setup

Copy [`.env.sample`](./.env.sample) to `.env` **in this folder** and add your API key:

```bash
cp .env.sample .env          # macOS/Linux
Copy-Item .env.sample .env   # Windows PowerShell
```

```env
WEBIQ_API_KEY=<your-web-iq-api-key>
WEBIQ_BASE_URL=https://api.microsoft.ai/v3
```

## 📓 Cookbook Notebook

The [**Web IQ Cookbook**](./web-iq-cookbook.ipynb) walks you through grounding an agent in the live web, step by step:

1. Calling the **Web Search** endpoint (`POST /search/web`) and inspecting grounding content
2. Calling the **News Search** endpoint (`POST /search/news`) for the last 14 days of coverage
3. Calling the **Images Search** endpoint (`POST /search/images`)
4. Handling errors and rate limits per the documented error schema
5. Configuring the **Web IQ MCP server** for use in VS Code / GitHub Copilot

### Quick Start

1. Install dependencies: `pip install -U requests python-dotenv`
2. Copy `.env.sample` to `.env` and add your API key (see above)
3. Open `web-iq-cookbook.ipynb` in VS Code and run the cells

### Learn with Copilot

Open any cookbook notebook and use Copilot Chat to help you learn and experiment:

- *"Explain what this notebook does step by step"*
- *"What's the difference between Web Search and the Auto (Beta) endpoint?"*
- *"Help me add a `site:` filter to this web search query"*

## Additional Resources

- [Episode 1 README](../README.md)
- [Web IQ documentation](https://webiq.microsoft.ai/documentation/overview/)
- [Web IQ error handling reference](https://webiq.microsoft.ai/documentation/error-handling/?view=md)
- [Web IQ support](https://aka.ms/microsoft-webiq-support)
