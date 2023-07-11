from core.providers.openai import api_call
import os
import json

GPT4 = "gpt-4"
MAX_TOKENS = 7000
MIN_TOKENS = MAX_TOKENS / 2.5

def token_counts(data):
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    prompt_tokens += data["prompt_tokens"]
    completion_tokens += data["completion_tokens"]
    total_tokens += data["total_tokens"]
    return print(f"This discussion has used {prompt_tokens} tokens for prompts and {completion_tokens} for completions, for a grand total of {total_tokens} tokens.")


def tokenizer(messages, model=None):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif "gpt-3.5-turbo" in model:
        return tokenizer(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        return tokenizer(messages, model="gpt-4-0613")

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens


def manage_buffers():
    global message_buffer, secondary_message_buffer
       
    if tokenizer(message_buffer, gpt4) > MAX_TOKENS:
        while tokenizer(message_buffer, gpt4) > MAX_TOKENS / 2.5:        
            secondary_message_buffer.append(message_buffer.pop(0))
            with open('secondary_buffer.json', 'w') as f:            
                json.dump(secondary_message_buffer, f)        
                manage_buffers()


def save_conversation(Fself):
    data = {
        'message_buffer': message_buffer,
        'secondary_message_buffer': secondary_message_buffer
    }
    with open('conversation_history.json', 'w') as f:
        json.dump(data, f)
