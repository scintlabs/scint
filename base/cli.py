import subprocess

from rich.console import Console

from base.handlers.message import chat
from base.state import StateManager
from util.logging import logger

console = Console()
exit_commands = ["/quit"]


def save_and_exit():
    console.print("Quitting.")


def get_input():
    q = console.input(f" ❯ ")  # type: ignore
    return q


async def run_cli():
    """Message handler class."""
    logger.info(f"Starting CLI.")
    state = StateManager()
    user_message = get_input()

    while user_message not in exit_commands:
        if user_message.startswith("/cmd"):
            command = user_message[4:].strip()

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

        elif user_message.startswith("/msg"):
            try:
                await chat(user_message)  # type: ignore
            except Exception as e:
                logger.exception(f"Error communicating with the assistant: {e}\n")

        user_message = get_input()

    save_and_exit()
