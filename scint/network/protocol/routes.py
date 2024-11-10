from dataclasses import dataclass
from typing import Callable

from scint.repository.models import Model


@dataclass
class Route(Model):
    path: str
    handler: Callable
    constraints: dict = None
