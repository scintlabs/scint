from deltron.utils.main import envar
from deltron.utils.logger import log

# external api keys and tokens
OPENAI_API_KEY = envar("OPENAI_API_KEY")
GOOGLE_API_KEY = envar("GOOGLE_API_KEY")
GOOGLE_SEARCH_ID = envar("GOOGLE_SEARCH_ID")

# openai models
GPT4_TURBO = "gpt-4-1106-preview"
GPT4 = "gpt-4"
GPT3 = "gpt-3.5-turbo"
GPT3_16K = "gpt-3.5-turbo-16k"
ADA2 = "text-embedding-ada-002"

# default component settings
IDENTITY = f"""
You are friendly and helpful.
"""
INSTRUCTIONS = f"""
You are a large language model.
"""
CONFIG = {
    "model": GPT4_TURBO,
    "temperature": 0,
    "top_p": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "tool_choice": "auto",
}
