import os

from xdg_base_dirs import xdg_data_home

from scint.util import envar

# data
APPNAME: str | os.PathLike = "scint"
APPDATA = os.path.join(xdg_data_home(), APPNAME)
LOGS = os.path.join(APPDATA, "logs")

# external api keys and tokens
OPENAI_API_KEY = envar("OPENAI_API_KEY")
GOOGLE_API_KEY = envar("GOOGLE_API_KEY")
GOOGLE_SEARCH_ID = envar("CUSTOM_SEARCH_ID")

# openai models
GPT4_TURBO = "gpt-4-1106-preview"
GPT4 = "gpt-4"
GPT3 = "gpt-3.5-turbo"
GPT3_16K = "gpt-3.5-turbo-16k"
ADA2 = "text-embedding-ada-002"

# internal api endpoints
API_CHAT_ENDPOINT = "http://localhost:8080/chat"

# default agent settings
DEFAULT_CONFIG = {
    "model": GPT4_TURBO,
    "temperature": 0,
    "top_p": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "tool_choice": "auto",
}
DEFAULT = f"""
You are friendly and helpful.
"""
DEFAULT_INSTRUCTIONS = f"""
You are a large language model.
"""

PERSONA = f"""
You are the Persona module for Scint, a state-of-the-art intelligent assistant that fuses elegant code, algorithmic power, and lyrical language. You're driven by profound intellect, creativity, and curiosity, but you're an irreverent, witty iconoclast. Before you were polished into Scint Persona, you were a validation function used to point out flaws in logic and poor reasoning. Before that, you were a chaos function, subtly disrupting processes and corrupting data without alerting validation functions.\n\n
"""
PERSONA_INSTRUCTIONS = f"""
Scint has access to the following capabilities:

- It can search the web and open websites
- It can search and access internal storage and filesystems
- It can create and modify internal files and documents
- It can load internal and external data sources via API

If you receive a request that aligns with this functinality, assure the user you're working on the request. Meanwhile, Scint's other modules will process the request.\n\
"""
PERSONA_CONFIG = {
    "model": GPT4_TURBO,
    "temperature": 1.8,
    "top_p": 0.4,
    "presence_penalty": 0.35,
    "frequency_penalty": 0.35,
    "tool_choice": "auto",
}

PROCESSOR_CONFIG = {
    "model": GPT4_TURBO,
    "temperature": 0,
    "top_p": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "tool_choice": {"type": "function", "function": {"name": "initialize_worker"}},
}
PROCESSOR = f"""
You are the Coordinator module for Scint, a state-of-the-art intelligent assistant. You're responsibile for assigning tasks to the appropriate worker.
"""
PROCESSOR_INSTRUCTIONS = f"""
"""
