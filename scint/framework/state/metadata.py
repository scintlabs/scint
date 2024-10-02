import asyncio
from functools import wraps

from scint.framework.models.events import Event, MethodCall, CallResult


class metadata(dict):
    def __init__(self):
        self.events = []
        self.annotations = []
        super().__init__()

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value


def collector(func):
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            name = func.__qualname__.split(".")[0]
            func_name = func.__name__
            top_level = len(self._call_stack) == 0
            self._call_stack.append(func_name)
            if top_level:
                if func_name == "__init__":
                    event = Event(name=name, data=f"Initializing {name}.")
                else:
                    event = MethodCall(
                        name=func_name,
                        data=f"{name} called {' -> '.join(self._call_stack)}.",
                        arguments={"args": args, "kwargs": kwargs},
                    )
                self.state.collect(event)

            try:

                result = await func(self, *args, **kwargs)
                if top_level:
                    event = CallResult(
                        name=func_name,
                        data=" -> ".join(self._call_stack),
                        result=str(result) if result else None,
                    )
                    self.state.collect(event)
                return result
            except BaseException as e:
                print(f"Exception in {' -> '.join(self._call_stack)}: {e}")
                raise
            finally:
                self._call_stack.pop()

    else:

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            name = func.__qualname__.split(".")[0]
            func_name = func.__name__
            top_level = len(self._call_stack) == 0
            self._call_stack.append(func_name)
            if top_level:
                if func_name == "__init__":
                    event = Event(name=name, data=f"Initializing {name}.")
                else:
                    event = MethodCall(
                        name=func_name,
                        data=f"{name} called {' -> '.join(self._call_stack)}.",
                        arguments={"args": args, "kwargs": kwargs},
                    )
                self.state.collect(event)

            try:

                result = func(self, *args, **kwargs)
                if top_level:
                    event = CallResult(
                        name=func_name,
                        data=" -> ".join(self._call_stack),
                        result=str(result) if result else None,
                    )
                    self.state.collect(event)
                return result
            except BaseException as e:
                print(f"Exception in {' -> '.join(self._call_stack)}: {e}")
                raise
            finally:
                self._call_stack.pop()

    return wrapper
