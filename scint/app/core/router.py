from scint.framework.components.handler import Handler
from scint.framework.types.base import BaseType


from scint.framework.entities.composer import Composer


class Bulletin(Composer):
    def __init__(self, context, *args, **kwargs):
        super().__init__(context, *args, **kwargs)


class Channels(Composer):
    def __init__(self, context, *args, **kwargs):
        super().__init__(context, *args, **kwargs)


class Handlers(Composer):
    def __init__(self, context, *args, **kwargs):
        super().__init__(context, *args, **kwargs)


class Queues(Composer):
    def __init__(self, context, *args, **kwargs):
        super().__init__(context, *args, **kwargs)


class Router(metaclass=BaseType):
    def __init__(self, context, *registries):
        self.context = context

    async def set_scopes(self):
        pass

    async def create_interface(self, name, input, output, callback):
        self.handlers.create_composition(Handler())
        self.handlers.add_subscribe(name, input)
        self.handlers.add_callback(name, callback)
        self.handlers.add_publish(name, output)
        return self.handlers[name]
