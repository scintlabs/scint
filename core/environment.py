import os
import tiktoken
import json


def rolling_token_count(data):
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    prompt_tokens += data["prompt_tokens"]
    completion_tokens += data["completion_tokens"]
    total_tokens += data["total_tokens"]
    return print(f"{prompt_tokens} + {completion_tokens} = {total_tokens}")


def thread_token_count(messages):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens


def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)


def load_files(pathname, chunk_size=500, ignore_dirs=[], ignore_files=[]):
    chunked_files = {}

    ignored_dirs = [".git", ".github", "docs"]
    ignored_dirs.append(ignore_dirs)
    ignored_files = [
        ".DS_Store",
        ".gitattributes",
        ".gitignore",
        "SCRATCH.md",
        "LICENSE.md",
    ]
    ignored_files.append(ignore_files)

    for dirpath, dirnames, filenames in os.walk(pathname):
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
                        chunked_files[(filepath, i)] = chunk
            except Exception as e:
                print(f"Failed to read file {filepath} with error {e}")

    return chunked_files
