import asyncio
from functools import wraps


def logger(method):
    if asyncio.iscoroutinefunction(method):

        @wraps(method)
        async def wrapper(self, *args, **kwargs):
            name = method.__qualname__.split(".")[0]
            print(f"{name} called method {method.__name__}.")
            return await method(self, *args, **kwargs)

        return wrapper

    else:

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            name = method.__qualname__.split(".")[0]
            print(f"{name} called method {method.__name__}.")
            return method(self, *args, **kwargs)

        return wrapper
