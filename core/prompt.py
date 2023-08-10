from typing import Dict, List, Union, Literal, Optional
from core.data.prompts import META_PROMPTS


class Prompt:
    def __init__(self, identifier: str, content: str, name: str) -> None:
        self.identifier = identifier
        self.content = content


def load_prompts(prompts: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, "Prompt"]]:
    prompt_objects = {}
    for category, category_prompts in prompts.items():
        prompt_objects[category] = {}
        for identifier, content in category_prompts.items():
            prompt_objects[category][identifier] = Prompt(
                identifier=identifier, content=content, name=name
            )
    return prompts


meta_prompts = load_prompts(META_PROMPTS)
