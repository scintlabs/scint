from uuid import uuid4

import numpy as np

from scint.core.containers import ContainerType, Messages
from scint.core.utils import cosine_similarity
from scint.modules.logging import log


class StructureType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, dct, **kwargs):
        def metadata(self):
            data = {}
            data["id"] = self.id
            data["name"] = self.name
            data["tags"] = self.tags
            data["description"] = self.description
            data["embeddings"] = self.embeddings
            return data

        def tags(self):
            container_tags = []
            for key, value in self.__dict__.items():
                if isinstance(value, ContainerType):
                    container_tags.extend(value.metadata["tags"])

        def embeddings(self):
            container_embeddings = []
            for key, value in self.__dict__.items():
                if isinstance(value, ContainerType):
                    container_embeddings.append({key: value.metadata["embedding"]})
                return container_embeddings

        dct["id"] = str(uuid4())
        dct["name"] = name
        dct["tags"] = []
        dct["description"] = None
        dct["structs"] = []
        dct["embeddings"] = property(embeddings)
        dct["tags"] = property(tags)
        dct["metadata"] = property(metadata)
        dct["allow_context"] = cls.allow_context
        dct["attach_struct"] = cls.attach_struct
        dct["detach_struct"] = cls.detach_struct
        dct["add_struct"] = cls.add_struct
        dct["find_struct"] = cls.find_struct
        return super().__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name, bases, dct, **kwargs):
        super().__init__(name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        return instance

    def allow_context(self, context):
        context.contextualize_struct(self)

    def attach_struct(self, struct):
        self.structs.append(struct)

    def detach_struct(self, struct):
        self.structs.remove(struct)

    def add_struct(self):
        new_struct = type(self)()
        self.attach_struct(new_struct)
        return new_struct

    def collapse_struct(self):
        pass

    def find_struct(self, embedding):
        def _find_recursive(struct, embedding, best_match=None, best_similarity=-1):
            struct_embeddings = struct.embeddings
            for struct_embedding in struct_embeddings:
                similarity = cosine_similarity([embedding], [struct_embedding])[0][0]
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = struct
            for struct in struct.structs:
                best_match, best_similarity = _find_recursive(
                    struct,
                    embedding,
                    best_match,
                    best_similarity,
                )
            return best_match, best_similarity

        best_match, best_similarity = _find_recursive(self, embedding)
        if best_similarity > 0.9:
            log.info(f"Found thread with {best_similarity:.2f} similarity.")
            return best_match
        else:
            return self.add_struct()


class Thread(metaclass=StructureType):
    def __init__(self):
        super().__init__()
        self.messages = Messages()
