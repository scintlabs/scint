from typing import Any, Callable, Dict, List, Union

from scint.base.models.messages import Model, Message, Prompt


class FunctionCall(Model):
    name: str
    type: str
    arguments: Dict[str, object]


class FunctionArguments(Model):
    name: str
    arguments: Dict[str, object]


class Function(Model):
    name: str
    description: str
    parameters: Dict[str, Any]
    callable: Callable
    labels: str

    def dump(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def select(self):
        return {"type": "function", "function": {"name": self.name}}


class Functions(Model):
    functions: List[Function] = []

    def dump(self):
        return [function.dump() for function in self.functions]


class Chain(Model):
    instructions: List[Union[Prompt, Message]]
    functions: List[Function]


class Generator(Model):
    prompts: List[Prompt]
    functions: List[Function]
