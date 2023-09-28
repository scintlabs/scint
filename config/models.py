from typing import Dict, List

from base.processing import Message


def preprocess(messages: List[Message]) -> List[Dict[str, str]]:
    processed: List[Dict[str, str]] = []

    for message in messages:
        processed.append({"role": "assistant", "content": message.content})

    return processed


logit_bias: Dict = {1102: -100, 4717: -100, 7664: -100}
