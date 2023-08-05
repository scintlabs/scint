import os


def read():
    chunked_files = {}
    path = "/Users/kaechle/Developer/projects/scint-server"
    chunk_size = 500
    ignored_dirs = [".git", ".github", "client"]
    ignored_files = [
        ".DS_Store",
        ".gitattributes",
        ".gitignore",
        "LICENSE.md",
        ".editorconfig",
        "__init__.py",
    ]

    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
        for filename in filenames:
            if filename in ignored_files:
                continue
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    chunks = [
                        content[i : i + chunk_size]
                        for i in range(0, len(content), chunk_size)
                    ]
                    for i, chunk in enumerate(chunks):
                        chunked_files[(filepath, i)] = chunk
            except Exception as e:
                print(f"Failed to read file {filepath} with error {e}")

    print(chunked_files)
    return chunked_files
