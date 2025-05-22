"""
title: OpenSearch Tool
author: Pedro Valente
author_url: TODO
git_url: TODO
description: OpenSearch tool for Open Web UI, allowing you to search and retrieve documents from an OpenSearch index.
required_open_webui_version: TODO
requirements: langchain-openai, langgraph, ollama, langchain_ollama, opensearch-py
version: 0.0.1
licence: MIT
"""


class Tools:
    class Valves(BaseModel):
        """Editable fields of the tool"""
        OPEN_SEARCH_ENDPOINT : str = Field(
            default="http://localhost:9200",
            description="OpenSearch endpoint URL. Default is http://localhost:9200",
        )

        DATABASE_DESCRIPTION : str = Field(
            default="A collection of documents stored in OpenSearch.",
            description="Description of the database. Default is 'A collection of documents stored in OpenSearch.'",
        )

    def __init__(self):
        """Initialize the tool"""
        self.valves = self.Valves()

    def query_opensearch(self, query : str) -> dict:
        """
        Query the OpenSearch index and return the results.
        :param query: The query string to search for.
        :return: The search results as a string.
        """

