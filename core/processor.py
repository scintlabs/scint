import os, subprocess, json
from typing import Dict, List, Any, Optional
from util.logger import logger
from core.state import State

state = State()


async def parse_env():
    logger.info(f"Initializing environment.")
    state.process()
    """Function for parsing information from the files and directories in the sandbox."""
    current_dir = os.getcwd()

    if current_dir != state.APPDATA:
        try:
            os.chdir(state.APPDATA)
            dir_data: subprocess.CompletedProcess[str] = subprocess.run(
                ["tree", "-J", "--gitignore", "-L", "3"],
                capture_output=True,
                text=True,
                check=True,
            )

            return dir_data

            # TODO: if files in dirs, recursively extract comments/docstrings
            # overview = dir_data.stdout, file_data.stdout
            # return overview

        except subprocess.CalledProcessError:
            logger.exception("Error parsing environment data.")


async def parse_files():
    mode = "r+"
    with open(state.APPDATA, mode) as f:
        file_content = f.read()
        if file_content is not None:
            return file_content
        else:
            return "No file information available."


async def eval_function(function_call):
    function_name = function_call["name"]
    function_args = json.loads(function_call["arguments"])
    code = function_args.get("code")
    print(code)
    exec(code)


# async def eval_function(function_call):
#     pass

# function_name = function_call["name"]
# function_args = json.loads(function_call["arguments"])

# if function_name == "folders":
#     directory = function_args.get("dir_path")
#     if directory:
#         folders(directory)
#         print(os.getcwd())
#     else:
#         print("Directory path not provided.")

# elif function_name == "files":
#     file = function_args.get("filename")
#     if file:
#         await files(file, writable)
#     else:
#         print("Filename not provided.")

# else:
#     print(f"We got issues.")
