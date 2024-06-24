import contextlib
import json
import os
from pathlib import Path

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings

from scint.support.logging import log
from scint.support.types import Any, Dict
from scint.support.utils import dictorial, env

Anthropic = AsyncAnthropic()
OpenAI = AsyncOpenAI()


base = {
    "api": {
        "host": "localhost",
        "port": 8000,
    },
    "search": {
        "indexes": {
            "messages": "scint/core/lib/messages.py",
            "functions": "scint/core/lib/functions.py",
        },
        "settings": {
            "features": {"vectorStore": True},
            "embedders": {
                "default": {
                    "source": "openai",
                    "apiKey": env("OPENAI_API_KEY"),
                    "model": "text-embedding-3-small",
                    "documentTemplate": "{{doc.description}}",
                    "dimensions": 1536,
                }
            },
        },
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


# class Settings(BaseSettings):
#     CONFIG_PATH: str = ""
#     REDIS_URL: str = "localhost"
#     MEILISEARCH_URL: str = "localhost"
#     RETHINKDB_URL: str = "localhost"
#     INDEXES: dict = {}
#     CONTEXT: dict = {}
#     PROVIDERS: dict = {}
#     PRESETS: dict = {}

#     @field_validator("CONFIG_PATH")
#     def set_config_path(cls, value):
#         return value

#     class Config:
#         env_prefix = "SCINT_"
#         validate_assignment = True
#         extra = "ignore"

#     @field_validator("REDIS_URL")
#     def set_redis_url(cls, value):
#         return value

#     @field_validator("RETHINKDB_URL")
#     def set_rethink_url(cls, value):
#         return value

#     @field_validator("INDEXES")
#     def set_indexes(cls, value):
#         return value

#     @field_validator("CONTEXT")
#     def set_context(cls, value):
#         return value

#     @model_validator(mode="after")
#     def validate_lists(cls, values):
#         for key, value in values.items():
#             if key != "dev" and not value:
#                 values[key] = []

#         return values

#     def update_settings(self, **kwargs):
#         log.info("Updating settings")
#         for key, value in kwargs.items():
#             if not hasattr(self, key):
#                 log.info(f"Key {key} not found in settings")
#                 continue

#             log.debug(f"Updating {key}")
#             if isinstance(getattr(self, key), list):
#                 with contextlib.suppress(json.decoder.JSONDecodeError):
#                     value = json.loads(str(value))
#                 if isinstance(value, list):
#                     for item in value:
#                         if isinstance(item, Path):
#                             item = str(item)
#                         if item not in getattr(self, key):
#                             getattr(self, key).append(item)
#                     log.debug(f"Extended {key}")

#                 else:
#                     if isinstance(value, Path):
#                         value = str(value)
#                     if value not in getattr(self, key):
#                         getattr(self, key).append(value)
#                         log.debug(f"Appended {key}")

#             else:
#                 setattr(self, key, value)
#                 log.info(f"Updated {key}")
#             log.info(f"{key}: {getattr(self, key)}")


# def save_settings(settings: Settings, file_path: str):
#     with open(file_path, "w") as f:
#         settings_dict = settings.model_dump()
#         json.dump(settings_dict, f)


# def load_settings(file_path: str) -> Settings:
#     if "/" not in file_path:
#         current_path = os.path.dirname(os.path.abspath(__file__))
#         file_path = os.path.join(current_path, file_path)

#     with open(file_path, "r") as f:
#         settings_dict = json.load(f)
#         settings_dict = {k.upper(): v for k, v in settings_dict.items()}

#         for key in settings_dict:
#             if key not in Settings.model_fields.keys():
#                 raise KeyError(f"Key {key} not found in settings")
#             log.debug(f"Loading {len(settings_dict[key])} {key} from {file_path}")

#     return Settings(**settings_dict)
