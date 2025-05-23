#!/usr/bin/env python3
"""
OpenSearch Client Script
A simple script to connect to OpenSearch and perform searches based on user input.
"""

from opensearchpy import OpenSearch

import dotenv

env_vars = dotenv.dotenv_values()
_user_id = env_vars['USER_ID']
_user_password = env_vars['USER_PASSWORD']

class ConfigOpenSearch:

    host = env_vars['HOST']
    port = env_vars['PORT']
    index_name = "farfetch_images"
    user = _user_id  # Add your username here.
    password = _user_password  # Add your user password here. For testing only. Don't store credentials in code.
    source = [] # TODO : Add your source fields here. For example: ['field1', 'field2']

    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress=True,
        http_auth=(user, password),
        url_prefix='opensearch',
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False
    )

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfigOpenSearch, cls).__new__(cls)
        return cls.instance


def main():
    """
    :return:
    """

    opensearch = ConfigOpenSearch()

    # Example search query
    search_query = "blue jeans"

    # Example search body
    query = {
        'size': 5,
        '_source': opensearch.source,
        "query": {
            "match": {
                "product_short_description": search_query
            }
        }
    }

    # Perform the search
    response = opensearch.client.search(
        body=query,
        index=opensearch.index_name
    )

    # Print the response
    print("Search Response:")
    for hit in response['hits']['hits']:
        print(f"ID: {hit['_id']}, Source: {hit['_source']}")


if __name__ == "__main__":
    main() # TODO: It's working !!!