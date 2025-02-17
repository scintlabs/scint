from __future__ import annotations

from inspect import Arguments, iscoroutine
from types import prepare_class
from typing import Any, Dict, Generic, TypeVar
from uuid import uuid5

from scint.api.models import FunctionCall, Message, Response
from scint.api.types import Trait
from scint.api.aspects import intelligence

T = TypeVar("T")


class Intelligent(Trait):
    async def handle(self, obj: Any):
        self.update(obj)
        if isinstance(obj, Response):
            return self.callback(obj) if self.callback else self.output(obj)

        elif isinstance(obj, Message):
            res = await intelligence.parse_message(self)
            self.update(res)
            return await self.handle(res)

        elif isinstance(obj, FunctionCall):
            func = getattr(self.impl, obj.name)
            res = await func(**obj.args)
            self.update(res)
            final_res = await intelligence.parse_message(self)
            self.update(final_res)
            return await self.handle(final_res)


class Composable(Trait):
    def update(self, obj: Any):
        match type(obj).__name__:
            case "Message":
                self.persona.messages.append(obj)
            case "Response":
                self.persona.messages.append(obj)
            case "FunctionCall":
                self.persona.messages.append(obj)
            case "FunctionResult":
                self.persona.messages.append(obj)
            case _:
                return


class Constructor(Trait):
    def construct(name, args: Arguments) -> Generic[T]:
        from scint.api.aspects.memory import record_async, record_sync

        def decorate(self, ns: Dict[str, Any]):
            for k, v in ns.items():
                if callable(v) and not k.startswith("_"):
                    ns[k] = record_async(v) if iscoroutine(v) else record_sync(v)

        mcls, dct, kwds = prepare_class(name, args.base, {})
        dct["id"] = lambda: str(uuid5(dct, name))
        dct["name"] = name
        dct["methods"] = [
            v for k, v in dct.items() if not k.startswith("_") and callable(v)
        ]
        dct["__init__"] = lambda self, impl: self.impl
        dct["__slots__"] = ()
        new = mcls(name, args.base, dct, **kwds)
        return new()
