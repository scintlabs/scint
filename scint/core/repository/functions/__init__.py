import hashlib
import os
from typing import Any, Dict, List

from tree_sitter import Language, Parser

PY_LANGUAGE = Language("scint/core/repository/languages.so", "python")
IGNORED_PATTERNS = [
    ".git",
    ".venv",
    ".venvs",
    "__pycache__",
    ".DS_Store",
    ".idea",
    ".vscode",
    "node_modules",
    ".gitignore",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.so",
    "*.dylib",
    "*.dll",
    "*.exe",
    "*.bin",
    "*.pkl",
    "*.db",
]


def should_ignore(path: str) -> bool:
    name = os.path.basename(path)
    return any(
        name == pattern
        or (pattern.startswith("*") and name.endswith(pattern[1:]))
        or (pattern in path)
        for pattern in IGNORED_PATTERNS
    )


def hash_file(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def read_file(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return None


def parse_code(content: str) -> List[Dict[str, Any]]:
    parser = Parser()
    parser.set_language(PY_LANGUAGE)
    tree = parser.parse(bytes(content, "utf-8"))

    result = []
    for node in tree.root_node.children:
        if node.type in ["import_statement", "import_from_statement"]:
            result.append(
                {
                    "type": "import",
                    "signature": node.text.decode("utf-8"),
                    "start_line": node.start_point[0],
                    "end_line": node.end_point[0],
                }
            )
        elif node.type == "class_definition":
            result.append(
                {
                    "type": "class",
                    "signature": node.children[1].text.decode("utf-8"),
                    "start_line": node.start_point[0],
                    "end_line": node.end_point[0],
                }
            )
        elif node.type == "function_definition":
            result.append(
                {
                    "type": "function",
                    "signature": node.children[1].text.decode("utf-8"),
                    "start_line": node.start_point[0],
                    "end_line": node.end_point[0],
                }
            )

    return result


def parse_doc(content: str) -> List[Dict[str, Any]]:
    lines = content.split("\n")
    result = []

    for i, line in enumerate(lines):
        if i == 0 or line.startswith("#"):
            result.append({"type": "heading", "content": line, "line": i})
        elif line.strip() and "." in line:
            first_sentence = line.split(".")[0] + "."
            result.append({"type": "paragraph", "content": first_sentence, "line": i})

    return result


def map_file(filepath: str) -> Dict[str, Any]:
    if should_ignore(filepath):
        return None

    content = read_file(filepath)
    if content is None:
        return None

    file_map = {
        "path": filepath,
        "hash": hash_file(filepath),
        "type": "file",
        "elements": [],
    }

    if filepath.endswith(".py"):
        file_map["elements"] = parse_code(content)
    else:
        file_map["elements"] = parse_doc(content)

    return file_map


def map_directory(path: str) -> Dict[str, Any]:
    if should_ignore(path):
        return None

    if os.path.isfile(path):
        return map_file(path)

    dir_map = {"path": path, "type": "directory", "contents": {}}

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            subdir_map = map_directory(item_path)
            if subdir_map:
                dir_map["contents"][item] = subdir_map
        else:
            file_map = map_file(item_path)
            if file_map:
                dir_map["contents"][item] = file_map

    return dir_map
