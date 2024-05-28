import asyncio
import time

from scint.core.context import Context
from scint.data.serialize import dictorial, keyfob
from scint.modules.logging import log
from scint.core.composer import composer
from scint.core.threads import thread_manager


class ContextController:
    def __init__(self):
        log.info(f"Initializing Controller.")
        self.threads = thread_manager
        self.composer = composer
        self.contexts = []

    async def contextualize(self, message):
        log.info(f"Contextualizing message.")
        context = await self.get_context(message)
        context_composition = await self.build_params(context)
        async for response in context_composition.process():
            yield response

    async def get_context(self, message):
        log.info(f"Getting context.")
        if len(self.contexts) == 0:
            thread = self.threads.get_thread(message.embedding)
            new = Context(thread.name, thread.description, thread.messages)
            self.contexts.append(new)

        context = self.contexts[-1]
        context.messages.append(message)
        return context

    async def build_params(self, context):
        log.info(f"Building context parameters.")
        params = {}
        params["query"] = extract_context_query(context.messages)
        params["prompts"] = ["identity", "instructions", "modifier"]
        params["functions"] = "initial"
        params["people"] = ["Tim", "Ken"]
        composed = await self.composer.compose_context(context, params)
        return composed

    async def manage_lifecycles(self):
        while True:
            current_time = time.time()
            self.threads.manage_lifecycle_events(current_time)
            await asyncio.sleep(60)

    async def current_context(self):
        if len(self.contexts) > 0:
            active_context = {}
            for context in self.contexts:
                prompts = extract_context_query(context.prompts)
                messages = extract_context_query(context.messages)
                active_context[context.name] = {
                    "description": context.description,
                    "messages": prompts + messages,
                }
            return active_context


controller = ContextController()


def extract_context_query(messages):
    strings = []
    for message in messages:
        if keyfob(message, "content"):
            strings.append(keyfob(message, "content"))
        if dictorial(message, "classification.annotations"):
            strings.append(keyfob(message, "content"))

    if strings:
        return " ".join(strings)
