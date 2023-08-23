import asyncio, os
from openai import ChatCompletion, api_key
from util.env import envar
from typing import List, Dict

envar = lambda var: os.environ.get(var)
api_key = envar("OPENAI_API_KEY")


async def openai(messages: List[Dict[str, str]], functions: List[Dict]):
    """A wrapper for the OpenAI ChatCompletion call"""

    logit_bias = {1102: -100, 4717: -100, 7664: -100}

    if api_key is None:
        raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")

    response = await ChatCompletion.acreate(
        model="gpt-4-0613",
        temperature=1.6,
        top_p=0.7,
        frequency_penalty=0.35,
        presence_penalty=0.35,
        logit_bias=logit_bias,
        messages=messages,
        functions=functions,
    )
    return response
