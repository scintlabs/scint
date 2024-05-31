from scint.core.context import Context
from scint.core.composers import context_composer
from scint.core.structures import Thread
from scint.data.serialize import dictorial, keyfob
from scint.modules.logging import log


class ContextController:
    def __init__(self):
        log.info(f"Initializing Controller.")
        self.composer = context_composer
        self.threads = Thread()
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
            new_context = Context()
            thread = self.threads.find_struct(message.embedding)
            thread.allow_context(new_context)
            self.contexts.append(new_context)
        context = self.contexts[-1]
        context.messages.append(message)
        return context

    async def build_params(self, context):
        log.info(f"Building context parameters.")
        params = {}
        params["query"] = self.extract_context(context.messages)
        params["prompts"] = ["identity", "instructions", "modifier"]
        params["functions"] = "initial"
        params["people"] = ["Tim", "Ken"]
        composed = await self.composer.compose_context(context, params)
        return composed

    def extract_context(self, messages, depth=3):
        strings = []
        for message in messages:
            if keyfob(message, "content"):
                strings.append(keyfob(message, "content"))
            if dictorial(message, "classification.annotations"):
                strings.append(keyfob(message, "content"))

        if strings:
            return " ".join(strings)


controller = ContextController()
