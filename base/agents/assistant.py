from base.observability.logging import logger
from base.processing.messaging import (Message, deserialize_thread,
                                       serialize_response)
from base.providers.openai import chat_completion
from data.functions.functions import initialize_entity
from data.models.lifecycle import Lifecycle
from data.prompts.prompts import assistant as assistant_prompt


class Assistant:
    def __init__(self):
        self.name = "Scint Assistant"
        self.lifecycle = Lifecycle()
        self.messages = []
        self.functions = []
        self.system_prompt = assistant_prompt
        self.messages.append(self.system_prompt)
        self.functions.append(initialize_entity.model_dump())

    async def initialize_context(self):
        logger.info(f"Initializing {self.name}.")

    async def emitter(self, event):
        logger.info(f"Emitting from {self.name}.")

    async def send_message(self, message: Message):
        logger.info(f"{self.name} is sending a message.")
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
