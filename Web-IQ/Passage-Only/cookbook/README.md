# Python Cookbook: Passage-Only Web IQ

Run [web-iq-passage-only-cookbook.ipynb](./web-iq-passage-only-cookbook.ipynb) to retrieve Web Search passages, discover Images and Videos, and prepare an answer with numbered citations.

This notebook is independent of the broader Web IQ cookbook. Web requests use `contentFormat: "passage"`; image and video requests do not have a content-format parameter.

## Prerequisites

- **Web IQ access and an API key** for a profile with Web, Images, and Videos enabled. Complete onboarding in the [Customer Portal](https://webiq.microsoft.ai/) and check the allowed services and quota in [Profile Management](https://webiq.microsoft.ai/profiles/).
- **Python 3.10+** and a Jupyter notebook kernel.
- **VS Code**, if you want to follow the optional MCP integration step, with the Python and Jupyter extensions for running the notebook.
- **Optional answer generation:** a Microsoft Foundry project, a Responses-compatible model deployment, and an Azure identity with the required project/model permissions. Run `az login` before using `DefaultAzureCredential` locally.

The retrieval examples authenticate with a Web IQ API key loaded from `.env`, matching the original cookbook. The optional Foundry call uses `DefaultAzureCredential`; it does not use the Web IQ key.

## Setup

Open a terminal in this cookbook directory. Copy the sample configuration:

**Windows PowerShell**

```powershell
Copy-Item .env.sample .env
```

**macOS or Linux**

```bash
cp .env.sample .env
```

Edit `.env`:

| Variable | Required | Purpose |
|---|---|---|
| `WEBIQ_API_KEY` | Yes | API key for your passage-only Web IQ profile |
| `WEBIQ_BASE_URL` | No | Defaults to `https://api.microsoft.ai/v3` |
| `FOUNDRY_PROJECT_ENDPOINT` | No | Enables optional answer generation in a Foundry project |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | With a Foundry endpoint | Name of your Responses-compatible model deployment |

Leave both Foundry variables blank to print the complete grounded prompt instead. The notebook will still retrieve real sources and produce the numbered source list.

`.env` is gitignored. Never commit API keys, access tokens, or notebook outputs containing credentials.

Open the notebook and select a Python 3.10+ kernel. Keep the kernel working directory set to this cookbook folder so it loads this folder's `.env`. Run the cells from top to bottom. The first code cell installs the Python dependencies in that kernel.

## Walkthrough

The example researches how urban trees help cities stay cooler, then finds related images and explanatory videos. Change the queries to explore your own scenario.

| Step | Topic | API or integration |
|---|---|---|
| 1 | Web passages and response anatomy | `POST /search/web` |
| 2 | Site, language, region, and location targeting | `POST /search/web` |
| 3 | Image discovery and filters | `POST /search/images` |
| 4 | Video summaries and relevant moments | `POST /search/videos` |
| 5 | Grounded answers and numbered citations | Retrieved sources plus optional Foundry model |
| 6 | Errors, quotas, and retry behavior | Shared REST helper |
| 7 | Agent integration | VS Code MCP configuration |
| 8 | Citation and click instrumentation | Optional response fields |

The model receives web passages as factual evidence and labeled image/video metadata for media suggestions. It does not receive image pixels or video frames. A caption, summary, watermark filter, or search ranking does not establish permission to reuse media.

## Troubleshooting

| Symptom | Action |
|---|---|
| `.env` or API key is missing | Check the kernel working directory, copy `.env.sample`, and replace the placeholder key. Rerun Setup. |
| `401` | Check whether the key is valid and active. |
| `403` | Check the profile's allowed services. The notebook requests only Web, Images, and Videos. |
| `429 AuthUserThrottled` | The helper honors the server's retry delay and retries a bounded number of times. Reduce request frequency if throttling persists. |
| `429 AuthUserDailyUsageExceeded` | The helper stops immediately. Wait for the quota reset or contact support. |
| Empty results | This is not an authentication error. Broaden the query or remove filters, then rerun the affected retrieval cell. |
| Missing video summary or moments | These fields are optional. The notebook uses available metadata and falls back to the video's main URL. |
| The model cell prints a prompt | Expected when `FOUNDRY_PROJECT_ENDPOINT` is blank. Copy the complete prompt into your chosen model. |
| Foundry authentication or model error | Check `az login`, role assignments, the project endpoint, deployment name, and Responses API support. Errors are surfaced rather than treated as an unavailable profile. |

Keep the response `traceId` when contacting [Web IQ Support](https://aka.ms/microsoft-webiq-support). Do not include your API key.

## Reference

Contributors can run the notebook's offline regression checks from this directory with `python -m unittest test_cookbook.py`. These checks use synthetic responses, require no credentials, and make no live API or model calls.

- [Passage-only learning path](../README.md)
- [Web Search API](https://webiq.microsoft.ai/documentation/api-reference/web/?view=md)
- [Images Search API](https://webiq.microsoft.ai/documentation/api-reference/images/?view=md)
- [Videos Search API](https://webiq.microsoft.ai/documentation/api-reference/videos/?view=md)
- [Error handling](https://webiq.microsoft.ai/documentation/error-handling/?view=md)
- [MCP integration](https://webiq.microsoft.ai/documentation/mcp/?view=md)
- [Instrumentation](https://webiq.microsoft.ai/documentation/instrumentation/?view=md)
