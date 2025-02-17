from __future__ import annotations

from enum import Enum
from typing import Any

from scint.lib.observability import Observable, Observant
from scint.lib.schema import Model
from scint.lib.common.struct import Struct
from scint.lib.common.traits import Trait, Traits
from scint.lib.common.typing import Constructor, _create_service


class ServiceStatus(Enum): ...


class ServiceSettings(Struct): ...


class ServiceRequest(Model): ...


class ServiceResponse(Model): ...


class ServiceError(Exception): ...


class ServiceType(type):
    def __new__(cls, name, bases, dct, **kwargs):
        dct = _create_service(name, bases, dct)
        return super().__new__(cls, name, bases, dct)


class Serviceable(Trait):
    def configure(self, settings: ServiceSettings):
        self.settings = settings
        return self

    def start(self, req: ServiceRequest):
        self.status = ServiceStatus.STARTING
        return self.on_request(req)

    def on_request(self, req: ServiceRequest): ...

    def on_response(self, req: ServiceRequest): ...

    def validate(self, req: ServiceRequest): ...

    def handle_error(self, error: ServiceError): ...


class Service(metaclass=ServiceType):
    type: str
    interface: Any
    manager: Any = None
    settings: ServiceSettings
    implements: Traits = Traits(Serviceable, Observant, Observable)
    status: ServiceStatus


class Services(Constructor):
    Service = ("Service", (Service,), {})
