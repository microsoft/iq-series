import argparse
import logging
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ServiceRequestError,
    ServiceResponseError,
)
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters,
    HnswAlgorithmConfiguration,
    KnowledgeBase,
    KnowledgeBaseAzureOpenAIModel,
    KnowledgeSourceReference,
    SearchField,
    SearchIndex,
    SearchIndexFieldReference,
    SearchIndexKnowledgeSource,
    SearchIndexKnowledgeSourceParameters,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    VectorSearch,
    VectorSearchProfile,
)
from azure.search.documents.knowledgebases.models import KnowledgeRetrievalOutputMode

INDEX_NAME = "earth-at-night"
KNOWLEDGE_SOURCE_NAME = "earth-knowledge-source"
KNOWLEDGE_BASE_NAME = "earth-knowledge-base"
DATA_URL = (
    "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/"
    "main/nasa-e-book/earth-at-night-json/documents.json"
)
logger = logging.getLogger("seed")


def retry_operation(operation, description, timeout=600):
    deadline = time.monotonic() + timeout
    while True:
        try:
            return operation()
        except (HttpResponseError, ServiceRequestError, ServiceResponseError) as error:
            if isinstance(error, HttpResponseError):
                if not isinstance(error, ClientAuthenticationError) and error.status_code not in (
                    401, 403, 408, 409, 429, 500, 502, 503, 504
                ):
                    raise
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise
            logger.warning("%s not ready; retrying: %s", description, error)
            time.sleep(min(15, remaining))


def create_index(endpoint, embedding_model, embedding_deployment):
    return SearchIndex(
        name=INDEX_NAME,
        fields=[
            SearchField(name="id", type="Edm.String", key=True, filterable=True),
            SearchField(name="page_chunk", type="Edm.String"),
            SearchField(
                name="page_embedding_text_3_large",
                type="Collection(Edm.Single)",
                stored=False,
                vector_search_dimensions=3072,
                vector_search_profile_name="hnsw_text_3_large",
            ),
            SearchField(name="page_number", type="Edm.Int32", filterable=True),
        ],
        vector_search=VectorSearch(
            profiles=[
                VectorSearchProfile(
                    name="hnsw_text_3_large",
                    algorithm_configuration_name="alg",
                    vectorizer_name="azure_openai_text_3_large",
                )
            ],
            algorithms=[HnswAlgorithmConfiguration(name="alg")],
            vectorizers=[
                AzureOpenAIVectorizer(
                    vectorizer_name="azure_openai_text_3_large",
                    parameters=AzureOpenAIVectorizerParameters(
                        resource_url=endpoint,
                        deployment_name=embedding_deployment,
                        model_name=embedding_model,
                    ),
                )
            ],
        ),
        semantic_search=SemanticSearch(
            default_configuration_name="semantic_config",
            configurations=[
                SemanticConfiguration(
                    name="semantic_config",
                    prioritized_fields=SemanticPrioritizedFields(
                        content_fields=[SemanticField(field_name="page_chunk")]
                    ),
                )
            ],
        ),
    )


def upload_documents(search_client, documents):
    for offset in range(0, len(documents), 32):
        batch = documents[offset:offset + 32]
        results = retry_operation(
            lambda: search_client.merge_or_upload_documents(documents=batch),
            "Document upload",
        )
        failed = [result for result in results if not result.succeeded]
        if failed:
            errors = "; ".join(
                f"{result.key}: {result.status_code} {result.error_message}"
                for result in failed
            )
            raise RuntimeError(f"Document upload failed: {errors}")
        logger.info("Uploaded %s/%s documents", offset + len(batch), len(documents))


def wait_for_documents(search_client, expected_count, timeout=120):
    deadline = time.monotonic() + timeout
    while True:
        count = retry_operation(search_client.get_document_count, "Index availability")
        if count >= expected_count:
            return
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Expected {expected_count} indexed documents, found {count}")
        time.sleep(5)


def seed_data():
    search_endpoint = os.environ["SEARCH_ENDPOINT"]
    openai_endpoint = os.environ["AOAI_ENDPOINT"]
    index = create_index(
        openai_endpoint,
        os.environ["EMBEDDING_MODEL"],
        os.environ["EMBEDDING_DEPLOYMENT"],
    )
    with DefaultAzureCredential(
        managed_identity_client_id=os.environ.get("AZURE_CLIENT_ID")
    ) as credential, SearchIndexClient(
        endpoint=search_endpoint,
        credential=credential,
        connection_timeout=15,
        read_timeout=60,
    ) as index_client, SearchClient(
        endpoint=search_endpoint,
        index_name=INDEX_NAME,
        credential=credential,
        connection_timeout=15,
        read_timeout=60,
    ) as search_client:
        retry_operation(
            lambda: index_client.create_or_update_index(index), "Index creation"
        )
        logger.info("Index '%s' ready", INDEX_NAME)

        with requests.get(DATA_URL, timeout=(15, 120)) as response:
            response.raise_for_status()
            documents = response.json()
        if not isinstance(documents, list) or not documents:
            raise ValueError("Sample dataset must be a nonempty list of documents")
        upload_documents(search_client, documents)
        wait_for_documents(search_client, len(documents))

        knowledge_source = SearchIndexKnowledgeSource(
            name=KNOWLEDGE_SOURCE_NAME,
            description="NASA Earth at Night data",
            search_index_parameters=SearchIndexKnowledgeSourceParameters(
                search_index_name=INDEX_NAME,
                source_data_fields=[
                    SearchIndexFieldReference(name="id"),
                    SearchIndexFieldReference(name="page_number"),
                ],
            ),
        )
        retry_operation(
            lambda: index_client.create_or_update_knowledge_source(
                knowledge_source=knowledge_source
            ),
            "Knowledge source creation",
        )
        knowledge_base = KnowledgeBase(
            name=KNOWLEDGE_BASE_NAME,
            models=[
                KnowledgeBaseAzureOpenAIModel(
                    azure_open_ai_parameters=AzureOpenAIVectorizerParameters(
                        resource_url=openai_endpoint,
                        deployment_name=os.environ["GPT_DEPLOYMENT"],
                        model_name=os.environ["GPT_MODEL"],
                    )
                )
            ],
            knowledge_sources=[KnowledgeSourceReference(name=KNOWLEDGE_SOURCE_NAME)],
            output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
            answer_instructions=(
                "Provide a concise, informative answer grounded in the retrieved documents."
            ),
        )
        retry_operation(
            lambda: index_client.create_or_update_knowledge_base(knowledge_base),
            "Knowledge base creation",
        )
        retry_operation(
            lambda: index_client.get_knowledge_base(KNOWLEDGE_BASE_NAME),
            "Knowledge base verification",
        )
        logger.info(
            "Seeding complete: %s documents; MCP endpoint: %s/knowledgebases/%s/mcp",
            len(documents), search_endpoint, KNOWLEDGE_BASE_NAME,
        )


class ReadinessHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/ready":
            self.send_error(404)
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Seeding complete\n")


def main():
    parser = argparse.ArgumentParser(description="Seed the Foundry IQ sample knowledge base")
    parser.add_argument("--serve", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.getLogger("azure").setLevel(logging.WARNING)
    seed_data()
    if args.serve:
        logger.info("Seeding verified; readiness endpoint listening on port 8080")
        HTTPServer(("0.0.0.0", 8080), ReadinessHandler).serve_forever()


if __name__ == "__main__":
    main()
