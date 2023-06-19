from rich.console import Console
from cogiter.interfaces.keanu import system_init as keanu_init
from cogiter.interface import Interface

exit_commands = ["/quit"]


def input():
    console = Console()
    q = console.input("[orange]❯❯  [/]")
    return q


def nina():
    interface = Interface(nina)
    message = input()

    while message not in exit_commands:
        _ = interface.__call__(message)
        message = input("[orange]❯❯  [/]")


def keanu():
    interface = Interface(keanu_init)
    message = input()

    while message not in exit_commands:
        _ = interface.__call__(message)
        message = input()


if __name__ == "__main__":
    keanu()
