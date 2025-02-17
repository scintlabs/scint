from __future__ import annotations

from functools import wraps
from typing import List

from scint.api.types import Trait
from scint.api.models import Event


def record_sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        class_name = args[0] if args else "Unknown"
        func_name = func.__name__
        print(f"{class_name} called {func_name}.")

        try:
            res = func(*args, **kwargs)
            print(f"{func_name} returned successfully.")
            return res
        except BaseException as e:
            print(f"Exception during method call: {e}\n")
            raise

    return wrapper


def record_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        class_name = args[0] if args else "Unknown"
        func_name = func.__name__
        print(f"{class_name} called {func_name}.")

        try:
            res = await func(*args, **kwargs)
            print(f"{func_name} returned successfully.")
            return res
        except BaseException as e:
            print(f"Exception during method call: {e}")
            raise

    return wrapper


class EventSource(Trait):
    events: List[Event] = []
