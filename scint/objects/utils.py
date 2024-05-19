import ast
import inspect
import json
import re

import numpy as np

from scint.support.logging import log


def function_metadata(function_name):
    """
    """
    with open(f"scint/data/functions.json", "r") as f:
        functions = json.load(f)
        for function in functions:
            if function["name"] == function_name:
                return function


def attr_from_source(source, attribute_name):
    """
    """
    pattern = re.compile(
        rf"{attribute_name}\s*=\s*({{(?:[^{{}}]*|{{[^{{}}]*}})*}}|\".*?\")", re.DOTALL
    )
    match = pattern.search(source)

    if match:
        value = match.group(1)
        if value.startswith("{"):
            return ast.literal_eval(value)
        else:
            return value.strip('"')
    return None


def parse_function(function):
    """
    """
    source = inspect.getsource(function)
    description = attr_from_source(source, "description")
    props = attr_from_source(source, "props")
    if props and description:
        return True
    return False


def parse_docstring(docstring, *args):
    """
    """
    return docstring.strip()


instancelist = lambda l, t: all(isinstance(i, t) for i in l)
attrlist = lambda l, t: all(hasattr(i, t) for i in l)


async def build_props(self):
    """
    """
    description = None
    props = {}
    if self.modules:
        for module in self.modules:
            description += f"{module.name}: {module.description}\n\n"

        props["module"] = {
            "type": "string",
            "description": "Select an available module to process the request.",
            "enum": [module.name for module in self.modules],
        }
    if self.relays:
        for relay in self.relays:
            description += f"{relay.name}: {relay.description}\n\n"
        props["relay"] = {
            "type": "string",
            "description": "Select an available relay to process the request.",
            "enum": [relay.name for relay in self.relays],
        }

    return props


def find_functions():
    """
    """
    function_info = []
    for name, obj in globals().items():
        if inspect.isfunction(obj):

            file = inspect.getsourcefile(obj)
            lines, start = inspect.getsourcelines(obj)
            end = start + len(lines) - 1
            source = "".join(lines)
            log.info(
                {
                    "function_name": name,
                    "source_file": file,
                    "lines": [start, end],
                    "source": [source],
                }
            )

    return function_info


def parse_function(function):
    """
    """
    source = inspect.getsource(function)
    description = attr_from_source(source, "description")
    props = attr_from_source(source, "props")
    if props and description:
        return True
    return False


def cosine_similarity(a, b):
    """
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
