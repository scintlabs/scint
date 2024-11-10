from functools import wraps

from scint.repository.models.base import Trait


class Initialize(Trait):
    def __new__(cls, name, bases, dct, **kwds):
        def initializer(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                try:
                    return func(self, *args, **kwargs)
                except BaseException:
                    raise

            return wrapper
