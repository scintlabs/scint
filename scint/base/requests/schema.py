from typing import Callable, Optional, Dict, List, Any, Union

from pydantic import BaseModel
from ..components.prompts.prompts import Message, Prompt


class Model(BaseModel):
    pass


class Function(Model):
    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable = None

    def build(self, function):
        return {
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": self.name,
                        "description": self.description,
                        "parameters": self.parameters,
                    },
                }
            ],
            "tool_choice": {
                "type": "function",
                "function": {"name": self.name},
            },
        }


class LanguageModelParameters(Model):
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


class LanguageModel(Model):
    name: str
    type: str
    method: Any
    parameters: LanguageModelParameters


class LanguageModelProvider(Model):
    name: str
    models: List[LanguageModel]


class RequestParameters(Model):
    provider: str = "openai"
    format: str = "completion"
    preset: str = "balanced"


class Request(Model):
    parameters: RequestParameters = RequestParameters()
    messages: List[Union[Message, Prompt]] = []
    functions: List[Function] = []
