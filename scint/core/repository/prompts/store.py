import asyncio
from functools import wraps

from scint.core import context


class StoreType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        store = context(cls)
        with context(store):
            return store.store

    def __new__(cls, name, bases, dct, **kwargs):
        def _logger(func):
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                print(f"Calling method: {func.__name__}")
                return func(*args, **kwargs)

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                print(f"Calling async method: {func.__name__}")
                return await func(*args, **kwargs)

            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper

        for attr_name, attr_value in dct.items():
            if callable(attr_value):
                dct[attr_name] = _logger(attr_value)
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, *args, **kwargs):
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance


class Store(metaclass=StoreType):
    def __init__(self):
        pass
