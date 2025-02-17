# from scint.build.network.resources import Resources
# from scint.build.settings import Settings


# def load_app(self, *args, **kwargs):
#     def load_aspects(self, *args, **kwargs):
#         pass

#     def load_data(self, *args, **kwargs):
#         pass

#     def load_network(self, *args, **kwargs):
#         pass

#     def load_resources(self):
#         return Resources()

#     def load_settings(self):
#         return Settings()


# def start(*args, **kwargs):
#     load_app(*args, **kwargs)


# app = {
#     "aspects": [
#         {"name": "attention", "instances": []},
#         {"name": "crawler", "instances": {}},
#         {
#             "name": "memory",
#             "components": {
#                 "event_source": {},
#                 "indexes": [],
#                 "context": {"map": {}},
#                 "state": {"map": {}},
#             },
#         },
#     ],
#     "data": [
#         {
#             "id": "id",
#             "parent": {},
#             "siblings": {"left": {}, "right": {}},
#             "children": [{}, {}, {}, {}],
#             "traits": [
#                 {"name": "function"},
#                 {"name": "function"},
#                 {"name": "function"},
#             ],
#             "state": {
#                 "messages": [],
#                 "tools": [],
#                 "metadata": {
#                     "labels": [],
#                     "embeddings": [],
#                 },
#             },
#         },
#         {
#             "id": "id",
#             "parent": {},
#             "siblings": {"left": {}, "right": {}},
#             "children": [
#                 {
#                     "id": "id",
#                     "parent": {},
#                     "siblings": {"left": {}, "right": {}},
#                     "children": [
#                         {
#                             "id": "id",
#                             "parent": {},
#                             "siblings": {"left": {}, "right": {}},
#                             "children": [{}, {}, {}, {}],
#                             "traits": [
#                                 {"name": "function"},
#                                 {"name": "function"},
#                                 {"name": "function"},
#                             ],
#                             "state": {
#                                 "aggregates": {
#                                     "labels": [],
#                                     "embeddings": [],
#                                     "objects": [
#                                         {"messages": []},
#                                         {"tools": []},
#                                     ],
#                                 }
#                             },
#                         }
#                     ],
#                     "traits": [
#                         {"name": "function"},
#                         {"name": "function"},
#                         {"name": "function"},
#                     ],
#                     "state": {
#                         "aggregates": {
#                             "labels": [],
#                             "embeddings": [],
#                             "objects": [
#                                 {"messages": []},
#                                 {"tools": []},
#                             ],
#                         }
#                     },
#                 },
#             ],
#             "traits": [
#                 {"name": "function"},
#                 {"name": "function"},
#                 {"name": "function"},
#             ],
#             "state": {
#                 "aggregates": {
#                     "labels": [],
#                     "embeddings": [],
#                     "objects": [
#                         {"messages": []},
#                         {"tools": []},
#                     ],
#                 }
#             },
#         },
#         {
#             "id": "id",
#             "parent": {},
#             "siblings": {"left": {}, "right": {}},
#             "children": [{}, {}, {}, {}],
#             "traits": [
#                 {"name": "function"},
#                 {"name": "function"},
#                 {"name": "function"},
#             ],
#             "state": {
#                 "aggregates": {
#                     "labels": [],
#                     "embeddings": [],
#                     "objects": [
#                         {"messages": []},
#                         {"tools": []},
#                     ],
#                 }
#             },
#         },
#     ],
#     "network": {
#         "bridges": [],
#         "channels": [],
#         "routes": [],
#     },
#     "resources": {
#         "library": {
#             "models": {},
#             "prompts": {},
#             "traits": {},
#             "tools": {},
#         },
#         "parse": {
#             "specifications": {},
#         },
#         "build": {
#             "rules": {},
#             "arguments": {},
#             "factories": {},
#         },
#     },
# }
