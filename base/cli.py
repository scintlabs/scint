import subprocess

from rich.console import Console

from base.definitions.types import Message
from conf.base import USER
from base.chat import send_message
from base.state import StateManager
from util.logging import logger

console = Console()
exit_commands = ["/quit"]


def save_and_exit():
    console.print("Quitting.")


def get_input():
    q = console.input(f" ❯ ")
    return q


async def run_cli():
    logger.info(f"Starting CLI.")
    message_content: str = get_input()

    while message_content not in exit_commands:
        if message_content.startswith("/cmd"):
            command = message_content[4:].strip()

            try:
                process = subprocess.Popen(
                    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                output, error = process.communicate()
                output_text = output.decode()
                error_text = error.decode()

                if output_text:
                    console.print(f"{output_text}\n")
                elif error_text:
                    console.print(f"{error_text}\n")

            except Exception as e:
                logger.exception(f"Error running command: {e}\n")

        elif message_content.startswith("/msg"):
            message_string = message_content[4:].strip()
            try:
                message = Message(author=USER, content=message_content)
                await send_message(message)
            except Exception as e:
                logger.exception(f"Error communicating with the assistant: {e}\n")

        message_content = get_input()

    save_and_exit()
