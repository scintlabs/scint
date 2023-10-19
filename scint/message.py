import os
import uuid
from datetime import datetime
from typing import Dict, List

from scint.data.providers.openai import chat
from scint.logging import logger
from scint.worker import WorkerManager


worker_manager = WorkerManager()


class Message:
    def __init__(self, sender, recipient, message, route_to=None):
        logger.info(f"Created message: {message}.")

        self.id = Message._generate_id()
        self.date: datetime = datetime.now()
        self.sender: str = sender
        self.recipient: str = recipient
        self.message: Dict[str, str] = message
        self.keywords: List[str] = []
        self.route_to: str | None = route_to

    @staticmethod
    def _generate_id():
        return str(uuid.uuid4())


class MessageManager:
    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def get_messages_for_recipient(self, recipient: str) -> List[Message]:
        return [msg for msg in self.messages if msg.recipient == recipient]

    def clear_messages(self):
        self.messages.clear()

    def get_last_n_messages_for_recipient(
        self, recipient: str, n: int
    ) -> List[Message]:
        return [msg for msg in reversed(self.messages) if msg.recipient == recipient][
            :n
        ]


message_manager = MessageManager()


async def message_handler(worker_name, message_content):
    logger.info(f"Initialized message handler with {message_content}")
    destination_worker = worker_manager.get_worker(worker_name)

    if not destination_worker:
        logger.error(f"Worker {worker_name} not found")
        return

    message = Message(
        sender="user",
        recipient=worker_name,
        message=message_content,
    )
    message_manager.add_message(message)

    last_three_messages = message_manager.get_last_n_messages_for_recipient(
        worker_name, 6
    )
    for msg in last_three_messages:
        destination_worker.messages.append(msg.message)

    try:
        state = await destination_worker.state()
        logger.info(f"{state}")
        res = await chat(**state)
        res_message = res["choices"][0].get("message")  # type: ignore
        res_func = res["choices"][0].get("function_call")  # type: ignore

        if res_message is not None:
            role = res_message.get("role")
            content = res_message.get("content")

            reply: dict[str, str] = {
                "role": role,
                "content": content,
                "name": worker_name,
            }

            reply_message = Message(
                sender=worker_name,
                recipient="user",
                message=reply,
            )

            message_manager.add_message(reply_message)
            return reply["content"]

        if res_func is not None:
            await func_handler(res_func)

    except Exception as e:
        logger.error(f"Error during message handling: {e}")
        raise


async def func_handler(function_call):
    pass


def temporality() -> dict[str, str]:
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%m")

    return {
        "role": "system",
        "content": f"The following message was sent at {time} on {date}.",
        "name": "ScintSystem",
    }
