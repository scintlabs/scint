import os

import dotenv
import injector
import numpy as np

from scint.utils.logger import log


def envar(var: str) -> str:
    dotenv.load_dotenv()
    return os.environ.get(var)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def read_file_in_chunks(file_object, chunk_size):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def inject_module(module_injector, module_interface):
    bridge = injector.Injector([module_injector])
    injected_module = bridge.get(module_interface)
    return injected_module


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
