import asyncio, json, logging
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import Dict, Any, Tuple, List, Optional
from core.data.providers import openai_chat
from core.prompt import Prompt
from core.function import generate_function


logging.basicConfig(level=logging.ERROR)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def generate(message: str, cls, prompts: List[Prompt]) -> List[Dict]:
    result = []
    messages = []
    messages.append({"role": "system", "content": message})
    iterations = 0
    tasks = len(prompts)
    # functions = generate_function(cls)

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


# @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
# async def send(message: str, prompts: List[Prompt]) -> Dict[List[str], Any]:
#     """Generator for producing content with functional prompts"""
#     result = {}
#     messages = []
#     messages.append({"role": "system", "content": message})
#     iterations = 0
#     tasks = len(prompts)
#     # functions = generate_function(cls)

#     try:
#         for prompt in prompts:
#             prompt_content = prompt

#             if len(messages) == 1:
#                 messages.insert(0, {"role": "system", "content": prompt_content})
#             else:
#                 messages[0] = {"role": "system", "content": prompt_content}

#             response: Dict[str, Any] = await openai_chat(messages)
#             data = response["choices"][0]
#             generated = data["message"].get("content")
#             result.append(f"{generated} \n")
#             messages.append({"role": "system", "content": generated})
#             iterations += 1
#             print(f"Completed task {iterations} of {tasks}\n")

#         return result

#     except Exception as e:
#         logging.error(f"There was a problem contacting the API: {e}")
#         raise


async def receive(
    response: Dict[str, Any]
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    message_log = []

    if response is None:
        raise ValueError("Response cannot be None")

    try:
        message = response["choices"][0].get("message")
        message_content = message.get("content")
        function_call = message.get("function_call")
    except Exception as e:
        logging.error(f"There was a problem: {e}")
        raise

    if function_call is not None:
        await eval_function(function_call)
        message_log.append(
            {
                "message": [message_content],
                "function_call": [function_call],
            }
        )

    return message_content


async def eval_function(function: Dict[str, Any]) -> Optional[str]:
    function_name = function["name"]
    function_arguments = function["arguments"]
    data = json.loads(function_arguments)
    content = data.get("content")

    if data.get("function_call"):
        content = await eval_function(data)

    return content
