class InterfaceType(type):
    def __new__(cls, name, bases, dct, **kwds):
        @property
        def model(self):
            dct = {}
            for k, v in self.__dict__.items():
                try:
                    dct[k] = v.model
                except AttributeError:
                    if isinstance(v, list):
                        dct[k] = [i.model for i in v]
                    elif isinstance(v, dict):
                        dct[k] = {k: v.__dict__ for k, v in self.__dict__.items()}
                    elif isinstance(v, str):
                        dct[k] = v
            return dct

        @property
        def context(self):
            return self.model

        dct["context"] = context
        return super().__new__(cls, name, bases, dct, **kwds)


class Interface(metaclass=InterfaceType):
    def __init__(self, *args, **kwargs): ...
