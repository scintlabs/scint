from enum import Enum
from functools import wraps


class Enumerator(Enum):
    def log_event(self):
        print(self.value)

    def __call__(self, func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            self.log_event()
            return await func(*args, **kwargs)

        return wrapped
