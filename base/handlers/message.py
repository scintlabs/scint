from typing import Dict, List

from util.logging import logger
from base.definitions.types import Message
from base.definitions.functions import LOCATOR, PROCESSOR, TRANSFORMER
from base.definitions.prompts import SYSTEM_MESSAGES


class MessageHandler:
    def __init__(self):
        logger.info(f"Message handler initialized.")

    def format_message(self, message: Message) -> Dict[str, str]:
        formatted_message = {
            "role": message.author.role.value,
            "content": message.content,
            "name": message.author.name,
        }

        return formatted_message

    async def build_manifest(self, message: Message):
        logger.info(f"Building manifest.")

        messages: List[Dict[str, str]] = []
        functions: List[Dict[str, str]] = []

        formatted_message = self.format_message(message)

        messages.append(formatted_message)
        functions.append(LOCATOR)

        return messages, functions

    # async def env_data(self):
    #     dirs = await base.processor.parse_dir()
    #     files = await base.processor.parse_files()
    #     data = str(dirs) + str(files)
    #     return env_message

    # def store_message(self, role, content, response_id):
    #     try:
    #         base.data.db.insert_message(role, content, response_id)
    #         logger.info(f"Stored {role} message in the database.")
    #     except Exception as e:
    #         logger.exception(f"Failed to store message: {e}")
