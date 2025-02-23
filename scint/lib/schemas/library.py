from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional

from meilisearch_python_sdk.models.search import Hybrid

from scint.lib.types.exceptions import PromptError
from scint.lib.schemas.signals import Block, Message
from scint.lib.schemas.models import Model
from scint.lib.types.struct import Struct
from scint.lib.types.traits import Trait


class Index(Model):
    name: str
    key: str
    sortables: List[str]
    filterables: List[str]
    searchables: List[str]
    embedding_config: Optional[Dict[str, Any]] = None


class Catalog(Model):
    name: str
    index: Index
    signals: List[str] = []


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


class Indexed(Trait):
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


class Catalogable(Trait):
    def create_catalog(self, name: str, index: Index):
        # root_node = DataNode(name="root", path="/")
        catalog = Catalog(name=name, type=type, index=index)
        self.catalogs[name] = catalog
        return catalog

    def create_view(self, name: str, catalogs: List[str], filters: Filters):
        view_catalogs = [self.catalogs[c] for c in catalogs if c in self.catalogs]
        view = LibraryView(view_catalogs, filters)
        self.views[name] = view
        return view

    def link_context(self, catalog_name: str, context_id: str):
        if catalog_name in self.catalogs:
            self.catalogs[catalog_name].contexts.append(context_id)

    def add_node(self, path: str, content: Block):
        pass
        # parts = path.split("/")
        # current = self.root

        # for i, part in enumerate(parts[:-1]):
        #     found = None
        #     for child in current.children:
        #         if child.name == part:
        #             found = child
        #             break
        # if not found:
        #     new_node = DataNode(name=part, path="/".join(parts[: i + 1]))
        #     current.add_child(new_node)
        #     current = new_node
        # else:
        #     current = found

        # leaf = DataNode(name=parts[-1], path=path, content=content)
        # current.add_child(leaf)
        # return leaf

    def get_node(self, path: str):
        return self.root.find_by_path(path)


class LibraryView(Trait):
    def sort_by(self, key: str) -> List[Any]:
        pass

    def apply_filters(self) -> List[Any]:
        pass


class PromptLoader:
    def get_prompt(self, prompt_id: str) -> List[Message]:
        prompt_path: Path = self.path / prompt_id
        prompt_files: list[Path] = list(prompt_path.glob("*.md"))
        if len(prompt_files) == 0:
            raise FileNotFoundError(f"Prompt template not found: {prompt_id}")

        messages: list[Message] = []
        for prompt_file in prompt_files:
            with open(prompt_file, "r") as file:
                content: str = file.read()
                role: str = prompt_file.name.split(".")[0]

                if role not in ["assistant", "user", "system", "tool", "function"]:
                    raise PromptError(
                        prompt_id=prompt_id,
                        message=(
                            f"invalid role: {role} in prompt template. "
                            "Valid roles are: assistant, user, system, tool, function"
                        ),
                    )

                messages.append(Message(role=role, content=content))
        return messages


class Library(Struct):
    indices: Dict[str, Index] = {}
    catalogs: Dict[str, Catalog] = {}
    views: Dict[str, LibraryView] = {}


Filters = Dict[str, Any]
