"""
title: OpenSearch Tool
author: Pedro Valente
author_url: https://github.com/pmvalente171
git_url: https://github.com/pmvalente171/open-webui_opensearch_tool
description: OpenSearch tool for Open Web UI, allowing you to search and retrieve documents from an OpenSearch index.
required_open_webui_version: 0.5.0
requirements: langchain-openai, langgraph, ollama, langchain_ollama, opensearch-py
version: 0.0.0
licence: MIT
"""

from opensearchpy import OpenSearch
from pydantic import BaseModel, Field


def print_error(error: str) -> str:
    return """
```md
# Error: {error}
```"""

class Tools:
    class Valves(BaseModel):
        """Editable fields of the tool"""

        OPENSEARCH_HOST: str = Field(
            default="http://localhost:9200",
            description="OpenSearch endpoint URL. Default is http://localhost:9200",
        )

        OPENSEARCH_USERNAME: str = Field(
            default="admin",
            description="OpenSearch username. Default is 'admin'",
        )

        OPENSEARCH_PASSWORD: str = Field(
            default="admin",
            description="OpenSearch password. Default is 'admin'",
        )

        OPENSEARCH_PORT: int = Field(
            default=9200,
            description="OpenSearch port. Default is 9200",
        )

        OPENSEARCH_INDEX: str = Field(
            default="images",
            description="OpenSearch index name. Default is 'images'",
        )

        OPENSEARCH_URL_PREFIX: str = Field(
            default="opensearch",
            description="OpenSearch URL prefix. Default is 'opensearch'",
        )

        OPENSEARCH_SOURCE: str = Field(
            default="",
            description="OpenSearch source formatting: List seperated by commmas `,`.",
        )

        DESCRIPTION: str = Field(
            default="A collection of documents stored in OpenSearch.",
            description="Description of the database. Default is 'A collection of documents stored in OpenSearch.'",
        )

    def __init__(self):
        """Initialize the tool"""
        self.valves = self.Valves()

    async def query_opensearch(self, query: str, __event_emitter__=None) -> str:
        """
        Query the OpenSearch index and return the results.
        :param query: The query string to search for.
        :param __event_emitter__: Optional event emitter for handling events.
        :return: The search results as a string.
        """

        client = OpenSearch(
            hosts=[
                {
                    "host": self.valves.OPENSEARCH_HOST,
                    "port": self.valves.OPENSEARCH_PORT,
                }
            ],
            http_compress=True,
            http_auth=(
                self.valves.OPENSEARCH_USERNAME,
                self.valves.OPENSEARCH_PASSWORD,
            ),
            url_prefix="opensearch",
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

        # get source
        source = self.valves.OPENSEARCH_SOURCE.split(",")

        # Search body
        search_body = {
            "size": 5,  # TODO: Make this parameter editable
            "_source": source,
            "query": {"match": {"product_short_description": query}},
        }

        try:
            # Perform the search
            response = client.search(
                index=self.valves.OPENSEARCH_INDEX, body=search_body
            )

            # Extract the hits from the response
            hits = response["hits"]["hits"]

            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Successfully retrieved {len(hits)} items from OpenSearch.",
                        "done": True,
                    },
                }
            )

            for hit in hits:
                await __event_emitter__(
                    {
                        "type": "message",
                        "data": {
                            "content": f"![Retrieved Image]({hit['_source']['product_image_path']})"
                        },
                    }
                )

            # Return the hits as a string
            return f"Successfully retrieved the following items: {str(hits)}"

        except Exception as e:

            await __event_emitter__(
                {
                    "type": "message",
                    "data": {
                        "content": print_error(f"An error occurred while querying OpenSearch:\n{str(e)}")
                    },
                }
            )

            # Handle any exceptions that occur during the search
            return f"An error occurred while querying OpenSearch: {str(e)}"
