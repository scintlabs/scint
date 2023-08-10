import asyncio, json, logging
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import Dict, Any, Tuple, List, Optional, Coroutine
from core.data.providers import openai_chat
from core.prompt import Prompt
from core.function import eval_function


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def complete(message: str):
    """"""

    consg = ""
    messages = []
    messages.append({"role": "system", "content": "You are a friendly assistant."})
    messages.append({"role": "user", "content": message})

    try:
        response = await openai_chat(messages)

        if response is None:
            raise ValueError("Error.")

        try:
            data = response
            print(data)

        except Exception as e:
            logging.error(f"There was a problem: {e}")
            raise

    except Exception as e:
        logging.error(f"There was a problem contacting the API: {e}")
        raise
