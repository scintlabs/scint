from unittest.mock import MagicMock, patch

import pytest
from scint.core.tasks.parse import (
    parse,
    parse_node,
    parse_strategy,
    parse_tree,
    parse_tree_strategy,
    read_file,
    with_filters,
    with_strategy,
    with_types,
)
from tree_sitter import Node, Parser, Tree


@pytest.fixture
def mock_config():
    return {
        "filetype": {
            "python": {
                "types": ["function_definition", "class_definition"],
                "filters": ["identifier"],
            }
        }
    }


def test_read_file():
    with patch("builtins.open", MagicMock()) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = (
            b"test content"
        )
        result = read_file("test.py")
        assert result == b"test content"
        mock_open.assert_called_once_with("test.py", "rb")


def test_parse_node():
    source = b"def test_function():\n    pass"
    node = MagicMock(spec=Node)
    node.type = "function_definition"
    node.start_byte = 0
    node.end_byte = len(source)
    node.children = []

    result = parse_node(source, node, ["function_definition"], ["function_definition"])
    assert result == [{"function_definition": "def test_function():\n    pass"}]


def test_parse_tree():
    source = b"def test_function():\n    pass"
    tree = MagicMock(spec=Tree)
    root_node = MagicMock(spec=Node)
    child_node = MagicMock(spec=Node)
    child_node.type = "function_definition"
    child_node.start_byte = 0
    child_node.end_byte = len(source)
    child_node.children = []
    root_node.children = [child_node]
    tree.root_node = root_node

    result = parse_tree(source, tree, ["function_definition"], ["function_definition"])
    assert result == [{"function_definition": "def test_function():\n    pass"}]


def test_parse_strategy():
    source = b"def test_function():\n    pass"
    node = MagicMock(spec=Node)
    node.type = "function_definition"
    node.start_byte = 0
    node.end_byte = len(source)
    node.children = []

    result = parse_strategy(source, node, ["function_definition"])
    assert result == [{"function_definition": "def test_function():\n    pass"}]


def test_parse_tree_strategy():
    source = b"def test_function():\n    pass"
    tree = MagicMock(spec=Tree)
    root_node = MagicMock(spec=Node)
    child_node = MagicMock(spec=Node)
    child_node.type = "function_definition"
    child_node.start_byte = 0
    child_node.end_byte = len(source)
    child_node.children = []
    root_node.children = [child_node]
    tree.root_node = root_node

    result = parse_tree_strategy(source, tree, ["function_definition"])
    assert result == [{"function_definition": "def test_function():\n    pass"}]


def test_with_types(mock_config):
    types_func = with_types(mock_config, "python")
    result = types_func(None)
    assert result == ["function_definition", "class_definition"]


def test_with_filters(mock_config):
    filters_func = with_filters(mock_config, "python")
    result = filters_func(None)
    assert result == ["identifier"]


def test_with_strategy():
    strategy_func = with_strategy("python", depth=2)
    result = strategy_func(None)
    assert callable(result)


@patch("scint.core.process.parse.get_parser")
@patch("scint.core.process.parse.get_language")
@patch("scint.core.process.parse.read_file")
@patch("scint.core.process.parse.parse_tree")
def test_parse(
    mock_parse_tree, mock_read_file, mock_get_language, mock_get_parser, mock_config
):
    mock_parser = MagicMock(spec=Parser)
    mock_get_parser.return_value = mock_parser
    mock_tree = MagicMock(spec=Tree)
    mock_parser.parse.return_value = mock_tree

    mock_read_file.return_value = b"def test_function():\n    pass"
    mock_parse_tree.return_value = [
        {"function_definition": "def test_function():\n    pass"}
    ]

    result = parse(mock_config, "python", "test.py")

    mock_get_parser.assert_called_once_with("python")
    mock_get_language.assert_called_once_with("python")
    mock_read_file.assert_called_once_with("test.py")
    mock_parse_tree.assert_called_once_with(
        mock_read_file.return_value,
        mock_tree,
        ["function_definition", "class_definition"],
        ["identifier"],
    )
    assert result == [{"function_definition": "def test_function():\n    pass"}]
