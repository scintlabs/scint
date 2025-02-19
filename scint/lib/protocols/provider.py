from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Generic, TypeVar, Optional

from scint.lib.observability import Observable, Observant
from scint.lib.protocols import Model
from scint.lib.types import Struct
from scint.lib.types import Trait, Traits
from scint.lib.types.typing import _create_provider

T = TypeVar("T")


class ProviderSettings(Struct):
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: int = 30
    retry_attempts: int = 3


class ProviderRequest(Model):
    operation: str
    params: Dict[str, Any]


class ProviderResponse(Model, Generic[T]):
    data: T
    metadata: Dict[str, Any]
    status: str


class ProviderError(Exception):
    def __init__(self, message: str, provider: str, details: Any = None):
        self.provider = provider
        self.details = details
        super().__init__(f"{provider}: {message}")


class ProviderStatus(Enum):
    INITIALIZED = "initialized"
    CONFIGURED = "configured"
    READY = "ready"
    ERROR = "error"
    DISCONNECTED = "disconnected"


class ProviderType(type):
    def __new__(cls, name, bases, dct, **kwargs):
        dct = _create_provider(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Providable(Trait):
    def configure(self, settings: ProviderSettings):
        self.settings = settings
        self.status = ProviderStatus.CONFIGURED
        return self

    def connect(self) -> bool:
        """Establish connection/authentication with the provider"""
        raise NotImplementedError

    def disconnect(self) -> bool:
        """Clean up provider resources"""
        raise NotImplementedError

    def validate_request(self, req: ProviderRequest) -> bool:
        """Validate provider-specific request"""
        raise NotImplementedError

    def handle_error(self, error: ProviderError):
        self.status = ProviderStatus.ERROR
        raise error


class Provider(metaclass=ProviderType):
    type: str
    name: str
    version: str
    settings: ProviderSettings
    implements: Traits = Traits(Providable, Observant, Observable)
    status: ProviderStatus = ProviderStatus.INITIALIZED

    def __init__(self, settings: ProviderSettings = None):
        if settings:
            self.configure(settings)


class ProviderRegistry:
    _providers: Dict[str, Provider] = {}

    @classmethod
    def register(cls, provider: Provider):
        cls._providers[provider.name] = provider
        return provider

    @classmethod
    def get(cls, name: str) -> Provider:
        return cls._providers.get(name)

    @classmethod
    def list(cls) -> Dict[str, Provider]:
        return cls._providers


class LLMProvider(Provider):
    def generate(self, prompt: str, **kwargs) -> ProviderResponse[str]:
        raise NotImplementedError


class CacheProvider(Provider):
    def get(self, key: str) -> ProviderResponse[Any]:
        raise NotImplementedError

    def set(self, key: str, value: Any) -> ProviderResponse[bool]:
        raise NotImplementedError


class StorageProvider(Provider):
    def save(self, key: str, data: Any) -> ProviderResponse[bool]:
        raise NotImplementedError

    def load(self, key: str) -> ProviderResponse[Any]:
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    name = "openai"
    version = "1.0.0"

    def connect(self) -> bool:
        if not self.settings.api_key:
            raise ProviderError("API key not configured", self.name)
        return True

    def generate(self, prompt: str, **kwargs) -> ProviderResponse[str]:
        if not self.validate_request(
            ProviderRequest(operation="generate", params={"prompt": prompt, **kwargs})
        ):
            raise ProviderError("Invalid request", self.name)
        return ProviderResponse(
            data="Generated text",
            metadata={"model": "gpt-4", "tokens": 150},
            status="success",
        )


class RedisCacheProvider(CacheProvider):
    name = "redis"
    version = "1.0.0"
