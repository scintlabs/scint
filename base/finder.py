import asyncio, typing

import googleapiclient

import util
from util.logging import logger

build = googleapiclient.discovery.build


async def google(query):
    logger.info(f"Running Google search query.")
    service = build("customsearch", "v1", developerKey=util.envar("GOOGLE_API_KEY"))
    try:
        response = (
            service.cse().list(q=query, cx=util.envar("CUSTOM_SEARCH_ID")).execute()
        )

        response_items = response.get("items", [])
        parsed_response = [
            {
                "title": item["title"],
                "url": item["link"],
                "description": item.get("snippet", ""),
            }
            for item in response_items
        ]

        return parsed_response

    except Exception as e:
        logger.exception(f"There was a problem: {e}")

        raise
