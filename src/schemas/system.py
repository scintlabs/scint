from __future__ import annotations

from typing import List, Dict

from src.resources.continuity import Continuity
from src.resources.indexing import Indexer
from src.resources.library import Library
from src.types.structure import Struct, Trait
from src.schemas.structure import Boundary, Link


class Construction(Trait):
    def get_boundary(self, name: str):
        return self.boundaries[name]

    def create_boundary(self, name: str):
        boundary = Boundary()
        self.add_boundary(name=name, boundary=boundary)
        return self.boundaries[name]

    def add_boundary(self, name: str, boundary: Boundary):
        self.boundaries[name] = boundary
        if name not in self.adjacency:
            self.adjacency[name] = []

    def remove_boundary(self, name: str):
        if name not in self.boundaries:
            return

        neighbors = self.adjacency.get(name, [])
        boundary = self.boundaries[name]

        for neighbor_id in neighbors:
            if neighbor_id in self.adjacency:
                self.adjacency[neighbor_id].remove(name)

        for link in list(boundary.links):
            self._remove_link_from_region(link)

        del self.adjacency[name]
        del self.boundaries[name]

    def link_boundaries(self, first_id: str, second_id: str, link_id: str, link: Link):
        if first_id not in self.boundaries or second_id not in self.boundaries:
            raise ValueError("Cannot link non-existent boundaries.")
        b1 = self.boundaries[first_id]
        b2 = self.boundaries[second_id]
        link.connect(b1)
        link.connect(b2)
        self.links[link_id] = link
        self.adjacency[first_id].append(second_id)
        self.adjacency[second_id].append(first_id)

    def unlink_boundaries(self, first_id: str, second_id: str, link_id: str):
        if link_id not in self.links:
            return

        link = self.links[link_id]
        b1 = self.boundaries.get(first_id)
        b2 = self.boundaries.get(second_id)

        if b1 and b2:
            link.disconnect(b1)
            link.disconnect(b2)

            if second_id in self.adjacency[first_id]:
                self.adjacency[first_id].remove(second_id)
            if first_id in self.adjacency[second_id]:
                self.adjacency[second_id].remove(first_id)

        del self.links[link_id]

    def get_neighbors(self, boundary_id: str) -> List[str]:
        return self.adjacency.get(boundary_id, [])

    def are_connected(self, first_id: str, second_id: str):
        return second_id in self.adjacency.get(first_id, [])

    def _remove_link_from_region(self, link: Link):
        link_ids = [lid for lid, lobj in self.links.items() if lobj is link]
        for lid in link_ids:
            if len(link.boundaries) == 2:
                b1, b2 = link.boundaries
                b1_id = self._find_boundary_id(b1)
                b2_id = self._find_boundary_id(b2)
                if b1_id and b2_id:
                    self.unlink_boundaries(b1_id, b2_id, lid)
            else:
                for b in list(link.boundaries):
                    link.disconnect(b)
                if lid in self.links:
                    del self.links[lid]

    def _find_boundary_id(self, boundary: Boundary) -> str:
        for bid, obj in self.boundaries.items():
            if obj is boundary:
                return bid
        return ""


class Base(Trait):
    def load(self):
        self.library.load()
        self.create_region("user")
        self.regions[-1].create_boundary("notes")
        self.regions[-1].create_boundary("projects")
        self.regions[-1].create_boundary("pipelines")
        self.regions[-1].create_boundary("default")

    def create_region(self, name: str):
        region = Region()
        self.regions.append(region)


class Region(Struct, traits=(Construction,)):
    adjacency: Dict[str, List[str]] = {}
    boundaries: Dict[str, Boundary] = {}
    links: Dict[str, Link] = {}


class System(Struct, traits=(Base,)):
    continuity: Continuity
    indexing: Indexer = Indexer()
    library: Library = Library()
    regions: List[Region] = []
