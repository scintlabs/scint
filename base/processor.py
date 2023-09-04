import os, json, subprocess
from enum import Enum
from typing import List

from rich.markdown import Markdown
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize

from util.logging import logger


class ProcessorContext:
    def __init__(self):
        self.cwd = os.getcwd()


class Processor:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/multi-qa-mpnet-base-cos-v1"
        )

        self.skip_filetypes = [
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".bmp",
            ".pdf",
            ".DS_Store",
            ".gitattributes",
            ".gitmodules",
        ]
        self.skip_dirs = [".git/"]
        self.text_output_file = "processed_data_text.json"
        self.embeddings_output_file = "processed_data_embeddings.json"
        self.chunk_size = 500
        self.overlap = 150
        self.code_filetypes = [".py", ".js", ".java", ".c"]
        self.text_filetypes = [".txt", ".md"]

    def _parse_gitignore(self, path="."):
        gitignore_path = os.path.join(path, ".gitignore")

        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as f:
                lines = f.readlines()

                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if line.endswith("/"):
                        self.skip_dirs.append(line)
                    else:
                        self.skip_filetypes.append(line)

    def _chunk_text_with_overlap(self, content):
        start = 0
        end = self.chunk_size
        while start < len(content):
            yield content[start:end]
            start = end - self.overlap
            end = start + self.chunk_size

    def _tokenize_content(self, content, file_type):
        if file_type in self.code_filetypes:
            return content.split("\n")
        elif file_type in self.text_filetypes:
            return sent_tokenize(content)
        else:
            return []

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
                                embeddings_data[file_path].append(
                                    chunk_embedding.tolist()
                                )
                except (UnicodeDecodeError, IOError) as e:
                    logger.error(f"Error reading {file_path}: {e}")
                    continue

        with open(self.text_output_file, "w") as f:
            json.dump(text_data, f)

        with open(self.embeddings_output_file, "w") as f:
            json.dump(embeddings_data, f)
