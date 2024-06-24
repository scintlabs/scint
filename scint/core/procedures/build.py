import importlib
import types
import uuid

from scint.intelligence.requests import completion
from scint.support.logging import log
from scint.support.types import Dict, List
from scint.settings.core import functions as functions_metadata
from scint.settings.intelligence import intelligence_config
from scint.messaging import SystemMessage, Function
from scint.support.utils import dictorial


def validate_metadata(self, func):
    for obj in self.metadata:
        if obj.get("name") == func.__name__:
            func.metadata = obj
    return func


async def generate_specification(description):
    yield SystemMessage()


async def generate_function(message):
    specification = await generate_specification(message)
    res = await completion([message])
    name = res["name"]
    desc = res["description"]
    params = res["params"]
    definition = res["source"]["definition"]
    body = res["source"]["body"]
    yields = res["source"]["yields"]
    metadata = {"name": name, "description": desc, "parameters": params}
    source = "\n".join([definition, body, yields])

    try:
        function = function_factory(source, metadata)
        yield SystemMessage(content=f"{function.__name__} created successfully.")
    except Exception as e:
        log.error(f"Error generating function: {e}")
        yield SystemMessage(content=f"Error generating function: {e}")


def function_factory(source, metadata):
    params = [f"{n}: {d['type']}" for n, d in metadata["parameters"].items()]
    header = f"async def {metadata['name']}({", ".join(params)}) -> SystemMessage:"
    assignment = f"    {metadata['name']}.metadata = {metadata}"
    body = f"    {source['body']}"
    yields = f"    yield SystemMessage(content={source['yields']})"

    try:
        full_function_code = "\n".join([header, assignment, body, yields])
        exec(full_function_code, globals())
    except Exception as e:
        log.error(f"Error building function: {e}")

    func = eval(metadata["name"])
    return func
