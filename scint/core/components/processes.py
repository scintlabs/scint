import os
import hashlib
import asyncio
import requests

import aiohttp
from typing import Dict, Any
from tree_sitter import Language, Parser

from scint.core import Process
from scint.core.primitives.messages import OutputMessage
from scint.core.utils.helpers import encode_image


class Process(Process):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.instructions = []
        self.messages = []


class Search(Process):
    def __init__(self, composition):
        super().__init__(composition)
        self.composition = composition

    async def evaluate(self):
        history = await self.search_conversations(self.message.sketch)
        knowledge = await self.search_knowledge(self.message.sketch)
        web_hits = await self.search_web(self.message.sketch)
        return [history, knowledge, web_hits]

    @staticmethod
    async def search_conversations(query: str):
        pass

    @staticmethod
    async def search_knowledge(query: str):
        pass

    @staticmethod
    async def search_web(query: str):
        pass


class Map(Process):
    def __init__(self, composition):
        super().__init__(composition)
        self.composition = composition

    async def evaluate(self):
        history = await self.search_history(self.message.sketch)
        web_hits = await self.search_web(self.message.sketch)
        return [history, web_hits]

    @staticmethod
    async def parse_code(content: str):
        parser = Parser()
        parser.set_language(Language("scint/core/repository/languages.so", "python"))
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

    @staticmethod
    async def parse_doc(content: str):
        lines = content.split("\n")
        result = []
        for i, line in enumerate(lines):
            if i == 0 or line.startswith("#"):
                result.append({"type": "heading", "data": line, "line": i})
            elif line.strip() and "." in line:
                first_sentence = line.split(".")[0] + "."
                result.append({"type": "paragraph", "data": first_sentence, "line": i})
        return result

    @staticmethod
    async def map_file(filepath: str):
        if Map._should_ignore(filepath):
            return None
        content = Map._read_file(filepath)
        if content is None:
            return None
        file_map = {
            "path": filepath,
            "hash": Map._hash_file(filepath),
            "type": "file",
            "elements": [],
        }
        if filepath.endswith(".py"):
            file_map["elements"] = Map.parse_code(content)
        else:
            file_map["elements"] = Map.parse_doc(content)
        return file_map

    @staticmethod
    async def map_directory(path: str):
        if Map._should_ignore(path):
            return None
        if os.path.isfile(path):
            return Map.map_file(path)
        dir_map = {"path": path, "type": "directory", "contents": {}}
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                subdir_map = Map.map_directory(item_path)
                if subdir_map:
                    dir_map["contents"][item] = subdir_map
            else:
                file_map = Map.map_file(item_path)
                if file_map:
                    dir_map["contents"][item] = file_map
        return dir_map

    @staticmethod
    def _should_ignore(path: str):
        name = os.path.basename(path)
        return any(
            name == pattern
            or (pattern.startswith("*") and name.endswith(pattern[1:]))
            or (pattern in path)
            for pattern in [
                ".git",
                ".venv",
                ".venvs",
                "__pycache__",
                ".DS_Store",
                ".idea",
                ".vscode",
                "node_modules",
                ".gitignore",
                "*.pyc",
                "*.pyo",
                "*.pyd",
                "*.so",
                "*.dylib",
                "*.dll",
                "*.exe",
                "*.bin",
                "*.pkl",
                "*.db",
            ]
        )

    @staticmethod
    def _hash_file(filepath: str):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    @staticmethod
    def _read_file(filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            return None


class Load(Process):
    def __init__(self, composition):
        super().__init__(composition)
        self.composition = composition

    @staticmethod
    async def load_website(website_url):
        url = "https://api.microlink.io"
        params = {"url": website_url, "pdf": True}
        response = requests.get(url, params)
        return response.json()

    @staticmethod
    async def load_image(image_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image = await response.read()
                    base64_image = encode_image(image)
                    return OutputMessage(f"data:image/;base64,{base64_image}")
                else:
                    return OutputMessage(content="Failed to download image.")

    @staticmethod
    async def load_file_segment(file_map: Dict[str, Any], index: int) -> str:
        if index < 0 or index >= len(file_map["elements"]):
            raise ValueError(
                f"Index {index} is out of range. File has {len(file_map['elements'])} elements."
            )

        element = file_map["elements"][index]
        filepath = file_map["path"]

        with open(filepath, "r", encoding="utf-8") as file:
            if "start_line" in element and "end_line" in element:
                # For code files
                lines = file.readlines()
                return "".join(lines[element["start_line"] : element["end_line"] + 1])
            elif "line" in element:
                # For text files
                for i, line in enumerate(file):
                    if i == element["line"]:
                        return line.strip()

        raise ValueError(f"Could not load segment at index {index}")


class Execute(Process):
    def __init__(self, composition):
        super().__init__(composition)
        self.composition = composition

    @staticmethod
    async def exec_application(app: str):
        pass

    @staticmethod
    async def exec_terminal_commands(commands: str):
        process = await asyncio.create_subprocess_shell(
            commands,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() if stdout else ""
        errors = stderr.decode().strip() if stderr else ""
        full_output = output + "\n" + errors if errors else output
        yield OutputMessage(content=full_output)
