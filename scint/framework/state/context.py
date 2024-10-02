import asyncio
from pprint import pp
from collections import ChainMap
from functools import wraps
from types import FunctionType, MethodType


class Context(ChainMap):
    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)

    def app_map(self):

        def _map(obj):
            if isinstance(obj, Context):
                return {k: _map(v) for k, v in obj.items() if not k.startswith("_")}
            elif isinstance(obj, dict) or issubclass(type(obj), dict):
                return {k: _map(v) for k, v in obj.items() if not k.startswith("_")}
            elif isinstance(obj, (list, tuple)):
                return [_map(item) for item in obj]
            elif isinstance(obj, MethodType) or isinstance(obj, FunctionType):
                return {
                    "name": obj.__qualname__,
                    "type": type(obj).__name__,
                    "module": obj.__module__,
                }
            elif hasattr(obj, "state"):
                return {
                    k: _map(v) for k, v in obj.state.items() if not k.startswith("_")
                }
            elif isinstance(obj, Context):
                return {k: _map(v) for k, v in obj.items() if not k.startswith("_")}
            elif isinstance(obj, (list, tuple)):
                return [_map(item) for item in obj]
            elif hasattr(obj, "__qualname__"):
                if getattr(obj, "is_public", False):
                    return {"name": obj.__qualname__, "type": "public_method"}
                return {"name": obj.__qualname__}
            elif isinstance(obj, MethodType):
                if getattr(obj, "is_public", False):
                    return {"name": obj.__func__.__name__, "type": "public_method"}
                return {"name": obj.__func__.__name__, "type": "method"}
            else:
                return obj

        return _map(self)

    def print(self):
        return pp(self.app_map())


def publicmethod(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        with self.state as context:
            context[func.__name__] = func
            if asyncio.iscoroutinefunction(func):
                result = asyncio.gather(
                    asyncio.create_task(func(self, *args, **kwargs))
                )
                return result
            result = func(self, *args, **kwargs)
            return result

    return wrapper
