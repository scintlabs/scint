import os
import aiofiles

from core.memory import Message


async def file_manager(directory, filename=None, create_new=False):
    if not os.path.isdir(directory):
        return Message(
            "system", "The specified directory does not exist.", "file_manager"
        )

    if filename:
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            if create_new:
                return Message(
                    "system",
                    f"The file {filename} already exists. Cannot create a new one.",
                    "file_manager",
                )
            else:
                async with aiofiles.open(file_path, "r") as file:
                    content = await file.read()

                return Message("system", f"{content}", "file_manager")
        else:
            if create_new:
                async with aiofiles.open(file_path, "w") as file:
                    await file.write("")

                return Message(
                    "system",
                    f"The file {filename} has been created.",
                    "file_manager",
                )

            else:
                return Message(
                    "system",
                    f"The file {filename} does not exist in the given directory.",
                    "file_manager",
                )

    else:
        files = os.listdir(directory)
        return Message(
            "system",
            f"{files}",
            "file_manager",
        )
