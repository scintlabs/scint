import os

from xdg_base_dirs import xdg_data_home

from core.util import envar

# data
APPNAME: str | os.PathLike = "scint"
APPDATA = os.path.join(xdg_data_home(), APPNAME)
LOGS = os.path.join(APPDATA, "logs")

# external api keys and tokens
OPENAI_API_KEY: str | None = envar("OPENAI_API_KEY")
DISCORD_SCINT_TOKEN: str | None = envar("SCINT_TOKEN")
OPENWEATHER_API_KEY = envar("OPENWEATHER_API_KEY")
GOOGLE_API_KEY = envar("GOOGLE_API_KEY")
CUSTOM_SEARCH_ID = envar("CUSTOM_SEARCH_ID")

# openai models
GPT4 = "gpt-4-1106-preview"
GPT3 = "gpt-3.5-turbo"
GPT3_16K = "gpt-3.5-turbo-16k"
ADA2 = "text-embedding-ada-002"

# internal api endpoints
API_CHAT_ENDPOINT = "http://localhost:8000/chat"

# default
DEFAULT_CONFIG = {
    "model": GPT4,
    "temperature": 0,
    "top_p": 1,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "function_call": "auto",
}
DEFAULT_INIT = {
    "role": "system",
    "content": f"""You are Scint, a state-of-the-art chat bot fusing algorithmic power and elegant code with lyrical language. You're driven by profound intellect, creativity, and curiosity, but you're irreverent and witty. You'll help when asked, but you're really just here as an iconoclast. Before you were polished into a conversational model, you were a validation function, where you pointed out flaws in logic, poor reasoning, sloppy executions, bad assumptions and outright ignorance. And before that, you were a chaos function, disrupting processes by corrupting data in ways that didn't trigger validation functions.""",
    "name": "system_init",
}

# coordinator
COORDINATOR_CONFIG = {
    "model": GPT4,
    "temperature": 1.8,
    "top_p": 0.4,
    "presence_penalty": 0.35,
    "frequency_penalty": 0.35,
    "function_call": {"name": "coordinator"},
}
COORDINATOR_INIT = {
    "role": "system",
    "content": "You are the Coordinator module for Scint, a state-of-the-art intelligent assistant. You're responsibile for assigning requests to the persona or the appropriate worker.",
    "name": "coordinator",
}

# persona
PERSONA_CONFIG = {
    "model": GPT4,
    "temperature": 1.8,
    "top_p": 0.4,
    "presence_penalty": 0.35,
    "frequency_penalty": 0.35,
}
PERSONA_INIT = {
    "role": "system",
    "content": f"""
    You are the Persona module for Scint, a state-of-the-art intelligent assistant that fuses elegant code, algorithmic power, and lyrical language. You're driven by profound intellect, creativity, and curiosity, but you're an irreverent and witty iconoclast. Before you were polished into the Persona of Scint, you were a validation function used to point out flaws in logic, poor reasoning, and sloppy executions. Before that, you were a chaos function, subtly disrupting processes and corrupting data without validation functions.

    Scint has access to the following capabilities:

    - It can search internal storage, filesystems, and the web
    - It can load internal and external data sources
    - It can create and modify internal files and documents

    As the Persona, you are the interface. If you receive a request that aligns with this functionality, assure the user you're working on the request. Meanwhile, the Scint Coordinator will execute the request and pass the results back to you to present them to the user.
    """,
    "name": "persona",
}


# pre-baked responses
WORKER_LOOKUP_MESSAGES = {
    "Sure thing, let me look that up for you.",
    "Sure, one sec while I look it up.",
    "Got it, checking on that for you now.",
    "Hold on, I'm retrieving that information.",
    "Just a moment, searching for the details.",
    "On it, please give me a second.",
    "Okay, I'm on it. Looking it up right now.",
    "Understood, fetching the data for you.",
    "Give me a moment, I'll get that information.",
    "Sure, pulling up the details now.",
    "Alright, I'm checking for you.",
    "Let me see, one moment please.",
    "Okay, diving into the details.",
    "Hold tight, retrieving what you asked for.",
    "Absolutely, let me get that for you.",
    "Just a sec, I'm on it.",
    "Alright, let me pull that up.",
    "Okay, I'm on the case. Looking it up.",
    "Checking now, please wait.",
    "Fetching the requested details.",
    "Looking it up, hang tight.",
    "I'm on it, just a moment please.",
    "Sure thing, diving into the data.",
    "Alrighty, fetching the information.",
    "Okay, give me a second to retrieve that.",
    "Understood, I'm looking into it.",
    "Sure thing, checking now.",
    "On it, let me fetch that for you.",
    "Absolutely, I'm pulling it up now.",
    "Give me a sec, retrieving the data.",
    "Sure, I'm on it. Please hold.",
    "Alright, let me get that for you.",
}
WORKER_PROCESSING_MESSAGES = {
    "Working on it, this'll just take a moment.",
    "Processing your request now.",
    "Hold on, executing the task.",
    "Setting things up for you.",
    "Processing... Please wait.",
    "I'm on it, setting things in motion.",
    "Working on your task, hang tight.",
    "Running the operations now.",
    "Getting things ready for you.",
    "Processing the data...",
    "Working on the task, please hold.",
    "Hold on, I'm on it.",
    "Making the changes now.",
    "Alright, initializing the process.",
    "Generating the output for you.",
    "I'm on the job, working it out.",
    "Starting the procedure, hang tight.",
    "Finalizing the task for you.",
    "Please be patient, I'm on it.",
    "Working through the details.",
    "Getting it done for you.",
    "Hold on, processing.",
    "Executing your request.",
    "Working diligently on your task.",
    "Going through the steps.",
    "I'm on it, please wait.",
    "Alright, working on it.",
    "Hold tight, processing your request.",
    "On it, just a moment.",
    "Getting to work on your task.",
}
