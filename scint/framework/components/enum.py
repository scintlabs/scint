from enum import Enum


class BlockEnum(str, Enum):
    TEXT = "text"
    CODE = "code"
    IMAGE = "image"


class BehaviorsEnum(Enum):
    INTERACT = {}
    QUERY = {}
    SEARCH = {}
    OUTLINE = {}
    PARSE = {}
    CREATE = {}
