from typing import List

import spacy
from tree_sitter import Language, Parser

from base.observability.logging import logger

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
