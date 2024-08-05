import inspect
from typing import Any, Callable, List, Optional, TypeVar, Generic
from collections import deque

from .function import FunctionResult
from .function import Function


class Chain:
    def __init__(self, initial_value: Any = None):
        self.value = initial_value

    def bind(self, function: Function):
        async def bound(*args, **kwargs):
            if self.value is not None:
                kwargs["previous_result"] = self.value
            result = await function.execute(*args, **kwargs)
            if result is not None:
                self.value = result.value
            return self

        return bound

    @property
    def result(self):
        return self.value
