from tenacity import retry, stop_after_attempt, wait_fixed

from core.providers.models import openai
from core.handler import MessageHandler
from core.processor import eval_function
from util.logging import logger


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
async def init_chat(user_message):
    logger.info(f"Starting chat process.")

    try:
        handler = MessageHandler()
        messages, functions = await handler.build_manifest()  # type: ignore
        formatted_user_message = handler.format_message(user_message)
        messages.append(formatted_user_message)

        # Store user message in the database assuming response_id is not known at this point for user messages
        handler.store_message("user", user_message, None)

        response = await openai(messages, functions)  # type: ignore
        data = response["choices"][0]  # type: ignore
        reply = None

        try:
            if "content" in data["message"] and data["message"]["content"] is not None:
                reply = data["message"]["content"]
                logger.info(f"Response received: {reply}")
                messages.append({"role": "assistant", "content": f"{reply}"})  # type: ignore

            if (
                "function_call" in data["message"]
                and data["message"]["function_call"] is not None
            ):
                function_call = data["message"]["function_call"]
                function_results = await eval_function(function_call)
                results = await init_chat(f"{function_results}")  # type: ignore
                return results

            # Return the reply if it exists
            if reply:
                # Store assistant's message in the database
                handler.store_message(
                    "assistant", reply, response["id"]
                )  # Assuming response ID is present in the response
                return reply

        except Exception as e:
            logger.exception(f"There was a problem: {e}")
            raise

    except Exception as e:
        logger.exception(f"There was a problem delivering the message manifest: {e}")
        raise
