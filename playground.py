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

fragment = types.Fragment()

data = "I'm conducting a test. Please rewrite this paragraph: In my view, the hybrid approach might be the most effective for someone with your diverse skill set. By emphasizing a few core competencies where you excel, while also subtly showcasing your versatility, you can appeal to clients who want both depth and breadth."

source = asyncio.run(
    generate(
        data,
        fragment,
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
        fragment,
        prompts=[
            validate["critique"],
            validate["rebuttal"],
            diverge["insight"],
            refactor["format"],
        ],
    )
)
