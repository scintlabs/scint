from __future__ import annotations

import functools
import asyncio
from asyncio.queues import PriorityQueue
from enum import Enum

from typing import Any, Callable, TypeVar

from scint.lib.entities import Entity
from scint.lib.common.tools import Task
from scint.lib.common.traits import Trait

_T = TypeVar("_T")


class ProcessorState(Enum):
    Started = ("Started", True)
    Running = ("Running", True)
    Stopped = ("Stopped", True)

    def __init__(self, state=None, _=False):
        self.state = state


class Processor(Entity):
    tasks: PriorityQueue = PriorityQueue(maxsize=6)


class Processing(Trait):
    def spawn(self, context):
        proc = Task(context.params)
        asyncio.create_task(self.init(proc, context))

    async def init(self, proc: Task, context):
        res = await self.process(context)
        context.update(res)
        self.processes[context.id] = proc
        return await self.execute(context)

    async def execute(self, context):
        for id, proc in self.processor.items():
            async for res in proc.execute(context):
                context.messages.append(res)
                yield res


class Chain(Trait):
    def __init__(self, context):
        for task in self.params.param:
            self.schema.threads.append(task)

    async def run(self, context):
        for task in self.schema.threads:
            res = await task.run(context)
            context.messages.append(res)
        return context


class Conditional(Trait):
    def __init__(self, context):
        self.condition = context.params.condition
        self.add_child(b for b in context.params.condition)

    async def run(self, context):
        for child in self.children:
            if self.condition(context):
                return await child.execute(context)


class Transform(Trait):
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


class Reduce(Trait):
    def __init__(self, process: Task, func: Callable, initial: Any = None):
        self.process = self.add_child(process)
        self.reduce_func = func
        self.initial = initial

    async def run(self, context):
        result = await self.entities.execute(context)
        return functools.reduce(self.reduce_func, result, self.initial)
