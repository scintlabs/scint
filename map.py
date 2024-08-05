import os
import json


def map_project(root_dir):
    repo_map = {}

    def walk_directory(directory, current_map):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)

            if os.path.isdir(item_path):
                current_map[item] = {}
                walk_directory(item_path, current_map[item])
            else:
                if item.endswith((".py", ".json", ".yaml", ".yml", ".md")):
                    with open(item_path, "r") as file:
                        try:
                            content = file.read()
                            current_map[item] = {
                                "type": "file",
                                "extension": os.path.splitext(item)[1],
                                "size": os.path.getsize(item_path),
                                "content": (
                                    content[:1000] if len(content) > 1000 else content
                                ),
                            }
                        except Exception as e:
                            current_map[item] = {
                                "type": "file",
                                "extension": os.path.splitext(item)[1],
                                "size": os.path.getsize(item_path),
                                "error": str(e),
                            }

    walk_directory(root_dir, repo_map)
    return repo_map


if __name__ == "__main__":
    repo_root = "."
    repo_structure = map_project(repo_root)

    with open("repo_structure.json", "w") as f:
        json.build()repo_structure, f, indent=2)
