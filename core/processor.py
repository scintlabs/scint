import os, subprocess, json
from typing import Dict, List, Any, Optional
from core.state import State, APPDATA
from core.data.providers.search import google
from rich.markdown import Markdown
from util.logging import logger


async def parse_env():
    logger.info(f"Parsing environment.")

    try:
        logger.info(f"Running tree subprocess.")
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
    logger.info(f"Processing a function call.")

    function_dict = dict(function_call)  # Parsing the JSON string
    function_name = function_dict["name"]
    function_args = function_dict["arguments"]  # This might still be a JSON string

    # If function_args is a string, parse it
    if isinstance(function_args, str):
        function_args = json.loads(function_args)

    if function_name == "generate_code":
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
