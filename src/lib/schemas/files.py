from __future__ import annotations

import os
import fnmatch
from enum import Enum
from typing import Dict, List, Any

from attrs import define, field


class FileType(Enum):
    Text = ("Text", "txt", ".txt")
    Markdown = ("Markdown", "md", ".md", ".markdown")
    JSON = ("JSON", "json", ".json")
    YAML = ("YAML", "yaml", ".yml", ".yaml")
    TOML = ("TOML", "toml", ".toml")
    XML = ("XML", "xml", ".xml")
    CSV = ("CSV", "csv", ".csv")
    INI = ("INI", "ini", ".ini")
    Python = ("Python", "python", ".py")
    PythonNotebook = ("Jupyter Notebook", "jupyter", ".ipynb")
    Requirements = ("Python Requirements", "requirements", "requirements.txt")
    PythonWheel = ("Python Wheel", "wheel", ".whl")
    PythonEgg = ("Python Egg", "egg", ".egg")
    PythonSetup = ("Python Setup", "python", "setup.py")
    PythonPytest = ("Python Pytest", "python", "conftest.py", "pytest.ini")
    PythonMypy = ("Python Mypy", "ini", "mypy.ini")
    PythonTox = ("Python Tox", "ini", "tox.ini")
    PythonCython = ("Cython", "cython", ".pyx", ".pxd", ".pxi")
    Rust = ("Rust", "rust", ".rs")
    RustCargo = ("Rust Cargo", "toml", "Cargo.toml")
    RustLock = ("Rust Cargo Lock", "toml", "Cargo.lock")
    RustConfig = ("Rust Config", "toml", ".cargo/config.toml")
    RustLib = ("Rust Library", "rust", "lib.rs")
    RustMain = ("Rust Main", "rust", "main.rs")
    RustMod = ("Rust Module", "rust", "mod.rs")
    HTML = ("HTML", "html", ".html", ".htm")
    CSS = ("CSS", "css", ".css")
    SCSS = ("SCSS", "scss", ".scss")
    SASS = ("SASS", "sass", ".sass")
    Less = ("Less", "less", ".less")
    JavaScript = ("JavaScript", "javascript", ".js")
    TypeScript = ("TypeScript", "typescript", ".ts")
    JSX = ("React JSX", "jsx", ".jsx")
    TSX = ("React TSX", "tsx", ".tsx")
    Vue = ("Vue", "vue", ".vue")
    Svelte = ("Svelte", "svelte", ".svelte")
    WebAssembly = ("WebAssembly", "wasm", ".wasm")
    WebAssemblyText = ("WebAssembly Text", "wat", ".wat")
    PHP = ("PHP", "php", ".php")
    Ruby = ("Ruby", "ruby", ".rb")
    RubyGemfile = ("Ruby Gemfile", "ruby", "Gemfile")
    RubyOnRails = ("Ruby on Rails", "ruby", ".erb")
    NPMPackage = ("NPM Package", "json", "package.json")
    NPMLock = ("NPM Lock", "json", "package-lock.json")
    YarnLock = ("Yarn Lock", "yaml", "yarn.lock")
    Webpack = ("Webpack Config", "javascript", "webpack.config.js")
    Babel = ("Babel Config", "json", ".babelrc", "babel.config.js")
    ESLint = ("ESLint Config", "json", ".eslintrc", ".eslintrc.js", ".eslintrc.json")
    Jest = ("Jest Config", "javascript", "jest.config.js")
    TypeScriptConfig = ("TypeScript Config", "json", "tsconfig.json")
    Docker = ("Dockerfile", "dockerfile", "Dockerfile")
    DockerCompose = (
        "Docker Compose",
        "yaml",
        "docker-compose.yml",
        "docker-compose.yaml",
    )
    Makefile = ("Makefile", "makefile", "Makefile")
    GitIgnore = ("GitIgnore", "gitignore", ".gitignore")
    GitAttributes = ("GitAttributes", "gitattributes", ".gitattributes")
    EditorConfig = ("EditorConfig", "editorconfig", ".editorconfig")
    JenkinsFile = ("Jenkinsfile", "groovy", "Jenkinsfile")
    TravisCI = ("Travis CI", "yaml", ".travis.yml")
    CircleCI = ("Circle CI", "yaml", ".circleci/config.yml")
    GitHubActions = (
        "GitHub Actions",
        "yaml",
        ".github/workflows/*.yml",
        ".github/workflows/*.yaml",
    )
    SQL = ("SQL", "sql", ".sql")
    SQLite = ("SQLite", "sql", ".sqlite", ".db")
    GraphQL = ("GraphQL", "graphql", ".graphql", ".gql")
    Prisma = ("Prisma Schema", "prisma", "schema.prisma")
    DotEnv = ("Environment Variables", "env", ".env")
    RST = ("reStructuredText", "rst", ".rst")
    AsciiDoc = ("AsciiDoc", "asciidoc", ".adoc", ".asciidoc")
    License = ("License", "text", "LICENSE", "LICENSE.txt", "LICENSE.md")
    Binary = ("Binary", "binary", ".bin", ".exe", ".dll", ".so", ".dylib")

    @classmethod
    def from_extension(cls, file_path):
        import os

        file_name = os.path.corename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()

        for ft in cls:
            for ext in ft.extensions:
                if not ext.startswith(".") and file_name == ext:
                    return ft

        for ft in cls:
            for ext in ft.extensions:
                if ext.startswith(".") and file_ext == ext:
                    return ft

        return cls.Text


@define
class Block:
    sequence: int
    data: str
    metadata: Dict[str, Any] = field(factory=dict)


@define
class File:
    type: FileType = field(default=FileType.Text)
    name: str = ""
    path: str = ""
    stats: Dict[str, Any] = field(factory=dict)
    blocks: List[Block] = field(factory=list)


@define
class Directory:
    name: str
    path: str
    stats: Dict[str, Any]
    files: List[File] = field(factory=list)
    subdirectories: List["Directory"] = field(factory=list)


def lazy_load_dir(path, ignore_list=None):
    if ignore_list is None:
        ignore_list = [
            "bin",
            ".git",
            "node_modules",
            "__pycache__",
            ".venv",
            "venv",
            "*.egg-info",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "*.so",
            "*.dll",
            "*.exe",
            ".gitignore",
            ".idea",
            ".DS_Store",
        ]

    def should_ignore(entry_name):
        for pattern in ignore_list:
            if fnmatch.fnmatch(entry_name, pattern):
                return True
        return False

    def _get_directory_contents(dir_path, dir_name=None):
        if dir_name is None:
            dir_name = os.path.corename(dir_path) or "."

        result = {"type": "directory", "name": dir_name, "contents": []}

        try:
            entries = sorted(os.listdir(dir_path))
            for entry in entries:
                if should_ignore(entry):
                    continue

                entry_path = os.path.join(dir_path, entry)

                if os.path.isdir(entry_path):
                    subdir = _get_directory_contents(entry_path, entry)
                    result["contents"].append(subdir)
                else:
                    result["contents"].append({"type": "file", "name": entry})
        except (PermissionError, FileNotFoundError):
            pass

        return result

    root_structure = _get_directory_contents(path)
    return [root_structure]
