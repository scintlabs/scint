import functools
import json
from types import FunctionType, MethodType
from typing import Any, Set
from uuid import uuid4

import numpy as np

from scint.core.data.containers.blocks import Block
from scint.settings.core import library as config
from scint.support.logging import log


def gather_metadata(obj, collection, collector=None, callback=None):
    def _recurse(obj, collection, collector, callback):
        for key, value in obj.items():
            if key in ["id", "messages", "prompts", "functions", "function_choice"]:
                collection[key] = value
        return collection

    def default_collector(value, callback=None):
        if callback:
            value = callback(value)
        return value

    def default_callback(value):
        return value

    collector = collector if collector else default_collector
    callback = callback if callback else default_callback

    if isinstance(obj, dict):
        return _recurse(obj, collection, collector, callback)
    else:
        return _recurse(obj.__dict__, collection, collector, callback)


def labels(self):
    obj = self.__dict__
    collection = set()
    return gather_metadata(obj=obj, collection=collection)


def embeddings(self):
    obj = self.__dict__
    collection = list()

    def _weight(embedding):
        total_weight = sum(self.connections.values())
        weighted_embeddings = [
            embedding * (self.connections[key] / total_weight)
            for key, embedding in embedding.items()
        ]
        return np.sum(weighted_embeddings, axis=0)

    weighted_embeddings = gather_metadata(
        obj=obj, collection=collection, callback=_weight
    )
    if weighted_embeddings:
        return np.mean(np.array(weighted_embeddings), axis=0)
