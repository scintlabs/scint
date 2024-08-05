import inspect
import ast
from typing import AsyncGenerator, Callable, Dict, Any, List

from scint.base.components.prompts import Message
from ...requests import request_completion

AsyncGen = AsyncGenerator[Any][Any]


def get_function_name(func: Callable) -> str:
    return func.__name__


def get_function_description(func: Callable) -> str:
    return inspect.getdoc(func) or ""


def get_function_parameters(func: Callable) -> Dict[str, Any]:
    signature = inspect.signature(func)
    parameters = {}
    for name, param in signature.parameters.items():
        param_info = {
            "type": (
                str(param.annotation)
                if param.annotation != inspect.Parameter.empty
                else "Any"
            ),
            "default": (
                param.default if param.default != inspect.Parameter.empty else None
            ),
            "required": param.default == inspect.Parameter.empty,
        }
        parameters[name] = param_info
    return parameters


def get_function_source(func: Callable) -> Dict[str, str]:
    source_lines, _ = inspect.getsourcelines(func)
    source = "".join(source_lines)

    tree = ast.parse(source)
    function_def = tree.body[0]

    if isinstance(function_def, ast.AsyncFunctionDef):
        definition = f"async def {function_def.name}({ast.unparse(function_def.args)}):"
    else:
        definition = f"def {function_def.name}({ast.unparse(function_def.args)}):"

    body_lines = source_lines[1:]  # Skip the definition line
    body = "".join(line.strip() for line in body_lines)

    yields = ""
    for node in ast.walk(tree):
        if isinstance(node, ast.Yield):
            yields = ast.unparse(node)
            break

    return {"definition": definition, "body": body, "yields": yields}


def extract_function_metadata(func: Callable) -> Dict[str, Any]:
    return {
        "name": get_function_name(func),
        "description": get_function_description(func),
        "parameters": get_function_parameters(func),
        "source": get_function_source(func),
    }


def prepare_llm_input(func: Callable) -> Dict[str, Any]:
    metadata = extract_function_metadata(func)
    return {
        "name": metadata["name"],
        "type": "function",
        "description": metadata["description"],
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The function's name. Use a verbose name that clearly describes the function's purpose.",
                },
                "description": {
                    "type": "string",
                    "description": "A description of the function, explaining succinctly but in detail what the function does and when and how to use it.",
                },
                "parameters": {
                    "type": "object",
                    "description": "The function's parameters. Return an object containing key value pairs for each parameter. The key should be the parameter name, and the value should be an object containing keys and values for parameter type, parameter description, any default values, and whether the parameter is required.",
                },
                "source": {
                    "type": "object",
                    "properties": {
                        "definition": {
                            "type": "string",
                            "description": "The function's definition line, as written in the source. All system functions must be asynchronous generators.",
                        },
                        "body": {
                            "type": "string",
                            "description": "The main function body.",
                        },
                        "yields": {
                            "type": "string",
                            "description": "The yield statement, as it should appear in the source code. Remember that all return values must be within a SystemMessage pydantic class, assigned to the 'content' parameter.",
                        },
                    },
                },
            },
            "required": ["name", "description", "parameters", "source"],
        },
    }


# Example usage:
async def example_function(param1: int, param2: str = "default") -> AsyncGen:
    """
    This is an example function that does something.

    It takes two parameters and returns a list of strings.
    """
    result = []
    for i in range(param1):
        result.append(f"{param2} {i}")
    yield Message(content=result)


llm_input = prepare_llm_input(example_function)
print(llm_input)


async def generate_specification(description):
    yield Message()


def validate_metadata(self, func):
    for obj in self.metadata:
        if obj.get("name") == func.__name__:
            func.metadata = obj
    return func


async def generate_function(message):
    specification = await generate_specification(message)
    res = await request_completion([message])
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
        yield Message(content=f"{function.__name__} created successfully.")
    except Exception as e:
        print(f"Error generating function: {e}")
        yield Message(content=f"Error generating function: {e}")


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
        print(f"Error building function: {e}")

    func = eval(metadata["name"])
    return func
