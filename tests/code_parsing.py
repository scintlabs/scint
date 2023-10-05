import unittest

from base.processing.parsers import PARSER_PYTHON, CodeParser


class TestCodeDataModel(unittest.TestCase):
    def test_code_tokenization_and_comment_extraction(self):
        content = """
        # This is a comment
        def foo():
            # Another comment
            print('Hello, World!')

        class bar:
            __init__(self):
                # One more comment
                pass

        # Final comment
        """
        code_data_model = CodeParser(content, PARSER_PYTHON)
        expected_tokens = [
            "comment",
            "def",
            "identifier",
            "(",
            ")",
            ":",
            "comment",
            "identifier",
            "(",
            "string_start",
            "string_content",
            "string_end",
            ")",
            "class",
            "identifier",
            ":",
            "identifier",
            "(",
            "identifier",
            ")",
            ":",
            "comment",
            "pass",
            "ERROR",
            "comment",
        ]
        expected_comments = [
            "# This is a comment",
            "# Another comment",
            "# One more comment",
            "# Final comment",
        ]

        self.assertEqual(code_data_model.tokens, expected_tokens)
        self.assertEqual(code_data_model.comments, expected_comments)
