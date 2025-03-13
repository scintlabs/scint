from __future__ import annotations

from typing import List

from src.types.structure import Struct, Trait


class Linking(Trait):
    def add_link(self, link: Link):
        if link not in self.links:
            self.links.append(link)
            link.connect(self)

    def remove_link(self, link: Link):
        if link in self.links:
            self.links.remove(link)
            link.disconnect(self)


class Connecting(Trait):
    def connect(self, boundary: Boundary):
        if boundary not in self.boundaries:
            self.boundaries.append(boundary)
            boundary.links.append(self)

    def disconnect(self, boundary: Boundary):
        if boundary in self.boundaries:
            self.boundaries.remove(boundary)
            boundary.links.remove(self)


class Link(Struct, traits=(Connecting,)):
    boundaries: List[Boundary] = []


class Boundary(Struct, traits=(Linking,)):
    links: List[Link] = []
