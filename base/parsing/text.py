from typing import List

import spacy

from base.observability.logging import logger

nlp = spacy.load("en_core_web_sm")


class TextParser:
    def __init__(self, content: str):
        self.content = content
        self.doc = nlp(content)
        self.tokens: List[str] = self.tokenize()
        self.lemmas: List[str] = self.lemmatize()
        self.entities: List[str] = self.extract_entities()

    def tokenize(self) -> List[str]:
        return [token.text for token in self.doc]

    def lemmatize(self) -> List[str]:
        return [token.lemma_ for token in self.doc]

    def extract_entities(self) -> List[str]:
        return [ent.text for ent in self.doc.ents]
