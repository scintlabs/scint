import unittest

from base.parsing.text import TextParser


class TestTextDataModel(unittest.TestCase):
    def test_tokenization_lemmatization_entity_recognition(self):
        content = "Apple is looking at buying U.K. startup for $1 billion"
        text_data_model = TextParser(content)
        expected_tokens = [
            "Apple",
            "is",
            "looking",
            "at",
            "buying",
            "U.K.",
            "startup",
            "for",
            "$",
            "1",
            "billion",
        ]
        expected_lemmas = [
            "Apple",
            "be",
            "look",
            "at",
            "buy",
            "U.K.",
            "startup",
            "for",
            "$",
            "1",
            "billion",
        ]
        expected_entities = ["Apple", "U.K.", "$1 billion"]

        self.assertEqual(text_data_model.tokens, expected_tokens)
        self.assertEqual(text_data_model.lemmas, expected_lemmas)
        self.assertEqual(text_data_model.entities, expected_entities)
