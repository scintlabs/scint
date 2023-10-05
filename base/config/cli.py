import asyncio

from rich.console import Console

from base.config.logging import logger
from base.processing.handlers import message_handler

console = Console()


async def get_input():
    q = console.input(f" ❯ ")
    return q


async def run_cli():
    logger.info(f"Starting Scint CLI.")
    while True:
        message_content = await get_input()
        if not message_content.strip():
            continue
        message = {"role": "user", "content": message_content, "name": "Tim"}
        reply = await message_handler(message)
        console.print(f" ❯ {reply}")


asyncio.run(run_cli())
