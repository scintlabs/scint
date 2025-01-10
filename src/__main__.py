import asyncio

from rich.console import Console, Theme
from rich.markdown import Markdown, Panel, box
from rich.prompt import Prompt

from src.core.controller import Controller
from src.models.blocks import Block
from src.models.messages import Message


console_theme = Theme({"user": "white", "assistant": "cyan", "error": "red"})


class Scint:
    def __init__(self):
        self.controller = Controller()
        self.console = Console(theme=console_theme)
        self.errors = Console(stderr=True)

    async def start(self):
        while True:
            entry = Prompt.ask("\n")
            if entry.lower() == "q":
                break
            try:
                with self.console.status("[white]", spinner="dots12", speed=0.75):
                    res = await self.input(Message(content=[Block(data=entry)]))
                    if res:
                        await self.output(res)
            except Exception as e:
                self.errors.print(f"[red]{str(e)}[/red]")

    async def input(self, entry: str):
        return await self.controller.input(entry)

    async def output(self, message: Message):
        content = "".join([b.data for b in message.content])
        self.console.print(
            Panel(
                Markdown(content),
                title="[assistant]Scint[/assistant]",
                border_style="white",
                padding=(1, 2),
                box=box.ROUNDED,
            )
        )


async def main():
    try:
        scint = Scint()
        await scint.start()
    except KeyboardInterrupt:
        scint.console.print("\n[error]Chat session terminated.[/error]")
    except Exception as e:
        scint.console.print(f"\n[error]An error occurred: {str(e)}[/error]")


if __name__ == "__main__":
    asyncio.run(main())
