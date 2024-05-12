import json

from meilisearch import Client

from scint.support.types import Message
from scint.support.logging import log


class SearchController:
    def __init__(self):
        self.url = "http://localhost:7700"
        self.key = "lmVPWlWw97HheYxtqRrm7mGc-BuoNJPzp_ZoYNApI-Y"
        self.client = Client(self.url, self.key)
        self.load_modules()

    def load_modules(self):
        self.modules = json.load(open("scint/modules.json", encoding="utf-8"))
        self.client.index("modules").add_documents(self.modules)

    def index_data(self):
        data = self.storage_controller.select_data("users", ["id", "name", "email"])
        documents = [{"id": row[0], "name": row[1], "email": row[2]} for row in data]
        self.add_documents(documents)

    def create_index(self, primary_key=None):
        if self.index_name not in self.client.get_indexes():
            self.client.create_index(self.index_name, {"primaryKey": primary_key})
            print(f"Index '{self.index_name}' created.")
        else:
            print(f"Index '{self.index_name}' already exists.")

    def add_documents(self, documents):
        index = self.client.get_index(self.index_name)
        index.add_documents(documents)
        print(f"{len(documents)} document(s) added to the index.")

    def update_documents(self, documents):
        index = self.client.get_index(self.index_name)
        index.update_documents(documents)
        print(f"{len(documents)} document(s) updated in the index.")

    def delete_documents(self, document_ids):
        index = self.client.get_index(self.index_name)
        index.delete_documents(document_ids)
        print(f"{len(document_ids)} document(s) deleted from the index.")

    async def search_documents(self, query, filters=None, limit=10):
        options = {
            "hybrid": {"semanticRatio": 0.9, "embedder": "default"},
            "limit": limit,
            "filters": filters,
        }
        res = self.client.index("documents").search(query, options)
        hits = res.get("hits")

        if hits and len(hits) > 0:
            yield hits[0].get("documents")

    def get_document(self, document_id):
        index = self.client.get_index(self.index_name)
        return index.get_document(document_id)

    def get_index_stats(self):
        index = self.client.get_index(self.index_name)
        return index.get_stats()
