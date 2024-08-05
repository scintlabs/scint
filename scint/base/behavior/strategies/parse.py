import os
from functools import partial, reduce
from typing import Any, Callable, Dict, List, Optional

from tree_sitter import Language, Parser as TreeSitter

from ...utils import dictorial

# Types
SourceType = bytes
ParserType = TreeSitter
ConfigType = Dict[str, Any]
FilterType = Dict[str, List[str]]
IgnorePatternType = List[str]
ParsedDataType = List[Dict[str, str]]


# Utility functions
def read_file(path: str) -> SourceType:
    with open(path, "rb") as f:
        return f.read()


def load_ignore_patterns(path: str) -> IgnorePatternType:
    if not os.path.exists(path):
        return []
    with open(path, "r") as file:
        return [
            line.strip() for line in file if line.strip() and not line.startswith("#")
        ]


def set_language(parser: ParserType, ext: str) -> ParserType:
    language = Language(f"scint/settings/build/languages.so", "python")
    return parser.set_language(language)


# core parsing funcs
def parse_node(
    source: SourceType, node: Any, types: List[str], filters: List[str]
) -> ParsedDataType:
    parsed = []
    if node.type in filters:
        parsed.append(
            {node.type: source[node.start_byte : node.end_byte].strip().decode()}
        )
    for child in node.children:
        if child.type in types:
            parsed.extend(parse_node(source, child, types, filters))
    return parsed


def parse_tree(
    source: SourceType, tree: Any, types: List[str], filters: List[str]
) -> ParsedDataType:
    return reduce(
        lambda acc, child: acc + parse_node(source, child, types, filters),
        tree.root_node.children,
        [],
    )


def parse_strategy(
    source: SourceType,
    node: Any,
    types: List[str],
    max_depth: int,
    current_depth: int = 1,
) -> ParsedDataType:
    if current_depth > max_depth:
        return []
    parsed = []
    if node.type in types:
        parsed.append(
            {node.type: source[node.start_byte : node.end_byte].strip().decode()}
        )
    for child in node.children:
        parsed.extend(
            parse_strategy(source, child, types, max_depth, current_depth + 1)
        )
    return parsed


def parse_tree_strategy(
    source: SourceType, tree: Any, types: List[str], max_depth: int
) -> ParsedDataType:
    return reduce(
        lambda acc, child: acc + parse_strategy(source, child, types, max_depth),
        tree.root_node.children,
        [],
    )


# higher-order funcs for composition
def with_parser(config: ConfigType, ext: str) -> Callable[[str], ParserType]:
    def get_parser(path: str) -> ParserType:
        if ext not in ["txt", "md"]:
            return set_language(TreeSitter(), ext)
        return TreeSitter()

    return get_parser


def with_types(config: ConfigType, language: str) -> Callable[[ParserType], List[str]]:
    return lambda _: dictorial(config, f"filetype.{language}.types")


def with_filters(
    config: ConfigType, language: str
) -> Callable[[ParserType], FilterType]:
    return lambda _: dictorial(config, f"filetype.{language}.filters")


def with_ignore(ignore_file: str) -> Callable[[ParserType], IgnorePatternType]:
    return lambda _: load_ignore_patterns(ignore_file)


def with_strategy(
    language: str, depth: Optional[int] = None
) -> Callable[[ParserType], Callable]:
    return lambda _: (
        partial(parse_tree_strategy, max_depth=depth) if depth else parse_tree
    )


# main parsing function
def parse(
    config: ConfigType,
    language: str,
    path: str,
    depth: Optional[int] = None,
    ignore_file: Optional[str] = None,
) -> ParsedDataType:
    if not os.path.exists(path) or os.path.isdir(path):
        raise ValueError(f"Invalid path: {path}")

    _, ext = os.path.splitext(path)
    source = read_file(path)

    parser = with_parser(config, ext)(path)
    types = with_types(config, language)(parser)
    filters = with_filters(config, language)(parser)
    ignore_patterns = with_ignore(ignore_file)(parser) if ignore_file else []
    parse_func = with_strategy(language, depth)(parser)

    tree = parser.parse(source)
    return parse_func(source, tree, types, filters)


# Usage example
def main():
    config = {}
    result = parse(config, "python", "example.py", depth=3, ignore_file=".gitignore")
    print(result)


if __name__ == "__main__":
    main()
