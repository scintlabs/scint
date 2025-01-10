from __future__ import annotations

import json
import hashlib
from enum import Enum, auto
from datetime import datetime
from typing import Any, Dict, List, Optional

from meilisearch_python_sdk import AsyncClient

from src.core.types import BaseType, Struct
from src.util.utils import env


class IndexStatus(Enum):
    AVAILABLE = auto()
    PROCESSING = auto()
    ERROR = auto()


class IndexConfig(Struct):
    name: str
    primary_key: str = "id"
    filterable_attributes: List[str] = []
    sortable_attributes: List[str] = []
    searchable_attributes: List[str] = []


class IndexStats(Struct):
    name: str
    num_documents: int
    created_at: datetime
    last_updated: Optional[datetime]
    size_bytes: int


class Indexer(metaclass=BaseType):
    def __init__(self, url: str, key: str):
        self.client = AsyncClient(url, env(key))
        self._indexes: Dict[str, Any] = {}

    async def create_index(self, config: IndexConfig) -> bool:
        try:
            index = await self.client.create_index(
                config.name,
                primary_key=config.primary_key,
            )

            if config.filterable_attributes:
                await index.update_filterable_attributes(config.filterable_attributes)
            if config.sortable_attributes:
                await index.update_sortable_attributes(config.sortable_attributes)
            if config.searchable_attributes:
                await index.update_searchable_attributes(config.searchable_attributes)

            self._indexes[config.name] = index
            return True
        except Exception as e:
            print(f"Failed to create index {config.name}: {str(e)}")
            return False

    async def add_documents(self, index_name: str, documents: List[Any]):
        try:
            index = self.client.index(index_name)
            docs_to_add = [
                {"id": self._generate_doc_id(doc.dict()), **doc.dict()}
                for doc in documents
            ]
            await index.update_documents(docs_to_add)
            return True
        except Exception as e:
            print(f"Failed to add documents to {index_name}: {str(e)}")
            return False

    async def get_index_stats(self, index_name: str) -> IndexStats:
        try:
            index = self.client.index(index_name)
            stats = await index.get_stats()
            return IndexStats(
                name=index_name,
                num_documents=stats.number_of_documents,
                created_at=stats.created_at,
                last_updated=stats.last_update,
                size_bytes=stats.database_size,
            )
        except Exception:
            return None

    async def list_indexes(self) -> List[str]:
        try:
            indexes = await self.client.get_indexes()
            return [index.uid for index in indexes]
        except Exception:
            return []

    async def get_index_status(self, index_name: str):
        try:
            index = self.client.index(index_name)
            status = await index.get_status()
            return IndexStatus.AVAILABLE if status.is_ready else IndexStatus.PROCESSING
        except Exception:
            return IndexStatus.ERROR

    async def update_documents(self, index_name: str, documents: List[Any]):
        return await self.add_documents(index_name, documents)

    async def delete_documents(self, index_name: str, document_ids: List[str]):
        try:
            index = self.client.index(index_name)
            await index.delete_documents(document_ids)
            return True
        except Exception:
            return False

    async def clear_index(self, index_name: str) -> bool:
        try:
            index = self.client.index(index_name)
            await index.delete_all_documents()
            return True
        except Exception:
            return False

    async def delete_index(self, index_name: str) -> bool:
        try:
            await self.client.delete_index(index_name)
            self._indexes.pop(index_name, None)
            return True
        except Exception:
            return False

    def _generate_doc_id(self, doc: dict):
        doc_copy = doc.copy()
        doc_copy.pop("id", None)
        stable_json = json.dumps(doc_copy, sort_keys=True)
        return hashlib.md5(stable_json.encode("utf-8")).hexdigest()
