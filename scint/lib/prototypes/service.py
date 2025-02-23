from __future__ import annotations

from enum import Enum
from typing import Any, Dict, TypeVar

from scint.lib.prototypes.notifier import Observable, Observe
from scint.lib.schemas.models import Model
from scint.lib.types.enum import Factory
from scint.lib.types.struct import Struct
from scint.lib.types.traits import Trait, Traits


T = TypeVar("T")


class ServiceState(Enum): ...


class Settings(Model): ...


class ServiceRequest(Model): ...


class ServiceResponse(Model): ...


class ServiceError(Exception): ...


class Serviceable(Trait):
    def configure(self, settings: Settings):
        self.settings = settings
        return self

    def start(self, req: ServiceRequest):
        self.status = ServiceState.STARTING
        return self.on_request(req)

    def on_request(self, req: ServiceRequest): ...

    def on_response(self, req: ServiceRequest): ...

    def validate(self, req: ServiceRequest): ...

    def handle_error(self, error: ServiceError): ...


class Providable(Trait):
    def configure(self, settings: Settings):
        self.settings = settings
        return self


class Service(Struct):
    traits = Traits(Serviceable, Observe, Observable)
    type: str
    interface: Any
    manager: Any = None
    settings: Settings
    status: ServiceState


class Provider(Struct):
    traits = Traits(Providable)
    type: str
    name: str
    version: str
    settings: Settings


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


class Services(Factory):
    Service = ("Service", (Service,), {})
