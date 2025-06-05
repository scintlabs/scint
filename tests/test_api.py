import sys
import importlib
import types
import os
from pathlib import Path

src_path = Path(__file__).resolve().parents[1] / "src"
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(src_path))
os.environ["PYTHONPATH"] = str(src_path)
tests_dir = str(Path(__file__).resolve().parent)
if tests_dir in sys.path:
    sys.path.remove(tests_dir)
sys.modules.pop("typing", None)
sys.modules.pop("socket", None)

import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_websocket_endpoint():

    import attrs

    import attrs
    saved = {}
    def patch(name, module):
        saved[name] = sys.modules.get(name)
        sys.modules[name] = module

    # Dummy records module
    records = types.ModuleType("src.model.records")

    @attrs.define
    class Message:
        content: object

    @attrs.define
    class Metadata:
        pass

    @attrs.define
    class Envelope:
        model: Message
        sender: object | None = None

        @classmethod
        def create(cls, sender: str, model: Message):
            return cls(model=model)

    records.Message = Message
    records.Metadata = Metadata
    records.Envelope = Envelope
    patch("src.model.records", records)

    model = types.ModuleType("src.model")
    model.Message = Message
    model.Metadata = Metadata
    model.Content = object
    model.Model = Message
    patch("src.model", model)

    dispatcher_mod = types.ModuleType("src.core.agents.dispatcher")

    class DummyDispatcher:
        def load(self):
            pass

        def start(self):
            pass

        def ref(self):
            class Ref:
                def tell(self, env, sender=None):
                    if sender is not None:
                        sender.tell(env)

            return Ref()

    dispatcher_mod.Dispatcher = DummyDispatcher
    patch("src.core.agents.dispatcher", dispatcher_mod)

    print('sys.path', sys.path[:3])
    print('modules patched')

    try:
        api = importlib.import_module("src.api")
        app = api.create_app()
        assert "/ws" in {r.path for r in app.router.routes}
    finally:
        for name, mod in saved.items():
            if mod is None:
                del sys.modules[name]
            else:
                sys.modules[name] = mod

