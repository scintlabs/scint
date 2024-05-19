import typing
from uuid import uuid4
from datetime import datetime
import websockets
from pydantic import BaseModel, Field

from scint.support.logging import log

WebSocket = websockets.WebSocketCommonProtocol
WebSocketDisconnect = websockets.exceptions.ConnectionClosed
Any = typing.Any
List = typing.List
Dict = typing.Dict
Optional = typing.Optional
Callable = typing.Callable
AsyncGenerator = typing.AsyncGenerator
Union = typing.Union


class Provider(BaseModel):
    text: Dict[str, Any]
    image: Dict[str, Any]
    embedding: Dict[str, Any]


class ModelParameters(BaseModel):
    model: Optional[str] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    stream: Optional[bool] = None
    max_tokens: Optional[int] = None
    messages: Optional[List[Dict[str, Any]]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Dict[str, Any]] = None
    prompt: Optional[str] = None
    quality: Optional[str] = None
    size: Optional[str] = None
    response_format: Optional[str] = None
    input: Optional[str] = None
    n: Optional[int] = None


class Model(BaseModel):
    name: str
    type: str
    method: Any
    parameters: ModelParameters


class ModelProvider(BaseModel):
    name: str
    module: Any
    models: List[Model]


class Header(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created: str = Field(default_factory=lambda: datetime.now().isoformat())


class Event(BaseModel):
    header: Header = Header()


class Message(Event):
    role: str
    content: str
    abstract: str = None
    annotations: str = None
    recipient: str = "default"

    @property
    def metadata(self):
        return self.__metadata__()

    def __metadata__(self):
        return {"role": self.role, "content": str(self.content)}


class UserMessage(Message):
    role: str = "user"


class AssistantMessage(Message):
    role: str = "assistant"


class SystemMessage(Message):
    role: str = "system"


class Task(BaseModel):
    name: str


class Arguments(BaseModel):
    name: str
    content: Dict[str, Any]


class FunctionArguments(Arguments):
    name: str
    content: Dict[str, Any]


# Data
class User(BaseModel):
    username: str
    full_name: str
    email: str
    timezone: str
    language: str
    schedule: Dict[str, Any]
    links: Dict[str, Any]
    files: Dict[str, Any]


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


class FunctionProps(Data):
    name: str
    type: str
    description: str
    enum: Optional[List[str]] = None


class FunctionParams(Data):
    type: str = "object"
    properties: FunctionProps
    required: List[str]


class Function(Data):
    name: str
    type: str = "function"
    description: str = None
    parameters: Dict[str, Any]

    @property
    def metadata(self):
        return self.__metadata__()

    def __metadata__(self):
        return {
            "type": self.type,
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class Classification(Data):
    provider: str = "openai"
    format: str = "completion"
    preset: str = "balanced"


class Messages(BaseModel):
    data: List[Message]

    @property
    def metadata(self):
        return self.__metadata__()

    def __metadata__(self):
        return {"messages": [message.metadata for message in self.messages]}


class ContextData(Data, Event):
    id: str
    name: str
    root: Optional[str] = None
    branches: Optional[List[str]] = None
    prompts: List[Message] = []
    messages: List[Message] = []
    functions: List[Function] = []
    function_choice: str | Dict[str, Any] = "auto"
    classification: Classification = Classification()
