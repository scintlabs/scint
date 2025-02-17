from __future__ import annotations

import json
import hashlib
from typing import Any, List

from meilisearch_python_sdk.models.search import Hybrid

from scint.api.structs import Index
from scint.api.types import Trait


class Indexable(Trait):
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


class Encodable(Trait):
    async def add_records(self, index_name: str, records: List[Any]):
        def _generate_record_id(self, rec: dict):
            rec_copy = rec.copy()
            rec_copy.pop("id", None)
            stable_json = json.dumps(rec_copy, sort_keys=True)
            return hashlib.md5(stable_json.encode("utf-8")).hexdigest()

        index = self.client.index(index_name)
        rec = [{"id": self._generate_record_id(r.dict()), **r.dict()} for r in records]
        await index.update_records(rec)
        return True

    async def update_records(self, index_name: str, records: List[Any]):
        return await self.add_records(index_name, records)

    async def delete_records(self, index_name: str, recument_ids: List[str]):
        index = self.client.index(index_name)
        await index.delete_records(recument_ids)
        return True


class Retrievable(Trait):
    async def list_indexes(self) -> List[str]:
        indexes = await self.client.get_indexes()
        return [index.uid for index in indexes]

    async def search(self, index_name, query, category=None, limit=4):
        hybrid = Hybrid(semantic_ratio=0.9, embedder="default")
        category_filter = f"categories = {category}" if category else None
        index = self.client.index(index_name)
        res = await index.search(
            query, hybrid=hybrid, limit=limit, filter=category_filter
        )
        return res.hits


class Composable(Trait):
    async def compose(self, composition):
        pass

    def encode_composition(self, kind, *args, **kwargs):
        composition = kind
        self.compositions[composition.id] = composition
        return self.compositions[composition]

    def get_composition(self, composition_id):
        if composition_id in self.compositions.keys():
            return self.compositions[composition_id]

    def update_composition(self, composition, *args, **kargs):
        for arg in args:
            print(composition)
            print(arg)
