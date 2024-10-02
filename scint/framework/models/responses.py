from typing import List

from scint.framework.types.model import Model
from scint.framework.models.properties import Block


class InteractModel(Model):
    blocks: List[Block]
    labels: List[str]
    annotation: str


class SearchOutput(Model):
    blocks: List[Block]
    labels: List[str]
    annotation: str


class SearchModel(Model):
    blocks: List[Block]
    labels: List[str]
    annotation: str


class ParseModel(Model):
    blocks: List[Block]
    labels: List[str]
    annotation: str


class OutlineModel(Model):
    blocks: List[Block]
    labels: List[str]
    annotation: str


class CreateModel(Model):
    blocks: List[Block]
    labels: List[str]
    annotation: str
