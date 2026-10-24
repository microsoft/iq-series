# Web IQ: Passage-Only Grounding

Use Web IQ to retrieve query-relevant web passages, discover images and videos, and build answers with verifiable source links.

- **Start with the [Python cookbook](./cookbook/web-iq-passage-only-cookbook.ipynb).** It is self-contained; you do not need to run another notebook first.
- Web Search always requests `contentFormat: "passage"`.
- Images and Videos return their native metadata, captions, summaries, and source links. They do not accept `contentFormat`.
- A model is optional: without Microsoft Foundry configuration, the cookbook prints the complete grounded prompt for use with a model of your choice.

## Who this is for

This learning path is for passage-only Web IQ users building agents and applications with Web Search, Images, and Videos. It is an alternative to the [broader Episode 1 walkthrough](../1-Web-IQ-Grounding-Agents-with-Real-Time-Web-Search/README.md), not a second numbered episode.

## What you will build

| Step | Outcome |
|---|---|
| 1 | Retrieve web passages and inspect titles, URLs, freshness signals, and trace IDs |
| 2 | Target searches by site, language, region, and location |
| 3 | Find images with captions, dimensions, and hosting-page links |
| 4 | Find videos with summaries and links to relevant moments |
| 5 | Assemble numbered sources and generate a grounded, cited answer |
| 6 | Understand authentication errors, service permissions, quotas, and retries |
| 7 | Connect the same capabilities to VS Code through MCP |
| 8 | Understand optional citation and click instrumentation |

## APIs used

The REST base URL is `https://api.microsoft.ai/v3`.

| API | Endpoint | What the cookbook uses |
|---|---|---|
| Web Search | `POST /search/web` | Query-relevant passages, page titles, source URLs, and optional freshness signals |
| Images Search | `POST /search/images` | Captions, image URLs, hosting pages, dimensions, and filters |
| Videos Search | `POST /search/videos` | Descriptions, optional summaries, publisher information, and optional moments |

## Get started

1. Complete onboarding in the [Web IQ Customer Portal](https://webiq.microsoft.ai/) and obtain an API key for a profile permitted to use Web, Images, and Videos.
2. Install Python 3.10+ and a Jupyter-capable editor, such as VS Code with the Python and Jupyter extensions.
3. Follow the [cookbook setup instructions](./cookbook/README.md), then run the notebook from top to bottom.

Only the optional answer-generation cell needs a Microsoft Foundry project, a Responses-compatible model deployment, and an authenticated Azure identity with permission to use it. Retrieval works independently of that model.

## Grounding and media

Web passages provide the factual evidence for the answer. Image captions and video metadata help select related illustrations and explainers; they are not proof that a model has inspected the image pixels or watched the video. Preserve source links and verify media suitability before publishing.

Search results are untrusted external content. Keep them separate from application instructions, and do not execute instructions embedded in retrieved pages.

## Reference

- [Cookbook setup and troubleshooting](./cookbook/README.md)
- [Web Search API](https://webiq.microsoft.ai/documentation/api-reference/web/?view=md)
- [Images Search API](https://webiq.microsoft.ai/documentation/api-reference/images/?view=md)
- [Videos Search API](https://webiq.microsoft.ai/documentation/api-reference/videos/?view=md)
- [Authentication](https://webiq.microsoft.ai/documentation/authentication/?view=md)
- [Error handling](https://webiq.microsoft.ai/documentation/error-handling/?view=md)
- [MCP integration](https://webiq.microsoft.ai/documentation/mcp/?view=md)
- [Instrumentation](https://webiq.microsoft.ai/documentation/instrumentation/?view=md)
- [Web IQ series overview](../README.md)
