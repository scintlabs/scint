from typing import Dict, List, Union
import os
import time

from tree_sitter import Language, Parser
from watchdog.observers import Observer
import spacy

from scint.services.logging import logger


nlp = spacy.load("en_core_web_sm")


class DataParser:
    def __init__(self) -> None:
        self.observer = Observer()
        self.file_map: Dict[str, Union[TextParser, CodeParser]] = {}

    def add_path(self, path: str) -> None:
        logger.info(f"Observing path: {path}")
        # self.observer.schedule(EventHandler(self), path=path, recursive=True)
        self._process_path(path)

    def _process_path(self, path: str) -> None:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                process_file(file_path)


def process_file(file_path: str) -> None:
    if os.path.isdir(file_path):
        return

    _, extension = os.path.splitext(file_path)

    text_extensions = [".txt", ".md"]
    code_extensions = [
        ".py",
        ".js",
        ".ts",
        ".html",
        ".css",
        ".toml",
        ".json",
        ".yml",
    ]

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    if extension in text_extensions:
        text_data = TextParser(content)
        text_data.tokenize()

    elif extension in code_extensions:
        code_data = CodeParser(content)
        code_data.tokenize()
        code_data.extract_comments()

    else:
        return


def run(self) -> None:
    self.observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        self.observer.stop()
    self.observer.join()
    logger.info("Observer stopped")


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


def read_markdown_files_from_folder(directory_path):
    documents = []

    for subdir, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".markdown"):
                file_path = os.path.join(subdir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    documents.append(f.read())

    return documents


PARSER_PYTHON = Language("data/parsers/python.so", "python")


class CodeParser:
    def __init__(self, content: str, language: Language = PARSER_PYTHON):
        self.content = content
        self.language = language
        self.parser = Parser()
        self.parser.set_language(self.language)
        self.tree = self.parser.parse(bytes(content, "utf8"))
        self.comments: List[str] = []
        self.tokens: List[str] = []
        self.comments = self.extract_comments()
        self.tokens = self.tokenize()

    def tokenize(self) -> List[str]:
        tokens = []

        def traverse_tree(node):
            if len(node.children) == 0:  # Leaf node
                tokens.append(node.type)
            else:
                for child in node.children:
                    traverse_tree(child)

        traverse_tree(self.tree.root_node)

        return tokens

    def extract_comments(self):
        query = self.language.query("""(comment) @spell""")
        captures = query.captures(self.tree.root_node)
        comments = [self.content[cap.start_byte : cap.end_byte] for cap, _ in captures]

        return comments
