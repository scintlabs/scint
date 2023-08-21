from typing import Dict, List
from tenacity import retry, stop_after_attempt, wait_fixed
from core.data.providers import openai_chat
from core.prompt import Prompt
from core.definitions.functions import generate_code as functions


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def generate(message: str, prompts: List[Prompt]) -> List[Dict]:
    """
    Experimental function for mutating a string with multiple prompts
    """
    messages = []
    messages.append({"role": "system", "content": message})

    try:
        for prompt in prompts:
            prompt_content = prompt

            if len(messages) == 1:
                messages.insert(0, {"role": "system", "content": prompt_content})
            else:
                messages[0] = {"role": "system", "content": prompt_content}

            response = await openai_chat(messages, functions)
            data = response["choices"][0]

            generated = data["message"].get("content")
            messages.append({"role": "system", "content": f"{generated}."})
            print(f"{generated}")

        print(messages)
        return messages

    except Exception as e:
        raise


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def complete(message: str, prompt: List[Prompt]) -> str:
    """"""
    messages = []
    messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": message})
    response = await openai_chat(messages, functions)

    if response is None:
        raise ValueError("Error.")

    message = response["choices"][0]["message"].get("content")
    return message
