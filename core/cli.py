import subprocess
from rich.console import Console
from core.chat import chat
from util.logging import logger
from core.state import State
from core.observer import Observer

console = Console()
exit_commands = ["q!"]


def save_and_exit():
    console.print("Exiting.")


def get_input():
    q = console.input(f"❯ ")  # type: ignore
    return q


async def run_cli():
    state = State()
    observer = Observer()
    user_message = get_input()

    while user_message not in exit_commands:
        if user_message.startswith("cmd"):
            command = user_message[3:].strip()

            try:
                process = subprocess.Popen(
                    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                output, error = process.communicate()
                output_text = output.decode()
                error_text = error.decode()

                # if output_text:
                #     console.print(f"{output_text}\n")
                # elif error_text:
                #     console.print(f"{error_text}\n")
            except Exception as e:
                logger.exception(f"Error running command: {e}\n")

        else:
            try:
                response = await chat(user_message)  # type: ignore
                # console.print(f"❯❯ {response} \n")
            except Exception as e:
                logger.exception(f"Error communicating with the assistant: {e}\n")

        user_message = get_input()

    save_and_exit()
