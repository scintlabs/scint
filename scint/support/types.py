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


# Data
