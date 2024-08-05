import inspect
from typing import Any, Callable, List, Optional, TypeVar, Generic
from collections import deque

from .function import Function
from .results import FunctionResult


class Generator:
    def __init__(self):
        self.function_stack = deque()
        self.results = []

    async def map(self, functions: List[Function], initial_data: Any = None):
        for func in reversed(functions):
            await self.function_stack.put(func)

        current_data = initial_data

        while not self.function_stack.empty():
            func = await self.function_stack.get()
            result = await self.process(func, current_data)

            if inspect.isasyncgen(result):
                async for item in result:
                    yield item
                    current_data = item
            else:
                yield result
                current_data = result

    async def process(self, function: Function, data: Any = None):
        request = function.build()
        arguments = await function.invoke(request)

        if data is not None:
            arguments["previous_result"] = data

        method = getattr(function, function.name)
        result = await method(**arguments)

        if hasattr(result, "__aiter__"):
            return self.generator(result)
        return result

    async def generator(self, gen):
        async for item in gen:
            yield item
