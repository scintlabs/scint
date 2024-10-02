import asyncio
from functools import wraps


class data(dict):
    def __getattr__(self, item):
        try:
            value = self[item]
            if isinstance(value, dict) and not isinstance(value, data):
                value = data(value)
                self[item] = value
            return value
        except KeyError:
            raise AttributeError(f"'ScintData' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        self[key] = value


class State:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance.state, self.name, None)

    def __set__(self, instance, value):
        setattr(instance.state, self.name, value)


class state(data):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.events = []
        self.context = context(name)

    def collect(self, event):
        self.events.append(event)

    def __enter__(self):
        return self.context

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.__exit__(exc_type, exc_value, traceback)


class context(data):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def create(self, name):
        new_state = state(name)
        self[name] = new_state
        return new_state

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    async def __aenter__(self):
        return self.__enter__()

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.__exit__(exc_type, exc_value, traceback)


def publicmethod(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        with self.state as context:
            context[func.__name__] = func
            if asyncio.iscoroutinefunction(func):
                result = asyncio.gather(
                    asyncio.create_task(func(self, *args, **kwargs))
                )
                return result
            result = func(self, *args, **kwargs)
            return result

    return wrapper
