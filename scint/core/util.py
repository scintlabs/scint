import json
import os
import uuid
from datetime import datetime
from typing import Dict, Optional, Union

import dotenv
import numpy as np
import tiktoken
from scint.services.logger import log


def envar(var: str) -> Optional[str]:
    dotenv.load_dotenv()
    return os.environ.get(var)


def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")


def generate_uuid4():
    return str(uuid.uuid4())


def load_config(dir) -> Union[Dict, None]:
    try:
        with open(dir, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        log.warning(f"State file {dir} not found.")
        return None


def count_tokens(s: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(s))


async def file_writer(filepath, content):
    if content is not None:
        try:
            with open(filepath, "w") as file:
                document = file.write(content)

                return document

        except Exception:
            log.info("{e}")

    return


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def read_file_in_chunks(file_object, chunk_size):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except (UnicodeDecodeError, FileNotFoundError, PermissionError):
        return None


def build_directory_mapping(path):
    directory_mapping = {
        "directory": os.path.basename(path) if os.path.basename(path) else path,
        "data": {"directories": [], "files": []},
    }

    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            if entry.name in {".git", "__pycache__", ".DS_Store"}:
                continue
            directory_mapping["data"]["directories"].append(
                build_directory_mapping(entry.path)
            )

        elif entry.is_file():
            if entry.name.endswith((".txt", ".md", ".py", ".json", ".xml")):
                content = read_file_content(entry.path)
                if content is not None:  # Only include text files that could be read
                    directory_mapping["data"]["files"].append(
                        {"name": entry.name, "content": content}
                    )

    return directory_mapping
