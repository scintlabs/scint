# from functools import partial, wraps
# from typing import Callable
# from types import new_class

# from scint.types.enum import Enum
# from scint.types.network import Model


# class StructType(type):
#     def __new__(cls, name, bases, dct, **kwds):

#         def initializer(func):
#             @wraps(func)
#             def wrapper(self, *args, **kwargs):
#                 try:
#                     func(self, *args, **kwargs)
#                     return super(self).__init__()
#                 except BaseException:
#                     raise

#         @property
#         def context(self):
#             return self

#         @property
#         def model(self):
#             return {k: v.__name__ for k, v in self.__dict__.items()}

#         for key, val in dct.items():
#             if callable(val) and not key.startswith("__"):
#                 dct[key] = dict(val)

#         dct["__init__"] = initializer(dct.get("__init__"))
#         dct["context"] = context
#         dct["model"] = model
#         return super().__new__(cls, name, bases, dct, **kwds)

#         def __call__(cls, *args, **kwargs):
#             instance = super().__call__(*args, **kwargs)
#             return instance

#         def __setattr__(self, name, value):
#             if not isinstance(Model):
#                 return AttributeError("")
#             return setattr(self.state, name, value)

#         return super().__new__(cls, name, bases, dct, **kwds)


# class Struct(metaclass=StructType):
#     def __init__(self, *args, **kwargs): ...


# class ComposerType(type):
#     def __new__(cls, name, bases, dct, **kwds):
#         def compose(self, other):
#             pass

#         def add_step(self, operation: Callable) -> Struct:
#             state = Struct(operation)
#             if not self.root:
#                 self.root = state
#             return state

#         def then(self, operation: Callable) -> Struct:
#             state = self.add_step(operation)
#             if self.current:
#                 self.current.right_sibling = state
#                 state.left_sibling = self.current
#             self.current = state
#             return state

#         def parallel(self, operation: Callable) -> Struct:
#             state = self.add_step(operation)
#             if self.current:
#                 if self.current.first_child:
#                     # Find last child
#                     last = self.current.first_child
#                     while last.right_sibling:
#                         last = last.right_sibling
#                     last.right_sibling = state
#                     state.left_sibling = last
#                 else:
#                     self.current.first_child = state
#                 state.parent = self.current
#             return state

#         dct["root"] = None
#         dct["current"] = None
#         dct["compose"] = compose
#         dct["add_step"] = add_step
#         dct["then"] = then
#         dct["parallel"] = parallel
#         return super().__new__(cls, name, bases, dct, **kwds)


# class Composer(metaclass=ComposerType):
#     def __init__(self, *args, **kwargs): ...


# class InterfaceType(type):
#     def __new__(cls, name, bases, dct, **kwds):
#         def __setattr__(self, name, value):
#             return setattr(self.state, name, value)

#         @property
#         def state(self):
#             return self._state

#         @property
#         def aspects(self):
#             pass

#         dct["_state"] = Struct()
#         dct["state"] = state
#         dct["aspects"] = aspects
#         return super().__new__(cls, name, bases, dct, **kwds)


# class Interface(metaclass=InterfaceType):
#     def __init__(self, *args, **kwargs): ...


# class TalentType(type):
#     def __new__(cls, name, bases, dct, **kwds):
#         def bind(self, func):
#             def unbind(method, other):
#                 original_func = method.__func__
#                 return partial(original_func, other)

#             @wraps(func)
#             def method_wrapper(self, *args, **kwargs):
#                 return func(*args, **kwargs)

#         dct["bind"] = bind
#         return super().__new__(cls, name, bases, dct, **kwds)


# class Talent(metaclass=TalentType):
#     def __init__(self, *args, **kwargs): ...


# # def Struct():
# #     return type("Struct", (), {"metaclass": StructType})


# # def Interface():
# #     return type("Interface", (), {"metaclass": InterfaceType})


# # def Talent():
# # return type("Talent", (), {"metaclass": TalentType})


# Processs = Enum(
#     {
#         "Broker": lambda: type("Broker", (Process,)),
#         "Intelligence": lambda: type("Intelligence", (Process,)),
#         "Persistence": lambda: type("Persistence", (Process,)),
#         "Recorder": lambda: type("Recorder", (Process,)),
#         "Registry": lambda: type("Registry", (Process,)),
#         "Repository": lambda: type("Repository", (Process,)),
#         "Search": lambda: type("Search", (Process,)),
#     }
# )

# Processes = Enum({"Processes": lambda: type("Parse", (Process,))})
# Interfaces = Enum({"Interfaces": lambda: type("Interface", (InterfaceType,))})
# Talents = Enum({"Talents": lambda: type("Talent", (Talent,))})
