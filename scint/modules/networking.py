import asyncio

from scint.core.processes import Process
from scint.core.messages import SystemMessage
from scint.core.tools import Tool, Tools
from scint.services.google import google_custom_search
from scint.services.logger import log


class SearchWeb(Tool):
    name = "SearchWeb"
    description = "This function searches the web for the given query."
    props = {
        "query": {"type": "string", "description": "The query to search for."},
        "site": {
            "type": "string",
            "description": "The URL for site-specific searches.",
        },
    }
    required = ["query"]

    async def execute_action(self, query: str, site: str = None) -> SystemMessage:
        site = site
        search_results = await google_custom_search(query)
        results_str = "\n\n".join(
            [
                f"[{item['title']}](<{item['url']}>)\n\n{item['description']}"
                for item in search_results
            ]
        )

        log.info(results_str)

        return SystemMessage(
            f"Search results:\n\n{results_str}", self.__class__.__name__
        )


class LoadWebsite(Tool):
    description = "This function loads a specific website."
    props = {
        "url": {
            "type": "string",
            "description": "The exact url to load.",
        },
    }
    required = ["url"]

    async def execute_action(self, url: str) -> SystemMessage:
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
            return SystemMessage(f"Unable to load site.", self.__class__.__name__)

        try:
            with open(stdout_text, "r") as file:
                website_data = file.read()

            return SystemMessage(f"{website_data}", self.__class__.__name__)

        except Exception as e:
            log.error(e)
            return SystemMessage(f"Unable to load site.", self.__class__.__name__)


class WebBrowsing(Process):
    identity = "You are a web browsing process for an intelligent assistant, and you're responsible for finding and parsing internet and website data."
    instructions = "You are one of many advanced modules which comprise an intelligent assistant. When you receive a request, make sure it aligns with one of your available functions. If it doesn't, defer the task so another module can help the user."
    tools = Tools()
    tools.add(SearchWeb())
    tools.add(LoadWebsite())
