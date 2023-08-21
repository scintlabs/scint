import asyncio, os, env, openai, requests, json
from typing import List, Dict, Any
from googleapiclient.discovery import build

google_api_key = "AIzaSyABuLAz5vgY6Xy1K8CWgONWmZIclIw0rqw"
custom_search_id = "66ac278048c154f5f"


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res["items"]


results = google_search("openai jobs", google_api_key, custom_search_id, num=10)

for result in results:
    print(result)


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


def nytimes_newsfeed(topic: str = "world"):
    api_key = "7NKUxGlG9nEuayaoQXaCuqAVdHqbDmYf"
    url = f"https://api.nytimes.com/svc/topstories/v2/{topic}.json?api-key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)

    return response
