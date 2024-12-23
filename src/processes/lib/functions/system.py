import asyncio

from src.network.models import Block, InputMessage


async def exec_term_cmd(commands: str):
    process = await asyncio.create_subprocess_shell(
        commands,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    blocks = [Block(data=errors) if errors else Block(data=output)]
    return InputMessage(blocks=blocks)
