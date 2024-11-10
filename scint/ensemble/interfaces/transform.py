import hashlib

import tree_sitter as ts

from scint.repository.models.base import Trait


class ParseDocs(Trait):
    async def parse(self, content: str):
        lines = content.split("\n")
        result = []
        for i, line in enumerate(lines):
            if i == 0 or line.startswith("#"):
                result.append({"type": "heading", "state": line, "line": i})
            elif line.strip() and "." in line:
                first_sentence = line.split(".")[0] + "."
                result.append({"type": "paragraph", "state": first_sentence, "line": i})
        return result


class ParseCode(Trait):
    async def parse(content: str):
        code_parser = ts.Parser()
        code_parser.set_language(ts.Language("settings/languages.so", "python"))
        tree = code_parser.parse(bytes(content, "utf-8"))
        result = []

        for node in tree.root_node.children:
            if node.type in ["import_statement", "import_from_statement"]:
                result.append(
                    {
                        "type": "import",
                        "signature": node.text.decode("utf-8"),
                        "start_line": node.start_point[0],
                        "end_line": node.end_point[0],
                    }
                )
            elif node.type == "class_definition":
                result.append(
                    {
                        "type": "class",
                        "signature": node.children[1].text.decode("utf-8"),
                        "start_line": node.start_point[0],
                        "end_line": node.end_point[0],
                    }
                )
            elif node.type == "function_definition":
                result.append(
                    {
                        "type": "function",
                        "signature": node.children[1].text.decode("utf-8"),
                        "start_line": node.start_point[0],
                        "end_line": node.end_point[0],
                    }
                )
        return result

    def hash_file(self, filepath: str):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()


class Parse(ParseDocs, ParseCode):
    pass
