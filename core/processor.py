import json
import os
import subprocess
from typing import Any, Dict, List, Optional

from rich.markdown import Markdown

from core.providers.search import google
from core.state import APPDATA, State
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
    """Function to process code function calls from LLMs."""

    function_dict = dict(function_call)  # Parsing the JSON string
    function_name = function_dict["name"]
    function_args = function_dict["arguments"]  # This might still be a JSON string

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
