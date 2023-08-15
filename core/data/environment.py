import os
import json
import tiktoken
from terminusdb_client import WOQLClient

APPDATA = os.path.expanduser("~/.local/share/scint/")
FILESTORE = os.path.join(APPDATA, "files/")

cwd = os.getcwd()
loadout = f"{cwd}"
env_vars = f"{os.environ}"


# team = "scint"
# client = WOQLClient("https://cloud.terminusdb.com/scint/")
# client.connect(team=team, use_token=True)


def parse_data(dir_path):
    total_lines = 0
    total_chars = 0

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                lines = f.readlines()
                total_lines += len(lines)
                total_chars += sum(len(line) for line in lines)

    return total_lines, total_chars


total_lines, total_chars = parse_data("/Users/kaechle/Developer/scint-python/")

print(f"Total lines: {total_lines}")
print(f"Total characters: {total_chars}")
