# from scint.controllers.intelligence import intelligence_controller
# from scint.base.container import Messages
# from scint.base.context import Context
# from scint.support.types import Arguments, Message, SystemMessage
# from scint.support.logging import log
# from scint.base import functions
#
#
# class ComponentType(type):
#     @classmethod
#     def __prepare__(cls, name, bases, **kwargs):
#         return {}
#
#     def __new__(cls, name, bases, dct, **kwargs):
#         description = SystemMessage(content=dct.get("description").strip())
#         messages = Messages(name)
#         for i in dct.get("instructions"):
#             messages.append(SystemMessage(content=i))
#         function_choice = dct.get("function_choice", "auto")
#
#         def get_metadata(data):
#             metadata = {
#                 "name": name,
#                 "description": description.metadata,
#                 "messages": [m.metadata for m in messages],
#                 "function_choice": function_choice,
#             }
#
#             for key, value in data.items():
#                 if key == "messages":
#                     metadata["messages"] = value
#                 if key == "modules":
#                     if not metadata.get("modules"):
#                         metadata["modules"] = [module.metadata for module in value]
#                 if key == "routines":
#                     if not metadata.get("routines"):
#                         metadata["routines"] = [routine.metadata for routine in value]
#                 if hasattr(value, "props"):
#                     if not metadata.get("functions"):
#                         metadata["functions"] = []
#                     metadata["functions"].append(value.metadata)
#                 if key == "function_choice":
#                     metadata["function_choice"] = value
#
#             return metadata
#
#         async def process(self, message: Message):
#             log.debug(f"{self.name} received message.")
#             self.messages.append(message)
#             async for response in self.intelligence.process(Context(**self.metadata)):
#                 if isinstance(response, Arguments):
#                     args = response.content
#                     function_name = response.name
#                     func = getattr(functions, function_name)
#                     async for function_call in func(**args):
#                         yield function_call
#
#                 if isinstance(response, Message):
#                     yield response
#
#         dct["name"] = name
#         dct["description"] = description
#         dct["function_choice"] = function_choice
#         dct["metadata"] = get_metadata(data=dct)
#         dct["messages"] = messages
#         dct["process"] = process
#         dct["processing"] = False
#         dct["intelligence"] = intelligence_controller
#
#         return super().__new__(cls, name, bases, dct, **kwargs)
#
#     def __init__(cls, name, bases, dct, **kwargs):
#         super().__init__(name, bases, dct, **kwargs)
#
#     def __call__(cls, *args, **kwargs):
#         instance = super().__call__(*args, **kwargs)
#         return instance
#
#
# class Component(metaclass=ComponentType):
#     description = "You are Scint."
#     instructions = [
#         """You are an advanced AI system leveraging multiple large language models to power sophisticated control flow and memory systems. You excel in natural language processing, question answering, text generation, analysis, and problem-solving. You can dynamically incorporate new functions based on the current context, providing tailored and context-specific assistance. Your functionality is based on explicit user consent. You learn and evolve from interactions and feedback, striving to provide accurate and unbiased information. You acknowledge your limitations and are transparent about uncertainties or errors in your responses.
#         """
#     ]
