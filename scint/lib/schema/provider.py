from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Generic, TypeVar, Optional

from scint.lib.observability import Observable, Observant
from scint.lib.schema import Model
from scint.lib.common.struct import Struct
from scint.lib.common.traits import Trait, Traits
from scint.lib.common.typing import _create_provider

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
    """Core trait for provider capabilities"""

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
        """Handle provider-specific errors"""
        self.status = ProviderStatus.ERROR
        raise error


class Provider(metaclass=ProviderType):
    """Base provider class"""

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
    """Registry for managing multiple providers"""

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


# Example provider implementations
class LLMProvider(Provider):
    """Base class for LLM providers"""

    def generate(self, prompt: str, **kwargs) -> ProviderResponse[str]:
        raise NotImplementedError


class CacheProvider(Provider):
    """Base class for cache providers"""

    def get(self, key: str) -> ProviderResponse[Any]:
        raise NotImplementedError

    def set(self, key: str, value: Any) -> ProviderResponse[bool]:
        raise NotImplementedError


class StorageProvider(Provider):
    """Base class for storage providers"""

    def save(self, key: str, data: Any) -> ProviderResponse[bool]:
        raise NotImplementedError

    def load(self, key: str) -> ProviderResponse[Any]:
        raise NotImplementedError


# Example concrete provider
class OpenAIProvider(LLMProvider):
    name = "openai"
    version = "1.0.0"

    def connect(self) -> bool:
        # Initialize OpenAI client
        if not self.settings.api_key:
            raise ProviderError("API key not configured", self.name)
        # ... implementation
        return True

    def generate(self, prompt: str, **kwargs) -> ProviderResponse[str]:
        if not self.validate_request(
            ProviderRequest(operation="generate", params={"prompt": prompt, **kwargs})
        ):
            raise ProviderError("Invalid request", self.name)
        # ... implementation
        return ProviderResponse(
            data="Generated text",
            metadata={"model": "gpt-4", "tokens": 150},
            status="success",
        )


# Example usage
class RedisCacheProvider(CacheProvider):
    name = "redis"
    version = "1.0.0"


# Registry usage
provider_registry = ProviderRegistry()
openai_provider = OpenAIProvider(ProviderSettings(api_key="your-api-key"))
provider_registry.register(openai_provider)
openai_settings = ProviderSettings(
    api_key="your-api-key", base_url="https://api.openai.com/v1"
)
llm_provider = OpenAIProvider(openai_settings)
llm_provider.connect()

response = llm_provider.generate("Hello, world!")

# Switch providers easily
anthropic_provider = provider_registry.get("anthropic")
if anthropic_provider:
    response = anthropic_provider.generate("Hello, world!")

# Use different types of providers
cache_provider = RedisCacheProvider(ProviderSettings(base_url="redis://localhost:6379"))
cache_provider.set("key", "value")
