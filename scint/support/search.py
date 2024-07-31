import asyncio
import uuid

from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.search import Hybrid

from scint.base.types.providers import ProviderType
from scint.base.utils import env


class SearchProvider(metaclass=ProviderType):
    def __init__(self):
        super().__init__()
        self.url = "http://localhost:7700"
        self.api_key = env("MEILISEARCH_KEY")
        self.client = AsyncClient(url=self.url, api_key=self.api_key)
        self.docs = {}
        self.context = None

    async def search(self, index_name, query, category=None, limit=4):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        filter = f"categories = {category}" if category else None
        index = self.client.index(index_name)
        res = await index.search(query, hybrid=hybrid, limit=limit, filter=filter)
        return res.hits

    async def load_indexes(self):
        async with asyncio.TaskGroup() as tg:
            for index_name, docs in self.docs.items():
                if self.client.index(index_name) is None:
                    tg.create_task(self.add_index(index_name))

    async def add_index(self, index_name):
        index = await self.client.index(index_name)
        await self.client.create_index(index, "id")

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
                {"id": str(uuid.uuid4()), **doc}
                name = doc.get("name")
                filter = f"name = {name}"
                tg.create_task(self.delete_docs(index, filter))

    async def delete_docs(self, index_name, filter):
        index = self.client.index(index_name)
        return await index.delete_documents_by_filter(filter)

    async def delete_all_docs(self, index_name):
        index = self.client.index(index_name)
        return await index.delete_all_documents()
