import os

from scint.core import Context
from scint.core.data.containers import Block
from scint.core.data.containers import Collection
from scint.support.utils import hash_object
from scint.support.logging import log


def map_file(path, file):
    Collection(
        name=os.path.join(file),
        path=os.path.join(path, file),
        hash=hash_object(os.path.join(path, file)),
        data=Block(
            name=os.path.basename(path),
            path=os.path.join(path, file),
        ),
    )


def map_directory(path, struct):
    struct.attach.append(
        Collection(
            name=os.path.basename(path),
            path=os.path.join(path, dir),
            labels={"directory", "filesystem"},
            data=[],
        ),
        os.path.join(path, dir),
    )


def create_filesystem_map(path):
    path = os.path.abspath(path)
    struct = (
        Collection(name=os.path.basename(path), data=[]),
        path,
    )
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            map_directory(path)
            if files:
                for file in files:
                    map_file(path, file)
    return struct
