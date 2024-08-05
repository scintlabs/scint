from dataclasses import dataclass, field
import inspect
from typing import Any, Callable, Dict, List, Optional, TypeVar, Generic
from collections import deque

from pydantic import BaseModel

from scint.base.components.functions.results import FunctionResult


class Model(BaseModel):
    pass

    class Config:
        arbitrary_types_allowed = True


class Function:
    def __init__(self, func: Callable, condition: Optional[Callable] = None):
        self.func = func
        self.condition = condition or (lambda *args, **kwargs: True)
        self.name = func.__name__
        self.description = func.__doc__ or ""
        self.parameters = self._extract_parameters(func)

    def _extract_parameters(self, func):
        # Implementation to extract parameters from func
        pass

    def build(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def select(self):
        return {"type": "function", "function": {"name": self.name}}

    async def execute(self, *args, **kwargs) -> "FunctionResult":
        if await self.condition(*args, **kwargs):
            result = await self.func(*args, **kwargs)
            if hasattr(result, "__aiter__"):
                messages = [message async for message in result]
                return FunctionResult(messages)
            return FunctionResult(result)
        return FunctionResult(None)


class Functions(Model):
    functions: List[Function] = []

    def build(self):
        return [function.build() for function in self.functions]


@dataclass
class FunctionData:
    name: str
    description: str
    parameters: Dict[str, Any]
    callable: Callable

    def to_llm_representation(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


@dataclass
class FunctionArgsData:
    name: str
    arguments: Dict[str, Any]


# @dataclass
# class Functions:
#     functions: List[Function] = field(default_factory=list)

#     def add(self, function: Function) -> None:
#         self.functions.append(function)

#     def dump(self) -> List[Dict[str, Any]]:
#         return [function.build() for function in self.functions]

#     def select(self):
#         return {"type": "function", "function": {"name": self.name}}

#     async def execute(self, *args, **kwargs) -> "FunctionResult":
#         if await self.condition(*args, **kwargs):
#             result = await self.func(*args, **kwargs)
#             if hasattr(result, "__aiter__"):
#                 messages = [message async for message in result]
#                 return FunctionResult(messages)
#             return FunctionResult(result)
#         return FunctionResult(None)


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


class Pipeline:
    def __init__(self, *functions: Function):
        self.functions = functions

    async def execute(self, llm_service, *args, **kwargs):
        chain = Chain()
        for function in self.functions:
            llm_representation = function.build()
            llm_args = await llm_service.generate_arguments(
                llm_representation, chain.result
            )
            function_call = FunctionArgsData(name=function.name, arguments=llm_args)
            result = await function.execute(**function_call.arguments)
            chain.value = result
        return chain.result


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
