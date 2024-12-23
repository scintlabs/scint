from typing import Any

from pydantic import BaseModel, ConfigDict


class AppModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Modules(AppModel):
    base: Any
    behaviors: Any
    processes: Any
    structures: Any


class Services(AppModel):
    cache: Any
    context: Any
    storage: Any


class App(AppModel):
    modules: Modules
    services: Services
