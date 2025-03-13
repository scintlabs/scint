from __future__ import annotations

import asyncio
import traceback

import rich
from rich.markdown import Markdown, Panel, box
from rich.prompt import Prompt

from src.schemas.system import System
from src.types.models import AgentMessage, UserMessage

system = System()

system.library.load()
system.load()


class Console:
    def __init__(self):
        self.boundary = system.regions[-1].get_boundary("default")
        self.console = rich.console.Console()
        self.errors = rich.console.Console(stderr=True)
        self.theme = {
            "user": "white",
            "assistant": "cyan",
            "error": "red",
        }

    async def start(self):
        while True:
            try:
                entry = Prompt.ask("\n")
                if entry.lower() == "q":
                    break

                await self.send(entry)
            except Exception as e:
                self.errors.print(f"[error]{str(e)}[/error]")
                self.errors.print(f"[error]Traceback: {traceback.format_exc()}[/error]")

    async def send(self, input: str):
        msg = UserMessage(content=input)
        self.boundary.update(msg)
        res = await self.boundary.invoke()
        return self.receive(res)

    def receive(self, message: AgentMessage):
        return self.console.print(
            Panel(
                Markdown("".join(b.content for b in message.content)),
                title="[assistant]Scint[/assistant]",
                border_style="white",
                padding=(1, 2),
                box=box.ROUNDED,
            )
        )


async def main():
    console = Console()
    await console.start()


if __name__ == "__main__":
    asyncio.run(main())
