import asyncio

from typing import Dict, List

from core.data.db import insert_message
from core.definitions.functions import generate_code, google_search
from util.logging import logger

system_message: str = "You are Scint, a stateful, collaborative, intelligent assistant. You have access to a secure sandbox environment which you can use to evaluate Python code. You can also create files and directories in this environment to build more complex projects."


class MessageHandler:
    def __init__(self):
        """Message handler class."""
        logger.info(f"Calling message handler.")

        self.roles = ["system", "assistant", "user"]
        self.message_template = lambda message, role, name: {
            "content": f"{message}",
            "role": f"{role}",
            "name": f"{name}",
        }

    def format_message(self, user_message):
        """Format messages."""
        logger.info(f"Formatting message.")

        return self.message_template(user_message, self.roles[2], "Tim")

    async def build_manifest(self):
        """Package messages and functions."""
        logger.info(f"Building message package manifest.")

        messages: List[Dict[str, str]] = []
        functions: List[Dict[str, str]] = []
        sys_init = self.message_template(system_message, self.roles[0], "system")
        # env_data = await parse_env()
        # data = self.message_template("None", str(self.roles[1]), "environment")
        # messages.append(data)
        messages.append(sys_init)
        functions.append(google_search)
        functions.append(generate_code)

        return messages, functions

    def store_message(self, role, content, response_id):
        """Store the message in the database."""
        try:
            insert_message(role, content, response_id)
            logger.info(f"Stored {role} message in the database.")
        except Exception as e:
            logger.exception(f"Failed to store message: {e}")
