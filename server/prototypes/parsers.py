from __future__ import annotations

import inspect
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Union
from typing_extensions import get_origin, get_args

import tree_sitter as ts


from src.types.aspects import Param, Params
from src.types.interfaces import Trait


class Parser(Trait):
    def parse_docs(self, content: str):
        lines = content.split("\n")
        result = []

        for i, line in enumerate(lines):
            if i == 0 or line.startswith("#"):
                result.append({"type": "heading", "storage": line, "line": i})
            elif line.strip() and "." in line:
                first_sentence = line.split(".")[0] + "."
                result.append(
                    {"type": "paragraph", "storage": first_sentence, "line": i}
                )
        return result

    def optional(self, annotation: Any) -> bool:
        origin = get_origin(annotation)
        if origin is Union:
            args = get_args(annotation)
            if type(None) in args:
                return True
        return False

    def parse_annotation(self, annotation: Any) -> Dict[str, Any]:
        if annotation == inspect.Parameter.empty:
            return {"type": "any"}

        origin = get_origin(annotation)
        args = get_args(annotation)

        if annotation in (str, int, bool, float):
            return {"type": annotation.__name__}

        if origin is Literal:
            return {"enum": list(args)}

        if origin in (list, List):
            (item_type,) = args
            return {"type": "array", "items": self.parse_annotation(item_type)}

        if origin in (dict, Dict):
            key_type, value_type = args
            return {
                "type": "object",
                "properties": self.parse_annotation(value_type),
            }

        if origin is Union:
            models = []
            for arg in args:
                if arg is type(None):
                    models.append({"type": "null"})
                else:
                    models.append(self.parse_annotation(arg))
            return {"oneOf": models}

        if inspect.isclass(annotation) and issubclass(annotation, Enum):
            enum_values = [z.value for z in annotation]
            return {"type": "string", "enum": enum_values}

    def parse_docstring(self, doc: str) -> Dict[str, str]:
        return {}

    def parse_function(self, func: Callable):
        sig = inspect.signature(func)
        doc = inspect.getdoc(func) or ""
        desc = doc.split("\n")[0] if doc else ""
        param_descs = self.parse_docstring(doc)
        properties: List[Params] = []

        for name, param in sig.parameters.items():
            schema = self.parse_annotation(param.annotation)
            ptype = schema.get("type", "any")

            if "enum" in schema:
                ptype = "enum"
                items = schema["enum"]
            elif ptype == "array":
                items = schema.get("items", {})
            else:
                items = []

            prop_desc = param_descs.get(name, "")
            if not prop_desc and schema.get("enum"):
                prop_desc = f"Possible values: {schema['enum']}"

            properties.append(
                Param(
                    name=name,
                    type=ptype,
                    description=prop_desc or f"Parameter '{name}'",
                    items=items if isinstance(items, list) else [items],
                )
            )

        params = Params(properties=properties)
        return dict(name=func.__name__, description=desc, parameters=params, code=None)

    def parse_class(self, cls: type):
        cls_doc = inspect.getdoc(cls) or ""
        cls_bases = [type.__name__ for base in cls.__bases__ if base is not object]

        attributes = {
            name: value
            for name, value in cls.__dict__.items()
            if not (callable(value) or name.startswith("__"))
        }

        methods = []
        for name, func in cls.__dict__.items():
            if callable(func) and not name.startswith("__"):
                func_parser = ts.Parser()
                method_spec = func_parser.parse_function(func)
                methods.append(method_spec)

        return dict(
            name=cls.__name__,
            base_classes=cls_bases,
            docstring=cls_doc,
            methods=methods,
            attributes=attributes,
        )

    def parse_code(self, content: str):
        code_parser = ts.Parser()
        ts.Language("settings/languages.so")
        tree = code_parser.parse(bytes(content, "utf-8"))
        result = []

        for node in tree.root_node.children:
            if node.type in ["import_statement", "import_from_statement"]:
                result.append(
                    {
                        "type": "import",
                        "signature": node.text.decode("utf-8"),
                        "start_line": node.start_point[0],
                        "end_line": node.end_point[0],
                    }
                )
            elif node.type == "class_definition":
                result.append(
                    {
                        "type": "class",
                        "signature": node.children[1].text.decode("utf-8"),
                        "start_line": node.start_point[0],
                        "end_line": node.end_point[0],
                    }
                )
            elif node.type == "function_definition":
                result.append(
                    {
                        "type": "intent",
                        "signature": node.children[1].text.decode("utf-8"),
                        "start_line": node.start_point[0],
                        "end_line": node.end_point[0],
                    }
                )
        return result
