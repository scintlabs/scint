from rich.console import Console

from base.agents.assistant import Assistant
from base.observability.logging import logger
from base.processing.messages import Message
from base.persistence import LifeCycle

scint = Assistant()
console = Console()


def get_input():
    q = console.input(f" ❯ ")
    return q


async def run_cli():
    logger.info(f"Starting the Scint CLI.")

    while True:
        message_content = get_input()
        if not message_content.strip():
            continue

        message = Message(
            role="user", content=message_content, name="Tim", lifecycle=LifeCycle()
        )
        await scint.generate_message(message)
