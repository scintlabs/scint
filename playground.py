import sys, signal, subprocess, asyncio
import core.prompt as prompt
import core.definitions.types as types
from core.prompt import Prompt, meta_prompts
from core.generator import generate
from core.completer import complete
from flask import Flask
from flask_restful import Api, Resource


validate = meta_prompts["validate"]
refactor = meta_prompts["refactor"]
sort = meta_prompts["sort"]
recurse = meta_prompts["recurse"]
diverge = meta_prompts["diverge"]

message = ""


asyncio.run(
    generate(
        message,
        prompts=[
            diverge["chaos"],
        ],
    )
)

# asyncio.run(
#     generate(
#         source,  # type: ignore
#         fragment,
#         prompts=[
#             validate["critique"],
#             validate["rebuttal"],
#             sort["task"],
#             sort["prioritize"],
#         ],
#     )
# )
