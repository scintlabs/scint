from __future__ import annotations

import ast
import json
import functools
import hashlib
import inspect
from importlib import import_module
from typing import Callable, Dict

from attrs import define, field

from src.runtime.actor import Actor
from src.core.serialize import serialize
from src.services.indexes import Indexes


@define
class ToolCatalog(Actor):
    _tools: Dict[str, Callable] = field(factory=dict)
    _indexes: Indexes = Indexes()

    async def load(self):
        if self._loaded:
            return
        async with self._lock:
            await self._load_modules()
            self._loaded = True

    async def _load_modules(self):
        module = import_module("src.lib.tools")

        for _, attr in inspect.getmembers(module):
            if inspect.isfunction(attr) and attr.__module__ == module.__name__:
                fp = generate_tool_signature(attr)
                wrapper = tool(attr)
                self._tools.setdefault("functions", {})[fp] = wrapper.schema
                await self._register_wrappers(wrapper)
        await self._sync_index()

    async def _register_wrappers(self, wrapper: Callable):
        self.registry[wrapper.schema["name"]] = wrapper
        record = {
            "id": hashlib.sha1(wrapper.schema["name"].encode()).hexdigest(),
            **wrapper.schema,
        }
        await self.index.add_records([record])


def generate_tool_signature(obj):
    node = ast.parse(inspect.getsource(obj)).body[0]
    node.body = []
    digest = hashlib.sha1(ast.unparse(node).encode()).hexdigest()
    return digest


def build_tool(func):
    sig = generate_tool_signature(func)
    return {"sig": sig, "schema": serialize(func)}


def tool(func):
    schema = build_tool(func)

    async def _exec(agent, tool_call):
        if tool_call.name != func.__name__:
            return
        args = json.loads(tool_call.arguments)
        res = await func(**args) if inspect.iscoroutinefunction(func) else func(**args)
        res.id = tool_call.id
        agent.input.extend([tool_call, res])
        async for resp in agent.evaluate():
            yield resp

    @functools.wraps(func)
    def dispatcher(*args, **kwargs):
        if not args and not kwargs:
            return schema
        if len(args) == 2 and hasattr(args[1], "arguments"):
            return _exec(*args)
        return func(*args, **kwargs)

    dispatcher.schema = schema
    dispatcher.exec = _exec
    return dispatcher
