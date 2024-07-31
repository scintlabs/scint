from typing import Optional, Dict, List, Any

from scint.base.models import Model
from scint.base.models.messages import Message, Prompt
from scint.base.models.functions import Function


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
    prompts: List[Prompt] = []
    messages: List[Message] = []
    functions: List[Function] = []
