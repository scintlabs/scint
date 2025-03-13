import asyncio

from scint.lib.schemas.signals import Block, Message, Result
from scint.lib.types.tools import Tools


class Develop(Tools):
    async def use_terminal_function(self, commands: str, *args, **kwargs):
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
        return Result(blocks=[Block(content=str(output if output else str(errors)))])

    async def search_github(self, query: str, *args, **kwargs):
        """
        Searches GitHub repositories using the GitHub CLI and returns the results.
        query: The search term to find repositories.
        """
        process = await asyncio.create_subprocess_shell(
            f"gh search repos {query}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() if stdout else ""
        errors = stderr.decode().strip() if stderr else ""
        return Message(content=errors) if errors else Message(content=output)
