import unittest
from src.morphological_lexer import MorphologicalLexer


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = MorphologicalLexer()
        self.test_code = """
        def calculate_area(radius):
            PI = 3.14159
            return PI * radius ** 2
        """

    def test_tokenize(self):
        tokens = self.lexer.tokenize(self.test_code)
        self.assertIsNotNone(tokens)
        self.assertTrue(len(tokens) > 0)
        self.assertEqual(tokens[0]['type'], 'keywords')

    def test_linguistics(self):
        tokens = self.lexer.tokenize(self.test_code)
        for token in tokens:
            if token['type'] == 'identifiers':
                analysis = self.lexer.analyze_linguistics(token)
                self.assertIsNotNone(analysis)
                self.assertIn('morphemes', analysis)
                self.assertIn('pattern', analysis)


if __name__ == '__main__':
    unittest.main()
