import asyncio
from functools import wraps

from ..models import Event


def record(func):
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            name = func.__qualname__.split(".")[0]
            func_name = func.__name__
            event = Event(
                name=func_name,
                data=f"{name} called {func_name}.",
                arguments={"args": args, "kwargs": kwargs},
            )
            self.events.append(event)
            print(event)

            try:
                result = await func(self, *args, **kwargs)
                event = Event(
                    name=func_name,
                    data=f"{func_name} returned successfully.",
                    result=str(result) if result else None,
                )
                self.events.append(event)
                print(event)
                return result
            except BaseException as e:
                event = Event(
                    name=func_name,
                    data=f"Exception during method call: {e}",
                    result=str(result) if result else None,
                )
                self.events.append(event)
                print(event)
                raise

    else:

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            name = func.__qualname__.split(".")[0]
            func_name = func.__name__
            event = Event(
                name=func_name,
                data=f"{name} called {' -> '.join(self._call_stack)}.",
                arguments={"args": args, "kwargs": kwargs},
            )
            self.events.append(event)
            print(event)

            try:
                result = func(self, *args, **kwargs)
                event = Event(
                    name=func_name,
                    data=f"{func_name} returned successfully.",
                    result=str(result) if result else None,
                )
                self.events.append(event)
                return result
            except BaseException as e:
                event = Event(
                    name=name,
                    data=f"Exception during method call: {e}",
                    result=str(result) if result else None,
                )
                self.events.append(event)
                print(event)
                raise

    return wrapper
