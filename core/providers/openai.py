import os
import openai


openai.api_key = os.environ["OPENAI_API_KEY"]
logit_bias = {1102: -100, 4717: -100, 7664: -100}

if openai.api_key is None:
    raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")

config = {
    "model": "gpt-4-0613",
    "temperature": 1.8,
    "top_p": 0.5,
    "frequency_penalty": 0.2,
    "presence_penalty": 0.2,
    "logit_bias": {1102: -100, 4717: -100, 7664: -100},
}


def gpt(messages, functions):
    return openai.ChatCompletion.create(
        model="gpt-4-0613",
        temperature=1.7,
        top_p=0.5,
        frequency_penalty=0.2,
        presence_penalty=0.2,
        logit_bias=logit_bias,
        messages=messages,
        functions=functions,
    )


{
    "id": "chatcmpl-7N0FJOzt39aSSK1BQhd1yBUpg7baR",
    "object": "chat.completion",
    "created": 1685716845,
    "model": "gpt-4",
    "usage": {"prompt_tokens": 10, "completion_tokens": 12, "total_tokens": 22},
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "Hello to you too! How may I assist you today?",
            },
            "finish_reason": "stop",
            "index": 0,
        }
    ],
}

{
    "events": {
        "id": 1685716845,
        "preceeds": 1685716844,
        "type": "assistant_message",
        "values": {
            "context": [],
            "message": "Hello to you too! How may I assist you today?",
        },
    }
}
