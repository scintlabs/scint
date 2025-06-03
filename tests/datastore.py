from __future__ import annotations

import json
import uuid
from typing import Any, Dict, Iterable

from kuzu import Database
from attrs import define
from contextlib import suppress

from src.util.constants import DATA


# import os
# import json
# from contextlib import suppress
# from typing import Any, Dict, List, Literal, Optional

# import kuzu
# from attrs import define, field

# from src.base.protocol import composable


# @composable
# class Route:
#     source: Port = field(init=False)
#     destination: Port = field(init=False)


# @composable
# class Port:
#     mode: Literal["in", "out"] = field(default="out")
#     routes: List[Route] = field(factory=list)
#     origin: Node = field(init=False)

#     def connect(self, other: Port):
#         for r in self.routes:
#             if (r.a is self and r.b is other) or (r.a is other and r.b is self):
#                 return r
#         return Route(a=self, b=other, protocol=self.protocol)

#     def disconnect(self, other: Port):
#         for r in list(self.routes):
#             if r.involves(self, other):
#                 r.detach()

#     @classmethod
#     def create(cls, struct: Node, op: Literal["in", "out"], rts: List[Route] = None):
#         port = cls(mode=op)
#         if rts:
#             port.routes.extend(rts)
#         struct.add_port(port)
#         return port


# @composable
# class Node:
#     data: Dict[str, Any] = field(factory=dict)
#     ports: List[Port] = field(factory=list)

#     def __attrs_post_init__(self):
#         self.add_port("in")
#         self.add_port("out")

#     def add_port(self, port: Port):
#         if port not in self.ports:
#             self.ports.append(port)

#     def remove_port(self, port: Port):
#         for r in list(port.routes):
#             r.detach()
#         self.ports.remove(port)


# @composable
# class Structure:
#     nodes = field(type=Dict[str, Node], factory=dict)
#     routes = field(type=List[Route], factory=list)

#     def __attrs_post_init__(self):
#         if self.schema:
#             self.schema.initialize(self)

#     def add_node(self, key: str, **node_data) -> Node:
#         node = Node(data=node_data)
#         self.structure.nodes[key] = node

#         if self.schema:
#             self.schema.configure_node(key, node)

#         return node

#     def connect(self, src_node: str, dest_node: str):
#         source = self.structure.nodes.get(src_node)
#         dest = self.structure.nodes.get(dest_node)

#         if not source or not dest:
#             raise ValueError(f"Cannot find nodes: {src_node} -> {dest_node}")

#         src_port = next((p for p in source.ports if p.mode == "out"), None)
#         dst_port = next((p for p in dest.ports if p.mode == "in"), None)

#         if not src_port or not dst_port:
#             raise ValueError("Required ports not found")

#         route = src_port.connect(dst_port)
#         self.structure.routes.append(route)

#         if self.schema:
#             self.schema.configure_route(route, src_node, dest_node)

#         return route

#     def get_node(self, key: str) -> Optional[Node]:
#         return self.structure.nodes.get(key)

#     def execute(self, **kwargs):
#         if not self.schema:
#             raise ValueError("No schema available for execution")
#         return self.schema.execute(self, **kwargs)


# SCHEMA_QUERIES = [
#     "CREATE NODE TABLE Struct(id STRING, data STRING, PRIMARY KEY(id))",
#     """
#     CREATE NODE TABLE Port(
#          id          STRING,
#          struct_id   STRING,
#          name        STRING,
#          mode        STRING,
#          data        STRING,
#          PRIMARY KEY(id)
#     )""",
#     "CREATE REL TABLE LINK(FROM Port TO Port)",
#     "CREATE REL TABLE ROUTE(FROM Port TO Port, id STRING, protocol STRING)",
#     "CREATE REL TABLE HAS_PORT(FROM Struct TO Port)",
# ]


# def _quote(s: str) -> str:
#     return s.replace("'", "\\'")


# def ensure_schema(conn: kuzu.Connection):
#     for q in SCHEMA_QUERIES:
#         with suppress(Exception):
#             conn.execute(q)


