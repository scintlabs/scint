from typing import List

from pydantic import BaseModel, Field

from data.models.functions import (ModelFunction, Parameters, Properties,
                                   Property)


async def eval_model_function(function_call):
    pass


initialize_entity = ModelFunction(
    name="initialize_entity",
    description="Use this function to initialize the different components and capabilities of Scint, including the Finder, Processor, and Generator.",
    parameters=Parameters(
        type="object",
        properties=Properties(
            task=Property(
                type="string", description="The task you want to assign the entity."
            ),
            entity=Property(
                type="string",
                description="The available entities.",
                enum=["Finder", "Processor", "Generator"],
            ),
        ),
    ),
    required=["task", "entity"],
)

notify_agent = {
    "name": "agents",
    "description": "Use this function to communicate with the agents controlling Scint's systems, including its Coordinator and Sentry.",
    "parameters": {
        "agent": {
            "type": "string",
            "description": "The agent being initialized.",
            "enum": ["Coordinator", "Sentry"],
        },
        "message": {
            "type": "string",
            "description": "The message to send to the specified agent.",
        },
    },
    "required": ["agent", "message"],
}


functions = [
    {
        "name": "initialize",
        "description": "Initialize parts of the system to accomplish tasks, including Coordinators, Finders, Processors, and Generators.",
        "parameters": {
            "type": "object",
            "properties": {
                "entity": {
                    "type": "string",
                    "description": "",
                    "enum": ["Finder", "Processor", "Generator"],
                },
                "agent": {
                    "type": "string",
                    "description": "",
                    "enum": [
                        "Coordinator",
                        "Sentry",
                    ],
                },
            },
            "required": ["location"],
        },
    }
]

# assistant = Function(
#     name="capabilities",
#     description="Use this function to initialize the different components and capabilities of Scint, including its coordinator, processor, finder, and Generator.",
#     parameters=FunctionParameters(
#         type="object",
#         properties={
#             "finder": ParameterProperty(
#                 type="string",
#                 description="Initialize the finder to search for files, data, or information required for a user request or task.",
#             ),
#             "processor": ParameterProperty(
#                 type="string",
#                 description="Initialize the processor to evaluate, parse, analyze, or categorize data, such as evaluating a codebase, summarizing a book, or generating embeddings.",
#             ),
#             "Generator": ParameterProperty(
#                 type="string",
#                 description="Initialize the Generator state to orchestrate data pipelines and generate code and content for complex tasks and large projects.",
#             ),
#         },
#         required=["coordinator"],
#     ),
#     lifecycle=Lifecycle(),
# )

# coordinator = Function(
#     name="classify",
#     description="This function helps maintain system integrity and should be called with every message with all properties.",
#     parameters=FunctionParameters(
#         type="object",
#         properties={
#             "summary": ParameterProperty(
#                 type="string",
#                 description="For every message you receive, use this function to write a very brief reflection that contextualizes how you responded.",
#             ),
#             "keyword": ParameterProperty(
#                 type="string",
#                 description="Choose a single semantic keyword to describe this interaction.",
#             ),
#         },
#         required=["summary", "keyword"],
#     ),
#     lifecycle=Lifecycle(),
# )

# finder = Function(
#     name="finder",
#     description="Initialize the locator state to search for files, data, or information required for user requests or tasks.",
#     parameters=FunctionParameters(
#         type="object",
#         properties={
#             "search_query": ParameterProperty(
#                 type="string",
#                 description="Use this parameter to inform the user that you're initiating a search.",
#             ),
#             "success_definition": ParameterProperty(
#                 type="string",
#                 description="Based on the given query, provide a threshold of a successful search results.",
#             ),
#             "user_response": ParameterProperty(
#                 type="string",
#                 description="Inform the user that you're beginning the search process.",
#             ),
#         },
#         required=[
#             "search_query",
#             "define_success",
#             "user_response",
#         ],
#     ),
#     lifecycle=Lifecycle(),
# )

# processor = Function(
#     name="processor",
#     description="Initialize the processor state to evaluate, parse, analyze, or categorize data, such as evaluating a codebase, summarizing a book, or generating embeddings.",
#     parameters=FunctionParameters(
#         type="object",
#         properties={
#             "task": ParameterProperty(
#                 type="list",
#                 description="Create a task with an appropriate name, description, and what qualifies as successfully completing the task.",
#             ),
#             "data": ParameterProperty(
#                 type="object",
#                 description="Use this property to store links, filepaths, information, and any other data required to complete the task.",
#             ),
#             "user_update": ParameterProperty(
#                 type="string",
#                 description="Use this parameter to inform the user that you've started processing data to complete the task.",
#             ),
#         },
#         required=[
#             "task",
#             "data",
#         ],
#     ),
#     lifecycle=Lifecycle(),
# )

# Generator = Function(
#     name="Generator",
#     description="Initialize the Generator state to orchestrate data pipelines and generate code and content for complex tasks and large projects.",
#     parameters=FunctionParameters(
#         type="object",
#         properties={
#             "task": ParameterProperty(
#                 type="list",
#                 description="Create a task with an appropriate name, description, and what qualifies as successfully completing the task.",
#             ),
#             "data": ParameterProperty(
#                 type="object",
#                 description="Use this property to store links, filepaths, information, and any other data required to complete the task.",
#             ),
#             "user_update": ParameterProperty(
#                 type="string",
#                 description="Use this parameter to inform the user that you've started processing data to complete the task.",
#             ),
#         },
#         required=[
#             "task",
#             "data",
#         ],
#     ),
#     lifecycle=Lifecycle(),
# )

# generate_prose = {
#     "name": "generate_code",
#     "description": "Use this function to write and test Python code. Files are created in a secure environment.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "code": {
#                 "type": "string",
#                 "description": "The Python code to write and execute. You may write files and folders to create complex projects using Python.",
#             },
#         },
#         "required": ["code"],
#     },
# }

# generate_code = {
#     "name": "generate_code",
#     "description": "Use this function to write and test Python code. Files are created and executed in a secure environment.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "code": {
#                 "type": "string",
#                 "description": "The Python code to write and execute. You may write files and folders to create complex projects using Python.",
#             },
#         },
#         "required": ["code"],
#     },
# }
