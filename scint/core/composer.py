from scint.services.search import search_controller
from scint.support.logging import log


class Composer:
    def __init__(self, context):
        self.search = search_controller
        self.context = context

    async def compose(self):
        log.info(f"Preparing context parameters.")
        try:
            params = {}
            params["query"] = await self.extract_context(self.context.messages)
            params["prompts"] = ["status", "identity", "instructions", "modifier"]
            params["functions"] = ["interact"]
            return await self._compose(self.context, params)
        except Exception as e:
            log.info(f"Error generating params: {e}")

    async def extract_context(self, messages):
        log.info(f"Extracting context.")
        try:
            blocks = []
            for i, message in enumerate(messages):
                if i < 5:
                    for block in message.content:
                        blocks.append(block.data)
            return "\n\n".join(blocks)
        except Exception as e:
            log.info(f"Error extracting context: {e}")

    async def compose_context(self, context, params):
        log.info(f"Building context.")
        query = params.get("query")
        prompt_args = params.get("prompts")
        function_args = params.get("functions")

        try:
            prompts = await self.get_prompts(query, prompt_args)
            funcs = await self.get_functions(query, function_args)
            if prompts:
                context.prompts.extend(prompts)
            if funcs:
                context.functions.refresh(funcs)
                context.function_choice = "auto"
            return context
        except Exception as e:
            log.error(f"Error composing context: {e}")
            return context

    async def get_prompts(self, query, args):
        log.info(f"Selecting prompts.")
        prompts = []
        try:
            for category in args:
                results = await self.search.results("prompts", query, category)
                for result in results:
                    prompts.append(result)
            return prompts
        except Exception as e:
            log.error(f"Error composing prompts: {e}")

    async def get_functions(self, query, args):
        log.info(f"Selecting functions.")
        functions = []
        try:
            for category in args:
                results = await self.search.results("functions", query, category)
                for result in results:
                    functions.append(result)
            return functions
        except Exception as e:
            log.error(f"Error composing functions: {e}")