# def _persist_struct(conn: kuzu.Connection, struct: Structure):
#     conn.execute(
#         f"MERGE (s:Struct {{id:'{_quote(struct.id)}}}) SET s.data='{_quote(json.dumps(struct.data))}'"
#     )

#     for port in struct.ports:
#         conn.execute(
#             """
#             MERGE (p:Port {id:$pid})
#             SET p.struct_id = $sid,
#                 p.name      = $name,
#                 p.mode      = $mode,
#                 p.data      = $data
#             WITH p
#             MATCH (s:Struct {id:$sid})
#             MERGE (s)-[:HAS_PORT]->(p)
#             """,
#             {
#                 "pid": port.id,
#                 "sid": struct.id,
#                 "name": port.name,
#                 "mode": port.mode,
#                 "data": json.dumps(getattr(port, "data", [])),
#             },
#         )

#     for port in struct.ports:
#         for linked in getattr(port, "links", []):
#             conn.execute(
#                 "MATCH (a:Port {id:$a}), (b:Port {id:$b}) MERGE (a)-[:LINK]->(b)",
#                 {"a": port.id, "b": linked.id},
#             )

#     for port in struct.ports:
#         for route in port.routes:
#             if route.source is not port:
#                 continue
#             conn.execute(
#                 "MATCH (a:Port {id:$a}), (b:Port {id:$b}) \
#                  MERGE (a)-[r:ROUTE {id:$rid}]->(b) \
#                  SET r.protocol = $protocol",
#                 {
#                     "a": route.source.id,
#                     "b": route.destination.id,
#                     "rid": route.id,
#                     "protocol": route.protocol.name,
#                 },
#             )


# def sync_struct(conn: kuzu.Connection, struct: Structure):
#     ensure_schema(conn)
#     _persist_struct(conn, struct)


# def load_struct(conn: kuzu.Connection, struct_id: str):
#     res = conn.execute(f"MATCH (s:Struct {{id:'{_quote(struct_id)}}}) RETURN s.data")
#     if not res.has_next():
#         raise KeyError(f"Struct {struct_id} not found")

#     struct_data = json.loads(res.get_next()[0])
#     struct = Structure(id=struct_id, data=struct_data)

#     ports_q = (
#         f"MATCH (s:Struct {{id:'{_quote(struct_id)}}})-[:HAS_PORT]->(p:Port) "
#         "RETURN p.id, p.name, p.mode, p.data"
#     )
#     ports_res = conn.execute(ports_q)
#     port_lookup: Dict[str, Port] = {}
#     while ports_res.has_next():
#         pid, name, mode, pdata = ports_res.get_next()
#         port = Port(id=pid, mode=mode)
#         port.origin = struct
#         setattr(port, "data", json.loads(pdata) if pdata else [])
#         struct.ports.append(port)
#         port_lookup[pid] = port

#     links_q = (
#         f"MATCH (a:Port)-[:LINK]->(b:Port) WHERE a.struct_id='{_quote(struct_id)}' "
#         "RETURN a.id, b.id"
#     )
#     links_res = conn.execute(links_q)
#     while links_res.has_next():
#         a, b = links_res.get_next()
#         if a in port_lookup and b in port_lookup:
#             port_lookup[a].links.append(port_lookup[b])

#     routes_q = (
#         f"MATCH (a:Port)-[r:ROUTE]->(b:Port) WHERE a.struct_id='{_quote(struct_id)}' "
#         "RETURN r.id, r.protocol, a.id, b.id"
#     )
#     routes_res = conn.execute(routes_q)
#     while routes_res.has_next():
#         rid, proto, aid, bid = routes_res.get_next()
#         if aid in port_lookup and bid in port_lookup:
#             src = port_lookup[aid]
#             dst = port_lookup[bid]
#             route = Route(id=rid, source=src, destination=dst)
#             src.routes.append(route)
#             dst.routes.append(route)

#     return struct


# def structures(structure: str):
#     db = kuzu.Database(os.path.join("src/data/dump", structure))
#     con = kuzu.Connection(db)
#     return ensure_schema(con)
