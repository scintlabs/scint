from enum import Enum, auto
from typing import Any, Dict, Optional

from scint.constants import ADA2, GPT4_TURBO
from scint.utils.logger import log


class Preset(Enum):
    assistant = auto()
    process = auto()
    tool = auto()
    embedding = auto()


class Presets:
    configurations: Dict[Preset, Dict[str, Any]] = {
        Preset.assistant: {
            "model": GPT4_TURBO,
            "temperature": 1.4,
            "top_p": 0.6,
            "presence_penalty": 0.35,
            "frequency_penalty": 0.35,
        },
        Preset.process: {
            "model": GPT4_TURBO,
            "temperature": 1,
            "top_p": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "tool_choice": "auto",
        },
        Preset.tool: {
            "model": GPT4_TURBO,
            "temperature": 1,
            "top_p": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "tool_choice": "auto",
        },
        Preset.embedding: {
            "model": ADA2,
        },
    }

    @staticmethod
    def load(Preset: Preset) -> Dict[str, Any]:
        return Presets.configurations.get(Preset)


class Configuration:
    @staticmethod
    def build(Preset=Preset.assistant, **overrides) -> Dict[str, Any]:
        if Preset is None:
            Preset = Preset.assistant

        parameters = Presets.load(Preset)
        for key, value in overrides.items():
            parameters[key] = value

        return parameters
