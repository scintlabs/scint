import asyncio, json, logging
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import Dict, Any, Tuple, List, Optional
from core.data.providers import openai_chat
from core.prompt import Prompt
from core.function import generate_function


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def generate(message: str, cls, prompts: List[Prompt]) -> List[Dict]:
    """"""
    result = []
    messages = []
    messages.append({"role": "system", "content": message})
    iterations = 0
    tasks = len(prompts)

    try:
        for prompt in prompts:
            prompt_content = prompt

            if len(messages) == 1:
                messages.insert(0, {"role": "system", "content": prompt_content})
            else:
                messages[0] = {"role": "system", "content": prompt_content}

            response = await openai_chat(messages)
            data = response["choices"][0]
            generated = data["message"].get("content")
            result += f"{generated} \n"
            messages.append({"role": "system", "content": generated})
            iterations += 1
            print(f"Completed task {iterations} of {tasks}\n")

        print(f"{result}\n")
        return result

    except Exception as e:
        logging.error(f"There was a problem contacting the API: {e}")
        raise
