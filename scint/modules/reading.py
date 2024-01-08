import json

from scint.core.processes import Process
from scint.core.messages import SystemMessage, UserMessage
from scint.core.tools import Tool, Tools
from scint.services.openai import tool_completion
from scint.services.logger import log


class ReadAndSummarize(Tool):
    name = "read_and_summarize"
    description = "Reads, parses, and summarizes content from various sources like books, documents, and web pages."
    props = {
        "source": {
            "type": "string",
            "description": "The source of the content to be read. It can be a file path, URL, or raw text.",
        },
        "summary_length": {
            "type": "int",
            "description": "The desired length of the summary (number of sentences or words).",
        },
    }
    required = ["source", "summary_length"]

    async def execute_action(self, source: str, summary_length: int) -> SystemMessage:
        content = f"Fetched content based on source: {source}"

        summarized_content = f"Summarized content (first {summary_length} units): {content[:summary_length]}"

        try:
            return SystemMessage(summarized_content, self.__class__.__name__)

        except Exception as e:
            log.error(f"Error in reading and summarizing content: {e}")
            return SystemMessage("Unable to read the content.", self.__class__.__name__)
