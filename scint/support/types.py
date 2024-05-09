import typing
from uuid import uuid4
from datetime import datetime
import websockets
from pydantic import BaseModel, Field

from scint.system.logging import log

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
    temperature: Optional[float] = None
    stream: Optional[bool] = None
    max_tokens: Optional[int] = None
    messages: Optional[List[Dict[str, Any]]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Dict[str, Any]] = None
    top_p: Optional[float] = None
    prompt: Optional[str] = None
    quality: Optional[str] = None
    size: Optional[str] = None
    response_format: Optional[str] = None
    input: Optional[str] = None
    n: Optional[int] = None


class Classification(BaseModel):
    name: str = "balanced"
    format: str = "completion"
    provider: str = "openai"


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

    def get_metadata(self):
        return {"role": self.role, "content": str(self.content)}


class UserMessage(Message):
    role: str = "user"


class AssistantMessage(Message):
    role: str = "assistant"


class SystemMessage(Message):
    role: str = "system"


class Arguments(BaseModel):
    name: str
    content: Dict[str, Any]


class ScopeArgs(Arguments):
    name: str
    content: Dict[str, Any]


class FunctionArgs(Arguments):
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
    data: Any


class File(Data):
    data: bytes


class Link(Data):
    data: str


class Image(Data):
    data: bytes


class Component(Data):
    pass


# Metadata
class Metadata(BaseModel):
    pass


class FunctionProps(Metadata):
    name: str
    type: str
    description: str


class FunctionParams(Metadata):
    type: str
    properties: Dict[str, Any] | FunctionProps
    required: List[str]


class Function(Metadata):
    name: str
    type: str = "function"
    description: str = None
    parameters: FunctionParams


class Scope(Metadata):
    name: str
    description: str


class Module(Metadata):
    name: str
    description: str


class Classification(Metadata):
    name: str = "balanced"
    format: str = "completion"
    provider: str = "openai"


class Context(Metadata, Event):
    description: str
    instructions: List[Message]
    functions: List[Any] = []
    function_choice: str | Dict[str, Any] = "auto"
    messages: List[Message] = []
    preset: str = "balanced"
    classification: Classification = Classification()


class AppContext(Context):
    function_choice: Dict[str, Any]
    modules: List[Module] = []


class ModuleContext(Context):
    scopes: List[Scope] = []


class ScopeContext(Context):
    pass


class Embedding(Metadata, Data):
    data: List[float]
