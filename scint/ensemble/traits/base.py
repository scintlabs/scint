from functools import partial, wraps


class TraitType(type):
    def __new__(cls, name, bases, dct, **kwds):
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
            return self.model

        def bind(self, func):
            def unbind(method, other):
                original_func = method.__func__
                return partial(original_func, other)

            @wraps(func)
            def method_wrapper(self, *args, **kwargs):
                return func(*args, **kwargs)

        dct["bind"] = bind
        dct["model"] = property(model)
        return super().__new__(cls, name, bases, dct, **kwds)


class Trait(metaclass=TraitType):
    @classmethod
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
