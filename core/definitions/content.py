from typing import NamedTuple, List, Dict


class Sentence:
    content: str
    properties: object = {"content": {"model": "statement", "type": "string"}}


class Paragraph(NamedTuple):
    content: str
    sentences: List[str]


class Function(CodeBlock):
    pass


class Parameters(NamedTuple):
    content: Dict[str, str]


class Document(NamedTuple):
    title: str
    paragraphs: List[Paragraph]
