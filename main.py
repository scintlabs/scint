import sys
import signal
import subprocess
import asyncio
from rich.console import Console

# from core.collaborator import send_request, get_response, eval_function
from core.generator import generate
from core.definitions.prompts import (
    Prompt,
    validate,
    refactor,
    sort,
    recurse,
    diverge,
)
from core.definitions.text import (
    Sentence,
    Paragraph,
    Title,
    Subtitle,
    Paragraph,
    Document,
)
from core.definitions.functions import generate_function


sentence = Sentence()
data = "I need to come up with a way to make lots and lots of money quickly."

source = asyncio.run(
    generate(
        data,
        sentence,
        prompts=[
            recurse["depth"],
            recurse["depth"],
            recurse["depth"],
            sort["categorize"],
            recurse["breadth"],
            validate["doubt"],
            validate["assurance"],
            diverge["abstract"],
            recurse["breadth"],
            validate["critique"],
            validate["rebuttal"],
            diverge["insight"]

        ],
    )
)

# outline = asyncio.run(
#     generate(
#         source,
#         sentence,
#         prompts=[
#     ])
# )










# console = Console()
# exit_commands = ["/quit"]


# def get_input():
#     q = console.input("\n❯ ")
#     return q


# def save_and_exit(signal, frame):
#     print("Exiting.")
#     sys.exit(0)


# signal.signal(signal.SIGINT, save_and_exit)
# signal.signal(signal.SIGTERM, save_and_exit)


# # async def main():
# #     user_message = get_input()

# #     while user_message not in exit_commands:
# #         if user_message.startswith("/cmd"):
# #             command = user_message[5:]
# #             process = subprocess.Popen(
# #                 command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
# #             )
# #             output, error = process.communicate()
# #             output_text = output.decode()
# #             error_text = error.decode()

# #             if output_text:
# #                 console.print(f"\n{output_text}\n")
# #                 response = await get_response(await send_request(output_text))
# #             elif error_text:
# #                 console.print(f"\n{error_text}\n")
# #                 response = await get_response(await send_request(error_text))

# #         response = await get_response(await send_request(user_message))
# #         console.print(f"\n❯❯ {response} \n")
# #         user_message = get_input()


# if __name__ == "__main__":
#     asyncio.run(main())
