import inspect
from typing import Any, get_args, get_origin, Callable, Dict, List, Literal, Union
from enum import Enum


def type_optional(annotation: Any) -> bool:
    origin = get_origin(annotation)
    if origin is Union:
        args = get_args(annotation)
        if type(None) in args:
            return True
    return False


def from_annotation(annotation: Any) -> Dict[str, Any]:
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
        # Python 3.9+ might use list, older might use List
        (item_type,) = args
        return {"type": "array", "items": from_annotation(item_type)}

    if origin is dict or origin is Dict:
        key_type, value_type = args
        return {
            "type": "object",
            "properties": from_annotation(value_type),
        }

    if origin is Union:
        schemas = []
        for arg in args:
            if arg is type(None):
                schemas.append({"type": "null"})
            else:
                schemas.append(from_annotation(arg))
        return {"oneOf": schemas}

    if inspect.isclass(annotation) and issubclass(annotation, Enum):
        enum_values = [item.value for item in annotation]
        return {"type": "string", "enum": enum_values}

    return None


def parse_docstring(doc: str) -> Dict[str, str]:
    # Stub implementation. Extend to parse docstrings if needed.
    return {}


def generate_schema(func: Callable) -> dict:
    sig = inspect.signature(func)
    doc = inspect.getdoc(func) or ""
    description = doc.split("\n")[0] if doc else ""
    param_descriptions = parse_docstring(doc)

    schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    }

    for name, param in sig.parameters.items():
        param_schema = from_annotation(param.annotation) or {"type": "any"}

        if name in param_descriptions:
            param_schema["description"] = param_descriptions[name]

        schema["function"]["parameters"]["properties"][name] = param_schema

        if param.default is inspect.Parameter.empty and not type_optional(
            param.annotation
        ):
            schema["function"]["parameters"]["required"].append(name)
    return schema


if __name__ == "__main__":
    from typing import Optional, List, Union

    class Color(Enum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    def my_func(
        name: str,
        count: int,
        color: Color,
        tags: Optional[List[str]] = None,
        meta: Dict[str, Union[int, str]] = {},
    ):
        """
        This is a test function.

        Args:
            name: The name to use.
            count: How many times.
            color: A color choice.
            tags: A list of tags.
            meta: Arbitrary key-value metadata.
        """
        pass

    schema = generate_schema(my_func)
    import json

    print(json.dumps(schema, indent=4))
