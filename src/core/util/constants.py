from __future__ import annotations

import os
from pathlib import Path

import dotenv
from openai import AsyncOpenAI

from meilisearch_python_sdk import AsyncClient


def env(var: str) -> str:
    dotenv.load_dotenv()
    return dotenv.get_key(".env", var)


MEILI_HOST = env("MEILISEARCH_HOST")
MEILI_API_KEY = env("MEILISEARCH_API_KEY")
MEILISEARCH = {"url": MEILI_HOST, "api_key": MEILI_API_KEY}

PG_HOST = env("DB_HOST")
PG_DB_NAME = env("DB_NAME")
PG_DB_USERNAME = env("DB_USERNAME")
PG_DB_PASS = env("DB_PASSWORD")
POSTGRES = f"postgresql://{PG_DB_USERNAME}:{PG_DB_PASS}@{PG_HOST}/{PG_DB_NAME}"

ANTHROPIC_API_KEY = env("OPENAI_API_KEY")
OPENAI_API_KEY = env("OPENAI_API_KEY")

CONFIG = Path("config")

DATA = Path("src/data")
LIBRARY = Path("src/lib")
ENSEMBLES = Path(os.path.join(LIBRARY, "ensembles"))
INTERFACES = Path(os.path.join(LIBRARY, "interfaces"))
PROTOCOLS = Path(os.path.join(LIBRARY, "protocols"))
SCHEMAS = Path(os.path.join(LIBRARY, "schemas"))

anthropic_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
indexes: AsyncClient = AsyncClient(**MEILISEARCH)
