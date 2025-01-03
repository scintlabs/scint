import hashlib
import json
from typing import Any, Dict

from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.search import Hybrid

from ...util.utils import env


class Index:
    def __init__(self, url, key):
        self.client = AsyncClient(url, env(key))
        self.indexes: Dict[str, Any] = {}

    def add_struct(self, struct):
        self.structs[struct.id] = struct
        self.index_struct(struct)

    def index_struct(self, struct):
        self.index[struct.id] = struct
        self.index[f"{struct.id}"] = {}

    def add(self, resource):
        self.indexes[resource.description] = {
            resource: resource.description,
            "children": resource.children,
        }


class Resources:
    def __init__(self, url, key):
        self.client = AsyncClient(url, env(key))
        self.indexes: Dict[str, Any] = {}

    def add_struct(self, struct):
        self.structs[struct.id] = struct
        self.index_struct(struct)

    def index_struct(self, struct):
        self.index[struct.id] = struct
        self.index[f"{struct.id}"] = {}

    def add(self, resource):
        self.indexes[resource.description] = {
            resource: resource.description,
            "children": resource.children,
        }

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

    async def update_docs(self, index_name, docs):
        index = self.client.index(index_name)
        updated_docs = []
        for doc in docs:
            doc_id = self._generate_doc_id(doc)
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

    def _generate_doc_id(self, doc):
        doc_copy = doc.copy()
        doc_copy.pop("id", None)
        stable_json = json.dumps(doc_copy, sort_keys=True)
        return hashlib.md5(stable_json.encode("utf-8")).hexdigest()
