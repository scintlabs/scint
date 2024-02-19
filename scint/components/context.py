import uuid
from typing import List

import injector
from pydantic import BaseModel

from scint.components.models import Message, SystemPrompt
from scint.utils.logger import log


class Context(BaseModel):
    name: str
    messages: List[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def model_dump(self):
        return [
            message.model_dump(include=["role", "content"]) for message in self.messages
        ]


class IContextProvider:
    async def register(self, agent_name: str, description: str) -> Context:
        pass


class ContextProvider(IContextProvider):
    @injector.inject
    def __init__(self):
        self.contexts: List[Context] = []

    def register(self, name: str, description: str):
        prompt = SystemPrompt(
            content=str(description), sender="System", receiver="System"
        )
        process_context = Context(name=name)
        process_context.messages.append(prompt)
        self.contexts.append(process_context)

        return self.get_context_instance(name)

    def get_context_instance(self, name: str) -> List[Message]:
        for context_instance in self.contexts:
            if context_instance.name == name:
                return context_instance


class ContextModule(injector.Module):
    @injector.provider
    def context_provider(self) -> IContextProvider:
        return ContextProvider()

    def configure(self, binder: injector.Binder) -> None:
        binder.bind(IContextProvider, to=ContextProvider)
