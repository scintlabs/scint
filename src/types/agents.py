from __future__ import annotations

import random
from types import FunctionType
from typing import Any, List, Dict, Optional, Type

from src.types.factory import BaseFactory
from src.types.models import AgentMessage, Context, Model, Signal
from src.types.typing import _finalize_type
from src.schemas.agents import default_agent


class Param(Model):
    type: str
    name: str
    description: str
    items: Optional[List[Any]] = None

    @property
    def model(self):
        prop = {"type": self.type, "description": self.description}
        if self.type == "enum":
            prop["enum"] = self.items
        elif self.type == "array":
            prop["array"] = self.items
        return prop

    @property
    def schema(self):
        return self.model


class Params(Model):
    parameters: List[Param]

    @property
    def model(self):
        return {
            "type": "object",
            "properties": {p.name: p.model for p in self.parameters},
            "additionalProperties": False,
            "required": [p.name for p in self.parameters],
        }

    @property
    def schema(self):
        return self.model


class AgentSchema(Model):
    prompts: List[Prompt] = []
    output: Output
    functions: List[Function] = []
    routine: Routine

    @property
    def schema(self):
        return {
            "prompts": [p.model for p in self.prompts],
            "output": self.output.model,
            "functions": [f.model for f in self.functions],
            "routine": self.routine.model,
        }


class AgentFactory(BaseFactory):
    Agent = ("Agent", True)
    Routine = ("Routine", True)
    Function = ("Function", True)
    Prompt = ("Prompt", True)
    Output = ("Output", True)


class AgentType(type):
    def __new__(cls, name, bases, dct):
        def __init__(self, schema: AgentSchema = None, context: Context = None):
            self.context = context
            self.__post_init__(schema)

        def __post_init__(self, schema: AgentSchema = None):
            schema = default_agent if schema is None else schema
            AgentFactory.Agent.init(self, schema)

        dct["__init__"] = __init__
        dct["__post_init__"] = __post_init__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class ComponentType(type):
    def __new__(cls, name, bases, dct):
        def __init__(self, obj: Any = None, *args, **kwargs):
            self.__post_init__(obj, *args, **kwargs)

        def __post_init__(self, obj: Any, *args, **kwargs):
            if isinstance(obj, str):
                AgentFactory.Prompt.init(self, obj)
            elif isinstance(obj, (Dict, Model)):
                AgentFactory.Output.init(self, obj)
            elif hasattr(self, "parameters"):
                AgentFactory.Function.init(self, obj)
            elif hasattr(self, "config"):
                AgentFactory.Routine.init(self, obj)

        dct["__init__"] = __init__
        dct["__post_init__"] = __post_init__
        dct = _finalize_type(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Agent(metaclass=AgentType):
    context: Context
    prompts: List[Prompt]
    output: Output
    functions: List[Function]
    routine: Routine

    async def evaluate(self):
        res = await self.routine.start(self)
        self.context.update(res)
        return res

    @property
    def schema(self):
        return {
            "prompts": [p.model for p in self.prompts],
            "output": self.output.model,
            "functions": [f.model for f in self.functions],
            "routine": self.routine.model,
        }


class Routine(metaclass=ComponentType):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Dict[str, Any] = None
    function: FunctionType = None

    def configure(self, context):
        self.config = {
            "model": "gpt-4o",
            "top_p": round(random.uniform(0.5, 1), 2),
            "temperature": round(random.uniform(0.9, 1.4), 2),
            **context.model,
        }
        return self

    def output(self, output: Any):
        self.config["response_format"] = output.model
        return self

    def functions(self, functions: Any):
        self.config["tools"] = functions
        return self

    def request(self, agent: Type):
        self.configure(agent.context).output(agent.output).functions(
            [f.model for f in agent.functions]
        )
        return self.config

    async def start(self, agent: Type):
        req = self.request(agent)
        return await self.function(agent, **req)

    @property
    def model(self):
        return {
            "name": self.name,
            "description": self.description,
            "config": self.config,
            "function": self.function.__name__,
        }

    @property
    def schema(self):
        return self.model


class Function(metaclass=ComponentType):
    name: str = None
    description: str = None
    parameters: Params = None
    function: FunctionType = None

    @property
    def model(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {**self.parameters.model},
                "strict": True,
            },
        }

    @property
    def schema(self):
        return self.model


class Prompt(metaclass=ComponentType):
    name: str = None
    description: str = None
    content: str = None

    @property
    def model(self):
        return {"role": "system", "content": self.content}

    @property
    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "content": self.content,
        }


class Output(metaclass=ComponentType):
    name: str = None
    description: str = None
    format: Dict[str, str] | Signal = AgentMessage

    @property
    def model(self):
        if hasattr(self.format, "model"):
            return self.format
        else:
            return {"type": "json_schema", "json_schema": self.format}

    @property
    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "format": self.format,
        }
