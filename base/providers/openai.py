import os, math
from typing import List, Dict

from openai import ChatCompletion, Embedding

from base.definitions.types import Message
from conf.base import logit_bias, ASSISTANT
from util.env import envar
from util.logging import logger


async def chat(messages: List[Dict[str, str]], functions: List[Dict]):
    api_key = envar("OPENAI_API_KEY")

    if api_key is None:
        logger.error("This action requires an OpenAI API key.")
        raise ValueError("The environment variable 'OPENAI_API_KEY' is not set.")

    response = await ChatCompletion.acreate(
        model="gpt-4-0613",
        temperature=1.7,
        top_p=0.5,
        frequency_penalty=0.35,
        presence_penalty=0.35,
        logit_bias=logit_bias,
        messages=messages,
        functions=functions,
    )

    message_response = Message(author=ASSISTANT, content="")
    message_function = None

    try:
        data = response["choices"][0]
        if "content" in data["message"]:
            if data["message"]["content"] is not None:
                content = str(data["message"]["content"])
                message_response.content = content

        if "function_call" in data["message"]:
            if data["message"]["function_call"] is not None:
                message_function = data["message"]["function_call"]

        if message_response and message_function is not None:
            return message_response, message_function
        elif message_response is not None:
            return message_response
        else:
            logger.exception(f"There was a problem delivering the message.")
            raise

    except Exception as e:
        logger.exception(f"There was a problem delivering the message: {e}")
        raise


async def embeddings(data):
    response = await Embedding.create(
        model="text-embedding-ada-002", input="Hello world!"
    )

    embeddings = response["data"][0]["embedding"]

    return embeddings
