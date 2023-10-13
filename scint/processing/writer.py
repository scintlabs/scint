import json
import os

from scint.system import config
from scint.services.logging import logger

datastore = lambda name: os.path.join(
    config.APPDATA, "conversations", name.lower() + ".json"
)


def load_messages(name) -> list[dict[str, str]]:
    logger.info(f"Loading messages: {datastore(name)}.")
    path = datastore(name)

    try:
        with open(path, "r") as f:
            if json.load(f) is not None:
                data = json.load(f)
                messages = data

                return messages

            else:
                with open(path, "w") as f:
                    data: list[dict[str, str]] = []
                    json.dump(data, f)

                    return data

    except Exception as e:
        logger.error(f"Error loading message store: {e}")
        raise


def append_messages(message, filepath) -> None:
    logger.info(f"Writing message: {datastore(filepath)}.")
    datastore(filepath)

    try:
        with open(datastore(filepath), "w") as f:
            data = json.load(filepath)
            data.append(message)
            json.dump(filepath, data)

    except Exception as e:
        logger.error(f"Error writing message: {e}.")
        raise


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
