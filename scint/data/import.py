import json
import plistlib

from scint.modules.logging import log
from scint.data.parse import parse_bookmarks, parse_documents, parse_files
from scint.support.types import List

activities = "scint/data/activities.json"
functions = "scint/data/functions.json"
files = "scint/data/files.json"
links = "scint/data/links.json"


def load_metadata(filepath: str):
    with open(filepath, "r") as file:
        return json.load(file)


def import_functions(funcs: str):
    metadata = load_metadata(funcs)
    function_metadata = []
    for function in functions:
        for metafunc in metadata:
            if metafunc["name"] == function:
                function_metadata.append(metafunc)
    return function_metadata


def import_files():
    paths = ["/Users/kaechle/Developer/scint/scintpy"]
    files = parse_files(paths)
    with open("scint/data/projects.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(files, indent=4))


def import_documents():
    paths = [
        "/Users/kaechle/Documents/Notes",
        "/Users/kaechle/Documents/Journal",
        "/Users/kaechle/Documents/Writing",
    ]
    docs = parse_documents(paths)
    with open("scint/data/documents.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(docs, indent=4))


def import_bookmarks():
    path = "/Users/kaechle/Library/Safari/bookmarks.plist"
    with open(path, "rb") as fp:
        bookmarks_dict = plistlib.load(fp, fmt=None, dict_type=dict)
        bookmarks, reading_list = parse_bookmarks(bookmarks_dict)
        links = {"bookmarks": bookmarks, "reading_list": reading_list}

        with open("scint/data/links.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(links, indent=4))

        return links
