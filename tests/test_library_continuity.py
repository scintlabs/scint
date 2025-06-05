import asyncio
import os
import sys
import types
import pytest
import importlib.util as iu
import pathlib
import sysconfig
path = pathlib.Path(sysconfig.get_path("stdlib")) / "typing.py"
spec = iu.spec_from_file_location("typing", path)
_typing = iu.module_from_spec(spec)
spec.loader.exec_module(_typing)
sys.modules["typing"] = _typing

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

if 'src' not in sys.modules:
    pkg = types.ModuleType('src')
    pkg.__path__ = [os.path.join(ROOT, 'src')]
    sys.modules['src'] = pkg

# stub external service modules so imports succeed
services = sys.modules.get('src.services')
if services is None:
    services = types.ModuleType('src.services')
    services.__path__ = []
    sys.modules['src.services'] = services

indexes_mod = sys.modules.get('src.services.indexes')
if indexes_mod is None:
    indexes_mod = types.ModuleType('src.services.indexes')
    sys.modules['src.services.indexes'] = indexes_mod
services.indexes = indexes_mod

if 'src.services.llm' not in sys.modules:
    llm_mod = types.ModuleType('src.services.llm')
    llm_mod.completion = lambda **kwargs: None
    llm_mod.response = lambda **kwargs: None
    sys.modules['src.services.llm'] = llm_mod

class DummyIndex:
    def __init__(self):
        self.updated = []
    async def update_documents(self, docs):
        self.updated.extend(docs)
    def search(self, q):
        return type('Res', (), {'hits':[{'content':'hit'}]})

class DummyIndexes:
    def __init__(self):
        self.index = DummyIndex()
    async def load_indexes(self):
        pass
    async def get_index(self, name):
        return self.index

indexes_mod.Indexes = DummyIndexes

from src.core.resources.library import Library
from src.core.resources.continuity import Continuity
from src.model.records import Message, Metadata

@pytest.mark.asyncio
async def test_library_loads_modules_into_index():
    idx = DummyIndexes()
    lib = Library(indexes=idx)
    await lib.load()
    assert lib._directions
    assert lib._outlines
    assert lib._instructions
    assert idx.index.updated

@pytest.mark.asyncio
async def test_continuity_thread_history():
    idx = DummyIndexes()
    cont = Continuity(indexes=idx)
    m1 = Message(content="hello")
    m1.metadata = Metadata(embedding=[0.1])
    m1.metadata.events = []
    ctx1 = await cont.get_context(m1)
    assert len(cont.get_threads()) == 1

    m2 = Message(content="world")
    m2.metadata = Metadata(embedding=[0.1])
    m2.metadata.events = []
    ctx2 = await cont.get_context(m2)
    threads = cont.get_threads()
    assert len(threads) == 1
    assert len(threads[0].content) == 2
    built = await ctx2.build()
    assert "## Active Thread" in built
