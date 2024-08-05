import asyncio
import uuid

from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.search import Hybrid

from scint.base.utils import env


class Search:
    def __init__(self, url, api_key):
        super().__init__()
        print("Starting search service.")
        self.url = url
        self.api_key = env(api_key)
        self.client = AsyncClient(self.url, self.api_key)
        self.docs = {}
        self.context = None

    async def search(self, index_name, query, category=None, limit=4):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        category_filter = f"categories = {category}" if category else None
        index = self.client.index(index_name)
        res = await index.search(
            query, hybrid=hybrid, limit=limit, filter=category_filter
        )
        return res.hits

    async def load_indexes(self):
        async with asyncio.TaskGroup() as tg:
            for index_name, docs in self.docs.items():
                if self.client.index(index_name) is None:
                    tg.create_task(self.add_index(index_name))

    async def add_index(self, index_name):
        await self.client.create_index(index_name, "id")

    async def update_index(self, index_name, attr):
        index = self.client.index(index_name)
        return await index.update_filterable_attributes(attr)

    async def add_docs(self, index_name, docs):
        index = self.client.index(index_name)
        return await index.add_documents(docs)

    async def update_docs(self, index_name, docs):
        index = self.client.index(index_name)
        async with asyncio.TaskGroup() as tg:
            for doc in docs:
                doc = {"id": str(uuid.uuid4()), **doc}
                name = doc.get("name")
                filter_template = f"name = {name}"
                tg.create_task(self.delete_docs(index, filter_template))

    async def delete_docs(self, index_name, filter):
        index = self.client.index(index_name)
        return await index.delete_documents_by_filter(filter)

    async def delete_all_docs(self, index_name):
        index = self.client.index(index_name)
        return await index.delete_all_documents()
