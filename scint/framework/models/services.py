from enum import Enum

from scint.framework.types.model import Model


class Provider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class RequestType(str, Enum):
    COMPLETION = "completion"
    EMBEDDING = "embedding"


class RequestParameters(Model):
    provider: Provider = Provider.OPENAI
    format: RequestType = RequestType.COMPLETION
    preset: str = "balanced"
