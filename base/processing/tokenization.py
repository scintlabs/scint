import tiktoken


def rolling_token_count(data):
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    prompt_tokens += data["prompt_tokens"]
    completion_tokens += data["completion_tokens"]
    total_tokens += data["total_tokens"]
    return print(f"{prompt_tokens} + {completion_tokens} = {total_tokens}")


def thread_token_count(messages):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    tokens_per_message = 0
    tokens_per_name = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens
