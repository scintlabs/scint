from datetime import datetime
from typing import List
from uuid import UUID

from scint.services.logger import log
from scint.util import generate_timestamp, generate_uuid4


class Message:
    def __init__(self, role: str, content: str, creator: str):
        self.id: UUID = generate_uuid4()
        self.created: datetime = generate_timestamp()
        self.last_processed = None
        self.role: str = role
        self.content: str = content
        self.content_summary: str = None
        self.keywords: List[str] = None
        self.named_entities: List[str] = None
        self.creator = creator

        log.info(f"{self.creator}: created message.")

    def data_dump(self, complete=False):
        if complete:
            return {
                "id": self.id,
                "created": self.created,
                "role": self.role,
                "content": self.content,
                "summary": self.content_summary,
                "keywords": self.keywords,
                "entities": self.named_entities,
            }
        else:
            return {
                "role": self.role,
                "content": self.content,
            }
