import ast
import inspect
import asyncio
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Union, get_args, get_origin

from src.models.blocks import Block
from src.models.messages import Message


def build_function(name: str):
    func = {}
    func["args"] = []
    func["kwonly_args"] = []
    func["defaults"] = []
    func["docstring"] = None
    func["body"] = []
    func["annotations"] = {}
    return func


def add_arg(func, name: str, /, anno=None, default=None):
    func.args.append(name)

    if anno:
        func.annotations[name] = anno

    if default is not None:
        func.defaults.append(default)

    return func


def set_body(func, body):
    if isinstance(body, str):
        body = ast.parse(body).body
    func.body.extend(body)
    return func


def set_docstring(func, docstring):
    func.docstring = docstring
    return func


def define_args(func, name: str):
    return ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(
                arg=arg,
                annotation=(
                    ast.Name(id=func.annotations[arg], ctx=ast.Load())
                    if arg in func.annotations
                    else None
                ),
            )
            for arg in func.args
        ],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[ast.Constant(value=d) for d in func.defaults],
    )


def define_body(func):
    body = []
    if func.docstring:
        body.append(ast.Expr(ast.Constant(value=func.docstring)))
    body.extend(func.body)


def build_definition(func, name, args, body):
    return ast.FunctionDef(
        name=name,
        args=args,
        body=body,
        decorator_list=[ast.Name(id=d, ctx=ast.Load()) for d in func.decorators],
        returns=None,
    )


def set_module(func, func_def):
    module = ast.Module(body=[func_def], type_ignores=[])
    ast.fix_missing_locations(module)
    return compile(module, "<ast>", "exec")


def set_namespace(func, code, name):
    namespace = {}
    exec(code, namespace)
    return namespace[name]


def optional_type(annotation: Any) -> bool:
    origin = get_origin(annotation)

    if origin is Union:
        args = get_args(annotation)
        if type(None) in args:
            return True
    return False


def parse_annotation(annotation: Any) -> Dict[str, Any]:
    origin = get_origin(annotation)
    args = get_args(annotation)

    if annotation == inspect.Parameter.empty:
        return {"type": "any"}

    if annotation in (str, int, bool, float):
        return {"type": annotation.__name__}

    if origin is Literal:
        values = list(args)
        return {"enum": values}

    if origin is list or origin is List:
        (item_type,) = args
        return {"type": "array", "items": parse_annotation(item_type)}

    if origin is dict or origin is Dict:
        key_type, value_type = args
        return {
            "type": "object",
            "properties": parse_annotation(value_type),
        }

    if origin is Union:
        models = []
        for arg in args:
            if arg is type(None):
                models.append({"type": "null"})
            else:
                models.append(parse_annotation(arg))
        return {"oneOf": models}

    if inspect.isclass(annotation) and issubclass(annotation, Enum):
        enum_values = [item.value for item in annotation]
        return {"type": "string", "enum": enum_values}

    return None


def parse_docstring(doc: str) -> Dict[str, str]:
    return {}


def generate_model(func: Callable) -> Dict:
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or ""
    desc = doc.split("\n")[0] if doc else ""
    param_desc = parse_docstring(doc)

    model = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    }

    for name, param in sig.parameters.items():
        param_model = parse_annotation(param.annotation) or {"type": "any"}

        if name in param_desc:
            param_model["description"] = param_desc[name]

        model["function"]["parameters"]["properties"][name] = param_model

        if param.default is inspect.Parameter.empty and not optional_type(
            param.annotation
        ):
            model["function"]["parameters"]["required"].append(name)
    return model


create_composition = {
    "type": "function",
    "function": {
        "name": "create_composition",
        "description": "Create a composition and pass it to the composer to create a new workflow or process. Use this function when the user requests complex, multi-step tasks.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "A short, simple composition name.",
                },
                "description": {
                    "type": "string",
                    "description": "Describe the intent of the composition.",
                },
            },
            "required": ["name", "description"],
            "additionalProperties": False,
        },
    },
}


load_process = {
    "type": "function",
    "function": {
        "name": "load_process",
        "description": "Load a process, workflow, or sequence and pass it to the Processor to accomplish a specific, multi-step task. Use this function when the user needs to accomplish a task that matches one of the processes listed.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the process to load.",
                    "enum": [],
                },
            },
            "required": ["name"],
            "additionalProperties": False,
        },
    },
}


async def exec_terminal_commands(commands: str):
    process = await asyncio.create_subprocess_shell(
        commands,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode().strip() if stdout else ""
    errors = stderr.decode().strip() if stderr else ""
    blocks = [Block(data=errors) if errors else Block(data=output)]
    return Message(blocks=blocks)
