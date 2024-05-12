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


class dotdict(dict):
    def __getattr__(self, attr):
        value = self[attr]
        if isinstance(value, dict) and not isinstance(value, dotdict):
            value = dotdict(value)
            self[attr] = value
        return value

    def __setattr__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, dotdict):
            value = dotdict(value)
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"{key} not found in {self}")

    def __missing__(self, key):
        return dotdict()

    @property
    def __metadata__(self):
        return {
            "name": self.name,
            "description": self.description,
            "instructions": [item.metadata for item in self.instructions],
            "messages": [message.metadata for message in self.messages],
            "functions": [func.metadata for func in self.functions],
            "function_choice": self.function_choice,
            "modules": [module.metadata for module in self.modules],
            "module_choice": self.module_choice,
            "scopes": [scope.metadata for scope in self.scopes],
            "scope_choice": self.scope_choice,
        }


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

    @property
    def metadata(self):
        return self.__build__()

    def __build__(self):
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


class FunctionArguments(Arguments):
    name: str
    content: Dict[str, Any]


class RouteArguments(Arguments):
    name: str
    content: Dict[str, Any]


class ScopeArguments(Arguments):
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
    enum: Optional[List[str]] = None


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
