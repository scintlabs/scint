import asyncio
import aiohttp
import requests

from scint.framework.models import Block, BlockEnum
from scint.framework.components.component import Component
from scint.framework.models.messages import OutputMessage
from scint.framework.utils.helpers import encode_image


class exec_terminal_commands(Component):
    async def exec_terminal_commands(commands: str):
        process = await asyncio.create_subprocess_shell(
            commands,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() if stdout else ""
        errors = stderr.decode().strip() if stderr else ""
        blocks = [Block(data=errors) if errors else Block(data=output)]
        return OutputMessage(blocks=blocks)


class interactive_session(Component):
    Component.interactive_session.state.metadata.description = {
        "description": f"This function starts an interaction session with {Component.user} creates a the workflow-creation state, which allows me to interactively define and outline a task or activity with the user."
    }
    Component.interactive_session.state.metadata.parameters = {
        "type": "object",
        "properties": {
            "new_workflow": {
                "type": "boolean",
                "description": "Return true to transition to the interactive outline state.",
            }
        },
        "required": ["commands"],
        "additionalProperties": False,
    }


async def search_github_repos(query: str):
    process = await asyncio.create_subprocess_shell(
        f"gh search repos {query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    blocks = [Block(data=errors) if errors else Block(data=output)]
    return OutputMessage(blocks=blocks)


async def download_image(url: str):
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


async def download_website(url: str):
    url = "https://api.microlink.io"
    params = {"url": url, "pdf": True}
    response = requests.get(url, params)
    print(response.json())
    blocks = [Block(data=str(response.json()))]
    return OutputMessage(blocks=blocks)


async def use_terminal(commands: str):
    process = await asyncio.create_subprocess_shell(
        commands,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    blocks = [Block(data=errors) if errors else Block(data=output)]
    return OutputMessage(blocks=blocks)
