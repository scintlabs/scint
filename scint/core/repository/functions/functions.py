import asyncio
import inspect
import json
import ast
import re
from typing import Any, Callable, Dict

from scint.core.primitives.block import Block
from scint.core.primitives.messages import OutputMessage


def update_function(self, function_name: str, function: Callable):
    if function_name in self.functions:
        self.functions[function_name]["function"] = function
        task = asyncio.create_task(self._build_function_model(function))
        self.functions[function_name]["task"] = task
    else:
        raise ValueError(f"Function '{function_name}' does not exist in the store.")


async def get_function_model(self, function_name: str):
    if function_name in self.functions:
        if self.functions[function_name]["model"] is None:
            await self.functions[function_name]["task"]
        return self.functions[function_name]["model"]
    else:
        raise ValueError(f"Function '{function_name}' does not exist in the store.")


async def build_function_model(self, function: Callable):
    def _parse_source(func):
        source_lines, _ = inspect.getsourcelines(func)
        source = "".join(source_lines)
        ast.parse(source)
        final = "".join(line for line in source_lines)
        return f"{final}"

    def _clean_and_parse_response(response: str) -> Dict[str, Any]:
        cleaned_response = re.sub(
            r"```(?:json)?\s*([\s\S]*?)\s*```", r"\1", response.strip()
        )

        try:
            parsed_response = json.loads(cleaned_response)

            if not isinstance(parsed_response, dict):
                raise ValueError("Parsed response is not a dictionary")

            return parsed_response
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse response as JSON: {e}")

    # source = _parse_source(function)
    # prompt = build_func_blocks
    # message = f"{str(prompt)}\n{source}"
    # response = await completion(message)

    # try:
    # model = _clean_and_parse_response(response)
    # except ValueError as e:
    #     raise ValueError(
    #         f"Invalid model response for function '{function.__name__}': {e}"
    #     )

    # self.functions[function.__name__]["model"] = model
    # await self._save_model_to_file(function.__name__, model)
    # return model


async def call_function(self, function_name: str, *args, **kwargs):
    if function_name in self.functions:
        function = self.functions[function_name]["function"]
        return await function(*args, **kwargs)
    else:
        raise ValueError(f"Function '{function_name}' does not exist in the store.")


async def search_github_repos(query: str):
    process = await asyncio.create_subprocess_shell(
        f"gh search repos {query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    full_output = [
        Block(data=output) + Block(data=errors) if errors else Block(data=output)
    ]
    yield OutputMessage(body=full_output)


async def use_terminal(commands: str):
    process = await asyncio.create_subprocess_shell(
        commands,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    full_output = [
        Block(data=output) + Block(data=errors) if errors else Block(data=output)
    ]
    yield OutputMessage(body=full_output)
