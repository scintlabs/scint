from typing import Any, Callable, List, TypeVar, Generic


T = TypeVar("T")
from typing import Dict, Any, Callable
from dataclasses import dataclass, asdict, field


class FunctionResult(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    @classmethod
    def unit(cls, value: T) -> "FunctionResult[T]":
        return cls(value)

    def bind(self, f: Callable[[T], "FunctionResult[Any]"]) -> "FunctionResult[Any]":
        return f(self.value)

    @classmethod
    def from_async(cls, coroutine):
        async def wrapper():
            result = await coroutine
            return cls(result)

        return wrapper()


class AsyncResult(FunctionResult):
    @classmethod
    async def from_coroutine(cls, coroutine):
        result = await coroutine
        return cls(result)


class ErrorResult(FunctionResult):
    def __init__(self, value, error=None):
        super().__init__(value)
        self.error = error

    def bind(self, f):
        if self.error:
            return self
        try:
            return f(self.value)
        except Exception as e:
            return ErrorResult(None, str(e))


class VoidResult(FunctionResult[None]):
    def __init__(self):
        super().__init__(None)

    @classmethod
    def unit(cls) -> "VoidResult":
        return cls()

    def bind(self, f: Callable[[None], FunctionResult[Any]]) -> FunctionResult[Any]:
        return f(None)

    @classmethod
    def from_async(cls, coroutine):
        async def wrapper():
            await coroutine
            return cls()

        return wrapper()

    def __bool__(self):
        return True

    def __repr__(self):
        return "VoidResult()"
