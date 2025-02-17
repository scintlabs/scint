import base64
import hashlib
import math
import os
import random
import dotenv
from datetime import datetime as dt
from typing import List


def identifier():
    id = int(dt.now().timestamp()) << 64 | random.getrandbits(64)
    return str(id)


def time(unix_ts=None):
    if unix_ts is None:
        return str(dt.now().timestamp())
    else:
        try:
            return dt.fromtimestamp(unix_ts).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return "Invalid timestamp provided"


def env(var: str) -> str:
    dotenv.load_dotenv()
    return dotenv.get_key(".env", var)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


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


# async def generate_tool_call(context):
#     req = {
#         "model": "gpt-4o",
#         "temperature": 1.2,
#         "top_p": 0.8,
#         "tool_choice": "required",
#         **context.model,
#     }
#     res = await Models.openai.chat.completions.create(**req)
#     return res.choices[0].message.parsed


# async def generate_image(context):
#     req = {"quality": "hd", "size": "1024x1024", "n": 1, "style": "vibrant"}
#     res = await Models.openai.images.generate.create(**req)
#     return res.choices[0].schema.url
