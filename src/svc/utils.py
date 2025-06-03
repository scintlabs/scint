from __future__ import annotations

import json
from typing import Any

import dotenv


_DEFAULT_BASELINE: tuple[str, ...] = (
    "CREATE NODE TABLE Generic(id STRING, props STRING, PRIMARY KEY(id))",
    "CREATE REL TABLE RELATED(FROM Generic TO Generic, props STRING)",
)


def _quote(value: str) -> str:
    return value.replace("'", "\\'")


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, separators=(",", ":"))


def env(var: str):
    dotenv.load_dotenv()
    return dotenv.get_key(".env", var)
