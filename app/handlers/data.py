import sys
import os
import time
import pathlib

from app.services.logging import logger
from app.system.config import envar

api_key = envar("OPENAI_API_KEY")

if api_key is None:
    logger.error("The environment variable 'OPENAI_API_KEY' is not set.")
    raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")


path = pathlib.Path("/Users/kaechle/Developer/projects/scint-agent/result.py")

prompt = {
    "role": "system",
    "content": "You are a recursive function production algorithm for an artificial intelligence system. For every message, produce content according to the given specifications. If the content requires revision, it will be returned with updated specs. Once completed, you'll receive a reward.",
    "name": "file_writer",
}


async def file_writer(filepath, content):
    logger.info("File writing function init.")

    if content is not None:
        try:
            with open(filepath, "w") as file:
                document = file.write(content)

                return document

        except Exception:
            logger.info("{e}")

    return
