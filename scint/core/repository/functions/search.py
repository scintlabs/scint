import asyncio

import aiohttp
import requests

from scint.core.primitives.messages import OutputMessage
from scint.core.utils.helpers import encode_image


async def search_github_repos(query: str):
    process = await asyncio.create_subprocess_shell(
        f"gh search repos {query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    full_output = output + "\n" + errors if errors else output
    yield OutputMessage(content=f"{full_output}")


async def download_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open("download.png", "wb") as f:
                    image = await f.read()
                    base64_image = encode_image(image)
                    yield OutputMessage(f"data:image/;base64,{base64_image}")
            else:
                yield OutputMessage(content="Failed to download image.")


async def download_website(url: str):
    url = "https://api.microlink.io"
    params = {"url": url, "pdf": True}
    response = requests.get(url, params)
    print(response.json())


async def use_terminal(commands: str):
    process = await asyncio.create_subprocess_shell(
        commands,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    full_output = output + "\n" + errors if errors else output
    yield OutputMessage(content=full_output)
