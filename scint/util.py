import difflib
import json
from datetime import datetime

import demjson3 as demjson
import numpy as np
import pytz
import tiktoken

from scint.logging import logger


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
            logger.info("{e}")

    return


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def united_diff(str1, str2):
    lines1 = str1.splitlines(True)
    lines2 = str2.splitlines(True)
    diff = difflib.unified_diff(lines1, lines2)
    return "".join(diff)


def get_local_time():
    current_time_utc = datetime.now(pytz.utc)
    sf_time_zone = pytz.timezone("America/Los_Angeles")
    local_time = current_time_utc.astimezone(sf_time_zone)
    # You may format it as you desire, including AM/PM
    formatted_time = local_time.strftime("%Y-%m-%d %I:%M:%S %p %Z%z")

    return formatted_time


def parse_json(string):
    result = None
    try:
        result = json.loads(string)
        return result
    except Exception as e:
        print(f"Error parsing json with json package: {e}")

    try:
        result = demjson.decode(string)
        return result
    except demjson.JSONDecodeError as e:
        print(f"Error parsing json with demjson package: {e}")
        raise e


def read_in_chunks(file_object, chunk_size):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
