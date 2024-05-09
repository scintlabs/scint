from scint.support import interfaces, types, utils
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

Anthropic = AsyncAnthropic()
OpenAI = AsyncOpenAI()

config = {
    "server": {
        "host": "localhost",
        "port": 8000,
    },
    "search": {
        "configuration": {
            "meilisearch": {
                "host": "http://localhost:7700",
                "api_key": "myapikey",
                "index_name": "myindex",
            },
        },
    },
    "storage": {
        "configuration": {
            "rethinkdb": {
                "host": "localhost",
                "port": 28015,
                "db": "mydb",
                "table": "mytable",
            },
        },
    },
    "context": {
        "configuration": {
            "redis": {
                "host": "localhost",
                "port": 6379,
                "db": 0,
            },
        },
    },
}


intelligence = {
    "providers": {
        "openai": {
            "api_keys": [utils.envar("OPENAI_API_KEY")],
            "format": {
                "completion": {
                    "method": OpenAI.chat.completions.create,
                    "response_path": [["choices", "0", "message"]],
                    "models": {
                        "gpt4": "gpt-4",
                        "gpt4_turbo": "gpt-4-turbo",
                        "gpt35": "gpt-3.5-turbo",
                    },
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
                    "method": OpenAI.images.generate,
                    "response_path": [["data", "0", "url"]],
                    "models": {"dalle3": "dall-e-3"},
                    "parameters": {
                        "model": "dall-e-3",
                        "prompt": "string",
                        "quality": "hd",
                        "size": "1024x1024",
                        "n": 1,
                    },
                },
                "embedding": {
                    "method": OpenAI.embeddings.create,
                    "models": {
                        "embeddings_small": "text-embeddings-3-small",
                        "embeddings_large": "text-embeddings-3-large",
                    },
                    "response_path": [["data", "0", "embedding"]],
                    "parameters": {
                        "model": "string",
                        "input": None,
                    },
                },
                "audio": {},
            },
        },
        "anthropic": {
            "api_keys": [utils.envar("ANTHROPIC_API_KEY")],
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
        "balanced": {
            "model": "gpt-4",
            "temperature": 1.0,
            "top_p": 0.9,
            "presence_penalty": 0.25,
            "frequency_penalty": 0.25,
        },
        "deterministic": {
            "temperature": 0.3,
            "top_p": 1.2,
            "presence_penalty": 0.35,
            "frequency_penalty": 0.35,
        },
        "creative": {
            "model": "gpt-4-turbo",
            "temperature": 1.7,
            "top_p": 0.6,
            "presence_penalty": 0.75,
            "frequency_penalty": 0.75,
        },
        "classifier": {
            "model": "gpt-4",
            "temperature": 0.5,
            "top_p": 0.9,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
        },
        "images": {
            "quality": "hd",
            "size": "1024x1024",
        },
    },
}
