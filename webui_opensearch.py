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

import os
import dotenv

from opensearchpy import OpenSearch
from pydantic import BaseModel, Field

class Tools:
    class Valves(BaseModel):
        """Editable fields of the tool"""
        OPEN_SEARCH_ENDPOINT : str = Field(
            default="http://localhost:9200",
            description="OpenSearch endpoint URL. Default is http://localhost:9200",
        )

        OPEN_SEARCH_USERNAME : str = Field(
            default="admin",
            description="OpenSearch username. Default is 'admin'",
        )

        OPEN_SEARCH_PASSWORD : str = Field(
            default="admin",
            description="OpenSearch password. Default is 'admin'",
        )

        OPEN_SEARCH_PORT : int = Field(
            default=9200,
            description="OpenSearch port. Default is 9200",
        )

        OPEN_URL_PREFIX : str = Field(
            default="opensearch",
            description="OpenSearch URL prefix. Default is 'opensearch'",
        )

        DESCRIPTION : str = Field(
            default="A collection of documents stored in OpenSearch.",
            description="Description of the database. Default is 'A collection of documents stored in OpenSearch.'",
        )

    def __init__(self):
        """Initialize the tool"""
        self.valves = self.Valves()

        # TODO: debug stuff
        env_vars = dotenv.dotenv_values()
        user = env_vars['USER_ID']
        password = env_vars['USER_PASSWORD']

        host = env_vars['HOST']
        port = env_vars['PORT']

        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=True,
            http_auth=(user, password),
            url_prefix='opensearch',
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )

        # TODO: More debug stuff
        self.source = ['product_id', 'product_family', 'product_category', 'product_sub_category', 'product_gender',
               'product_main_colour', 'product_second_color', 'product_brand', 'product_materials',
               'product_short_description', 'product_attributes', 'product_image_path',
               'product_highlights', 'outfits_ids', 'outfits_products']


    def query_opensearch(self, query : str) -> str:
        """
        Query the OpenSearch index and return the results.
        :param query: The query string to search for.
        :return: The search results as a string.
        """

        # Search body
        search_body = {
            'size': 5, # TODO: Make this parameter editable
            '_source': self.source,
            "query": {
                "match": {
                    "product_short_description": query
                }
            }
        }

        # Perform the search
        response = self.client.search(index="farfetch_images", body=search_body)

        # Extract the hits from the response
        hits = response['hits']['hits']

        # Return the hits as a string
        return str(hits)

    def get_tool_info(self) -> dict:
        """
        Get the tool information.
        :return: A dictionary containing the tool information.
        """

        return {
            "name": "OpenSearch Tool",
            "description": self.valves.DESCRIPTION,
            "endpoint": self.valves.OPEN_SEARCH_ENDPOINT,
            "username": self.valves.OPEN_SEARCH_USERNAME,
            "password": self.valves.OPEN_SEARCH_PASSWORD,
            "port": self.valves.OPEN_SEARCH_PORT,
            "url_prefix": self.valves.OPEN_URL_PREFIX
        }
