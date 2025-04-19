from __future__ import annotations

import asyncio
import traceback

import rich
from attrs import define
from rich.markdown import Markdown, Panel, box
from rich.prompt import Prompt

from src.core.broadcast import Broadcast
from src.core.continuity import Continuity
from src.core.types.ensemble import Ensemble
from src.core.types.signals import Input, Output


@define
class Console:
    broadcast: Broadcast
    console = rich.console.Console()
    errors = rich.console.Console(stderr=True)
    theme = {"user": "white", "assistant": "cyan", "error": "red"}

    async def start(self):
        while True:
            try:
                entry = Prompt.ask("\n")
                if entry.lower() == "q":
                    break
                async for res in self.send(entry):
                    await self.receive(res)
            except Exception as e:
                self.errors.print(f"[error]{str(e)}[/error]")
                self.errors.print(f"[error]{traceback.format_exc()}[/error]")

    async def send(self, input: str):
        msg = Input(content=input)
        async for res in self.broadcast.input(msg):
            yield res

    async def receive(self, output: Output):
        self.console.print(
            Panel(
                Markdown(output.content),
                title="[assistant]Scint[/assistant]",
                border_style="white",
                padding=(1, 2),
                box=box.ROUNDED,
            )
        )


async def main():
    persona = Ensemble("Persona")
    continuity = Continuity()
    continuity.register(persona)
    console = Console(continuity.broadcast)
    await console.start()


if __name__ == "__main__":
    asyncio.run(main())
