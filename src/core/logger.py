from enum import Enum, auto
from functools import wraps
import inspect
from typing import Callable, TypeVar

from src.core.types import Aspect
from src.models.events import Event


F = TypeVar("F", bound=Callable)


class LogLevel(Enum):
    INFO = auto()
    DEBUG = auto()
    WARNING = auto()
    ERROR = auto()


def logged(level: LogLevel = LogLevel.INFO):
    def decorator(func: F) -> F:
        setattr(func, "_logged", True)
        setattr(func, "_log_level", level)
        return func

    return decorator


class Loggable(Aspect):
    @staticmethod
    def record_sync(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
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
                res = func(self, *args, **kwargs)
                event = Event(
                    name=func_name,
                    data=f"{func_name} returned successfully.",
                    result=str(res) if res else None,
                )
                self.events.append(event)
                print(event)
                return res
            except BaseException as e:
                event = Event(
                    name=func_name,
                    data=f"Exception during method call: {e}",
                    result=None,
                )
                self.events.append(event)
                print(event)
                raise

        return wrapper

    @staticmethod
    def record_async(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            name = func.__qualname__.split(".")[0]
            func_name = func.__name__
            event = Event(
                name=func_name,
                data=f"{name} called {func_name}.",
                arguments={"args": args, "kwargs": kwargs},
            )
            print(event)

            try:
                res = await func(self, *args, **kwargs)
                event = Event(
                    name=func_name,
                    data=f"{func_name} returned successfully.",
                    result=str(res) if res else None,
                )
                print(event)
                return res
            except BaseException as e:
                event = Event(
                    name=func_name,
                    data=f"Exception during method call: {e}",
                    result=None,
                )
                print(event)
                raise

        return wrapper

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        for name, method in cls.__dict__.items():
            if name.startswith("_"):
                continue

            if not callable(method):
                continue

            if not getattr(method, "_logged", False):
                continue

            if inspect.iscoroutinefunction(method):
                setattr(cls, name, cls.record_async(method))
            else:
                setattr(cls, name, cls.record_sync(method))


__all__ = LogLevel, Loggable
