class Multiplex(dict):
    def __init__(self, objs):
        super().__init__(objs)

    def __call__(self, *args, **kwargs):
        return self.__class__(
            [(alias, obj(*args, **kwargs)) for alias, obj in self.items()]
        )

    def __bool__(self):
        return all(self.values())

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.__class__(
                [(alias, getattr(obj, name)) for alias, obj in self.items()]
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def create(self, other):
        name = type(other).__name__.lower()
        self[name] = other
