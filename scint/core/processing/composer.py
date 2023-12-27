from scint import config
from scint.core.context import Message
from scint.core.tools import Tool, Tools
from scint.core.worker import Worker
from scint.services.logger import log


class Composer(Worker):
    def __init__(self):
        super().__init__()
        self.name = "Composer"
        self.tools = Tools()

        log.info(f"{self.name} loaded.")


# class Composer(Worker):
#     def __init__(self):
#         self.name = "Composer"
#         self.tools = Tools()
#         generate_prose = Tool(
#             name="generate_prose",
#             description="This function generates prose based on a given topic or prompt.",
#             props={
#                 "prompt": {
#                     "type": "string",
#                     "description": "The prompt or topic to generate prose about.",
#                 }
#             },
#             required=["prompt"],
#         )
#         generate_code = Tool(
#             name="generate_code",
#             description="This function generates code based on a given specification or prompt.",
#             props={
#                 "specification": {
#                     "type": "string",
#                     "description": "The specification or prompt to generate code about.",
#                 }
#             },
#             required=["specification"],
#         )

#         # Add the tools to the Composer's toolset.
#         self.tools.add(generate_prose, generate_prose)
#         self.tools.add(generate_code, generate_code)

#         # Initialize the state of the Composer.
#         self.state = State(
#             self.name,
#             self.identity,
#             self.instructions,
#             self.config,
#             self.tools,
#             self.context,
#         )

#         log.info(f"{self.name}: initialized self.")

#     async def generate_prose(self, prompt: str) -> Message:
#         # Placeholder function for prose generation
#         log.info("Generating prose for prompt.")
#         # Implement your prose generation logic here
#         generated_text = "Generated prose based on the prompt: " + prompt
#         return Message(generated_text, "prose_composer")

#     async def generate_code(self, specification: str) -> Message:
#         # Placeholder function for code generation
#         log.info("Generating code for specification.")
#         # Implement your code generation logic here
#         generated_code = "Generated code based on the specification: " + specification
#         return Message(generated_code, "code_composer")


# class Composer(Worker):
#     def __init__(self):
#         self.name = "Planner"
#         self.identity = "You are a research module for Scint, an intelligent assistant."
#         self.instructions = ""
#         self.config = config.DEFAULT_CONFIG
#         self.tools = Tools()
#         self.tools.add(create_event, self.create_event)
#         self.tools.add(get_events, self.get_events)
#         self.state = State(
#             self.name,
#             self.identity,
#             self.instructions,
#             self.config,
#             self.tools,
#             self.context,
#         )

#         log.info(f"{self.name}: initializing self.")

#     async def create_event(self):
#         return Message(f"Event created.")

#     async def get_events(self):
#         return Message(f"Event list.")
