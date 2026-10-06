# Episode 1 Cookbook: Grounding Agents with Real-Time Web Search

This folder contains the hands-on cookbook for Episode 1 of The Web IQ Series.

## 📋 Prerequisites

- **Web IQ access** — Web IQ is currently in **limited access** for select enterprise customers building AI agents and applications at scale. Request access at [webiq.microsoft.ai](https://webiq.microsoft.ai/).
- **A Web IQ API key** — In the [Web IQ Portal → Profile Management](https://webiq.microsoft.ai/profiles/), open the **Authentication** tab and select **Create API Key**. The **Profile** tab shows your quota (for example, `60 QPM`) and which services (Web, Videos, Browse, News, Images) your key can call.
- **Python 3.10+** installed
- *(Optional — Step 9 only)* A **Microsoft Foundry project** with a chat model deployment, plus `az login` so `DefaultAzureCredential` can authenticate

> **💡 No Azure infrastructure needed for the core cookbook.** Web IQ is a standalone, hosted service — there's no index, knowledge base, or deployment to provision. Steps 1–8 and 10–12 need only your API key. Step 9 uses a Microsoft Foundry model if you've configured one, and otherwise prints the grounded prompt so you can use any model.

## 🔑 Authentication

Web IQ supports two authentication modes:

| Mode | Header | Setup |
|---|---|---|
| **API key** *(used in this cookbook)* | `x-apikey: <key>` | **Create API Key** in [Profile Management](https://webiq.microsoft.ai/profiles/) |
| **Entra ID OAuth 2.0** (client credentials) | `Authorization: Bearer <token>` | Bind your app registration's Application (Client) ID under **Profile Management → Authentication → Application (Client) IDs** (allow ~1 minute to sync), then request an app-only token from `https://login.microsoftonline.com/<tenant-id>` with scope `https://api.microsoft.ai/.default` |

All requests must use **HTTPS** and `content-type: application/json`.

## 🔧 Setup

Copy [`.env.sample`](./.env.sample) to `.env` **in this folder** and fill in your values:

```bash
cp .env.sample .env          # macOS/Linux
Copy-Item .env.sample .env   # Windows PowerShell
```

| Variable | Required | Description |
|---|---|---|
| `WEBIQ_API_KEY` | ✅ | Your Web IQ API key |
| `WEBIQ_BASE_URL` | | Defaults to `https://api.microsoft.ai/v3` |
| `FOUNDRY_PROJECT_ENDPOINT` | Step 9 only | `https://<your-foundry-resource>.services.ai.azure.com/api/projects/<your-project>` — find it on your project's **Overview** page in [Microsoft Foundry](https://ai.azure.com) |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Step 9 only | A chat model deployment in that project, for example `gpt-4o-mini` |

> 🔒 `.env` is gitignored. Never commit your API key.

## 📓 Cookbook Notebook

The [**Web IQ Cookbook**](./web-iq-cookbook.ipynb) walks you through every Web IQ API, step by step:

| Step | Topic | API |
|---|---|---|
| 1 | Web Search and the response anatomy — content, freshness, provenance, query signals | `POST /search/web` |
| 2 | Content formats (`passage`, `text`, `markdown`, `html`) and token budgets with `maxLength` | `POST /search/web` |
| 3 | Targeting with `site:`, language/region, and location | `POST /search/web` |
| 4 | News Search — last 14 days, with publisher and snippet | `POST /search/news` |
| 5 | Images Search with aspect ratio, size, and watermark filters | `POST /search/images` |
| 6 | Videos Search with freshness filters and moments | `POST /search/videos` |
| 7 | Browse a specific URL, with live crawl and `202` polling | `POST /browse` |
| 8 | Auto (Beta) — typed evidence with result-scoped citations | `POST /auto` |
| 9 | Ground a model's answer with numbered citations | Web IQ + Microsoft Foundry *(optional)* |
| 10 | Errors, rate limits, and retries | All |
| 11 | Web IQ as an MCP server — VS Code config and JSON-RPC | `https://api.microsoft.ai/v3/mcp` |
| 12 | Instrumentation — citation and click telemetry | Ping URLs |

### Quick Start

1. Copy `.env.sample` to `.env` and add your API key (see above)
2. Open `web-iq-cookbook.ipynb` in VS Code and select a Python 3.10+ kernel
3. Run the cells top to bottom — the first code cell installs `requests`, `python-dotenv`, `azure-identity`, and `azure-ai-projects`

## 🩺 Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `401 AuthInvalidApiKey` | The key is wrong or missing. Check `WEBIQ_API_KEY` in `.env`, then restart the kernel so `load_dotenv` reloads it |
| `403` on one endpoint only | Your profile isn't allowed to call that service. Check **allowed services** in Profile Management |
| `429 AuthUserThrottled` | You've hit your per-minute quota — common when re-running the whole notebook quickly. The helper retries automatically; wait a minute if it persists |
| `429 AuthUserDailyUsageExceeded` | Daily cap reached. It resets at 00:00 UTC |
| `404` from Browse | The URL isn't indexed. Use `liveCrawl="fallback"` (the cookbook does this by default) |
| Auto (Beta) cell says it isn't available | Auto is enabled per profile. Skip Step 8 or contact your Microsoft contact |
| Step 9 prints a prompt instead of an answer | `FOUNDRY_PROJECT_ENDPOINT` isn't set — that's expected if you're not using Microsoft Foundry |
| Can't verify your invitation code | Reply to the invitation with the address shown in the top-right corner of [portal.azure.com](https://portal.azure.com) |

Include the `traceId` from the response when you contact [Web IQ Support](https://aka.ms/microsoft-webiq-support).

### Learn with Copilot

Open the notebook and use Copilot Chat to help you learn and experiment:

- *"Explain what this notebook does step by step"*
- *"What's the difference between Web Search and the Auto (Beta) endpoint?"*
- *"Change Step 9 to use only news results from the last week and cite the publisher"*
- *"Add a `-site:` filter to exclude a domain from Step 3"*
- *"Turn the Step 9 code into a reusable `answer_with_web(question)` function"*

## Additional Resources

- [Episode 1 README](../README.md)
- [Web IQ overview](../../README.md)
- [Web IQ Quick Start](https://webiq.microsoft.ai/documentation/quick-start/?view=md)
- [Web IQ Error Handling](https://webiq.microsoft.ai/documentation/error-handling/?view=md)
- [Web IQ Playground](https://webiq.microsoft.ai/playground/)
- [Web IQ Support](https://aka.ms/microsoft-webiq-support)
