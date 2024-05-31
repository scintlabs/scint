import json
import asyncio

import aiohttp
from meilisearch import Client

from scint.modules.logging import log
from scint.support.utils import env
from scint.core.loader import loader
from scint.modules.logging import log


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {env('MEILI_MASTER_KEY')}",
}


class SearchController:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.search = Client(self.url, self.key)

    async def results(self, index, query, category=None, limit=4):
        hybrid = {"semanticRatio": 0.9, "embedder": "default"}
        options = {"hybrid": hybrid, "limit": limit}
        if category:
            options["filter"] = f"categories = {category}"
        res = self.search.index(index).search(query, options)
        hits = res.get("hits")
        if hits:
            return hits
        return []

    def load_indexes(self):
        log.info("Loading search indexes.")
        for libname, libdata in loader.library.items():
            self.add_index(libname, primary_key="id")
            self.search.index(libname).delete_all_documents()
            self.add_documents(libname, loader.library.get(libname))
            self.search.index(libname).update_filterable_attributes(["categories"])

    def update_indexes(self, index):
        self.search.index(index).update_filterable_attributes(["categories"])

    def add_index(self, index_name, primary_key=None, docs=None):
        log.info(f"Creating {index_name} index.")
        self.search.create_index(index_name, {"primaryKey": primary_key})
        if docs:
            self.add_documents(index_name, docs)

    def delete_index(self, index_name):
        self.search.index(index_name).delete()

    def add_documents(self, index_name, documents):
        self.search.index(index_name).update_documents(documents)
        log.info(f"Added {len(documents)} items to {index_name}.")

    def delete_documents(self, index_name, document_ids):
        index = self.search.index(index_name)
        index.delete_documents(document_ids)
        log.info(f"{len(document_ids)} document(s) deleted from the index.")

    def delete_all_documents(self, index_name):
        index = self.search.index(index_name)
        index.delete_all_documents()
        log.info(f"All documents deleted from the index.")

    async def update_settings(self, index_name, settings):
        url = f"{self.url}/indexes/{index_name}/settings"
        data = json.dumps(settings)
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, data=data, headers=headers) as r:
                if r.status == 200:
                    return await r.json()
                else:
                    return await r.text()

    async def enable_features(self, features_data):
        full_url = f"{self.url}/experimental-features/"
        data = json.dumps(features_data)
        async with aiohttp.ClientSession() as session:
            async with session.patch(full_url, data=data, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    log.error(f"{response.status}")
                    return await response.text()

    async def monitor_and_update_indexes(self):
        while True:
            try:
                self.load_indexes()
                log.info("Indexes loaded and updated.")
            except Exception as e:
                log.error(f"Error loading/updating indexes: {e}")
            await asyncio.sleep(3600)


search_controller = SearchController("http://localhost:7700", env("MEILI_MASTER_KEY"))
