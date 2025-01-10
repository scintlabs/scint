import hashlib


import tree_sitter as ts


async def parse_docs(self, content: str):
    lines = content.split("\n")
    result = []

    for i, line in enumerate(lines):
        if i == 0 or line.startswith("#"):
            result.append({"type": "heading", "storage": line, "line": i})
        elif line.strip() and "." in line:
            first_sentence = line.split(".")[0] + "."
            result.append({"type": "paragraph", "storage": first_sentence, "line": i})
    return result


async def parse_code(self, content: str):
    code_parser = ts.Parser()
    ts.Language("settings/languages.so")
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
                    "type": "intent",
                    "signature": node.children[1].text.decode("utf-8"),
                    "start_line": node.start_point[0],
                    "end_line": node.end_point[0],
                }
            )
    return result


def hash_file(self, filepath: str):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()
