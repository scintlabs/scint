from __future__ import annotations

from typing import Any, Dict, List

from attrs import define
from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.search import Hybrid

from src.core.types.signals import Query
from src.core.util.constants import MEILISEARCH


@define
class Index:
    name: str
    provider: IndexProvider

    async def search(self, query: Query):
        index = self.provider.index(query.index)
        res = await index.search(
            query=query.content,
            limit=query.limit,
            hybrid=Hybrid(**query.hybrid),
        )
        return res.hits

    async def add_records(self, index_name: str, records: List[Dict[str, Any]]):
        index = self.provider.index(index_name)
        await index.update_documents(records)
        return True

    async def delete_records(self, index_name: str, document_ids: List[str]) -> bool:
        index = self.provider.index(index_name)
        await index.delete_documents(document_ids)
        return True

    @classmethod
    def create(cls, name: str):
        index = cls(name)
        index.provider.register(index)
        return index


@define
class IndexProvider:
    client: AsyncClient = AsyncClient(**MEILISEARCH)

    async def search(self, query: Query):
        index = self.provider.index(query.index)
        res = await index.search(query.content, query.limit, query.hybrid)
        return res.hits

    async def add_records(self, index_name: str, records: List[Dict[str, Any]]):
        index = self.provider.index(index_name)
        await index.update_documents(records)
        return True

    async def update_records(self, index_name: str, documents: List[Any]) -> bool:
        return await self.add_records(index_name, documents)

    async def delete_records(self, index_name: str, document_ids: List[str]) -> bool:
        index = self.provider.index(index_name)
        await index.delete_documents(document_ids)
        return True

    async def create_index(self, name: str, key: str):
        index_obj = await self.client.create_index(name, primary_key=key)
        self.indexes[name] = index_obj
        return True

    async def clear_index(self, index_name: str):
        index = self.client.index(index_name)
        await index.delete_all_records()
        return True

    async def delete_index(self, index_name: str):
        await self.client.delete_index(index_name)
        self.indexes.pop(index_name, None)
        return True
