from __future__ import annotations

from types import SimpleNamespace
from functools import partial
from typing import TypeAlias

from src.compose.library import Library
from src.execute.executor import Executor
from src.execute.catalog import Catalog
from src.compose.composer import Composer
from src.interpret.continuity import Continuity
from src.interpret.interpreter import Interpreter
from src.base.broker import Broker
from src.svc.datastore import DataStore
from src.svc.config import MEILI_CLIENT
from src.svc.indexes import Indexes

ns = partial(SimpleNamespace, _mutable=False)

Container: TypeAlias = SimpleNamespace


async def build_interpreter(services: Container):
    continuity = Continuity(indexes=services.indexes)
    interpreter = Interpreter(continuity=continuity)
    services.broker.register(interpreter)
    return interpreter


async def build_executor(services: Container):
    catalog = Catalog(indexes=services.indexes)
    executor = Executor(catalog=catalog)
    services.broker.register(executor)
    return executor


async def build_composer(services: Container):
    library = Library(indexes=services.indexes)
    composer = Composer(library=library)
    services.broker.register(composer)
    return composer


async def build_container():
    broker = Broker()
    datastore = DataStore()
    indexes = Indexes(MEILI_CLIENT)
    services = ns(broker=broker, indexes=indexes, datastore=datastore)
    interpreter = await build_interpreter(services)
    executor = await build_executor(services)
    composer = await build_composer(services)
    return ns(
        broker=broker,
        interpreter=interpreter,
        composer=composer,
        executor=executor,
        services=services,
    )
