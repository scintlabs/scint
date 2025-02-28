from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional, TypeVar

from src.types.base import Model
from src.types.traits import Trait


T = TypeVar("T")


class ProviderType(Enum):
    pass


class Provider(Model):
    name: str
    client: Any = None
    settings: Optional[Dict[str, Any]] = None

    def client(self):
        return self.client(**self.settings)


class ResourceStatus(Enum): ...


class Settings(Model): ...


class Serviceable(Trait):
    def configure(self, settings: Settings): ...
    def start(self, req): ...
    def get_res(self, obj): ...
    def set_res(self, obj): ...
    def validate(self, req): ...
    def handle_error(self, error): ...
