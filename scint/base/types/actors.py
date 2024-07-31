import asyncio
import functools
import inspect

from scint.base.models.messages import Messages, Prompts
from scint.base.models.functions import Functions
from scint.base.models import generate_id

__all__ = "Actor"


settings = {}


class ActorType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        def log_method_call(func):
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                print(f"Calling method: {func.__name__}")
                return func(*args, **kwargs)

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                print(f"Calling async method: {func.__name__}")
                return await func(*args, **kwargs)

            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper

        def unpack(self, parent):
            for name, value in inspect.getmembers(self):
                if not name.startswith("__") and name != "assign_to_parent":
                    if inspect.ismethod(value) or inspect.isfunction(value):
                        setattr(parent, name, value.__func__.__get__(parent))
                    else:
                        setattr(parent, name, value)

        cls._id = generate_id(name)
        components = cls._context.build_actor(cls, cls._build)
        for component in components:
            dct[component.name] = component.unpack(cls)

        for attr_name, attr_value in dct.items():
            if callable(attr_value):
                dct[attr_name] = log_method_call(attr_value)
        return super().__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, *args, **kwargs):
        cls._context.init_actor(cls)
        super().__init__(name, bases, dct)


class Actor(metaclass=ActorType):
    def __init__(self, settings=settings):
        super().__init__()
        self.prompts = Prompts()
        self.messages = Messages()
        self.functions = Functions()
        self.running = False


class ActorSystem:
    def __init__(self):
        self.actors = {}

    def create_actor(self, actor_class):
        actor = actor_class(id, self)
        self.actors[id] = actor
        return id

    def send_message(self, actor_id, message: str):
        if actor_id in self.actors:
            self.actors[actor_id].receive(message)
