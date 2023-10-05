import asyncio
import httpx
import os

import dotenv
from typing import List, Dict, Optional
from base.config.logging import logger
from base.config.system import envar

dotenv.load_dotenv()
GOOGLE_API_KEY = envar("GOOGLE_API_KEY")
CUSTOM_SEARCH_ID = envar("CUSTOM_SEARCH_ID")

if not GOOGLE_API_KEY or not CUSTOM_SEARCH_ID:
    raise ValueError("Google API Key and Custom Search ID must be set.")

ParsedResponseItem = Dict[str, Optional[str]]


async def fetch_google_search_results(query: str) -> List[ParsedResponseItem]:
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": GOOGLE_API_KEY, "cx": CUSTOM_SEARCH_ID}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            response_items = response.json().get("items", [])
            parsed_response = [
                {
                    "title": item["title"],
                    "url": item["link"],
                    "description": item.get("snippet", ""),
                }
                for item in response_items
            ]

            return parsed_response

        except httpx.HTTPStatusError as e:
            logger.exception(f"HTTP error occurred: {str(e)}")
            raise

        except Exception as e:
            logger.exception(f"An unexpected error occurred: {str(e)}")
            raise


async def google(query: str) -> List[ParsedResponseItem]:
    logger.info("Running Google search query.")
    return await fetch_google_search_results(query)


asyncio.run(google("openai cookbook"))
