import os


def data_parsing(path="."):
    gitignore_path = os.path.join(path, ".gitignore")

    text_output_file = "processed_data_text.json"
    embeddings_output_file = "processed_data_embeddings.json"
    code = [".py", ".js", ".ts", ".html", ".css", ".toml", ".json", ".yml"]
    text = [".txt", ".md"]
    skip = [
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".pdf",
        ".DS_Store",
        ".gitattributes",
        ".gitmodules",
        ".git/",
    ]

    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            lines = f.readlines()

            for line in lines:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue
                else:
                    skip.append(line)


def _chunk_text_with_overlap(self, content):
    chunk_size = 500
    overlap = 150

    start = 0
    end = self.chunk_size
    while start < len(content):
        yield content[start:end]
        start = end - self.overlap
        end = start + self.chunk_size


def _tokenize_content(self, content, file_type):
    if file_type in self.code_filetypes:
        return content.split("\n")
    else:
        return []
