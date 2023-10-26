import os
import uuid
from datetime import datetime
from typing import Dict, List

from services.openai import completion
from services.logger import log


class Message:
    def __init__(self, sender, recipient, message):
        log.info(f"Created message: {message}.")

        self.id = Message._generate_id()
        self.date: datetime = datetime.now()
        self.sender: str = sender
        self.recipient: str = recipient
        self.message: Dict[str, str] = message
        self.keywords: List[str] = []

    def add_keywords(self, keywords: List[str]):
        self.keywords.extend(keywords)

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())


def temporality() -> dict[str, str]:
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%m")

    return {
        "role": "system",
        "content": f"The following message was sent at {time} on {date}.",
        "name": "ScintSystem",
    }
