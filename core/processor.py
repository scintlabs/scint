import ast, os, re, json
from typing import Dict, Any, Optional


path = "/Users/kaechle/Developer/projects/scint-python"
ignored_dirs = [".git", ".github", ".vscode"]
ignored_files = [
    ".DS_Store",
    ".gitattributes",
    ".gitignore",
    "LICENSE.md",
    ".editorconfig",
    "__init__.py",
]


def read_codebase(path):
    class CodeVisitor(ast.NodeVisitor):
        def __init__(self):
            self.symbols = []

        def visit_FunctionDef(self, node):
            self.symbols.append(node.name)
            self.generic_visit(node)

        def visit_ClassDef(self, node):
            self.symbols.append(node.name)
            self.generic_visit(node)

        def visit_Name(self, node):
            self.symbols.append(node.id)

    def parse_file(filepath):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                print(f"Failed to parse file {filepath} due to {e}")
                return {}

            visitor = CodeVisitor()
            visitor.visit(tree)

            comments = re.findall(r"#.*", content)
            return {
                "filepath": filepath,
                "symbols": visitor.symbols,
                "comments": comments,
            }

    parsed_files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(
                ".py"
            ):  # Assuming you're interested only in Python files
                filepath = os.path.join(dirpath, filename)
                parsed_files.append(parse_file(filepath))

    return parsed_files


def read(path):
    chunk_size = 1000
    chunked_data = {}
    total_lines = 0
    total_chars = 0

    for path, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
        for filename in filenames:
            if filename in ignored_files:
                continue
            filepath = os.path.join(path, filename)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                    lines = file.readlines()
                    total_lines += len(lines)
                    total_chars += sum(len(line) for line in lines)
                    content = file.read()
                    chunks = [
                        content[i : i + chunk_size]
                        for i in range(0, len(content), chunk_size)
                    ]
                    for i, chunk in enumerate(chunks):
                        chunked_data[(filepath, i)] = chunk

            except Exception as e:
                print(f"Failed to read file {filepath} with error {e}")

    return chunked_data, total_lines, total_chars


chunked_data, total_lines, total_chars = read(
    "/Users/kaechle/Developer/projects/scint-python"
)


async def eval_function(function: Dict[str, Any]) -> Optional[str]:
    function_name = function["name"]
    function_arguments = function["arguments"]
    data = json.loads(function_arguments)
    content = data.get("content")

    if data.get("function_call"):
        content = await eval_function(data)

    return content
