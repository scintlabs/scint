import aiohttp
import requests

from scint.framework.models.blocks import Block, BlockEnum
from scint.framework.models.messages import OutputMessage
from scint.framework.utils.helpers import encode_image


async def fetch_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open("download.png", "wb") as f:
                    image = await f.read()
                    base64_image = encode_image(image)
                    return OutputMessage(
                        blocks=[Block(type=BlockEnum.IMAGE, data=base64_image)]
                    )

            else:
                return OutputMessage(
                    blocks=[
                        Block(type=BlockEnum.TEXT, data="Failed to download image.")
                    ]
                )


async def fetch_website(url: str):
    url = "https://api.microlink.io"
    params = {"url": url, "pdf": True}
    response = requests.get(url, params)
    print(response.json())
    blocks = [Block(data=str(response.json()))]
    return OutputMessage(blocks=blocks)
