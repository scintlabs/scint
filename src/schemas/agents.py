from __future__ import annotations

from src.schemas.components.functions import use_terminal_function
from src.schemas.components.routines import compose, parse
from src.schemas.components.prompts import (
    instructions_prompt,
    composition_prompt,
    processor_prompt,
)
from src.schemas.components.outputs import compose_structure_output, select_agent_output
from src.types.models import AgentMessage


default_agent = {
    "prompts": [instructions_prompt],
    "output": AgentMessage,
    "functions": [use_terminal_function],
    "routine": parse,
}

composer_agent = {
    "prompts": [composition_prompt],
    "output": compose_structure_output,
    "functions": [use_terminal_function],
    "routine": compose,
}


processor_agent = {
    "prompts": [processor_prompt],
    "output": select_agent_output,
    "functions": [use_terminal_function],
    "routine": compose,
}
