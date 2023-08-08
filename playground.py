import sys, signal, subprocess, asyncio
import core.prompt as prompt
import core.definitions.content as content
from core.prompt import Prompt, meta_prompts
from core.generator import generate
from flask import Flask
from flask_restful import Api, Resource


validate = meta_prompts["validate"]
refactor = meta_prompts["refactor"]
sort = meta_prompts["sort"]
recurse = meta_prompts["recurse"]
diverge = meta_prompts["diverge"]

sentence = content.Sentence()
data = """"""

# generate some shit based on the input
# source = asyncio.run(
#     generate(
#         data,
#         sentence,
#         prompts=[
#             recurse["depth"],
#             recurse["depth"],
#             recurse["breadth"],
#             recurse["depth"],
#         ],
#     )
# )


source = asyncio.run(
    generate(
        data,
        sentence,
        prompts=[
            refactor["prune"],
            refactor["clarify"],
            refactor["format"],
        ],
    )
)

source = asyncio.run(generate(source, sentence, prompts=[diverge["insight"]]))
