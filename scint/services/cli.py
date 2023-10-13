import asyncio

from rich.console import Console

from scint.services.logging import logger
from scint.handlers.message import message_handler

console = Console()


async def get_input():
    q = console.input(f" ❯ ")
    return q


target = "scint"


async def run_cli():
    logger.info(f"Starting Scint CLI.")
    while True:
        content = await get_input()
        if not content.strip():
            continue
        message = {"role": "user", "content": content, "name": "Tim"}
        reply = await message_handler(target, message)
        console.print(f" ❯ {reply}")


asyncio.run(run_cli())
