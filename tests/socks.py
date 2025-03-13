import asyncio
import json
import threading
import queue

import websockets


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


# if __name__ == "__main__":
#     try:
#         asyncio.run(websocket_client())
#     except KeyboardInterrupt as k:
#         print(k)
#         print("exiting...")
#         exit()
