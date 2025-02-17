from __future__ import annotations

from typing import Generator

from scint.api.types import Aspect, Struct


class Crawler(Aspect):
    __slots__ = ()

    def __init__(self, struct: Struct, **kwargs):
        super().__init__(struct, **kwargs)

    def walk(self, visited=None) -> Generator[Struct, None, None]:
        if visited is None:
            visited = set()
        if self in visited:
            return

        visited.add(self)
        from collections import deque

        queue = deque([self._root])
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            yield current

            for child in current._children:
                if child not in visited:
                    queue.append(child)

            if current._origin and current._origin not in visited:
                queue.append(current._origin)

    def step(self):
        pass
