import contextlib
import json
import os
from pathlib import Path

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator

from scint.modules.logging import log


Anthropic = AsyncAnthropic()
OpenAI = AsyncOpenAI()


config = {
    "api": {
        "host": "localhost",
        "port": 8000,
    },
    "search": {
        "host": "localhost",
        "port": 7700,
        "api_key": "myapikey",
    },
    "storage": {
        "host": "localhost",
        "port": 28015,
        "db": "mydb",
    },
    "queue": {
        "host": "localhost",
        "port": 6379,
        "db": 0,
    },
}

extract = {
    "paths": [
        "/Users/kaechle/Documents",
        "/Users/kaechle/Developer",
    ]
}

parse = {
    "code": {
        "grammars": [
            "/Users/kaechle/.config/tree-sitter/tree-sitter-python",
            "/Users/kaechle/.config/tree-sitter/tree-sitter-swift",
            "/Users/kaechle/.config/tree-sitter/tree-sitter-javascript",
        ],
        "languages": {
            "python": {
                "grammar": "/Users/kaechle/.config/tree-sitter/tree-sitter-python",
                "build": "scint/data/etc/languages.so",
            },
            "swift": {
                "grammar": "/Users/kaechle/.config/tree-sitter/tree-sitter-swift",
                "build": "scint/data/etc/languages.so",
            },
            "javascript": {
                "grammar": "/Users/kaechle/.config/tree-sitter/tree-sitter-javascript",
                "build": "scint/data/etc/languages.so",
            },
        },
    }
}

search = {
    "indexes": {
        "people": "scint/core/lib/people.py",
        "prompts": "scint/core/lib/prompts.py",
        "functions": "scint/core/lib/functions.py",
        "events": "scint/core/lib/events.py",
        "notes": "scint/core/lib/notes.py",
        "links": "scint/core/lib/links.py",
    },
    "settings": {
        "features": {"vectorStore": True},
        "embedders": {
            "default": {
                "source": "openAi",
                "apiKey": "",
                "model": "text-embedding-3-small",
                "documentTemplate": "{{doc.description}}",
                "dimensions": 1536,
            }
        },
    },
}

intelligence = {
    "providers": {
        "openai": {
            "api_keys": [os.environ.get("OPENAI_API_KEY")],
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
                        "input": None,
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
            "model": "gpt-4o",
            "temperature": 0.4,
            "top_p": 1.2,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "response_format": {"type": "json_object"},
        },
        "balanced": {
            "model": "gpt-4o",
            "temperature": 1.4,
            "top_p": 0.6,
            "presence_penalty": 0.25,
            "frequency_penalty": 0.25,
            "response_format": {"type": "json_object"},
        },
        "creative": {
            "model": "gpt-4o",
            "temperature": 1.7,
            "top_p": 0.6,
            "presence_penalty": 0.45,
            "frequency_penalty": 0.45,
            "response_format": {"type": "json_object"},
        },
        "classifier": {
            "model": "gpt-4o",
            "temperature": 1.0,
            "top_p": 1.0,
            "presence_penalty": 0.3,
            "frequency_penalty": 0.3,
            "response_format": {"type": "json_object"},
        },
        "embedding": {"model": "text-embeddings-3-small"},
        "images": {
            "quality": "hd",
            "size": "1024x1024",
            "n": 1,
            "style": "vibrant",
        },
    },
}


class Settings(BaseSettings):
    CONFIG_PATH: str = ""
    REDIS_URL: str = None
    MEILISEARCH_URL: str = None
    RETHINKDB_URL: str = None
    INDEXES: dict = {}
    CONTEXT: dict = {}
    PROVIDERS: dict = {}
    PRESETS: dict = {}

    @field_validator("CONFIG_PATH")
    def set_config_path(cls, value):
        return value

    class Config:
        env_prefix = "SCINT_"
        validate_assignment = True
        extra = "ignore"

    @field_validator("REDIS_URL")
    def set_redis_url(cls, value):
        return value

    @field_validator("RETHINKDB_URL")
    def set_rethink_url(cls, value):
        return value

    @field_validator("INDEXES")
    def set_indexes(cls, value):
        return value

    @field_validator("CONTEXT")
    def set_context(cls, value):
        return value

    @model_validator(mode="after")
    def validate_lists(cls, values):
        for key, value in values.items():
            if key != "dev" and not value:
                values[key] = []

        return values

    def update_settings(self, file_path: str, dev: bool = False):
        new_settings = load_settings(file_path)
        self.CONFIG_PATH = new_settings.CONFIG_PATH or {}
        self.DATA_PATH = new_settings.DATA_PATH or {}
        self.RETHINKDB_URL = new_settings.POSTGRES_URL or {}
        self.MEILISEARCH_URL = new_settings.REDIS_URL or {}
        self.REDIS_URL = new_settings.REDIS_URL or {}
        self.LOADERS = new_settings.LOADERS or {}
        self.INDEXES = new_settings.INDEXES or {}
        self.PROVIDERS = new_settings.PROVIDERS or {}
        self.PRESETS = new_settings.PRESETS or {}

    def update_settings(self, **kwargs):
        log.info("Updating settings")
        for key, value in kwargs.items():
            if not hasattr(self, key):
                log.info(f"Key {key} not found in settings")
                continue

            log.debug(f"Updating {key}")
            if isinstance(getattr(self, key), list):
                with contextlib.suppress(json.decoder.JSONDecodeError):
                    value = json.loads(str(value))
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, Path):
                            item = str(item)
                        if item not in getattr(self, key):
                            getattr(self, key).append(item)
                    log.debug(f"Extended {key}")

                else:
                    if isinstance(value, Path):
                        value = str(value)
                    if value not in getattr(self, key):
                        getattr(self, key).append(value)
                        log.debug(f"Appended {key}")

            else:
                setattr(self, key, value)
                log.info(f"Updated {key}")
            log.info(f"{key}: {getattr(self, key)}")


def save_settings(settings: Settings, file_path: str):
    with open(file_path, "w") as f:
        settings_dict = settings.model_dump()
        json.dump(settings_dict, f)


def load_settings(file_path: str) -> Settings:
    if "/" not in file_path:
        current_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_path, file_path)

    with open(file_path, "r") as f:
        settings_dict = json.load(f)
        settings_dict = {k.upper(): v for k, v in settings_dict.items()}

        for key in settings_dict:
            if key not in Settings.model_fields.keys():
                raise KeyError(f"Key {key} not found in settings")
            log.debug(f"Loading {len(settings_dict[key])} {key} from {file_path}")

    return Settings(**settings_dict)
