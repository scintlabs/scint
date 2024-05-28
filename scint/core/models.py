import typing
from uuid import uuid4
from datetime import datetime

import websockets
from pydantic import BaseModel, Field

from scint.modules.logging import log

WebSocket = websockets.WebSocketCommonProtocol
WebSocketDisconnect = websockets.exceptions.ConnectionClosed
Any = typing.Any
List = typing.List
Dict = typing.Dict
Optional = typing.Optional
Callable = typing.Callable
AsyncGenerator = typing.AsyncGenerator
Union = typing.Union


class Header(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created: str = Field(default_factory=lambda: datetime.now().isoformat())


class Event(BaseModel):
    header: Header = Header()


class ProviderParams(BaseModel):
    provider: str = "openai"
    format: str = "completion"
    preset: str = "balanced"


class MessageClassification(BaseModel):
    continuation: bool = False
    annotations: str = None


class MessageContent(BaseModel):
    response: Optional[List[Dict[str, Any]]] = []
    content: str = ""

    def __init__(self, **data):
        super().__init__(**data)
        self.content = self.rgetblocks(self.response)

    @staticmethod
    def rgetblocks(response, blocks=None):
        if blocks is None:
            blocks = []

        def _rgetblocks(block):
            try:
                if "block" in block:
                    return f"{block["block"]}"
                if "code" in block and "language" in block:
                    return f"```{block['language']}\n\n{block['code']}\n```"
                if "content" in block:
                    return block["content"]
            except (KeyError, IndexError, AttributeError):
                return None

        for block in response:
            result = _rgetblocks(block)
            if result:
                blocks.append(result)

        return "\n\n".join(blocks)

    class Config:
        arbitrary_types_allowed = True


class Message(Event):
    role: str
    content: str
    category: Optional[str] = None
    embedding: Optional[List[float]] = []
    classification: Optional[MessageClassification] = None

    def __init__(self, **data):
        content_data = data.pop("content", None)
        if isinstance(content_data, list):
            message_content = MessageContent(response=content_data)
            data["content"] = message_content.content
        else:
            data["content"] = content_data
        super().__init__(**data)

    @property
    def metadata(self):
        return self.__metadata__()

    def __metadata__(self):
        return {"role": self.role, "content": self.content}


class UserMessage(Message):
    role: str = "user"


class AssistantMessage(Message):
    role: str = "assistant"


class SystemMessage(Message):
    role: str = "system"


class Arguments(BaseModel):
    name: str
    arguments: Dict[str, Any]


class FunctionArguments(Arguments):
    name: str
    arguments: Dict[str, Any]


class Data(BaseModel):
    pass


class File(Data):
    data: bytes


class Link(Data):
    data: str


class Image(Data):
    data: bytes


class Embedding(Data):
    data: List[float]


class Function(Data):
    id: str
    name: str
    description: str = None
    parameters: Dict[str, Any] = {}
    categories: List[str] = []
    keywords: List[str] = []
    type: str = "function"
    import_path: str = "scint.core.lib.functions"

    @property
    def metadata(self):
        return self.__metadata__()

    @property
    def choice(self):
        return self.__metadata__(choice=True)

    def __metadata__(self, choice=False):
        if choice:
            return {"type": self.type, self.type: {"name": self.name}}

        return {
            "type": self.type,
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class ProviderParams(Data):
    provider: str = "openai"
    format: str = "completion"
    preset: str = "balanced"


class Structure(BaseModel):
    name: str

    @property
    def metadata(self):
        return self.__metadata__()

    def __metadata__(self):
        return {"name": self.name}


class Completion(Data, Event):
    id: str | int
    name: str
    prompts: List[SystemMessage] = []
    messages: List[Message] = []
    functions: List[Function] = []
    classification: ProviderParams = ProviderParams(
        provider="openai",
        format="completion",
        preset="balanced",
    )

    def as_embedding(self):
        string = ""
        for message in self.messages:
            string += message.content

        return Embedding(
            id=self.id,
            string=string,
            classification=ProviderParams(
                provider="openai",
                format="embedding",
                preset="embedding",
            ),
        )


class Embedding(Data, Event):
    id: str | int
    string: str
    classification: ProviderParams = ProviderParams(
        provider="openai", format="embedding", preset="embedding"
    )


class Settings:
    pass


class Person(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    accounts: Optional[Dict[str, Any]] = {}
    locations: Optional[List[Dict[str, Any]]] = []
    description: Optional[str] = None
    interests: Optional[List[str]] = []
    annotations: Optional[List[str]] = []

    @property
    def metadata(self):
        return self.__metadata__()

    def __metadata__(self):
        return f"""
        Name: {self.name}
        Email: {self.email}
        Accounts: {self.accounts}
        Locations: {self.locations}
        Description: {self.description}
        Interests: {self.interests}
        Annotations: {self.annotations}
        """
