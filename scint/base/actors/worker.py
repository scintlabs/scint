from scint.base.types.actors import ActorType


class Worker(metaclass=ActorType):
    def __init__(self, context, parent=None, **kwargs):
        super().__init__()
        self.context = context
        self.parent = parent
        self.children = []
