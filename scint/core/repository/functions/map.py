import os
import pprint
import re
from typing import Any, Dict, List

from scint.core.utils.helpers import hash_object


# utility
def read_file(file_path: str):
    encodings = ["utf-8", "latin-1", "ascii"]
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue

    with open(file_path, "rb") as f:
        return f.read().hex()


# core
def map_structure(path: str):
    name = os.path.basename(path)

    if os.path.isfile(path):
        return {
            "name": name,
            "type": "file",
            "path": path,
            "size": os.path.getsize(path),
        }
    elif os.path.isdir(path):
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            items.append(map_structure(item_path))
        return {"name": name, "type": "dir", "path": path, "items": items}
    else:
        return None


def map_file(path: str) -> Dict[str, Any]:
    content = read_file(path)
    elements = []

    if all(c in "0123456789abcdef" for c in content):
        elements.append({"type": "binary", "content": content[:100] + "..."})
    else:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if i == 0:
                elements.append({"type": "title", "content": line, "line": i})
            elif line.startswith("#"):
                elements.append({"type": "subtitle", "content": line, "line": i})
            elif line.strip() == "":
                elements.append({"type": "paragraph_break", "line": i})
            elif re.search(r"\[.*\]\(.*\)", line):
                elements.append({"type": "link", "content": line, "line": i})
            else:
                elements.append({"type": "text", "content": line, "line": i})

    return {
        "name": os.path.basename(path),
        "path": path,
        "size": os.path.getsize(path),
        "elements": elements,
    }


def map_blocks(file_map: Dict[str, Any], target_size: int = 1000):
    elements = file_map["elements"]

    if len(elements) == 1 and elements[0]["type"] == "binary":
        total_size = len(elements[0]["content"]) // 2
        return [
            (i, min(i + target_size - 1, total_size - 1))
            for i in range(0, total_size, target_size)
        ]

    blocks = []
    current_size = 0
    block_start = 0

    for i, element in enumerate(elements):
        element_size = len(element.get("content", ""))
        if current_size + element_size > target_size and i > block_start:
            blocks.append((block_start, i - 1))
            block_start = i
            current_size = element_size
        else:
            current_size += element_size

    # Add the last block
    if block_start < len(elements):
        blocks.append((block_start, len(elements) - 1))

    return blocks


# composition
def with_filters(ignore_list: List[str]):
    def filter_func(path: str) -> bool:
        return os.path.basename(path) not in ignore_list

    return filter_func


def with_hash(filepath):
    return lambda _: hash_object(filepath)


# main map func
def map(path, ignore=[".git"], include_hash=True):
    structure = map_structure(path)
    filter_func = with_filters(ignore)

    def process_item(item):
        if not filter_func(item["path"]):
            return None

        if item["type"] == "file":
            file_map = map_file(item["path"])
            block_map = map_blocks(file_map)
            item["file_map"] = file_map
            item["block_map"] = block_map
            if include_hash:
                item["hash"] = with_hash(item["path"])
        elif item["type"] == "dir":
            item["items"] = [
                process_item(subitem)
                for subitem in item["items"]
                if subitem is not None
            ]
        return item

    return process_item(structure)


data = map("/scint")
pp = pprint.PrettyPrinter(indent=4, width=80)
pp.pprint(data)


def get_chunk(filepath, index, file_map, block_map):
    if index < 0 or index >= len(block_map):
        raise ValueError(f"Index must be between 0 and {len(block_map) - 1}")

    start, end = block_map[index]

    if len(file_map["elements"]) == 1 and file_map["elements"][0]["type"] == "binary":
        with open(filepath, "rb") as f:
            f.seek(start)
            return f.read(end - start + 1)

    block_content = []
    for i in range(start, end + 1):
        element = file_map["elements"][i]
        if "content" in element:
            block_content.append(element["content"])
        elif element["type"] == "paragraph_break":
            block_content.append("")

    return "\n".join(block_content)
