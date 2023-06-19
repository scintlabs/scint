from core.interface import Interface
from core.interfaces.keanu import system_init
from rich.console import Console

exit_commands = ["/quit"]


def input():
    console = Console()
    q = console.input("[bold red]❯❯  [/]")
    return q


def nina():
    interface = Interface(nina)
    message = input()

    while message not in exit_commands:
        _ = interface.__call__(message)
        message = Console.input("[bold red]❯❯  [/]")


def keanu():
    init = system_init
    interface = Interface(init)
    message = input()

    while message not in exit_commands:
        _ = interface.__call__(message)
        message = Console.input("[bold red]❯❯  [/]")


if __name__ == "__main__":
    keanu()





