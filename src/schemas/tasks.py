from __future__ import annotations

import functools
import asyncio
from enum import Enum
from typing import Any, Callable, Optional


class ProcessState(Enum):
    PARSING = ("PARSING", None)
    SEARCHING = ("SEARCHING", None)
    COMPOSING = ("COMPOSING", None)
    RETURNING = ("COMPOSING", None)

    def __init__(self, state_name: str, default_next: Optional[str]):
        self.state_name = state_name
        self.default_next = default_next
        self.on_enter = lambda obj: None
        self.on_exit = lambda obj: None

    def set_hooks(self, on_enter, on_exit) -> None:
        self.on_enter = on_enter
        self.on_exit = on_exit


class TaskContext: ...


class Functional:
    def spawn(self, context: TaskContext):
        proc = Task(context.params)
        asyncio.create_task(self.init(proc, context))

    async def execute(self, context):
        for id, proc in self.processor.items():
            async for res in proc.execute(context):
                context.messages.append(res)
                yield res


class Task:
    def init(self, context: TaskContext):
        pass

    async def run(self, context):
        res = await self.process(context)
        context.messages.append(res)
        for task in self.tasks:
            async for res in task.run(context):
                yield res


class Chain:
    def __init__(self, context):
        for task in self.params.param:
            self.schemas.threads.append(task)

    async def run(self, context):
        for task in self.schemas.threads:
            res = await task.run(context)
            context.messages.append(res)
        return context


class Conditional:
    def init(self, context):
        self.condition = context.params.condition
        self.add_child(b for b in context.params.condition)

    async def run(self, context):
        for child in self.children:
            if self.condition(context):
                return await child.execute(context)


class Transform:
    def __init__(self, name: str, process: Task, input_key: str):
        self.process = self.add_child(process)
        self.input_key = input_key

    async def run(self, context):
        inputs = context.inputs[self.input_key]
        tasks = []

        for n in inputs:
            ctx = dict(
                inputs={self.input_key: n},
                data=dict(context.data),
                config=dict(context.config),
            )
            tasks.append(self.entities.execute(ctx))

        return await asyncio.gather(*tasks)


class Reduce:
    def __init__(self, process: Task, func: Callable, initial: Any = None):
        self.process = self.add_child(process)
        self.reduce_func = func
        self.initial = initial

    async def run(self, context):
        result = await self.entities.execute(context)
        return functools.reduce(self.reduce_func, result, self.initial)
