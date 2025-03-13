from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.types.models import Model


class Provider(Model):
    name: str
    module: Any = None
    parameters: Optional[Dict[str, Any]] = None

    def client(self):
        return self.module(**self.parameters)


class Providers(Model):
    providers: List[Provider]


class Resource: ...
