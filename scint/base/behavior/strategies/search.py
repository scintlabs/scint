import asyncio
import aiohttp

from ...components.containers import Container
from ...components.functions import Function
from ...components.prompts import Message
from ...utils import encode_image


search_github_repos = Function(
    name="search_github_repos",
    description="Searches GitHub repositories using the specified query and yields the search results.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query string.",
            }
        },
        "required": ["query"],
    },
)


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
                    yield Message(f"data:image/;base64,{base64_image}")
            else:
                yield Message(content="Failed to download image.")


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
    yield Message(content=full_output)
