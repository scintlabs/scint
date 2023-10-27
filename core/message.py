import uuid
from datetime import datetime
from typing import Dict, List

from services.logger import log


class Message:
    def __init__(self, sender, recipient, message_data):
        log.info(f"Created message.")

        self.id = Message._generate_id()
        self.date: datetime = datetime.now()
        self.sender: str = sender
        self.recipient: str = recipient
        self.message_data: Dict[str, str] = message_data
        self.keywords: List[str] = []

    def add_keywords(self, keywords: List[str]):
        self.keywords.extend(keywords)

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())
