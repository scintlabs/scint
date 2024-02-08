import os
import json

import openai
import aiofiles
from jinja2 import Environment, FileSystemLoader

from deltron.data.pipeline import SystemMessage
from deltron.agents.process import Worker
from deltron.utils.logger import log


class SummarizeData(Worker):
    description = "Use this function to summarize content."
    props = {
        "summary": {
            "type": "string",
            "description": "The summary of the original text.",
        },
    }

    async def function(self, summary: str):
        yield SystemMessage(content=f"{summary}")
