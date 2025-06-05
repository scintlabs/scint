from __future__ import annotations

from functools import partial
from types import SimpleNamespace
from typing import TypeAlias

Container: TypeAlias = SimpleNamespace
ns = partial(SimpleNamespace, _mutable=False)


async def bootstrap():
    pass
