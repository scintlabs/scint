import functools


url = {"data": [{"url": "example.com"}]}
embedding = {"data": [{"embedding": [12, 123, 42]}]}
content = {"choices": [{"message": {"content": "guess what?"}}]}


def rgetattr(obj, attr, *args):
    """
    """
    def _getattr(obj, attr):
        try:
            if isinstance(obj, dict):
                return obj[attr]
            elif isinstance(obj, list):
                return obj[int(attr)]
            else:
                return getattr(obj, attr, *args)
        except (KeyError, IndexError, AttributeError):
            return None

    return functools.reduce(_getattr, [obj] + attr.split("."))


function = {"choices": [{"message": {"tool_calls": {"function": "getattr, bitch"}}}]}
function_attrs = ["choices", "0", "message", "tool_calls", "function"]
keypath = ".".join(function_attrs)

print(rgetattr(function, keypath, None))
