import importlib.util
from pathlib import Path
import sys
import importlib.util as iu
import pathlib
import sysconfig
path = pathlib.Path(sysconfig.get_path("stdlib")) / "typing.py"
spec = iu.spec_from_file_location("typing", path)
_typing = iu.module_from_spec(spec)
spec.loader.exec_module(_typing)
sys.modules["typing"] = _typing
import attrs
import pytest

# Patch minimal model modules required by mailbox
records_spec = importlib.util.spec_from_loader("src.model.records", loader=None)
records = importlib.util.module_from_spec(records_spec)

@attrs.define
class Message:
    content: str

@attrs.define
class Metadata:
    pass

records.Message = Message
records.Metadata = Metadata
records.Content = str

model_spec = importlib.util.spec_from_loader("src.model", loader=None)
model = importlib.util.module_from_spec(model_spec)
model.Message = Message
model.Metadata = Metadata
model.Content = str
model.Model = Message

_orig_model = sys.modules.get("src.model")
_orig_records = sys.modules.get("src.model.records")
sys.modules["src.model.records"] = records
sys.modules["src.model"] = model

# Load mailbox module directly
MAILBOX_PATH = Path(__file__).resolve().parents[1] / 'src/runtime/mailbox.py'
spec = importlib.util.spec_from_file_location('mailbox', MAILBOX_PATH)
mailbox_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mailbox_mod)
Mailbox = mailbox_mod.Mailbox
Envelope = mailbox_mod.Envelope

@pytest.mark.asyncio
async def test_mailbox_put_get():
    box = Mailbox()
    env = Envelope.create("user", Message("hi"))
    await box.put(env)
    assert not box.empty()
    received = await box.get()
    assert received.model.content == "hi"
    box.task_done()
    assert box.empty()
    if _orig_model is not None:
        sys.modules["src.model"] = _orig_model
    else:
        sys.modules.pop("src.model", None)
    if _orig_records is not None:
        sys.modules["src.model.records"] = _orig_records
    else:
        sys.modules.pop("src.model.records", None)
