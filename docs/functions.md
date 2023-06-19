# OpenAI API Responses

## Normal chat response

```json
{
  "id": "chatcmpl-7N0FJOzt39aSSK1BQhd1yBUpg7baR",
  "object": "chat.completion",
  "created": 1685716845,
  "model": "gpt-4",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 12,
    "total_tokens": 22
  },
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello to you too! How may I assist you today?"
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```

## Chat response with function call

```json
{
  "id": "chatcmpl-7N0FJOzt39aSSK1BQhd1yBUpg7baR",
  "object": "chat.completion",
  "created": 1685716845,
  "model": "gpt-4",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 12,
    "total_tokens": 22
  },
  "choices": [
    {
      "finish_reason": "function_call",
      "index": 0,
      "message": {
        "content": null,
        "function_call": {
          "arguments": "{\n  \"code\": \"import time\\n\\ntime.sleep(300)  # sleep for 300 seconds, which is 5 minutes\\nprint(\\\"Hey Tim, it's time to go to bed!\\\")\"\n}",
          "name": "execute_python_code"
        },
        "role": "assistant"
      }
    }
  ]
}
```

```json
{
  "finish_reason": "function_call",
  "index": 0,
  "message": {
    "content": null,
    "function_call": {
      "arguments": "{\n  \"code\": \"import time\\n\\ntime.sleep(300)  # sleep for 300 seconds, which is 5 minutes\\nprint(\\\"Hey Tim, it's time to go to bed!\\\")\"\n}",
      "name": "execute_python_code"
    },
    "role": "assistant"
  }
}