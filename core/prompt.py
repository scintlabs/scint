from typing import Dict, List, Union, Literal, Optional
from core.data.prompts import prompt_data


class Prompt:
    def __init__(
        self,
        identifier: str,
        user_message: bool,
        content: str,
        name: Optional[str] = None,
    ) -> None:
        self.identifier = identifier
        self.content = content


def load_prompts(prompts: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, "Prompt"]]:
    prompt_objects = {}
    for category, category_prompts in prompts.items():
        prompt_objects[category] = {}
        for identifier, content in category_prompts.items():
            prompt_objects[category][identifier] = Prompt(
                identifier=identifier, user_message=False, content=content
            )
    return prompts


prompts = load_prompts(prompt_data)
