class ProcessType(type):
    def __new__(cls, name, bases, dct, **kwds):
        def model(self):
            for k, v in self.__dict__.items():
                try:
                    return {k: v.model for k, v in self.__dict__.items()}
                except AttributeError:
                    if isinstance(v, dict):
                        try:
                            return {k: v.model for k, v in self.__dict__.items()}
                        except AttributeError:
                            pass
                    elif isinstance(v, list):
                        pass
                    else:
                        dct[k] = v
            return dct

        dct["model"] = property(model)

        return super().__new__(cls, name, bases, dct, **kwds)


class Process(metaclass=ProcessType):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create_thread(name, interface, *args, **kwargs):
        def prepare(cls, name, bases, **kwds):
            return {}

        def new(cls, name, bases, dct, **kwds):
            return super().__new__(cls, name, bases, dct, **kwds)

        dct = {"__prepare__": classmethod(prepare), "__new__": new}
        return type(name, (Thread,), dct)


class Thread(Process):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create_thread(name, interface, *args, **kwargs):
        def prepare(cls, name, bases, **kwds):
            return {}

        def new(cls, name, bases, dct, **kwds):
            return super().__new__(cls, name, bases, dct, **kwds)

        dct = {"__prepare__": classmethod(prepare), "__new__": new}
        return type(name, (Thread,), dct)
