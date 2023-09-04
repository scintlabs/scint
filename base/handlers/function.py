import json

from rich.markdown import Markdown
from base.providers.google import google

from util.logging import logger


async def eval_function(self, function_call):
    """Function for evaluating assistant function calls."""

    function_dict = dict(function_call)
    function_name = function_dict["name"]
    function_args = function_dict["arguments"]

    if isinstance(function_args, str):
        function_args = json.loads(function_args)

    if function_name == "classify_message":
        logger.info(f"Classifying message.")
        keywords = function_args.get("keywords")
        logger.info(f"Keywords: {keywords}")

    elif function_name == "generate_code":
        logger.info(f"Evaluating: {function_name}().")
        code = function_args.get("code")
        code_results = exec(code)
        print(Markdown(code))
        return code_results

    elif function_name == "google_search":
        logger.info(f"Evaluating: {function_name}().")
        query = function_args.get("query")
        search_results = await google(query)
        return search_results
