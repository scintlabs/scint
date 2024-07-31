from typing import Dict, List, Tuple

from scint.base.models import Model
from scint.base.models.functions import Function
from scint.base.models.messages import Block, Messages, Prompt, Prompts


class Instructions(Prompt):
    pass


class Task(Model):
    body: Block


class Thread(Model):
    name: str
    description: str
    parameters: Dict[str, str]
    tasks: List[Task]


class Process(Model):
    name: str
    description: str
    parameters: Dict[str, str]
    threads: List[Thread]


class Instructions(Model):
    prompts: List[Prompt]
    functions: List[Function]


class InstructionSet(Model):
    context: Tuple[Prompts, Messages]
    instructions: Tuple[Instructions]
