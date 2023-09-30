from base.observability.logging import logger
from base.processing.messaging import (Message, deserialize_thread,
                                       serialize_response)
from base.providers.openai import chat_completion
from data.functions.functions import initialize_entity
from data.models.lifecycle import Lifecycle
from data.prompts.prompts import assistant as assistant_prompt


class Sentry:
    def __init__(self):
        self.name = "Sentry"
        self.lifecycle = Lifecycle()
        self.active = True
        self.messages = []
        self.functions = []
        self.system_prompt = assistant_prompt
        self.messages.append(self.system_prompt)
        self.functions.append(initialize_entity)

        logger.info(f"Initializing {self.name}.")
        logger.info(f"Initializing {self.functions}.")

    async def send_message(self, message: Message):
        try:
            self.messages.append(message)
            messages = deserialize_thread(self.messages)
            functions = self.functions
            response = await chat_completion(messages, functions)
            response_message = response["choices"][0].get("message")  # type: ignore
            serialized_response = serialize_response(response_message)
            self.messages.append(serialized_response)

            return serialized_response.content

        except Exception as e:
            logger.exception(f"{e}")
            raise
