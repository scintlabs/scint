from deltron.data.pipeline import SystemMessage
from deltron.agents import Process
from deltron.agents import Worker
from deltron.agents import SelectSearchResult, SummarizeData
from deltron.utils.logger import log


class Select(Process):
    instructions = "You are a web search selection process. For every message, select the website that best matches the search query."

    def initialize_workers(self):
        self.workers.add(SelectSearchResult())


class Parse(Process):
    instructions = "You are a website parsing process. For every message you receive, generate a contextually rich summary."

    def initialize_workers(self):
        self.workers.add(SummarizeData())


class SelectSearchResult(Worker):
    description = (
        "Use this function to select the single best entry from the provided list of search results."
    )
    props = {
        "url": {
            "type": "string",
            "description": "The URL for the selected link.",
        },
    }

    async def function(self, url: str):
        yield SystemMessage(content=f"{url}")
