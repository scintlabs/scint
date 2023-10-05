import json
import os

import tiktoken

from base.config.logging import logger


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
    tokens_per_message = 0
    tokens_per_name = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens


def process_files(self, path="."):
    text_data = {}
    embeddings_data = {}

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d + "/" not in self.skip_dirs]

        for file in files:
            file_extension = os.path.splitext(file)[-1]
            if file_extension in self.skip_filetypes:
                continue
            file_path = os.path.join(root, file)
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                    tokens = self._tokenize_content(content, file_extension)
                    for token in tokens:
                        for chunk in self._chunk_text_with_overlap(token):
                            chunk_embedding = self.model.encode(chunk.strip())

                            if file_path not in text_data:
                                text_data[file_path] = []
                                embeddings_data[file_path] = []

                            text_data[file_path].append(chunk)
                            embeddings_data[file_path].append()
            except (UnicodeDecodeError, IOError) as e:
                logger.error(f"Error reading {file_path}: {e}")
                continue

    with open(self.text_output_file, "w") as f:
        json.dump(text_data, f)

    with open(self.embeddings_output_file, "w") as f:
        json.dump(embeddings_data, f)
