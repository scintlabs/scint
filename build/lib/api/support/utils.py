import base64
import hashlib
import math
import os
from importlib import import_module
from typing import List

import dotenv


def get_module(name, package):
    try:
        obj = import_module(name, package)
        return getattr(obj, package)
    except ImportError as e:
        print(e)


def set_module(api, settings):
    try:
        name = settings.get("name")
        package = settings.get("package")
        params = settings.get("parameters")
        ref = get_module(package, name)
        setattr(api, name.lower(), ref(**params))
    except AttributeError as e:
        print(e)


def env(var: str) -> str:
    dotenv.load_dotenv()
    return dotenv.get_key(".env", var)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)


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
