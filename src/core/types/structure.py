from __future__ import annotations

from enum import Enum
from uuid import uuid4
from typing import Any, Dict, List, Literal, TypeAlias
from typing import Callable

from attrs import define, field


class RoutingProtocol(Enum):
    Context = ("context", {})
    Execution = ("execution", {})
    Hierarchy = ("hierarchy", {})
    Relation = ("relation", {})

    def __init__(self, *args):
        self.protocol = args

    def __call__(self):
        return self.protocol


@define(slots=True)
class Route:
    id: str = field(factory=lambda: str(uuid4()))
    source: Port = field(init=False)
    destination: Port = field(init=False)
    protocol: RoutingProtocol = field(default=RoutingProtocol.Context)

    def create(self, source: Port, destination: Port, protocol: RoutingProtocol):
        self.source.routes.append(source)
        self.destination.routes.append(destination)

    def detach(self) -> None:
        if self in self.a.routes:
            self.a.routes.remove(self)
        if self in self.b.routes:
            self.b.routes.remove(self)


@define(slots=True)
class Port:
    id: str = field(factory=lambda: str(uuid4()))
    mode: Literal["in", "out"] = field(default="out")
    routes: List[Route] = field(factory=list)
    origin: Struct = field(init=False)

    def connect(self, other: Port) -> Route:
        for r in self.routes:
            if (r.a is self and r.b is other) or (r.a is other and r.b is self):
                return r
        return Route(a=self, b=other, protocol=self.protocol)

    def disconnect(self, other: Port) -> None:
        for r in list(self.routes):
            if r.involves(self, other):
                r.detach()

    def pull(self) -> List[Any]:
        buf, self.data[:] = self.data[:], []
        return buf

    @classmethod
    def create(cls, struct: Struct, op: Literal["in", "out"], rts: List[Route] = None):
        port = cls(mode=op)
        if rts:
            port.routes.extend(rts)
        struct.add_port(port)
        return port


@define(slots=True)
class Struct:
    id: str = field(factory=lambda: str(uuid4()))
    data: Dict[str, Any] = field(factory=dict)
    ports: List[Port] = field(factory=list)

    def __attrs_post_init__(self):
        self.add_port("input", RoutingProtocol.Context())
        self.add_port("output", RoutingProtocol.Context())

    def add_port(self, port: Port):
        if port not in self.ports:
            self.ports.append(port)

    def remove_port(self, port: Port) -> None:
        for r in list(port.routes):
            r.detach()
        self.ports.remove(port)

    def port(self, name: str) -> Port | None:
        return self.ports_by_name.get(name)


RuleFn: TypeAlias = Callable[[Port, Port], Any]


def context_rule(source: Port, dest: Port) -> Dict[str, Any]:
    summary = {"count": len(dest.data), "sample": dest.data[: min(5, len(dest.data))]}
    return {"out_data": list(source.data), "in_summary": summary}


def execution_rule(source: Port, dest: Port) -> None:
    items = source.pull()
    dest.data.extend(items)


def hierarchy_rule(source: Port, dest: Port) -> None:
    parent = source.origin
    child = dest.origin
    parent.data.setdefault("children", []).append(child.id)


def relation_rule(src: Port, dst: Port) -> None:
    triples = []
    for obj in dst.data:
        triples.append((src.data, dst.data))
    src.origin.data.setdefault("relations", []).extend(triples)
