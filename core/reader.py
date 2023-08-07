import os, json
from core.util import minify

path = "/Users/kaechle/Developer/projects/scint-server"
ignored_dirs = [".git", ".github", "client"]
ignored_files = [
    ".DS_Store",
    ".gitattributes",
    ".gitignore",
    "LICENSE.md",
    ".editorconfig",
    "__init__.py",
]


def read():
    chunk_size = 1000
    chunked_data = {}

    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
        for filename in filenames:
            if filename in ignored_files:
                continue
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    chunks = [
                        content[i : i + chunk_size]
                        for i in range(0, len(content), chunk_size)
                    ]
                    for i, chunk in enumerate(chunks):
                        chunked_data[(filepath, i)] = chunk
            except Exception as e:
                print(f"Failed to read file {filepath} with error {e}")

    parsed_data = minify(chunked_data)
    return parsed_data
