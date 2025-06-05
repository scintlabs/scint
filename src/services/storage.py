from __future__ import annotations

import uuid
import json
from contextlib import suppress
from typing import Any, Dict, Iterable
from attrs import define

from kuzu import Database


from .config import DATA
from .utils import _DEFAULT_BASELINE, _json_dumps, _quote


@define
class Node(str):
    label: str

    def __new__(cls, node_id: str, *, label: str):
        obj = super().__new__(cls, node_id)
        obj.label = label
        return obj


@define
class DataStore:
    schema: Iterable[str] = _DEFAULT_BASELINE
    database: Database = Database(DATA)

    def upsert_node(self, label: str, node_id: str = None, **props):
        node_id = node_id or uuid.uuid4().hex
        props_json = _json_dumps(props) if props else "{}"
        self._exec(
            f"MERGE (n:{label} {{id:'{_quote(node_id)}'}}) SET n += {{props:'{_quote(props_json)}'}}"
        )
        return Node(node_id, label=label)

    def upsert_edge(self, rel: str, src: Node, dst: Node, **props):
        props_json = _json_dumps(props) if props else "{}"
        self._exec(
            "MATCH (a:{lsrc} {{id:'{src_id}'}}), (b:{ldst} {{id:'{dst_id}'}}) "
            "MERGE (a)-[r:{rel}]->(b) SET r += {{props:'{props}'}}".format(
                lsrc=_quote(src.label),
                src_id=_quote(str(src)),
                ldst=_quote(dst.label),
                dst_id=_quote(str(dst)),
                rel=rel,
                props=_quote(props_json),
            )
        )

    def get_node(self, label: str, node_id: str):
        res = self._query(
            f"MATCH (n:{label} {{id:'{_quote(node_id)}'}}) RETURN n.props LIMIT 1"
        )
        if not res:
            return None
        return json.loads(res[0]) if res[0] else {}

    def list_nodes(self, label: str):
        res = self._query(f"MATCH (n:{label}) RETURN n.id, n.props")
        return [{"id": nid, **json.loads(props if props else {})} for nid, props in res]

    def query(self, cypher: str, params: Dict[str, Any] = None):
        return self._query(cypher, params)

    def _exec(self, cypher: str, params: Dict[str, Any] = None):
        try:
            self._con.execute(cypher, params or {})
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(cypher) from exc

    def _query(self, cypher: str, params: Dict[str, Any] = None):
        cur = self._con.execute(cypher, params or {})
        rows = []
        while cur.has_next():
            rows.append(cur.get_next())
        return rows

    def _ensure_schema(self, stmts: Iterable[str]):
        for stmt in stmts:
            with suppress(Exception):
                self._con.execute(stmt)


__all__ = DataStore, Node
