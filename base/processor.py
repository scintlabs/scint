import os, json, subprocess

from rich.markdown import Markdown

from base.providers.search import google
from base.state import APPDATA, StateManager
from util.logging import logger


async def parse_dir():
    """Function to parse the current working directory."""
    logger.info(f"Parsing environment.")
    try:
        dir_data: subprocess.CompletedProcess[str] = subprocess.run(
            ["tree", "-J", "--gitignore", "-L", "3", APPDATA],
            capture_output=True,
            text=True,
            check=True,
        )

        return dir_data

    except subprocess.CalledProcessError as e:
        logger.exception(f"Error parsing environment: {e}")


async def parse_files():
    """Function to parse files."""
    logger.info(f"Parsing files.")
    file_path = os.path.join(APPDATA, "filename")
    mode = "r+"
    with open(file_path, mode) as f:
        file_content = f.read()
        if file_content:
            return file_content
        else:
            return "No file information available."


async def eval_function(function_call):
    """
    Function for handling the assistant's function calls.
    """

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
