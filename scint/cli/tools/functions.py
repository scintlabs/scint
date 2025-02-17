from __future__ import annotations

import asyncio
import aiohttp

from scint.api.models import (
    Block,
    BlockType,
    FuncResult,
    Response,
    Tool,
    Parameter,
    Parameters,
)
from scint.support.utils import encode_image


async def use_terminal(commands: str):
    process = await asyncio.create_subprocess_shell(
        commands,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    return FuncResult(content=[Block(data=str(output if output else str(errors)))])


use_terminal.model = Tool(
    name="use_terminal",
    description="Executes shell commands asynchronously and yields the output and errors.",
    parameters=Parameters(
        properties=[
            Parameter(
                name="commands",
                type="string",
                description="The shell commands to be executed.",
            )
        ]
    ),
)


async def search_github(tool, query: str):
    process = await asyncio.create_subprocess_shell(
        f"gh search repos {query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    blocks = [Block(data=errors) if errors else Block(data=output)]
    return FuncResult(blocks=blocks)


async def load_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open("download.png", "wb") as f:
                    image = await f.read()
                    base64_image = encode_image(image)
                    return Response(
                        blocks=[Block(type=BlockType.IMAGE, data=base64_image)]
                    )

            else:
                return Response(
                    blocks=[
                        Block(type=BlockType.TEXT, data="Failed to download image.")
                    ]
                )


async def load_website(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.microlink.io",
            {"url": url, "pdf": True},
        ) as response:
            if response.status == 200:
                blocks = [Block(data=str(response.json()))]
                return Response(blocks=blocks)


tools = []
