import sys, signal, subprocess, asyncio
import core.prompt as prompt
import core.definitions.types as types
from core.prompt import Prompt, meta_prompts
from core.generator import generate
from flask import Flask
from flask_restful import Api, Resource


validate = meta_prompts["validate"]
refactor = meta_prompts["refactor"]
sort = meta_prompts["sort"]
recurse = meta_prompts["recurse"]
diverge = meta_prompts["diverge"]

sentence = types.Fragment()
data = """"""


data = "Testing Python code."


source = asyncio.run(
    generate(
        data,
        sentence,
        prompts=[
            recurse["depth"],
            recurse["depth"],
            recurse["depth"],
        ],
    )
)

asyncio.run(
    generate(
        source,
        sentence,
        prompts=[
            validate["critique"],
            validate["rebuttal"],
            diverge["insight"],
            refactor["format"],
        ],
    )
)
