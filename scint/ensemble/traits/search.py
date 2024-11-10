import asyncio

from scint.ensemble.traits.base import Trait
from scint.repository.models.message import Block, Message


class SearchGithub(Trait):
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

        return Message(blocks=blocks)
