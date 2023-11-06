import os
import aiofiles

from core.util import format_message


async def file_operations(directory, filename=None, create_new=False):
    if not os.path.isdir(directory):
        return format_message(
            "system", "The specified directory does not exist.", "file_operations"
        )

    if filename:
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            if create_new:
                return format_message(
                    "system",
                    f"The file {filename} already exists. Cannot create a new one.",
                    "file_operations",
                )
            else:
                async with aiofiles.open(file_path, "r") as file:
                    content = await file.read()

                return format_message("system", f"{content}", "file_operations")
        else:
            if create_new:
                async with aiofiles.open(file_path, "w") as file:
                    await file.write("")

                return format_message(
                    "system",
                    f"The file {filename} has been created.",
                    "file_operations",
                )

            else:
                return format_message(
                    "system",
                    f"The file {filename} does not exist in the given directory.",
                    "file_operations",
                )

    else:
        files = os.listdir(directory)
        return format_message(
            "system",
            f"{files}",
            "file_operations",
        )
