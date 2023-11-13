import asyncio
from uuid import UUID
from typing import Dict, List, Any

from services.logger import log
from services.openai import embedding, summary
from core.util import generate_timestamp, generate_uuid4


class Artifact:
    def __init__(self):
        self.id: UUID = generate_uuid4()
        self.created: str = generate_timestamp()


class File(Artifact):
    def __init__(self):
        super().__init__()
