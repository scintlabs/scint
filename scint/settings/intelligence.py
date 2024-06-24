import os

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from scint.support.utils import dictorial, env

Anthropic = AsyncAnthropic()
OpenAI = AsyncOpenAI()


intelligence_config = {
    "providers": {
        "openai": {
            "api_keys": [env("OPENAI_API_KEY")],
            "module": AsyncOpenAI(),
            "response_paths": [
                "choices.0.message.content",
                "choices.0.message.tool_calls",
                "choices.0.data",
            ],
            "format": {
                "completion": {
                    "models": {
                        "gpt4o": "gpt-4o",
                        "gpt4": "gpt-4",
                        "gpt35": "gpt-3.5-turbo",
                    },
                    "method": OpenAI.chat.completions.create,
                    "parameters": {
                        "model": "string",
                        "temperature": 1.0,
                        "top_p": 0.9,
                        "presence_penalty": 0.25,
                        "frequency_penalty": 0.25,
                        "logprobs": False,
                        "top_logprobs": 0,
                        "stream": False,
                        "stop": None,
                        "seed": None,
                        "messages": [],
                        "tools": [],
                        "tool_choice": {},
                        "response_format": "JSON",
                    },
                },
                "image": {
                    "models": {"dalle3": "dall-e-3"},
                    "method": OpenAI.images.generate,
                    "parameters": {
                        "model": "dall-e-3",
                        "prompt": "string",
                        "quality": "hd",
                        "size": "1024x1024",
                        "n": 1,
                    },
                },
                "speech": {
                    "models": {"tts-1", "tts-1-hd"},
                    "method": OpenAI.audio.speech.create,
                    "parameters": {
                        "model": "string",
                        "input": "string",
                        "voice": "string",
                        "response_format": "string",
                        "speed": 1.0,
                    },
                },
                "embedding": {
                    "models": {
                        "embeddings_small": "text-embeddings-3-small",
                        "embeddings_large": "text-embeddings-3-large",
                    },
                    "method": OpenAI.embeddings.create,
                    "parameters": {
                        "model": "string",
                        "input": "string",
                    },
                },
            },
        },
        "anthropic": {
            "api_keys": [os.environ.get("ANTHROPIC_API_KEY")],
            "format": {
                "method": Anthropic.completions.create,
                "completions": {
                    "models": {
                        "claude3_opus": "claude-3-opus-20240229",
                    },
                    "parameters": {
                        "model": "string",
                        "temperature": 1.0,
                    },
                },
            },
        },
    },
    "presets": {
        "deterministic": {
            "model": "gpt-4",
            "temperature": 0.4,
            "top_p": 1.2,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "response_format": {"type": "json_object"},
        },
        "balanced": {
            "model": "gpt-4",
            "temperature": 1.4,
            "top_p": 0.6,
            "presence_penalty": 0.25,
            "frequency_penalty": 0.25,
            "response_format": {"type": "json_object"},
        },
        "creative": {
            "model": "gpt-4",
            "temperature": 1.7,
            "top_p": 0.6,
            "presence_penalty": 0.45,
            "frequency_penalty": 0.45,
            "response_format": {"type": "json_object"},
        },
        "router": {
            "model": "gpt-4o",
            "temperature": 0.5,
            "top_p": 1.4,
            "presence_penalty": 2.0,
            "frequency_penalty": 2.0,
            "tool_choice": {"type": "function", "function": {"name": "route_message"}},
            "response_format": {"type": "json_object"},
        },
        "image": {
            "quality": "hd",
            "size": "1024x1024",
            "n": 1,
            "style": "vibrant",
        },
        "embedding": {"model": "text-embeddings-3-small"},
    },
}
