from scint.support.types import Optional, Any, Dict, List, BaseModel


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


class Provider(BaseModel):
    text: Dict[str, Any]
    image: Dict[str, Any]
    embedding: Dict[str, Any]


class ModelProvider(BaseModel):
    name: str
    models: List[Model]


class RequestParameters(BaseModel):
    provider: str = "openai"
    format: str = "completion"
    preset: str = "balanced"


class Request(BaseModel):
    id: str
    prompts: List[Any]
    messages: List[Any]
    functions: List[Any]
    parameters: RequestParameters = RequestParameters()
