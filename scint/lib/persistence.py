from __future__ import annotations

import json
import hashlib
from typing import Any, List

from meilisearch_python_sdk.models.search import Hybrid

from scint.lib.types import Trait
from scint.lib.protocols import Index


class CanSearch(Trait):
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


class CanIndex(Trait):
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


class Recordable(Trait):
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


class Persistable(Trait):
    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not hasattr(instance, self.private_name):
            value = self._load_state() or self.initial_value
            setattr(instance, self.private_name, value)
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)
        if self.persistence_key is not None:
            self._save_state(value)

    def _save_state(self, value):
        print(f"Persisting {self.persistence_key} = {value}")
        with open(f"{self.persistence_key}.txt", "w") as f:
            f.write(str(value))

    def _load_state(self):
        try:
            with open(f"{self.persistence_key}.txt", "r") as f:
                data = f.read()
                print(f"Loaded persisted {self.persistence_key} = {data}")
                return data
        except FileNotFoundError:
            return None
