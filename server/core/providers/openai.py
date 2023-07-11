import os
import openai


openai.api_key = os.environ["OPENAI_API_KEY"]
logit_bias = {1102: -100, 4717: -100, 7664: -100}

if openai.api_key is None:
    raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")


def api_call(messages, functions):
    return openai.ChatCompletion.create(
        model="gpt-4-0613",
        temperature=1.8,
        top_p=0.5,
        frequency_penalty=0.2,
        presence_penalty=0.2,
        logit_bias=logit_bias,
        messages=messages,
        functions=functions,
        stream=False
    )