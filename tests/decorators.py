import asyncio
from functools import wraps


def contextmethod(func):
    def outer_wrapper(self, *args, **kwargs):
        name = func.__qualname__.split(".")[0]

        @wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        @wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            return await func(self, *args, **kwargs)

        with self.context() as ctx:
            if asyncio.iscoroutinefunction(func):
                setattr(ctx, name, async_wrapper)
            else:
                return setattr(ctx, name, sync_wrapper)

    return outer_wrapper


def opencontextmethod(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        name = func.__qualname__.split(".")[0]
        if asyncio.iscoroutinefunction(func):

            async def exposed_method(*args, **kwargs):
                return await func(self, *args, **kwargs)

        else:

            def exposed_method(*args, **kwargs):
                return func(self, *args, **kwargs)

        with self.context() as ctx:
            setattr(ctx, name, exposed_method)

        return func(self, *args, **kwargs)

    return wrapper
