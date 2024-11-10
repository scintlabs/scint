import aiohttp
import requests

from scint.repository.models.message import Block, Message


async def fetch_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with open("download.png", "wb") as f:
                    image = await f.read()
                    return Message(blocks=[Block(data=image)])

            else:
                return Message(blocks=[Block(data="Failed to download image.")])


async def fetch_website(url: str):
    url = "https://api.microlink.io"
    params = {"url": url, "pdf": True}
    response = requests.get(url, params)
    print(response.json())
    blocks = [Block(data=str(response.json()))]
    return Message(blocks=blocks)


def fetch_file(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return None
