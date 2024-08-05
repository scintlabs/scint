import ast
import inspect


def get_source_code(func):
    def wrapper(*args, **kwargs):
        source = inspect.getsource(func)
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func.__name__:
                func_source = ast.get_source_segment(source, node)
                print(f"Source code of {func.__name__}:")
                print(func_source)
                break

        return func(*args, **kwargs)

    return wrapper


# @get_source_code
# def example_function(x, y):
#     """This is a docstring."""
#     return x + y


# # Using the decorated function
# result = example_function(3, 4)
