from enum import Enum


class Agents(str, Enum):
    assistant = "Assistant"
    coordinator = "Coordinator"
    sentry = "Sentry"


class System(str, Enum):
    finder = "Finder"
    processor = "Processor"
    generator = "Generator"
