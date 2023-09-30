import os
import time
from typing import Dict, Union

import spacy
from watchdog.observers import Observer

from base.observability.logging import logger
from base.parsing.code import CodeParser
from base.parsing.handlers import EventHandler
from base.parsing.text import TextParser

nlp = spacy.load("en_core_web_sm")


class DataParser:
    def __init__(self) -> None:
        self.observer = Observer()
        self.file_map: Dict[str, Union[TextParser, CodeParser]] = {}

    def add_path(self, path: str) -> None:
        logger.info(f"Observing path: {path}")
        self.observer.schedule(EventHandler(self), path=path, recursive=True)
        self._process_path(path)

    def _process_path(self, path: str) -> None:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                self.process_file(file_path)

    def process_file(self, file_path: str) -> None:
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
            self.file_map[file_path] = text_data

        elif extension in code_extensions:
            code_data = CodeParser(content)
            code_data.tokenize()
            code_data.extract_comments()
            self.file_map[file_path] = code_data

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
