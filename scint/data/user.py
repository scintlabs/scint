import json
import os
import plistlib
import json
import os

from openai import OpenAI
from tree_sitter import Language, Parser

from scint.system.logging import log

client = OpenAI()


def parse_bookmarks(bookmarks_dict):
    bookmarks = []
    reading_list = []

    def traverse(node):
        if isinstance(node, dict):
            if "Title" in node and node["Title"] == "com.apple.ReadingList":
                for child in node["Children"]:
                    reading_list.append(
                        {
                            "title": child["URIDictionary"].get("title", ""),
                            "description": child.get("previewText"),
                            "url": child["URLString"],
                        }
                    )
            elif "URLString" in node:
                bookmarks.append(
                    {
                        "title": node["URIDictionary"].get("title", ""),
                        "description": node.get("previewText"),
                        "url": node["URLString"],
                    }
                )

            elif "Children" in node:
                for child in node["Children"]:
                    traverse(child)

    traverse(bookmarks_dict)

    return bookmarks, reading_list


def load_bookmarks():
    path = "/Users/kaechle/Library/Safari/bookmarks.plist"
    with open(path, "rb") as fp:
        bookmarks_dict = plistlib.load(fp, fmt=None, dict_type=dict)
        bookmarks, reading_list = parse_bookmarks(bookmarks_dict)
        links = {"bookmarks": bookmarks, "reading_list": reading_list}

        with open("scint/data/links.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(links, indent=4))

        return links


def parse_documents(paths):
    ignore = [
        ".DS_Store",
        ".git",
        ".vscode",
        "__pycache__",
        "node_modules",
        ".venv",
        ".env",
    ]
    documents = {}

    for path in paths:
        trailing_dir = os.path.basename(path)
        if trailing_dir not in documents:
            documents[trailing_dir] = []

        file_id = 1
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = file
                file_stats = os.stat(file_path)

                if file_name in ignore:
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    file = {
                        "id": file_id,
                        "name": file_name,
                        "path": root,
                        "size": file_stats.st_size,
                        "modified": file_stats.st_mtime,
                        "content": content,
                    }
                    documents[trailing_dir].append(file)
                    file_id += 1

                except UnicodeDecodeError:
                    log.info(f"Skipping non-UTF-8 file: {file_path}")

    return documents


def load_documents():
    paths = [
        "/Users/kaechle/Documents/Notes",
        "/Users/kaechle/Documents/Journal",
        "/Users/kaechle/Documents/Writing",
    ]
    files = parse_documents(paths)
    with open("scint/data/documents.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(files, indent=4))


grammars = [
    "/Users/kaechle/.config/tree-sitter/tree-sitter-python",
    "/Users/kaechle/.config/tree-sitter/tree-sitter-swift",
    "/Users/kaechle/.config/tree-sitter/tree-sitter-javascript",
]

python_lang = Language("scint/data/build/languages.so", "python")
swift_lang = Language("scint/data/build/languages.so", "swift")
javascript_lang = Language("scint/data/build/languages.so", "javascript")


def load_parser():
    Language.build_library("build/my-languages.so", grammars)
    python_lang = Language("scint/data/build/languages.so", "python")
    parser = Parser()
    parser.set_language(python_lang)
    return parser


def build_language_lib(grammars):
    Language.build_library("scint/data/build/languages.so", grammars)


def parse_imports(node, source_code):
    imports = []
    if node.type == "import_statement" or node.type == "import_from_statement":
        module_name = ""
        imported_items = []
        for child in node.children:
            if child.type == "dotted_name":
                module_name = source_code[child.start_byte : child.end_byte]
            elif child.type == "import_list":
                imported_items = [
                    source_code[n.start_byte : n.end_byte]
                    for n in child.children
                    if n.type == "identifier"
                ]
        imports.append(
            {
                "type": "import",
                "from": module_name,
                "imported": imported_items,
            }
        )
    return imports


def parse_functions(node, source_code):
    functions = []
    if node.type == "function_definition" or node.type == "method_definition":
        func_name = ""
        params = []
        for child in node.children:
            if child.type == "identifier":
                func_name = source_code[child.start_byte : child.end_byte]
            elif child.type == "parameters":
                params = [
                    source_code[n.start_byte : n.end_byte]
                    for n in child.children
                    if n.type == "identifier"
                ]
        functions.append(
            {
                "type": "function",
                "path": func_name,
                "parameters": params,
            }
        )
    return functions


def parse_classes(node, source_code):
    classes = []
    if node.type == "class_definition":
        class_name = ""
        methods = []
        for child in node.children:
            if child.type == "identifier":
                class_name = source_code[child.start_byte : child.end_byte]
            elif child.type == "block":
                methods.extend(parse_functions(child, source_code))
        classes.append(
            {
                "type": "class",
                "path": class_name,
                "content": methods,
            }
        )
    return classes


def parse_source(source_code):
    parser = load_parser()
    tree = parser.parse(bytes(source_code, "utf8"))
    root_node = tree.root_node
    metadata = []

    def recursive_extract(node):
        metadata.extend(parse_imports(node, source_code))
        metadata.extend(parse_functions(node, source_code))
        metadata.extend(parse_classes(node, source_code))
        for child in node.children:
            recursive_extract(child)

    recursive_extract(root_node)
    return metadata


def parse_projects(paths):
    default_ignored_items = [
        ".DS_Store",
        ".git",
        ".vscode",
        "__pycache__",
        "node_modules",
        ".venv",
        ".env",
    ]
    documentation_ext = [".md", ".txt", ".rst", ".pdf", ".docx"]
    source_ext = [
        ".py",
        ".swift",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".html",
        ".css",
        ".scss",
        ".json",
        ".toml",
    ]
    projects = []

    for path in paths:
        project = {
            "name": None,
            "description": None,
            "links": [],
            "version": {
                "current": None,
                "last_commit": None,
                "commit_history": [],
            },
            "languages": [],
            "dependencies": [],
            "path": path,
            "data": [],
        }

        ignored_items = default_ignored_items.copy()
        gitignore_path = os.path.join(path, ".gitignore")

        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r") as file:
                for line in file:
                    stripped_line = line.strip()
                    if stripped_line and not stripped_line.startswith("#"):
                        ignored_items.append(stripped_line)

        trailing_dir = os.path.basename(path)
        project["name"] = trailing_dir
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ignored_items]
            files = [f for f in files if f not in ignored_items]
            for item in dirs + files:
                full_path = os.path.join(root, item)

                if os.path.isdir(full_path):
                    stats = os.stat(full_path)
                    directory = {
                        "type": "directory",
                        "path": full_path,
                        "size": stats.st_size,
                        "modified": stats.st_mtime,
                        "data": [],
                        "embedding": None,
                    }
                    project["data"].append(directory)

                elif os.path.isfile(full_path):
                    stats = os.stat(full_path)
                    ext = os.path.splitext(item)[1]
                    file_data = None
                    file_type = "file"

                    if ext in documentation_ext:
                        file_type = "documentation"
                        try:
                            with open(full_path, "r", encoding="utf-8") as f:
                                file_data = f.read()
                        except UnicodeDecodeError:
                            log.info(f"Skipping non-UTF-8 file: {full_path}")

                    elif ext in source_ext:
                        file_type = "source"
                        try:
                            with open(full_path, "r", encoding="utf-8") as f:
                                file_data = parse_source(f.read())
                        except UnicodeDecodeError:
                            log.info(f"Skipping non-UTF-8 file: {full_path}")

                    response = client.embeddings.create(
                        input=str(file_data), model="text-embedding-3-small"
                    )
                    embedding = response.data[0].embedding
                    file_info = {
                        "type": file_type,
                        "path": full_path,
                        "size": stats.st_size,
                        "modified": stats.st_mtime,
                        "data": file_data,
                        "embedding": embedding,
                    }
                    project["data"].append(file_info)

        projects.append(project)

    return project


def load_files():
    paths = ["/Users/kaechle/Developer/scint/scintpy"]
    files = parse_projects(paths)
    with open("scint/data/projects.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(files, indent=4))
