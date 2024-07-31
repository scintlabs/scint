import os

from tree_sitter import Language
from tree_sitter import Parser as TreeSitter

from scint.base.models import dictorial


class ParserIgnore:
    def __init__(self, parser):
        self.parser = parser
        self.ignored_files = []

    def ignored(self, ignore_file):
        self.ignored_files = self._load_ignore_patterns(ignore_file)
        return self.parser

    def _load_ignore_patterns(self, path):
        patterns = []
        if os.path.exists(path):
            with open(path, "r") as file:
                patterns = [
                    line.strip()
                    for line in file
                    if line.strip() and not line.startswith("#")
                ]
        return patterns


class ParserFilter:
    def __init__(self, parser):
        self.parser = parser
        self.filter_save = None
        self.filter_discard = None

    def filtered(self, **filters):
        self.filter_save = filters.get("save")
        self.filter_discard = filters.get("discard")
        return self.parser


class ParserStrategy:
    def __init__(self, parser, language, **rules):
        self.parser = parser
        self.types = rules.get(language)
        self.depth_level = None

    def depth(self, depth):
        self.depth_level = depth
        return self.parser

    def _recurse_parse(self, location, current_depth):
        if current_depth > self.depth_level:
            return []
        parsed_data = []
        if location.type in self.types:
            parsed_data.append(
                {
                    location.type: self.parser.source[
                        location.start_byte : location.end_byte
                    ].strip()
                }
            )
        for child in location.children:
            parsed_data.extend(self._recurse_parse(child, current_depth + 1))
        return parsed_data


class ParserContext:
    def __init__(self, parser, src):
        self.parser = parser
        self.source = src
        self._parsed = []

    def parsed(self, location, symbol, types, filters):
        def _parse(location):
            parsed = []
            if location.type in filters:
                parsed.append(
                    {
                        location.type: self.source[
                            location.start_byte : location.end_byte
                        ].strip()
                    }
                )
            for child in location.children:
                if child.type in types:
                    parsed.extend(_parse(child))
            return parsed

        symbols = []
        for child in location.children:
            symbols.extend(_parse(child))
        return symbols

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def parse(self):
        tree = self.parser._last.parse(self.source.decode())
        self._parsed = []
        for child in tree.root_location.children:
            if isinstance(self.parser._strategy, ParserStrategy):
                self._parsed.extend(self.parser._strategy._recurse_parse(child, 1))
            else:
                self._parsed.extend(
                    self.parsed(
                        child, child.type, self.parser._types, self.parser._filters
                    )
                )
        return self


class Parser:
    def __init__(self, config):
        self._config = config
        self._last = None
        self._types = None
        self._filters = None
        self._strategy = None

    def _get_source(self, path):
        with open(path, "rb") as f:
            return f.read()

    def _get_parser(self, ext):
        if ext != "txt" or "md":
            self._set_language(TreeSitter(), ext)

    def _set_language(self, parser, ext):
        language = Language(f"scint/settings/build/languages.so", "python")
        self._last = parser.set_language(language)
        return self._last

    def __call__(self, language, path, depth=None):
        if not os.path.exists(path):
            raise ValueError(f"{path} does not exist.")
        elif os.path.isdir(path):
            raise ValueError(f"{path} is a directory.")
        else:
            _, ext = os.path.splitext(path)
            self._get_parser(ext)
            self._strategy = ParserStrategy(self, language)
            if depth is not None:
                self._strategy.depth(depth)
            self._types = dictorial(self._config, f"filetype.{language}.types")
            self._filters = dictorial(self._config, f"filetype.{language}.filters")
            return ParserContext(self, self._get_source(path))

    def filtered(self, **filters):
        self._filters = filters
        return self

    def ignored(self, ignore_file):
        ParserIgnore(self).ignored(ignore_file)
        return self
