from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, Any, TypeVar
from datetime import datetime as dt
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from scint.lib.common.struct import Struct
from scint.lib.common.traits import Trait

T = TypeVar("T")


class Record(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created: str = Field(default_factory=lambda: dt.now().isoformat())
    modified: str = Field(default_factory=lambda: dt.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)
    model_config = ConfigDict(arbitrary_types_allowed=True)


class ContentType(Enum):
    TextContent = "TextContent"
    CodeContent = "CodeContent"
    ImageContent = "ImageContent"
    AudioContent = "AudioContent"
    VideoContent = "VideoContent"
    StructuredContent = "StructuredContent"
    BinaryContent = "BinaryContent"


class CatalogType(Enum):
    FileSystem = "FileSystem"
    DOMTree = "DOMTree"
    Database = "Database"
    Graph = "Graph"
    Collection = "Collection"


class Content(Record):
    type: ContentType
    content: str
    annotation: str
    embedding: Optional[List[float]] = None
    references: List[str] = Field(default_factory=list)


class ImageContent(Content):
    type: ContentType = ContentType.ImageContent
    data: str
    mime_type: str
    dimensions: Optional[tuple[int, int]] = None


class DataNode(Record):
    name: str
    path: str
    content: Optional[Content] = None
    children: List[DataNode] = Field(default_factory=list)
    parent_id: Optional[str] = None
    relationships: Dict[str, List[str]] = Field(default_factory=dict)

    def add_child(self, node: DataNode):
        node.parent_id = self.id
        self.children.append(node)

    def find_by_path(self, path: str) -> Optional[DataNode]:
        parts = path.split("/")
        current = self
        for part in parts:
            found = False
            for child in current.children:
                if child.name == part:
                    current = child
                    found = True
                    break
            if not found:
                return None
        return current


class Index(Record):
    name: str
    key: str
    sortables: List[str]
    filterables: List[str]
    searchables: List[str]
    embedding_config: Optional[Dict[str, Any]] = None


class Catalog(Struct):
    name: str
    type: CatalogType
    root: DataNode
    index: Index
    signals: List[str] = Field(default_factory=list)

    def add_node(self, path: str, content: Content) -> DataNode:
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
