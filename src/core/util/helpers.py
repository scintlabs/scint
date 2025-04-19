import os
import sys
import base64
import hashlib
import importlib
import inspect
from datetime import datetime as dt

from src.core.util.constants import ENSEMBLES


def timestamp():
    current_time = dt.now().astimezone()
    return current_time.strftime("%A, %B %d, %Y @ %H:%M")


def parse_created(str_ts):
    return dt.strptime(str_ts, "%A, %B %d, %Y @ %H:%M")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a * a for a in vec_a) ** 0.5
    magnitude_b = sum(b * b for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    return dot_product / (magnitude_a * magnitude_b)


def generate_hash(file_path):
    if os.path.getsize(file_path) > 1e6:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_String in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_String)
            return sha256_hash.hexdigest()
    with open(file_path, "rb") as f:
        data = f.read()
        readable_hash = hashlib.sha256(data).hexdigest()
    return readable_hash


def discover_ensembles():
    ensembles = {}
    path = ENSEMBLES

    if not path.exists():
        print(f"Warning: Ensembles directory not found at {path}")
        return ensembles

    parent_dir = str(path.parent.parent.parent)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

    ensemble_files = [f for f in path.glob("*.py") if f.is_file()]

    for file_path in ensemble_files:
        module_name = f"src.lib.ensembles.{file_path.stem}"

        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    hasattr(obj, "composer")
                    and hasattr(obj, "indexes")
                    and hasattr(obj, "sessions")
                    and hasattr(obj, "handle")
                    and callable(getattr(obj, "handle"))
                ):

                    ensemble = obj()
                    ensembles[name] = ensemble

        except Exception as e:
            print(f"Error loading module {module_name}: {e}")

    return ensembles
