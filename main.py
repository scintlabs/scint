import sys
import signal
import subprocess
import assistant
from rich.console import Console


console = Console()
exit_commands = ["/quit"]
keanu = "keanu"
assistant = assistant.Assistant(keanu)


def input():
    q = console.input("❯ ")
    return q


def save_and_exit(signal, frame):
    print("Saving the assistant's state.")
    assistant.save()
    sys.exit(0)


signal.signal(signal.SIGINT, save_and_exit)
signal.signal(signal.SIGTERM, save_and_exit)


def main():
    message = input()
    while message not in exit_commands:
        if message.startswith("/cmd"):
            command = message[5:]
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output, error = process.communicate()
            output_text = output.decode()
            error_text = error.decode()
            if output_text:
                console.print(f"\n{output_text}\n")
                response = assistant.chat(output_text)
                pass
            elif error_text:
                console.print(f"\n{error_text}\n")
                response = assistant.chat(output_text)
                pass
        response = assistant.chat(message)
        console.print(f"\n❯❯ {response} \n")
        message = input()


if __name__ == "__main__":
    main()
