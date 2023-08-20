import subprocess, asyncio
from rich.console import Console
from core.chat import chat

console = Console()

exit_commands = ["quit"]


def get_input():
    q = console.input("\n❯ ")
    return q


def save_and_exit():
    console.print("Exiting.")


async def cli():
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

                if output_text:
                    console.print(f"\n{output_text}\n")
                elif error_text:
                    console.print(f"\n{error_text}\n")
            except Exception as e:
                console.print(f"Error executing command: {e}")

        else:
            try:
                response = await chat(user_message)
                console.print(f"\n❯❯ {response} \n")
            except Exception as e:
                console.print(f"Error communicating with OpenAI: {e}")

        user_message = get_input()

    save_and_exit()


if __name__ == "__main__":
    asyncio.run(cli())
