from __future__ import annotations

import os
from pathlib import Path

from meilisearch_python_sdk import AsyncClient
from redis.asyncio import Redis

from src.services.utils import env

CONFIG = Path("config")
CONFIG.parent.mkdir(parents=True, exist_ok=True)
CONFIG_CONTINUITY = os.path.join(CONFIG, "continuity.json")
CONFIG_LIB = os.path.join(CONFIG, "library.json")

DATA = Path("data")
DATA.parent.mkdir(parents=True, exist_ok=True)
DATA_THREADS = os.path.join(DATA, "threads")
DATA_LIBRARY = os.path.join(DATA, "library")
DATA_KNOWLEDGE = os.path.join(DATA, "knowledge")

PG_HOST = env("PG_HOST")
PG_DB_NAME = env("PG_DB_NAME")
PG_DB_USERNAME = env("PG_DB_USERNAME")
PG_DB_PASSWORD = env("PG_DB_PASSWORD")
PG_STRING = f"postgresql://{PG_DB_USERNAME}:{PG_DB_PASSWORD}@{PG_HOST}/{PG_DB_NAME}"
PG_CLIENT = None

REDIS_HOST = "redis://localhost"
REDIS_CLIENT = Redis(host=REDIS_HOST)

MEILI_HOST = env("MEILISEARCH_HOST")
MEILI_API_KEY = env("MEILISEARCH_API_KEY")
MEILI_STRING = {"url": MEILI_HOST, "api_key": MEILI_API_KEY}
MEILI_CLIENT: AsyncClient = AsyncClient(**MEILI_STRING)
