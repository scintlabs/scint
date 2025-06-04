import importlib
import types
import sys
import attrs
import pytest


@pytest.mark.asyncio
async def test_bootstrap_runs():
    sent = {"flag": False}

    records = types.ModuleType("src.model.records")
    @attrs.define
    class Message:
        content: str
    @attrs.define
    class Metadata:
        pass
    records.Message = Message
    records.Metadata = Metadata
    records.Content = str
    sys.modules["src.model.records"] = records

    model = types.ModuleType("src.model")
    model.Message = Message
    model.Metadata = Metadata
    model.Content = str
    model.Model = Message
    sys.modules["src.model"] = model

    dispatcher = types.ModuleType("src.core.agents.dispatcher")
    class DummyDispatcher:
        def load(self):
            pass
        def start(self):
            pass
        def ref(self):
            class Ref:
                def tell(self, env, sender=None):
                    sent["flag"] = True
            return Ref()
    dispatcher.Dispatcher = DummyDispatcher
    sys.modules["src.core.agents.dispatcher"] = dispatcher

    bootstrap = importlib.import_module("src.bootstrap").bootstrap
    await bootstrap()
    assert sent["flag"]
