import hashlib

from tree_sitter import Language, Parser
from scint.framework.components import Component


class parse_code(Component):
    async def parse_code(content: str):
        parser = Parser()
        parser.set_language(
            Language("scint/framework/repository/languages.so", "python")
        )
        tree = parser.parse(bytes(content, "utf-8"))
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


class parse_document(Component):
    async def parse_doc(self, content: str):
        lines = content.split("\n")
        result = []
        for i, line in enumerate(lines):
            if i == 0 or line.startswith("#"):
                result.append({"type": "heading", "data": line, "line": i})
            elif line.strip() and "." in line:
                first_sentence = line.split(".")[0] + "."
                result.append({"type": "paragraph", "data": first_sentence, "line": i})
        return result


class hash_file(Component):
    def hash_file(self, filepath: str):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()


class load_file(Component):
    def load_file(self, filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            return None
