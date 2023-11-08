from typing import Dict, List, Optional
import asyncio

import aiohttp
import wikipediaapi

from services.logger import log
from core.config import GOOGLE_API_KEY, CUSTOM_SEARCH_ID


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

    return {
        "role": "system",
        "content": f"{results_str}",
        "name": "web_search",
    }


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

        # Assuming the command returns the filename, read the file contents
        with open(stdout_text, "r") as file:
            file_contents = file.read()

        message = {
            "role": "system",
            "content": f"Here's the data for the requested URL:\n {file_contents}\n\n Summarize the data for the user.",
            "name": "load_website",
        }
        return message

    except Exception as e:
        print(f"Error during subprocess execution or file reading: {e}")
        return None
