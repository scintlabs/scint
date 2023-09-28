from base.agents import Agent
from providers.openai import chat_completion
from base.observability.logging import logger

# from base.processing import preprocess, serializer
# from config.functions import assistant as assistant_funcs
# from config.prompts import assistant as assistant_prompt


# class Coordinator(Agent):
#     def __init__(self):
#         self.name = "Coordinator"
#         self.messages = []
#         self.functions = []
#         self.system_prompt = assistant_prompt
#         self.messages.append(self.system_prompt)
#         self.functions.append(assistant_funcs)
#         logger.info(f"Initializing {self.name}.")

#     async def send_message(self, message):
#         try:
#             self.thread.messages.append(message)
#             messages_data = preprocess.messages(self.thread)
#             functions_data = preprocess.functions(self.thread)
#             chat_completion(messages_data)

#         except Exception as e:
#             logger.exception(f"{e}")
#             raise

#     async def receive_message(self, data):
#         try:
#             message_content = data["choices"][0]["message"].get("content")
#             function_call = data["choices"][0]["message"].get("function_call")
#             message = serializer.message(message_content)
#             function = serializer.function(function_call)

#             return message, function

#         except Exception as e:
#             logger.exception(f"{e}")
#             raise
