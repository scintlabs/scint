# from __future__ import annotations

# import json

# from attrs import asdict, field

# from src.base.intelligence import ModelConfig
# from src.base.records import Message, Metadata, Result
# from src.base.protocol import protocol


# async def generate_meta(self):
#     res = await oai.responses.create(
#         input=f"Generate concise, intelligent, semantically-rich metadata for the following thread:\n\n{await self.render()}",
#         text={"format": self.serialize(Metadata)},
#         model="gpt-4.1",
#     )
#     for obj in res.output:
#         if obj.type == "message":
#             for content in obj.content:
#                 text = json.loads(content.text)
#                 return Metadata(**text)


# async def generate(self):
#     async def build_request(context):
#         ctx = await context.render()
#         await self.tools.search_tools(ctx)
#         return {
#             "input": ctx,
#             "instructions": self.instructions.content,
#             "text": {"format": self.serialize(self.format)},
#             "tools": self.tools.tools,
#             **asdict(self.config),
#         }

#     async def create_response(req):
#         res = await oai.responses.create(**req)
#         async for res in parse_response(res):
#             yield res

#     async def parse_response(res):
#         for obj in res.output:
#             if obj.type == "message":
#                 async for msg in handle_message(obj):
#                     yield msg
#             elif obj.type == "function_call":
#                 async for call_res in handle_tool_call(obj):
#                     yield call_res

#     async def handle_message(message):
#         for obj in message.content:
#             yield Message(**json.loads(obj.text))

#     async def handle_tool_call(tool_call):
#         for func in self.tools:
#             if tool_call.name == func.__name__:
#                 args = json.loads(tool_call.arguments)
#                 res = await func(**args)
#                 yield Result(tool_call.call_id, tool_call.name, str(res))

#     req = await build_request(self.context)
#     async for res in create_response(req):
#         await self.context.update(res)
#         yield res


# agentic_attrs = {
#     # "tools": field(type=Harness, default=Harness()),
#     "config": field(type=ModelConfig, default=ModelConfig()),
# }
# agentic_interfaces = [generate, generate_meta]
# agentic = protocol("agentic", agentic_attrs, agentic_interfaces, data=True)
