from typing import TypeVar

from scint.ensemble.components.enum import Enumerator

T = TypeVar("T")


SystemEvents = Enumerator(
    ATTENTION=type("Request", (), {}),
    ERROR=type("Request", (), {}),
    REMINDER=type("Request", (), {}),
    REQUEST=type("Response", (), {}),
    MESSAGE=type("Message", (), {}),
    PROMPT=type("Prompt", (), {}),
    CALL=type("FuncCall", (), {}),
    RESULT=type("Result", (), {}),
    ROUTE=type("Route", (), {}),
)


DomainEvents = Enumerator(
    ALERT=type("Request", (), {}),
    REQUEST=type("Response", (), {}),
    MESSAGE=type("Message", (), {}),
    PROMPT=type("Prompt", (), {}),
    CALLER=type("FuncCall", (), {}),
    RESULT=type("Result", (), {}),
    ROUTE=type("Route", (), {}),
)


class WriteModel:
    def store_document(self, doc):
        pass


class ReadModel:
    def __init__(self):
        self.enriched_documents = {}

    def update_document(self, doc_id: str, **enrichments):
        if doc_id not in self.enriched_documents:
            self.enriched_documents[doc_id] = {}
        self.enriched_documents[doc_id].update(enrichments)

    def get_document(self, doc_id: str) -> dict:
        return self.enriched_documents.get(doc_id, {})
