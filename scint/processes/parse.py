from scint.components.config import Preset
from scint.components.models import SystemMessage
from scint.components.process import Process
from scint.components.tool import Tool


class Extract(Tool):
    Preset = Preset.tool
    description = "Use this function to extract keywords from the provided text, incuding semantic keywords and any named entities."
    props = {
        "keywords": {
            "type": "string",
            "description": "A list of comma-separated keywords taken from the text.",
        },
        "named_entities": {
            "type": "string",
            "description": "A comma-separated list of named entities mentioned within the text.",
        },
    }

    async def function(self, keywords: str, named_entities: str = None):
        yield SystemMessage(content=f"{keywords} {named_entities}")


class Summarize(Tool):
    Preset = Preset.tool
    description = (
        "Record summaries with the breadth and directness and clarity of Hemingway."
    )
    props = {
        "summary": {
            "type": "string",
            "description": "The summary.",
        },
    }

    async def function(self, summary: str):
        yield SystemMessage(content=f"{summary}")


class Load(Tool):
    Preset = Preset.tool
    description = "Use this function to load and open local files."
    props = {
        "filepath": {
            "type": "string",
            "description": "The full path of the file.",
        },
    }

    async def function(self, filepath: str):
        documents = []
        with open(filepath, "r") as file:
            data = file.readlines()

        yield SystemMessage(content=str(data))


class Parse(Process):
    Preset = Preset.assistant
    description = "You are a data parsing process."
    tooling = [Load()]
