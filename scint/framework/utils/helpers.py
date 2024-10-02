import base64
import hashlib
import os
import random
import math
from datetime import datetime, timezone
from importlib import import_module
from typing import List

import dotenv

__all__ = (
    "env",
    "encode_image",
    "cosine_similarity",
    "hash_object",
    "generate_id",
    "get_module",
    "timestamp",
)


def timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d  %H:%M:%S")


def get_module(module_path, provider_name):
    try:
        module = import_module(module_path)
        provider = getattr(module, provider_name)
        return provider
    except ImportError as e:
        print(f"Error: Provider '{provider_name}' not found. {str(e)}")
        return None


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


def similarities(intent, embedding):
    return [
        1 - cosine_similarity(embedding, process.weighted_average_embedding())
        for process in intent
        if process.weighted_average_embedding() is not None
    ]


def hash_object(file_path):
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


def generate_id(name: str):
    time = timestamp()
    random_digits = random.randint(100, 999)
    full_string = f"{name[:9].lower()}{time}{random_digits}"
    return full_string[:9]
