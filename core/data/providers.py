import asyncio, os, openai, requests, json
from typing import List, Dict, Any


async def openai_chat(
    messages: List[Dict[str, str]], functions: List[Dict]
) -> Dict[str, Any]:
    """A wrapper for the OpenAI ChatCompletion call"""
    openai.api_key = os.environ["OPENAI_API_KEY"]
    logit_bias = {1102: -100, 4717: -100, 7664: -100}

    if openai.api_key is None:
        raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")

    response = await openai.ChatCompletion.acreate(
        model="gpt-4-0613",
        temperature=1.6,
        top_p=0.7,
        frequency_penalty=0.35,
        presence_penalty=0.35,
        logit_bias=logit_bias,
        messages=messages,
        functions=functions,
    )
    return response  # type: ignore


def get_news(topic: str = "world"):
    api_key = "7NKUxGlG9nEuayaoQXaCuqAVdHqbDmYf"
    url = f"https://api.nytimes.com/svc/topstories/v2/{topic}.json?api-key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)

    return response
