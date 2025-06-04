import importlib.util
from pathlib import Path
import attrs
import sys
import pytest

# Patch minimal model modules required by mailbox
records = importlib.util.module_from_spec(
    importlib.util.spec_from_loader("src.model.records", loader=None)
)
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

model = importlib.util.module_from_spec(
    importlib.util.spec_from_loader("src.model", loader=None)
)
model.Message = Message
model.Metadata = Metadata
model.Content = str
model.Model = Message
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
