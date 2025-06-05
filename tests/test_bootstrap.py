import importlib
import types
import sys
import importlib
import pathlib
import sysconfig

path = pathlib.Path(sysconfig.get_path("stdlib")) / "typing.py"
spec = importlib.util.spec_from_file_location("typing", path)
_typing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_typing)
sys.modules["typing"] = _typing

import os
from pathlib import Path
import attrs
import pytest


@pytest.mark.asyncio
async def test_bootstrap_runs():
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
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
    orig_records = sys.modules.get("src.model.records")
    sys.modules["src.model.records"] = records

    model = types.ModuleType("src.model")
    model.Message = Message
    model.Metadata = Metadata
    model.Content = str
    model.Model = Message
    orig_model = sys.modules.get("src.model")
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
    if orig_model is not None:
        sys.modules["src.model"] = orig_model
    else:
        sys.modules.pop("src.model", None)
    if orig_records is not None:
        sys.modules["src.model.records"] = orig_records
    else:
        sys.modules.pop("src.model.records", None)
