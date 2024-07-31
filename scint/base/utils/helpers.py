import os
import time
import random
import base64
import hashlib

import dotenv
import numpy as np

__all__ = "env", "encode_image", "cosine_similarity", "hash_object", "generate_id"


def env(var: str) -> str:
    dotenv.load_dotenv()
    return dotenv.get_key(".env", var)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


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
    full_string = f"{name[:4].lower()}-{timestamp}{random_digits}"
    return full_string[:8]
