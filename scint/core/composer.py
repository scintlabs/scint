from scint.core.models import Function, SystemMessage
from scint.data.serialize import keyfob
from scint.modules.search import search_controller
from scint.data.load import loader
from scint.modules.logging import log


class Composer:
    def __init__(self):
        self.library = loader.library
        self.prompts = self.library["prompts"]
        self.functions = self.library["functions"]
        self.people = self.library["people"]
        self.search = search_controller

    async def compose_context(self, context, params):
        log.info(f"Composing context.")
        try:
            prompts, funcs, people = await self.parse_context_params(params)
            if prompts:
                for prompt in prompts:
                    context.prompts.insert(prompt, prompt.category)
            if people:
                for person in people:
                    context.prompts.insert(person, "people")
            if funcs:
                context.functions.refresh(funcs)
                context.function_choice = "auto"
            return context
        except Exception as e:
            log.info(f"Error composing context: {e}")

    async def parse_context_params(self, params):
        log.info(f"Parsing context parameters.")
        try:
            prompts = await self.compose_prompts(
                keyfob(params, "query"),
                keyfob(params, "prompts"),
            )
            funcs = await self.compose_functions(
                keyfob(params, "query"),
                keyfob(params, "functions"),
            )
            people = await self.compose_people(
                keyfob(params, "query"),
                keyfob(params, "people"),
            )
            return prompts, funcs, people
        except Exception as e:
            log.info(f"Error parsing context params: {e}")

    async def compose_prompts(self, query, prompt_args):
        try:
            log.info(f"Selecting prompts.")
            if prompt_args:
                prompts = []
                for entry in prompt_args:
                    category = entry
                    results = await self.search.results("prompts", query, category)
                    prompt = results[0].get("content")
                    prompts.append(SystemMessage(content=prompt, category=category))
                return prompts
        except Exception as e:
            log.info(f"Error composing prompts: {e}")

    async def compose_functions(self, query, func_args):
        try:
            log.info(f"Selecting functions.")
            if func_args:
                functions = []
                results = await self.search.results("functions", query, func_args)
                if results and len(results) == 1:
                    self.compose_functions.append(Function(**results[0]))
                    self.function_choice = results[0].choice
                else:
                    for result in results:
                        functions.append(Function(**result))
                return functions
        except Exception as e:
            log.info(f"Error composing functions: {e}")

    async def compose_people(self, query, people_args):
        try:
            log.info(f"Selecting prompts.")
            if people_args:
                prompts = []
                for entry in people_args:
                    category = entry
                    results = await self.search.results("people", query)
                    prompt = results[0]
                    prompts.append(
                        SystemMessage(content=str(prompt), category=category)
                    )
                return prompts
        except Exception as e:
            log.info(f"Error composing prompts: {e}")


composer = Composer()
