import asyncio
from typing import Dict, List, Optional

import aiohttp

from scint import config
from scint.core.context import Message
from scint.core.tools import Tool, Tools
from scint.core.worker import Worker
from scint.services.logger import log

ParsedResponseItem = Dict[str, Optional[str]]


async def google_search(query: str) -> List[ParsedResponseItem]:
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": config.GOOGLE_API_KEY, "cx": config.GOOGLE_SEARCH_ID}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(endpoint, params=params) as response:
                response.raise_for_status()
                response_data = await response.json()
                response_items = response_data.get("items", [])
                parsed_response = [
                    {
                        "title": item["title"],
                        "url": item["link"],
                        "description": item.get("snippet", ""),
                    }
                    for item in response_items[:5]
                ]

                return parsed_response

        except aiohttp.ClientResponseError as e:
            log.exception(f"HTTP error occurred: {str(e)}")
            raise

        except Exception as e:
            log.exception(f"An unexpected error occurred: {str(e)}")
            raise


class LoadWebsite(Tool):
    description = ("This function loads a specific website.",)
    props = {
        "url": {
            "type": "string",
            "description": "The exact url to load.",
        },
    }
    required = ["url"]

    async def load_website(self, url: str) -> Message:
        cmd = ["bunx", "percollate", "md", url]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stdout_text = stdout.decode("utf-8")
        stderr_text = stderr.decode("utf-8")

        if process.returncode != 0:
            log.error(f"{stderr_text}")
            return Message(f"There was a problem loading the site.")

        try:
            with open(stdout_text, "r") as file:
                website = file.read()

            return Message(f"{website}")

        except Exception as e:
            log.error(e)
            return Message(f"There was a problem loading the site.")


class SearchWeb(Tool):
    description = "This function searches the web for the given query."
    props = {
        "query": {"type": "string", "description": "The query to search the web for."},
        "site": {
            "type": "string",
            "description": "The URL for site-specific searches.",
        },
    }
    required = ["query"]

    async def search_web(self, query: str, site: str = None) -> Message:
        log.info("Running Google search query.")

        site = site
        search_results = await google_search(query)
        results_str = "\n\n".join(
            [
                f"[{item['title']}](<{item['url']}>)\n\n{item['description']}"
                for item in search_results
            ]
        )

        return Message(f"Search results:\n\n{results_str}", "web_researcher")


class Researcher(Worker):
    def __init__(self):
        super().__init__()
        self.name = "Researcher"
        self.tools = Tools()
        self.tools.add(SearchWeb())
        self.tools.add(LoadWebsite())

        log.info(f"{self.name} loaded.")
