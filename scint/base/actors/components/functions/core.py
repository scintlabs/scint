import asyncio
import aiohttp

from scint.base.models.messages import SystemMessage
from scint.base.models import encode_image
from scint.base.models.messages import Message


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
    yield Message(content=f"{full_output}")


async def download_image(image_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                with open("download.png", "wb") as f:
                    image = await response.read()
                    base64_image = encode_image(image)
                    yield SystemMessage(f"data:image/;base64,{base64_image}")
            else:
                yield SystemMessage(content="Failed to download image.")


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
    yield SystemMessage(content=full_output)
