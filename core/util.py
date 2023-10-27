import os
import difflib
import json
import random
from datetime import datetime
from typing import Optional, Dict, Union

import dotenv
import numpy as np
import tiktoken

from services.logger import log


def get_random_message(message_type, message_dict):
    last_five_messages = []

    message = random.choice(list(message_dict))

    # Ensure the message hasn't been used in the last five messages
    while message in last_five_messages:
        message = random.choice(list(message_dict))

    # Update the list of last five messages
    last_five_messages.append(message)
    if len(last_five_messages) > 5:
        last_five_messages.pop(0)

    return message


def envar(var: str) -> Optional[str]:
    dotenv.load_dotenv()
    return os.environ.get(var)


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


def create_temporality_message() -> dict[str, str]:
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%m")

    return {
        "role": "system",
        "content": f"The following message was sent at {time} on {date}.",
        "name": "coordinator",
    }


def split_discord_message(message, max_length=2000):
    if len(message) <= max_length:
        return [message]

    lines = message.split("\n")
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(line) > max_length:
            words = line.split(" ")
            for word in words:
                if len(word) > max_length:
                    if current_chunk:
                        chunks.append(current_chunk)
                        current_chunk = ""
                    chunks.append(word)
                elif len(current_chunk) + len(word) > max_length:
                    chunks.append(current_chunk)
                    current_chunk = word
                else:
                    current_chunk = f"{current_chunk} {word}" if current_chunk else word
        elif len(current_chunk) + len(line) > max_length:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk = f"{current_chunk}\n{line}" if current_chunk else line

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
