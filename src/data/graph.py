from __future__ import annotations

import json
from contextlib import suppress
from typing import Dict

import kuzu

from src.core.types.structure import Struct, Port, Route, RoutingProtocol

SCHEMA_QUERIES = [
    "CREATE NODE TABLE Struct(id STRING, data STRING, PRIMARY KEY(id))",
    """
    CREATE NODE TABLE Port(
         id          STRING,
         struct_id   STRING,
         name        STRING,
         mode        STRING,
         data        STRING,
         PRIMARY KEY(id)
    )""",
    "CREATE REL TABLE LINK(FROM Port TO Port)",
    "CREATE REL TABLE ROUTE(FROM Port TO Port, id STRING, protocol STRING)",
    "CREATE REL TABLE HAS_PORT(FROM Struct TO Port)",
]


def _quote(s: str) -> str:
    return s.replace("'", "\\'")


def ensure_schema(conn: kuzu.Connection) -> None:
    for q in SCHEMA_QUERIES:
        with suppress(Exception):
            conn.execute(q)


def _persist_struct(conn: kuzu.Connection, struct: Struct) -> None:
    conn.execute(
        f"MERGE (s:Struct {{id:'{_quote(struct.id)}}}) SET s.data='{_quote(json.dumps(struct.data))}'"
    )

    for port in struct.ports:
        conn.execute(
            """
            MERGE (p:Port {id:$pid})
            SET p.struct_id = $sid,
                p.name      = $name,
                p.mode      = $mode,
                p.data      = $data
            WITH p
            MATCH (s:Struct {id:$sid})
            MERGE (s)-[:HAS_PORT]->(p)
            """,
            {
                "pid": port.id,
                "sid": struct.id,
                "name": port.name,
                "mode": port.mode,
                "data": json.dumps(getattr(port, "data", [])),
            },
        )

    for port in struct.ports:
        for linked in getattr(port, "links", []):
            conn.execute(
                "MATCH (a:Port {id:$a}), (b:Port {id:$b}) MERGE (a)-[:LINK]->(b)",
                {"a": port.id, "b": linked.id},
            )

    for port in struct.ports:
        for route in port.routes:
            if route.source is not port:
                continue
            conn.execute(
                "MATCH (a:Port {id:$a}), (b:Port {id:$b}) \
                 MERGE (a)-[r:ROUTE {id:$rid}]->(b) \
                 SET r.protocol = $protocol",
                {
                    "a": route.source.id,
                    "b": route.destination.id,
                    "rid": route.id,
                    "protocol": route.protocol.name,
                },
            )


def sync_struct(conn: kuzu.Connection, struct: Struct) -> None:
    ensure_schema(conn)
    _persist_struct(conn, struct)


def load_struct(conn: kuzu.Connection, struct_id: str) -> Struct:
    res = conn.execute(f"MATCH (s:Struct {{id:'{_quote(struct_id)}}}) RETURN s.data")
    if not res.has_next():
        raise KeyError(f"Struct {struct_id} not found")

    struct_data = json.loads(res.get_next()[0])
    struct = Struct(id=struct_id, data=struct_data)

    ports_q = (
        f"MATCH (s:Struct {{id:'{_quote(struct_id)}}})-[:HAS_PORT]->(p:Port) "
        "RETURN p.id, p.name, p.mode, p.data"
    )
    ports_res = conn.execute(ports_q)
    port_lookup: Dict[str, Port] = {}
    while ports_res.has_next():
        pid, name, mode, pdata = ports_res.get_next()
        port = Port(id=pid, mode=mode)
        port.origin = struct
        setattr(port, "data", json.loads(pdata) if pdata else [])
        struct.ports.append(port)
        port_lookup[pid] = port

    links_q = (
        f"MATCH (a:Port)-[:LINK]->(b:Port) WHERE a.struct_id='{_quote(struct_id)}' "
        "RETURN a.id, b.id"
    )
    links_res = conn.execute(links_q)
    while links_res.has_next():
        a, b = links_res.get_next()
        if a in port_lookup and b in port_lookup:
            port_lookup[a].links.append(port_lookup[b])

    routes_q = (
        f"MATCH (a:Port)-[r:ROUTE]->(b:Port) WHERE a.struct_id='{_quote(struct_id)}' "
        "RETURN r.id, r.protocol, a.id, b.id"
    )
    routes_res = conn.execute(routes_q)
    while routes_res.has_next():
        rid, proto, aid, bid = routes_res.get_next()
        if aid in port_lookup and bid in port_lookup:
            src = port_lookup[aid]
            dst = port_lookup[bid]
            route = Route(
                id=rid, source=src, destination=dst, protocol=RoutingProtocol[proto]
            )
            src.routes.append(route)
            dst.routes.append(route)

    return struct
