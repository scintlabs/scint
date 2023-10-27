import asyncio
import os
from typing import Dict, List, Optional

import aiohttp

from core.config import envar
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


from typing import Dict


async def search_web(query: str) -> Dict[str, str]:
    log.info("Running Google search query.")
    search_results = await fetch_google_search_results(query)

    results_str = "\n\n".join(
        [
            f"Title: {item['title']}\nURL: {item['url']}\nDescription: {item['description']}"
            for item in search_results
        ]
    )

    message_data = {
        "role": "system",
        "content": f"Parse these web search results for the user: {results_str}",
        "name": "web_search",
    }
    return message_data
