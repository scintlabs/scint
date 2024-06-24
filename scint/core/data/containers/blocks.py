from datetime import datetime
import sys
from uuid import uuid4

import numpy as np
import websockets
from pydantic import BaseModel, Field

from scint.support.types import Any, Dict, List, Optional, Union
from scint.support.logging import log
from scint.settings import intelligence


WebSocket = websockets.WebSocketCommonProtocol
WebSocketDisconnect = websockets.exceptions.ConnectionClosed


class Block(BaseModel):
    id: str = Field(default_factory=uuid4)
    created: str = Field(default_factory=datetime.now)
    data: Any

    @property
    def metadata(self):
        return self.data


class Annotations(Block):
    data: List[str]


class Embedding(Block):
    data: List[float]


class Link(Block):
    data: List[float]


class Speech(Block):
    data: List[float]


class File(Block):
    data: List[float]


# class BlockType(type):
#     @classmethod
#     def __prepare__(cls, name, bases, **kwds):
#         return {}

#     def __new__(cls, name, bases, dct, **kwds):
#         def metadata(self):
#             def _rmetadata(obj):
#                 md = {}
#                 if isinstance(obj, dict):
#                     for key, value in obj.items():
#                         if not key.startswith("__") and value is not None:
#                             md.update(_rmetadata(value))
#                 elif isinstance(obj, list):
#                     list_md = []
#                     for item in obj:
#                         item_md = _rmetadata(item)
#                         if item_md:
#                             list_md.append(item_md)
#                     md["data"] = list_md
#                 if obj.__class__.__name__ == "Collection":
#                     md = _rmetadata(obj.__dict__)
#                 elif isinstance(obj, Block):
#                     md = obj.metadata
#                 return md

#         dct["id"] = str(uuid4())
#         dct["name"] = None
#         dct["description"] = None
#         dct["labels"] = []
#         dct["embedding"] = []
#         dct["data"] = []
#         dct["metadata"] = property(metadata)
#         return super().__new__(cls, name, bases, dct, **kwds)

#     def __init__(cls, name, bases, dct, **kwargs):
#         super().__init__(name, bases, dct, **kwargs)


# class BlockBase(metaclass=BlockType):
#     def __init__(self, seq):
#         if isinstance(seq, str):
#             self.data = seq
#         elif isinstance(seq, BlockBase):
#             self.data = seq.data[:]
#         else:
#             self.data = str(seq)

#     def __str__(self):
#         return str(self.data)

#     def __repr__(self):
#         return repr(self.data)

#     def __int__(self):
#         return int(self.data)

#     def __float__(self):
#         return float(self.data)

#     def __complex__(self):
#         return complex(self.data)

#     def __hash__(self):
#         return hash(self.data)

#     def __getnewargs__(self):
#         return (self.data[:],)

#     def __eq__(self, string):
#         if isinstance(string, BlockBase):
#             return self.data == string.data
#         return self.data == string

#     def __lt__(self, string):
#         if isinstance(string, BlockBase):
#             return self.data < string.data
#         return self.data < string

#     def __le__(self, string):
#         if isinstance(string, BlockBase):
#             return self.data <= string.data
#         return self.data <= string

#     def __gt__(self, string):
#         if isinstance(string, BlockBase):
#             return self.data > string.data
#         return self.data > string

#     def __ge__(self, string):
#         if isinstance(string, Block):
#             return self.data >= string.data
#         return self.data >= string

#     def __contains__(self, char):
#         if isinstance(char, Block):
#             char = char.data
#         return char in self.data

#     def __len__(self):
#         return len(self.data)

#     def __getitem__(self, index):
#         return self.__class__(self.data[index])

#     def __add__(self, other):
#         if isinstance(other, Block):
#             return self.__class__(self.data + other.data)
#         elif isinstance(other, str):
#             return self.__class__(self.data + other)
#         return self.__class__(self.data + str(other))

#     def __radd__(self, other):
#         if isinstance(other, str):
#             return self.__class__(other + self.data)
#         return self.__class__(str(other) + self.data)

#     def __mul__(self, n):
#         return self.__class__(self.data * n)

#     __rmul__ = __mul__

#     def __mod__(self, args):
#         return self.__class__(self.data % args)

#     def __rmod__(self, template):
#         return self.__class__(str(template) % self)

#     def capitalize(self):
#         return self.__class__(self.core.capitalize())

