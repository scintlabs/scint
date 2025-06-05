import os
import hashlib
from importlib import import_module
from datetime import datetime as dt, timezone as tz

import dotenv


TS_FMT = "%A, %B %d, %Y @ %H:%M"


def timestamp():
    current_time = dt.now().astimezone()
    return current_time.strftime(TS_FMT)


def timestamp_to_epoch(ts: str):
    return dt.strptime(ts, TS_FMT).timestamp()


def iso_to_epoch(ts: str):
    return dt.fromisoformat(ts).astimezone(tz.utc).timestamp()


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


def env(var: str):
    dotenv.load_dotenv()
    return dotenv.get_key(".env", var)


def import_object(module_path: str, obj_name: str):
    module = import_module(module_path)
    return getattr(module, obj_name)
