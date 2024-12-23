import asyncio
import sys

from rich.box import ROUNDED
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme
from rich.prompt import Prompt

from src.base.models import Block, InputMessage
from src.network.interfaces import Struct


console_theme = Theme(
    {"user": "cyan", "assistant": "green", "system": "yellow", "error": "red"}
)


class Scint:
    def __init__(self):
        self.structure = Struct()
        self.console = Console(theme=console_theme)
        self.errors = Console(stderr=True)

    async def get_response(self, user_input: str):
        try:
            message = InputMessage(content=[Block(data=user_input)])
            res = await self.structure.input(message)
            return res if res else None
        except Exception as e:
            self.errors.print(f"[red]Error in get_response: {str(e)}[/red]")
            raise

    async def input(self):
        while True:
            try:
                entry = Prompt.ask("\n")
                if entry.lower() == ":q":
                    self.console.print("[system][/system]")
                    break

                with self.console.status("[white]", spinner="dots12", speed=0.75):
                    res = await self.get_response(entry)

                    if res:
                        response_text = "".join([b.data for b in res.content])
                        self.console.print(
                            Panel(
                                Markdown(response_text),
                                title="[assistant]Scint[/assistant]",
                                border_style="white",
                                padding=(1, 2),
                                box=ROUNDED,
                            )
                        )
            except Exception as e:
                self.errors.print(f"[red]{str(e)}[/red]")
                print(f"{str(e)}", file=sys.stderr)


async def main():
    try:
        scint = Scint()
        await scint.input()
    except KeyboardInterrupt:
        scint.console.print("\n[error]Chat session terminated.[/error]")
    except Exception as e:
        scint.console.print(f"\n[error]An error occurred: {str(e)}[/error]")


if __name__ == "__main__":
    asyncio.run(main())