#     def casefold(self):
#         return self.__class__(self.core.casefold())

#     def center(self, width, *args):
#         return self.__class__(self.core.center(width, *args))

#     def count(self, sub, start=0, end=sys.maxsize):
#         if isinstance(sub, Block):
#             sub = sub.data
#         return self.core.count(sub, start, end)

#     def removeprefix(self, prefix, /):
#         if isinstance(prefix, Block):
#             prefix = prefix.data
#         return self.__class__(self.core.removeprefix(prefix))

#     def removesuffix(self, suffix, /):
#         if isinstance(suffix, Block):
#             suffix = suffix.data
#         return self.__class__(self.core.removesuffix(suffix))

#     def encode(self, encoding="utf-8", errors="strict"):
#         encoding = "utf-8" if encoding is None else encoding
#         errors = "strict" if errors is None else errors
#         return self.core.encode(encoding, errors)

#     def endswith(self, suffix, start=0, end=sys.maxsize):
#         return self.core.endswith(suffix, start, end)

#     def expandtabs(self, tabsize=8):
#         return self.__class__(self.core.expandtabs(tabsize))

#     def find(self, sub, start=0, end=sys.maxsize):
#         if isinstance(sub, Block):
#             sub = sub.data
#         return self.core.find(sub, start, end)

#     def format(self, /, *args, **kwds):
#         return self.core.format(*args, **kwds)

#     def format_map(self, mapping):
#         return self.core.format_map(mapping)

#     def index(self, sub, start=0, end=sys.maxsize):
#         return self.core.index(sub, start, end)

#     def isalpha(self):
#         return self.core.isalpha()

#     def isalnum(self):
#         return self.core.isalnum()

#     def isascii(self):
#         return self.core.isascii()

#     def isdecimal(self):
#         return self.core.isdecimal()

#     def isdigit(self):
#         return self.core.isdigit()

#     def isidentifier(self):
#         return self.core.isidentifier()

#     def islower(self):
#         return self.core.islower()

#     def isnumeric(self):
#         return self.core.isnumeric()

#     def isprintable(self):
#         return self.core.isprintable()

#     def isspace(self):
#         return self.core.isspace()

#     def istitle(self):
#         return self.core.istitle()

#     def isupper(self):
#         return self.core.isupper()

#     def join(self, seq):
#         return self.core.join(seq)

#     def ljust(self, width, *args):
#         return self.__class__(self.core.ljust(width, *args))

#     def lower(self):
#         return self.__class__(self.core.lower())

#     def lstrip(self, chars=None):
#         return self.__class__(self.core.lstrip(chars))

#     maketrans = str.maketrans

#     def partition(self, sep):
#         return self.core.partition(sep)

#     def replace(self, old, new, maxsplit=-1):
#         if isinstance(old, Block):
#             old = old.data
#         if isinstance(new, Block):
#             new = new.data
#         return self.__class__(self.core.replace(old, new, maxsplit))

#     def rfind(self, sub, start=0, end=sys.maxsize):
#         if isinstance(sub, Block):
#             sub = sub.data
#         return self.core.rfind(sub, start, end)

#     def rindex(self, sub, start=0, end=sys.maxsize):
#         return self.core.rindex(sub, start, end)

#     def rjust(self, width, *args):
#         return self.__class__(self.core.rjust(width, *args))

#     def rpartition(self, sep):
#         return self.core.rpartition(sep)

#     def rstrip(self, chars=None):
#         return self.__class__(self.core.rstrip(chars))

#     def split(self, sep=None, maxsplit=-1):
#         return self.core.split(sep, maxsplit)

#     def rsplit(self, sep=None, maxsplit=-1):
#         return self.core.rsplit(sep, maxsplit)

#     def splitlines(self, keepends=False):
#         return self.core.splitlines(keepends)

#     def startswith(self, prefix, start=0, end=sys.maxsize):
#         return self.core.startswith(prefix, start, end)

#     def strip(self, chars=None):
#         return self.__class__(self.core.strip(chars))

#     def swapcase(self):
#         return self.__class__(self.core.swapcase())

#     def title(self):
#         return self.__class__(self.core.title())

#     def translate(self, *args):
#         return self.__class__(self.core.translate(*args))

#     def upper(self):
#         return self.__class__(self.core.upper())

#     def zfill(self, width):
#         return self.__class__(self.core.zfill(width))


# class Block(BlockBase):
#     def __init__(self):
#         super().__init__()
