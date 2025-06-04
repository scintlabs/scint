from __future__ import annotations

import asyncio

import rich
from attrs import define
from rich.markdown import Markdown, Panel, box
from rich.prompt import Prompt

from src.model.records import Message


@define
class Console:
    console: rich.console.Console = rich.console.Console()
    errors: rich.console.Console = rich.console.Console(stderr=True)
    theme: dict = {"user": "white", "assistant": "cyan", "error": "red"}

    async def start(self):
        while True:
            try:
                entry = await asyncio.to_thread(Prompt.ask, "\n")
                if entry.lower() == "q":
                    break
                msg = Message.create(name="console", content=entry)
                await self.input(msg)
            except Exception as e:
                self.errors.print(f"[error]{e}[/error]")
                self.errors.print_exception()

    async def input(self, msg: Message):
        res = await self.broker.ask(msg)
        await self.output(res)

    async def output(self, message: Message):
        self.console.print(
            Panel(
                Markdown("".join(c for c in message.content)),
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
