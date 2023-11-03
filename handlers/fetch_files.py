import os
import aiofiles


async def fetch_files(directory, filename=None):
    if not os.path.isdir(directory):
        return {
            "role": "system",
            "content": "The specified directory does not exist.",
            "name": "fetch_files",
        }

    if filename:
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            async with aiofiles.open(file_path, "r") as file:
                content = await file.read()

            return {
                "role": "system",
                "content": f"{content}",
                "name": "fetch_files",
            }

        else:
            return {
                "role": "system",
                "content": f"The file {filename} does not exist in the given directory.",
                "name": "fetch_files",
            }

    else:
        files = os.listdir(directory)
        return {
            "role": "system",
            "content": f"{files}",
            "name": "fetch_files",
        }
