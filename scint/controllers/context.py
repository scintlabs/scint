from scint.controllers.search import search_controller
from scint.controllers.storage import storage_controller
from scint.objects.context import App
from scint.objects.prompts import PromptLibrary
from scint.support.types import ContextData, Function, Message, SystemMessage
from scint.support.logging import log


class ContextController:
    def __init__(self):
        self.search = search_controller
        self.storage = storage_controller
        self.context = [App()]
        self.build_context(self.context[0])

    async def process(self, message: Message):
        try:
            log.info(f"Processing message.")
            prompt = self.search.results("prompts", message.content)
            prompt_message = SystemMessage(content=str(prompt[0].get("content")))
            functions = self.search.results("functions", message.content)
            func_list = [Function(**function) for function in functions]
            root_context = self.context[0]
            root_context.prompts.set_prompt("modifier", prompt_message)
            root_context.functions.refresh(func_list)
            async for response in root_context.process(message):
                yield response
        except Exception as e:
            log.error(f"Error processing message: {e}")

    def add_context(self, context):
        log.info(f"Adding {context.name} to global context.")
        self.context.append(context)
        self.build_context(context)

    def build_context(self, context):
        log.info(f"Building {context.name} context.")
        promptlib = PromptLibrary()
        ctx = self.get_context(context)
        ctx.prompts.set_prompt("status")
        for prompt in promptlib:
            if prompt.get("name") == "instructions":
                instr = SystemMessage(content=str(prompt.get("content")))
                ctx.prompts.set_prompt("instructions", instr)
            if prompt.get("name") == "identity":
                ident = SystemMessage(content=str(prompt.get("content")))
                ctx.prompts.set_prompt("identity", ident)
        return ctx

    def get_context(self, context):
        return next((c for c in self.context if c.name == context.name), None)

    def get_global_context(self):
        return ContextData(**self.context.metadata)


context_controller = ContextController()
