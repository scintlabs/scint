from typing import NamedTuple, List, Dict
from core.definitions.content import Sentence, Paragraph, Title, Subtitle


def generate_function(cls):
    name = "generate"
    description = f"Use this function to return a {cls} based on the user's input and your functional design."
    parameters = {"type": "object", "properties": cls.properties}
    required = ["content"]

    return [
        {
            "name": name,
            "description": description,
            "parameters": parameters,
            "required": required,
        },
    ]


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
