import os
from tree_sitter import Language, Parser as TreeSitter


def load_language(language):
    return Language("scint/core/store/languages.so", "python")


def create_parser(language):
    parser = TreeSitter()
    return parser


def read_file(path):
    with open(path, "rb") as f:
        return f.read()


def parse_source(parser, source):
    return parser.parse(source)


def filter_node_types(node, allowed_types, depth=None, current_depth=0):
    if depth is not None and current_depth > depth:
        return []

    result = []
    if node.type in allowed_types:
        result.append({node.type: node.text.decode("utf-8").strip()})

    for child in node.children:
        result.extend(filter_node_types(child, allowed_types, depth, current_depth + 1))

    return result


def parse_file(file_path, language_name, allowed_types, depth=None):
    language = load_language(language_name)
    parser = create_parser(language)
    source = read_file(file_path)
    tree = parse_source(parser, source)
    return filter_node_types(tree.root_node, allowed_types, depth)


def load_ignore_patterns(ignore_file):
    if not os.path.exists(ignore_file):
        return []
    with open(ignore_file, "r") as file:
        return [
            line.strip() for line in file if line.strip() and not line.startswith("#")
        ]


def is_file_ignored(file_path, ignore_patterns):
    return any(pattern in file_path for pattern in ignore_patterns)


def parse_directory(
    directory_path, language, allowed_types, depth=None, ignore_file=None
):
    ignore_patterns = load_ignore_patterns(ignore_file) if ignore_file else []
    results = {}

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not is_file_ignored(file_path, ignore_patterns):
                try:
                    parsed = parse_file(file_path, language, allowed_types, depth)
                    if parsed:
                        results[file_path] = parsed
                except Exception as e:
                    print(f"Error parsing {file_path}: {str(e)}")

    return results


# def generate_tree_structure(dir):
#     dir = Path(dir).resolve()

#     def tree_recursive(path):
#         item = {"path": str(path.relative_to(dir)), "size": path.stat().st_size}
#         if path.is_dir():
#             item["content"] = [tree_recursive(p) for p in sorted(path.iterdir())]
#         else:
#             item["store"] = []
#         return item

#     return tree_recursive(dir)


# # Example usage
# if __name__ == "__main__":
#     directory = "/Users/kaechle/Developer/scint/scint"
#     structure = generate_tree_structure(directory)
#     print(json.dumps(structure, indent=4))

path = "/scint/core/process/states/parse.py"
result = parse_file(
    path,
    "python",
    ["function_definition", "class_definition"],
    depth=2,
)

print(result)
