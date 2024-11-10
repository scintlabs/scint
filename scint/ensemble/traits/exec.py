import asyncio

from scint.ensemble.traits.base import Trait
from scint.repository.models.message import Block, Message


class TerminalAccess(Trait):
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
        return Message(blocks=blocks)
