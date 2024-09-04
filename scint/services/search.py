import hashlib
import json

from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.search import Hybrid

from scint.core.utils.helpers import env
from scint.services import Service


class Search(Service):
    def __init__(self, context, prompts, functions):
        super().__init__()
        self.indexes = {"prompts": prompts, "functions": functions}
        self.url = "http://localhost:7700/"
        self.key = env("MEILISEARCH_API_KEY")
        self.client = AsyncClient(self.url, self.key)
        self.context = context.create("search")
        self.context = context
        self.context.search.results = self.results

    async def results(self, index_name, query, category=None, limit=4):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        category_filter = f"categories = {category}" if category else None
        index = self.client.index(index_name)
        res = await index.search(
            query, hybrid=hybrid, limit=limit, filter=category_filter
        )
        return res.hits

    async def load_indexes(self):
        for key, value in self.indexes.items():
            await self.update_docs(key, value)

    async def add_index(self, index_name):
        await self.client.create_index(index_name, "id")

    async def update_index(self, index_name, attr):
        index = self.client.index(index_name)
        return await index.update_filterable_attributes(attr)

    def generate_doc_id(self, doc):
        doc_copy = doc.copy()
        doc_copy.pop("id", None)
        stable_json = json.dumps(doc_copy, sort_keys=True)
        return hashlib.md5(stable_json.encode("utf-8")).hexdigest()

    async def update_docs(self, index_name, docs):
        index = self.client.index(index_name)
        updated_docs = []
        for doc in docs:
            doc_id = self.generate_doc_id(doc)
            updated_doc = {"id": doc_id, **doc}
            updated_docs.append(updated_doc)
        return await index.update_documents(updated_docs)

    async def delete_docs(self, index_name, filter):
        index = self.client.index(index_name)
        return await index.delete_documents_by_filter(filter)

    async def delete_all_docs(self, index_name):
        index = self.client.index(index_name)
        return await index.delete_all_documents()

    async def delete_index(self, index_name):
        index = self.client.index(index_name)
        return await index.delete()
