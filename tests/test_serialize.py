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

# Load serialize module without importing package __init__
SERIALIZE_PATH = Path(__file__).resolve().parents[1] / 'src/runtime/serialize.py'
spec = importlib.util.spec_from_file_location('serialize', SERIALIZE_PATH)
serialize_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(serialize_mod)
serialize = serialize_mod.serialize

@attrs.define
class Sample:
    x: int
    y: str


def example(a: int, b: str):
    """Example function.

    Args:
        a: first value
        b: second text
    """
    return f"{a}-{b}"


def test_serialize_class():
    data = serialize(None, Sample)
    assert data["type"] == "json_schema"
    assert data["name"] == "Sample"
    props = data["schema"]["properties"]
    assert props["x"]["type"] == "integer"
    assert props["y"]["type"] == "string"
    assert set(data["schema"]["required"]) == {"x", "y"}


def test_serialize_function():
    data = serialize(None, example)
    assert data["type"] == "function"
    assert data["name"] == "example"
    params = data["parameters"]
    assert params["properties"]["a"]["type"] == "integer"
    assert params["properties"]["b"]["type"] == "string"
    assert set(params["required"]) == {"a", "b"}
