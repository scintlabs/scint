from typing import Dict, List, Union, Literal, Optional
from core.definitions.prompts import meta


class Prompt:
    def __init__(
        self,
        identifier: str,
        content: str,
    ):
        self.identifier = identifier
        self.content = content


def load_prompts(prompts: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, "Prompt"]]:
    prompt_objects = {}
    for category, category_prompts in prompts.items():
        prompt_objects[category] = {}
        for identifier, content in category_prompts.items():
            prompt_objects[category][identifier] = Prompt(
                identifier=identifier, content=content
            )
    return prompts  # type: ignore


meta_prompts = load_prompts(meta)
