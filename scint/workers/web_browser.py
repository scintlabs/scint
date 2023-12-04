from typing import Dict, List, Optional

import asyncio
import aiohttp

from scint.core.worker import Worker
from scint.services.logger import log
from scint.core.memory import Message
from scint.core.config import GOOGLE_API_KEY, CUSTOM_SEARCH_ID


search_web = Worker(
    name="search_web",
    purpose="You are a web search function for Scint, an intelligent assistant.",
    description="Use this function to search the web.",
    params={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The string to search the web for.",
            },
        },
    },
    req=["query"],
)

load_website = Worker(
    name="load_website",
    purpose="You are a website parsing function for Scint, an intelligent assistant.",
    description="Use this function to get website data from a URL.",
    params={
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The URL of the website to parse.",
            },
        },
    },
    req=["url"],
)

ParsedResponseItem = Dict[str, Optional[str]]


async def fetch_google_search_results(query: str) -> List[ParsedResponseItem]:
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": GOOGLE_API_KEY, "cx": CUSTOM_SEARCH_ID}

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


async def search_web(query: str) -> Dict[str, str]:
    log.info("Running Google search query.")

    search_results = await fetch_google_search_results(query)
    results_str = "\n\n".join(
        [
            f"[{item['title']}](<{item['url']}>)\n\n{item['description']}"
            for item in search_results
        ]
    )

    return Message("system", f"Web search data for the requested query: {results_str}")


async def load_website(url):
    try:
        cmd = ["bunx", "percollate", "md", url]
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stdout_text = stdout.decode("utf-8")
        stderr_text = stderr.decode("utf-8")

        if process.returncode != 0:
            print(f"Command failed with error: {stderr_text}")
            return None

        with open(stdout_text, "r") as file:
            file_contents = file.read()

        return Message("system", f"Data for the requested URL:\n {file_contents}\n\n")

    except Exception as e:
        log.info(f"Error during subprocess execution or file reading: {e}")
        return None
