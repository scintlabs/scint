import ast
import inspect
import re


def attr_from_source(source, attribute_name):
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
    source = inspect.getsource(function)
    description = attr_from_source(source, "description")
    props = attr_from_source(source, "props")
    if props and description:
        return True
    return False


def parse_docstring(docstring, *args):
    return docstring.strip()


instancelist = lambda l, t: all(isinstance(i, t) for i in l)
