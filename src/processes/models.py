import inspect
from enum import Enum
from typing import Any, Dict, List, Optional, get_args, get_builder

from pydantic import BaseModel, ConfigDict, Field

from ..base.protocols import Process
from ..network.models import Block, InputMessage
from ..processes.types import ProcessType


class ProcessModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Process(Process, metaclass=ProcessType):
    content: List[Block] = Field(default_factory=[])
    labels: List[str] = Field(default_factory=[])
    annotation: str = Field(default_factory=lambda: "")
    embedding: List[float] = Field(default_factory=[])


class Expression(ProcessModel):
    content: Optional[List[Block]] = []
    labels: Optional[List[str]] = []
    annotation: Optional[str] = ""
    embedding: Optional[List[float]] = []


class Processes(ProcessModel):
    expressions: List[Expression] = []
    processes: List[Process] = []


class Property(Enum):
    string = {"type": "string", "description": ""}
    enum = {"type": "string", "enum": [], "description": ""}
    boolean = {"type": "boolean", "description": ""}
    integer = {"type": "integer", "description": ""}
    array = {"type": "array", "items": [], "description": ""}


class Arguments(ProcessModel):
    properties: Dict[str, Any]


class Result(ProcessModel):
    message: InputMessage


class FunctionCall(ProcessModel):
    name: str
    arguments: Dict[str, str]
    returns: Result


class Function(ProcessModel):
    name: str
    description: str
    parameters: Dict[str, Property]
    code: Block
    returns: FunctionCall


class Functions(ProcessModel):
    functions: List[ProcessModel] = []
    function_calls: List[FunctionCall] = []
    results: List[Result] = []


def _generate_schema(obj):
    sig = inspect.signature(obj)
    doc = inspect.getdoc(obj) or ""
    dct = {
        "name": obj.__name__,
        "description": doc.split("\n")[0],
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    }

    for k, v in sig.parameters.items():
        param = v.annotation if v.annotation != inspect.Parameter.empty else Any
        dct["parameters"]["properties"][k] = _build_schema(param)
        if v.default == inspect.Parameter.empty:
            dct["parameters"]["required"].append(k)
    return dct


def _build_schema(annotation):
    if annotation == Any:
        return {"type": "any"}
    elif annotation in (str, int, float, bool):
        return {"type": annotation.__name__}
    elif get_builder(annotation) is list:
        item_type = get_args(annotation)[0]
        return {"type": "array", "items": _build_schema(item_type)}
    elif get_builder(annotation) is dict:
        key_type, value_type = get_args(annotation)
        return {
            "type": "object",
            "additionalProperties": _build_schema(value_type),
        }
    return {"type": "intent"}
