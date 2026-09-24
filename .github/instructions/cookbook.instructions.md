---
applyTo: "**/cookbook/**"
---

# Cookbook Instructions

## Environment Setup

Cookbooks load configuration from a `.env` file in the cookbook directory. Required variables:

```
SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AOAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com
AOAI_EMBEDDING_MODEL=text-embedding-3-large
AOAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AOAI_GPT_MODEL=gpt-5-mini
AOAI_GPT_DEPLOYMENT=gpt-5-mini
FOUNDRY_PROJECT_ENDPOINT=https://<your-ai-services>.services.ai.azure.com/api/projects/<your-project>
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-5-mini
AZURE_AI_SEARCH_CONNECTION_NAME=iq-series-search-connection
```

## Authentication

Always use `DefaultAzureCredential` from `azure-identity`. Never hardcode API keys or connection strings.

## Key Packages

- `azure-search-documents` (>=12.1.0b1) — Search index, knowledge source, knowledge base, and retrieval APIs
- `azure-ai-projects` — Foundry Agent Service client (`AIProjectClient`, `MCPTool`)
- `azure-identity` — `DefaultAzureCredential` for RBAC-based auth
- `python-dotenv` — Load `.env` files

## Common Patterns

### Knowledge Source (pointer to a search index)
```python
from azure.search.documents.indexes.models import (
    SearchIndexKnowledgeSource,
    SearchIndexKnowledgeSourceParameters,
    SearchIndexFieldReference,
)
knowledge_source = SearchIndexKnowledgeSource(
    name="my-source",
    search_index_parameters=SearchIndexKnowledgeSourceParameters(
        search_index_name="my-index",
        source_data_fields=[SearchIndexFieldReference(name="id")],
    ),
)
index_client.create_or_update_knowledge_source(knowledge_source=knowledge_source)
```

### Knowledge Base (retrieval + reasoning layer)
```python
from azure.search.documents.indexes.models import (
    KnowledgeBase,
    KnowledgeBaseAzureOpenAIModel,
    KnowledgeSourceReference,
)
from azure.search.documents.knowledgebases.models import KnowledgeRetrievalOutputMode
knowledge_base = KnowledgeBase(
    name="my-kb",
    models=[KnowledgeBaseAzureOpenAIModel(...)],
    knowledge_sources=[KnowledgeSourceReference(name="my-source")],
    output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
)
index_client.create_or_update_knowledge_base(knowledge_base)
```

### Agentic Retrieval (query the knowledge base)
```python
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
retrieval_client = KnowledgeBaseRetrievalClient(
    endpoint=SEARCH_ENDPOINT,
    knowledge_base_name="my-kb",
    credential=credential,
)
result = retrieval_client.retrieve(retrieval_request=...)
```

### MCP Endpoint (for agent integration)
```python
mcp_endpoint = f"{SEARCH_ENDPOINT}/knowledgebases/{KB_NAME}/mcp?api-version=2025-11-01-Preview"
```

## Naming Conventions

- Index names: lowercase with hyphens (e.g., `earth-at-night`)
- Knowledge source/base names: lowercase with hyphens
- Connection names: lowercase with hyphens
