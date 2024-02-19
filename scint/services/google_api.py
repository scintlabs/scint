from typing import Dict, Optional

import aiohttp

from scint.constants import GOOGLE_API_KEY, GOOGLE_SEARCH_ID
from scint.utils.logger import log

ParsedResponseItem = Dict[str, Optional[str]]


def dict_to_string(d):
    return "\n".join(f"{key}: {value}" for key, value in d.items())


async def google_custom_search(query: str):
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": GOOGLE_API_KEY, "cx": GOOGLE_SEARCH_ID}

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

                parsed_string = ""
                for dict in parsed_response:
                    string = dict_to_string(dict)
                    parsed_string += string + "\n"

                yield parsed_string

        except aiohttp.ClientResponseError as e:
            log.exception(f"HTTP error occurred: {str(e)}")
            raise

        except Exception as e:
            log.exception(f"An unexpected error occurred: {str(e)}")
            raise


async def google_custom_search_test(query: str):
    parsed_response = [
        {
            "title": "Steve Jobs",
            "url": "https://en.wikipedia.org/wiki/Steve_Jobs",
            "description": "Steven Paul Jobs (February 24, 1955 – October 5, 2011) was an American businessman, inventor, and investor best known for co-founding the technology giant ...",
        },
        {
            "title": "Remembering Steve Jobs",
            "url": "https://www.apple.com/stevejobs/",
            "description": "Steve Jobs lived and lives on vicariously through everything that apple has accomplished. He has inspired and changed the lives of millions. I want to be short ...",
        },
        {
            "title": "Steve Jobs | Biography, Education, Apple, & Facts",
            "url": "https://www.britannica.com",
            "description": "Steve Jobs, the visionary co-founder of Apple Inc., revolutionized technology and consumer electronics with his innovative products that ...",
        },
        {
            "title": "Remembering Steve Jobs",
            "url": "https://www.apple.com/stevejobs/",
            "description": "Steve Jobs lived and lives on vicariously through everything that apple has accomplished. He has inspired and changed the lives of millions. I want to be short ...",
        },
        {
            "title": "Steve Jobs",
            "url": "https://en.wikipedia.org/wiki/Steve_Jobs",
            "description": "Steven Paul Jobs (February 24, 1955 – October 5, 2011) was an American businessman, inventor, and investor best known for co-founding the technology giant ...",
        },
    ]

    parsed_string = ""
    for dict in parsed_response:
        string = dict_to_string(dict)
        parsed_string += string + "\n"

    yield parsed_string
