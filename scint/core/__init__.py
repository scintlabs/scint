# async def process_message(message):
#     try:
#         state = self.get_state()
#         state["messages"].append(message.data_dump())
#         response = await tool_call(**state)
#         tool_calls = response.get("tool_calls")

#         if tool_calls is not None:
#             async for response in evaluate_tool_call(tool_calls):
#                 if response is not None:
#                     await self.generate_response(response)

#     except Exception as e:
#         log.info(f"{self.name}: {e}.")


# async def generate_response(self, message):
#     try:
#         self.context.add(message)
#         state = self.persona.get_state()
#         state["messages"].append(message.data_dump())
#         response = await message_completion(**state)
#         tool_calls = response.get("tool_calls")

#         if tool_calls is not None:
#             async for response in self.parse_tool_call(tool_calls):
#                 message.message_type = response.message_type
#                 message.keywords = response.keywords
#                 message.named_entities = response.named_entities
#                 yield response

#     except Exception as e:
#         log.info(f"{self.name}: {e}.")


# async def parse_tool_call(self, tool_calls):
#     try:
#         for tool_call in tool_calls:
#             func = tool_call.get("function")
#             tool_name = func.get("name")
#             arguments = func.get("arguments")
#             func_args = json.loads(arguments)

#             for tool in self.search.tools:
#                 if tool.__class__.__name__ == tool_name:
#                     async for response in tool.execute_action(**func_args):
#                         yield response

#     except Exception as e:
#         log.error(f"{self.name}: {e}")
