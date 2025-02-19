# from scint.lib.types.base import (
#     ExtensionType,
#     StructType,
#     ToolsType,
#     Tool,
#     TraitType,
#     InterfaceType,
# )


# class Struct(metaclass=StructType): ...


# class Trait(metaclass=TraitType): ...


# class Tools(metaclass=ToolsType):
#     def __init__(self, *tools):
#         self._tools = {}
#         self.original_tools = list(tools)
#         self.current_tools = []

#     def __call__(self, *tools):
#         merged_tools = {}
#         starting = []
#         target = []
#         for k, v in self._tools.items():
#             starting.append(k)
#         for tool_class in tools:
#             target.append(tool_class)
#             merged_tools.update(tool_class._tools)
#         self._tools = merged_tools
#         print(f"Swapping tools in {starting} for tools in {target}.")
#         return self

#     @property
#     def model(self):
#         return [v.model for k, v in self._tools.items()]


# class Extension(metaclass=ExtensionType):
#     def __init_construct__():
#         pass

#     def get_context(self):
#         pass

#     def set_context(self):
#         pass

#     def share_context(self, other_node, key):
#         if key in self.context.data:
#             other_node.context.update(key, self.context.data[key])

#     def disconnect(self, other_node):
#         if other_node.node_id in self.interfaces:
#             del self.interfaces[other_node.node_id]
