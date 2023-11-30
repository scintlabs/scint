import os

from core.util import envar
from xdg_base_dirs import xdg_data_home

# data
APPNAME: str | os.PathLike = "scint"
APPDATA = os.path.join(xdg_data_home(), APPNAME)
LOGS = os.path.join(APPDATA, "logs")

# external api keys and tokens
OPENAI_API_KEY: str | None = envar("OPENAI_API_KEY")
DISCORD_SCINT_TOKEN: str | None = envar("SCINT_DISCORD_TOKEN")
OPENWEATHER_API_KEY = envar("OPENWEATHER_API_KEY")
GOOGLE_API_KEY = envar("GOOGLE_API_KEY")
CUSTOM_SEARCH_ID = envar("CUSTOM_SEARCH_ID")

# openai models
GPT4 = "gpt-4-1106-preview"
GPT3 = "gpt-3.5-turbo"
GPT3_16K = "gpt-3.5-turbo-16k"
ADA2 = "text-embedding-ada-002"

# internal api endpoints
API_CHAT_ENDPOINT = "http://localhost:8080/chat"

# default
DEFAULT_CONFIG = {
    "model": GPT4,
    "temperature": 0,
    "top_p": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "function_call": "auto",
}
PERSONA_CONFIG = {
    "model": GPT4,
    "temperature": 1.8,
    "top_p": 0.4,
    "presence_penalty": 0.35,
    "frequency_penalty": 0.35,
}
COORDINATOR_CONFIG = {
    "model": GPT4,
    "temperature": 0,
    "top_p": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
}
