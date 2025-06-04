from __future__ import annotations

from typing import Any, Dict, List

from attr import define
from attrs import field
from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.index import AsyncIndex

from src.config import MEILI_CLIENT


_INDEXES = ("threads", "tools")


@define
class Indexes:
    _client: AsyncClient = MEILI_CLIENT
    _indexes: Dict[str, AsyncIndex] = field(factory=dict)

    async def load_indexes(self):
        for i in _INDEXES:
            index = await self.get_index(i)
            self._indexes[i] = index

    async def add_records(self, records: List[Dict[str, Any]]):
        index = await self._client.get_index(self.name)
        await index.update_documents(records)
        return True

    async def delete_records(self, document_ids: List[str]):
        index = await self._client.get_index(self.name)
        await index.delete_documents(document_ids)
        return True

    async def get_index(self, name: str):
        return await self._client.get_index(name)

    async def create_index(self, name: str, primary_key: str):
        index = await self._client.create_index(name, primary_key=primary_key)
        self._indexes[name] = index
        return self._indexes[name]

    async def delete_index(self, name: str):
        await self._client.delete_index(name)
