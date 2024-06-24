from uuid import uuid4
from datetime import datetime

import websockets
from pydantic import BaseModel, Field

from scint.support.types import Any, Dict, List, Optional, Union
from scint.support.logging import log
from scint.support.types import Dict, List, Optional
from scint.settings import intelligence

WebSocket = websockets.WebSocketCommonProtocol
WebSocketDisconnect = websockets.exceptions.ConnectionClosed


class Function(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = {}
    categories: List[str] = []
    labels: List[str] = None

    @property
    def metadata(self):
        return self._metadata()

    def _metadata(self):
        type = self.__class__.__name__.lower()

        return {
            "type": type,
            type: {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def invoke(func):
        return func


class Arguments(BaseModel):
    name: str
    arguments: Dict[str, Any]


class Message(BaseModel):
    content: List[Dict[str, Any]]
    labels: List[str] = None
    embedding: List[float] = None

    @property
    def metadata(self):
        role = ""
        content = []
        if self.__class__.__name__.startswith("Assistant"):
            role = "assistant"
        elif self.__class__.__name__.startswith("User"):
            role = "user"
        elif role == "":
            role = "system"

        for block in self.content:
            content.append(block.data)

        return {"role": role, "content": content}


class AssistantMessage(Message):
    pass


class UserMessage(Message):
    pass


class SystemMessage(Message):
    pass


class Event(Message):
    pass


class Prompt(Message):
    pass
