import json

import aiohttp
from meilisearch import Client

from scint.support.logging import log
from scint.support.utils import envar


# with open("scint/data/functions.json", "r", encoding="utf-8") as f:
#     await search_controller.update_documents("functions", json.load(f))


class SearchController:
    """
    """
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.client = Client(self.url, self.key)

    def results(self, index, query, limit=4):
        """
        """
        options = {
            "hybrid": {"semanticRatio": 0.9, "embedder": "default"},
            "limit": limit,
        }
        res = self.client.index(index).search(query, options)
        hits = res.get("hits")
        if hits and len(hits) > 0:
            return hits

    def add_index(self, index_name, primary_key=None, docs=None):
        """
        """
        self.client.create_index(index_name, {"primaryKey": primary_key})
        if docs:
            self.add_documents(index_name, docs)
            return log.info(f"Index {index_name} created and documents added.")
        return log.info(f"Index {index_name} created.")

    def delete_index(self, index_name):
        """
        """
        if self.client.index(index_name).delete():
            return log.info(f"{index_name} deleted.")
        return log.info(f"{index_name} not found.")

    def add_documents(self, index_name, documents):
        """
        """
        self.client.index(index_name).update_documents(documents)
        log.info(f"{len(documents)} document(s) updated in the index.")

    def delete_documents(self, index_name, document_ids):
        """
        """
        index = self.client.get_index(index_name)
        index.delete_documents(document_ids)
        log.info(f"{len(document_ids)} document(s) deleted from the index.")

    async def enable_experimental_feature(self, feature_data):
        """
        """
        endpoint_url = f"{self.url}/experimental-features/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer lmVPWlWw97HheYxtqRrm7mGc-BuoNJPzp_ZoYNApI-Y",
        }
        data = json.dumps(feature_data)

        async with aiohttp.ClientSession() as session:
            async with session.patch(
                endpoint_url, data=data, headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to enable experimental feature: {response.status}")
                    return await response.text()

    async def update_settings(self, index_name, settings):
        """
        """
        full_url = f"{self.url}/indexes/{index_name}/settings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer lmVPWlWw97HheYxtqRrm7mGc-BuoNJPzp_ZoYNApI-Y",
        }
        data = json.dumps(settings)

        async with aiohttp.ClientSession() as session:
            async with session.patch(full_url, data=data, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return await response.text()


search_controller = SearchController("http://localhost:7700", envar("MEILI_MASTER_KEY"))
