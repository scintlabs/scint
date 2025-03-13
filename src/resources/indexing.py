from __future__ import annotations

import hashlib
import json
from typing import Any, Optional, List, Dict

from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.search import Hybrid


from src.schemas.resources import Provider
from src.types.models import Model
from src.types.structure import Struct, Trait
from src.util.utils import env


class Index(Model):
    name: str
    key: str
    sortables: List[str]
    filterables: List[str]
    searchables: List[str]
    embedding_config: Optional[Dict[str, Any]] = None


class Indexing(Trait):
    async def list_indexes(self) -> List[str]:
        indexes = await self.client.get_indexes()
        return [index.uid for index in indexes]

    async def create_index(self, index: Index) -> bool:
        index = await self.client.create_index(index.name, primary_key=index.key)
        self._indexes[index.name] = index
        return True

    async def clear_index(self, index_name: str) -> bool:
        index = self.client.index(index_name)
        await index.delete_all_records()
        return True

    async def delete_index(self, index_name: str) -> bool:
        await self.client.delete_index(index_name)
        self._indexes.pop(index_name, None)
        return True

    async def search_index(self, index_name, query, category=None, limit=4):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        category_filter = f"categories = {category}" if category else None
        index = self.client.index(index_name)
        res = await index.search(
            query,
            hybrid=hybrid,
            limit=limit,
            filter=category_filter,
        )
        return res.hits


class Documenting(Trait):
    async def add_documents(self, index_name: str, documentas: List[Any]):
        def _generate_document_id(self, rec: dict):
            rec_copy = rec.copy()
            rec_copy.pop("id", None)
            stable_json = json.dumps(rec_copy, sort_keys=True)
            return hashlib.md5(stable_json.encode("utf-8")).hexdigest()

        index = self.client.index(index_name)
        rec = [{"id": self._generate_document_id(r.dict()), **r.dict()} for r in index]
        await index.update_documents(rec)
        return True

    async def update_documents(self, index_name: str, documents: List[Any]):
        return await self.add_documents(index_name, documents)

    async def delete_documents(self, index_name: str, recument_ids: List[str]):
        index = self.client.index(index_name)
        await index.delete_documents(recument_ids)
        return True


class Indexer(Struct, traits=(Indexing, Documenting)):
    indexes: Dict[str, List[Dict]] = {}
    provider: Provider = Provider(
        name="Meilisearch",
        module=AsyncClient,
        parameters={
            "host": "localhost",
            "port": 7700,
            "key": env("MEILISEARCH_API_KEY"),
        },
    )
