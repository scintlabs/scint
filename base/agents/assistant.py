from base.processing.serialize import serialize_messages, deserialize_messages
from base.providers.openai import chat_completion
from base.processing.messages import Message
from base.observability.logging import logger
from base.persistence import LifeCycle
from config.prompts import assistant as assistant_prompt
from base.processing.functions import initialize_entity


class Assistant:
    def __init__(self):
        self.name = "Scint Assistant"
        self.lifecycle = LifeCycle()
        self.active = True
        self.messages = []
        self.functions = []
        self.system_prompt = assistant_prompt
        self.messages.append(self.system_prompt)

        logger.info(f"Initializing {self.name}.")

    async def generate_message(self, message: Message):
        try:
            self.messages.append(message)
            messages = deserialize_messages(self.messages)
            functions = self.functions
            response = await chat_completion(messages, functions)
            response_content = response["choices"][0]["message"].get("content")  # type: ignore
            serialized_response = serialize_messages(response_content)
            self.messages.append(serialized_response)

            return serialized_response.content

        except Exception as e:
            logger.exception(f"{e}")
            raise
