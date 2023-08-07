import sys, signal, subprocess, asyncio
import core.prompt as prompt
import core.definitions.content as content
from core.prompt import Prompt, prompts
from core.generator import generate
from flask import Flask
from flask_restful import Api, Resource


validate = prompts["validate"]
refactor = prompts["refactor"]
sort = prompts["sort"]
recurse = prompts["recurse"]
diverge = prompts["diverge"]

sentence = content.Sentence()


data = "Testing Python code."
print(validate["critique"])
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
        prompts=[validate["critique"], validate["rebuttal"], diverge["insight"]],
    )
)
