from __future__ import annotations

from typing import Dict, List, Optional, Any

from pydantic import Field

from scint.lib.types import Struct
from scint.lib.types import Trait
from scint.lib.schema.records import CatalogType, Block, DataNode, Index


class Catalog(Struct):
    name: str
    type: CatalogType
    root: DataNode
    index: Index
    signals: List[str] = Field(default_factory=list)

    def add_node(self, path: str, content: Block) -> DataNode:
        parts = path.split("/")
        current = self.root

        for i, part in enumerate(parts[:-1]):
            found = None
            for child in current.children:
                if child.name == part:
                    found = child
                    break
            if not found:
                new_node = DataNode(name=part, path="/".join(parts[: i + 1]))
                current.add_child(new_node)
                current = new_node
            else:
                current = found

        leaf = DataNode(name=parts[-1], path=path, content=content)
        current.add_child(leaf)
        return leaf

    def get_node(self, path: str) -> Optional[DataNode]:
        return self.root.find_by_path(path)


class Catalogable(Trait):
    def create_catalog(self, name: str, type: CatalogType, index: Index):
        root_node = DataNode(name="root", path="/")
        catalog = Catalog(name=name, type=type, root=root_node, index=index)
        self.catalogs[name] = catalog
        return catalog

    def create_view(self, name: str, catalogs: List[str], filters: Filters):
        view_catalogs = [self.catalogs[c] for c in catalogs if c in self.catalogs]
        view = LibraryView(view_catalogs, filters)
        self.views[name] = view
        return view

    def search(self, query: str, names: Optional[List[str]] = None):
        pass

    def link_to_signal(self, catalog_name: str, signal_id: str):
        if catalog_name in self.catalogs:
            self.catalogs[catalog_name].signals.append(signal_id)


class DataThread(Struct):
    catalog_views: Dict[str, LibraryView] = Field(default_factory=dict)

    def attach_view(self, name: str, view: LibraryView):
        self.catalog_views[name] = view

    def get_context_data(self) -> List[DataNode]:
        pass


class LibraryView(Trait):
    def apply_filters(self) -> List[DataNode]:
        pass

    def sort_by(self, key: str) -> List[DataNode]:
        pass


class Library(Struct):
    indices: Dict[str, Index] = Field(default_factory=dict)
    catalogs: Dict[str, Catalog] = Field(default_factory=dict)
    views: Dict[str, LibraryView] = Field(default_factory=dict)


Filters = Dict[str, Any]
