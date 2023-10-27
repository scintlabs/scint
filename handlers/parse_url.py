import subprocess

import asyncio

from core.message import Message
import asyncio


async def parse_url(url):
    try:
        cmd = ["bunx", "percollate", "md", url]

        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        stdout_text = stdout.decode("utf-8")
        stderr_text = stderr.decode("utf-8")

        if process.returncode != 0:
            print(f"Command failed with error: {stderr_text}")
            return None

        # Assuming the command returns the filename, read the file contents
        with open(stdout_text, "r") as file:
            file_contents = file.read()

        message_data = {
            "role": "system",
            "content": f"Here's the data for the requested URL:\n {file_contents}\n\n Summarize the data for the user.",
            "name": "parse_url",
        }

        return message_data

    except Exception as e:
        print(f"Error during subprocess execution or file reading: {e}")
        return None
