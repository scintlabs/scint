console = Console()
exit_commands = ["/quit"]


def get_input():
    q = console.input("\n❯ ")
    return q


def save_and_exit(signal, frame):
    print("Exiting.")
    sys.exit(0)


signal.signal(signal.SIGINT, save_and_exit)
signal.signal(signal.SIGTERM, save_and_exit)


async def cli():
    user_message = get_input()

    while user_message not in exit_commands:
        if user_message.startswith("/cmd"):
            command = user_message[5:]
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output, error = process.communicate()
            output_text = output.decode()
            error_text = error.decode()

            if output_text:
                console.print(f"\n{output_text}\n")
                response = await get_response(await send_request(output_text))
            elif error_text:
                console.print(f"\n{error_text}\n")
                response = await get_response(await send_request(error_text))

        response = await get_response(await send_request(user_message))
        console.print(f"\n❯❯ {response} \n")
        user_message = get_input()


if __name__ == "__cli__":
    asyncio.run(cli())
