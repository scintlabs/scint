# from __future__ import annotations

# import asyncio

# import rich
# from attrs import define
# from rich.markdown import Markdown, Panel, box
# from rich.prompt import Prompt

# from src.base.records import Message
# from src.base.broker import Broker
# from src.svc.config import MEILI_CLIENT, REDIS_CLIENT
# from src.svc.indexes import Indexes


# @define
# class Console:
#     broker: Broker
#     console: rich.console.Console = rich.console.Console()
#     errors: rich.console.Console = rich.console.Console(stderr=True)
#     theme: dict = {"user": "white", "assistant": "cyan", "error": "red"}

#     def __attrs_post_init__(self):
#         self.broker.register_interface(self.output)

#     async def start(self):
#         while True:
#             try:
#                 entry = await asyncio.to_thread(Prompt.ask, "\n")
#                 if entry.lower() == "q":
#                     break
#                 await self.input(Message(content=[entry]))
#             except Exception as e:
#                 self.errors.print(f"[error]{e}[/error]")
#                 self.errors.print_exception()

#     async def input(self, message: Message):
#         await self.broker.input(message)

#     async def output(self, message: Message):
#         self.console.print(
#             Panel(
#                 Markdown("".join(c for c in message.content)),
#                 title="[assistant]Scint[/assistant]",
#                 border_style="white",
#                 padding=(1, 2),
#                 box=box.ROUNDED,
#             )
#         )


# async def main():
#     indexes = Indexes(MEILI_CLIENT)
#     continuity = Continuity(indexes=indexes)
#     broker = Broker(client=REDIS_CLIENT, continuity=continuity)
#     console = Console(broker=broker)
#     await console.start()


# if __name__ == "__main__":
#     asyncio.run(main())
