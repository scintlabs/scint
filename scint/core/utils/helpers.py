import base64
import hashlib
from importlib import import_module
import os
import random
import time
import dotenv

import numpy

__all__ = (
    "env",
    "encode_image",
    "cosine_similarity",
    "hash_object",
    "generate_id",
    "get_module",
)


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


def cosine_similarity(a, b):
    a = numpy.asarray(a)
    b = numpy.asarray(b)
    a = a.flatten()
    b = b.flatten()

    if numpy.all(a == 0) or numpy.all(b == 0):
        return 0.0

    return numpy.dot(a, b) / (numpy.linalg.norm(a) * numpy.linalg.norm(b))


def similarities(processes, embedding):
    return [
        1 - cosine_similarity(embedding, process.weighted_average_embedding())
        for process in processes
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
        bytes = f.read()
        readable_hash = hashlib.sha256(bytes).hexdigest()
    return readable_hash


def generate_id(name: str):
    timestamp = int(time.time())
    random_digits = random.randint(100, 999)
    full_string = f"{name[:9].lower()}{timestamp}{random_digits}"
    return full_string[:9]
