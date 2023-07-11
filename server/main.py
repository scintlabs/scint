from core.assistant import Assistant
from core.definitions.assistants import keanu
from rich.console import Console

console = Console()
exit_commands = ["/quit"]
assistant = Assistant(keanu)

def input():
    q = console.input("❯  ")
    return q

def main():
    message = input()
    while message not in exit_commands:
        response = assistant.chat(message)
        console.print(f"❯ {message} \n")
        console.print(f"❯❯ {response} \n")
        message = input()

if __name__ == "__main__":
    main()
