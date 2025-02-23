from __future__ import annotations

import asyncio
import json
import threading
import queue
import websockets
import traceback

import rich
from rich.markdown import Markdown, Panel, box
from rich.prompt import Prompt

from scint.lib.schemas.signals import Message, Response
from scint.lib.types import Struct, Trait
from scint.lib.types import Interface, Processor


class Interfacable(Trait):
    async def start(self, entity: Interface):
        while True:
            try:
                entry = Prompt.ask("\n")
                if entry.lower() == "q":
                    break

                await self.send(entity, entry)
            except Exception as e:
                self.errors.print(f"[error]{str(e)}[/error]")
                self.errors.print(f"[error]Traceback: {traceback.format_exc()}[/error]")

    async def send(self, entity: Interface, input: str):
        entity.context.update(Message(content=input))
        res = await entity.process()
        return self.receive(res)

    def receive(self, res: Response):
        return self.console.print(
            Panel(
                Markdown(res.content),
                title="[assistant]Scint[/assistant]",
                border_style="white",
                padding=(1, 2),
                box=box.ROUNDED,
            )
        )


class Console(Struct):
    interpreter = Processor()
    console = rich.console.Console()
    errors = rich.console.Console(stderr=True)
    theme = {
        "user": "white",
        "assistant": "cyan",
        "error": "red",
    }


def format_message(message):
    return json.dumps({"body": [{"type": "text", "schema": message}]})


def input_thread(input_queue):
    while True:
        message = input(" ❯ ")
        input_queue.put(message)


async def websocket_client():
    uri = "ws://localhost:8000/ws"
    input_queue = queue.Queue()
    threading.Thread(target=input_thread, args=(input_queue,), daemon=True).start()

    async with websockets.connect(uri) as websocket:
        while True:
            try:
                try:
                    message = input_queue.get_nowait()
                    if message.lower() == "quit":
                        break
                    await websocket.send(format_message(message))
                except queue.Empty:
                    pass

                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                    data = json.loads(message)
                    blocks = data.get("blocks")
                    for block in blocks:
                        print(block.get("schema"))

                except asyncio.TimeoutError:
                    pass
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed, reconnecting.")
                return await websocket_client()
            except Exception as e:
                print(e)
                break


if __name__ == "__main__":
    try:
        asyncio.run(websocket_client())
    except KeyboardInterrupt as k:
        print(k)
        print(" exiting...")
        exit()
