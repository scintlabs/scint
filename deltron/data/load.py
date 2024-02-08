import json
from datetime import datetime
from typing import Dict, List
from deltron.constants import CONFIG

from deltron.data.pipeline import SystemMessage
from deltron.agents import Process, Worker
from deltron.services.openai import completion
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


class Load(Process):
    instructions = "You are a website loading process. For every message, load the appropriate data for the search query."

    def initialize_workers(self):
        pass
