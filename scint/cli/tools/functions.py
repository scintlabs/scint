from __future__ import annotations

import asyncio
import aiohttp

from scint.lib.schema.records import Block
from scint.lib.schema.signals import Result


async def use_terminal(commands: str):
    """
    Executes shell commands asynchronously and yields the output and errors.
    commands: The shell commands to be executed.
    """
    process = await asyncio.create_subprocess_shell(
        commands,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    return Result(content=Block(content=str(output if output else str(errors))))


async def search_github(query: str):
    process = await asyncio.create_subprocess_shell(
        f"gh search repos {query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    return Block(content=errors) if errors else Block(content=output)


async def load_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open("download.png", "wb") as f:
                    image = await f.read()
                    return Block(content=image)
            else:
                return Block(content="Failed to download image.")


async def load_website(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.microlink.io",
            {"url": url, "pdf": True},
        ) as response:
            if response.status == 200:
                return Block(content=response.json())
