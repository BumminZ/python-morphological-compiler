import unittest
from src.morphological_lexer import MorphologicalLexer, Token


class TestMorphologicalLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = MorphologicalLexer()

    def test_basic_tokenization(self):
        code = "def test_function():"
        tokens = self.lexer.tokenize(code)

        self.assertEqual(len(tokens), 4)
        self.assertEqual(tokens[0].type, 'keyword')
        self.assertEqual(tokens[1].type, 'identifier')

    def test_identifier_morphemes(self):
        code = "calculateTotalValue"
        tokens = self.lexer.tokenize(code)

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].morphemes, ['calculate', 'Total', 'Value'])

    def test_naming_conventions(self):
        test_cases = {
            "snake_case_var": "snake_case",
            "camelCaseVar": "camelCase",
            "PascalCaseVar": "PascalCase",
            "CONSTANT_VAR": "CONSTANT_CASE"
        }

        for identifier, expected_convention in test_cases.items():
            tokens = self.lexer.tokenize(identifier)
            self.assertEqual(len(tokens), 1)
            self.assertEqual(tokens[0].convention, expected_convention)

    def test_complex_code(self):
        code = """
        def processUserData(pre_processed_input):
            MAX_RETRY_COUNT = 3
            unvalidatedResult = 0
            
            for item in pre_processed_input:
                if item > MAX_RETRY_COUNT:
                    continue
                unvalidatedResult += processImplementation(item)
            
            return unvalidatedResult
        """
        tokens = self.lexer.tokenize(code)

        # Verify key tokens
        identifiers = [t for t in tokens if t.type == 'identifier']
        keywords = [t for t in tokens if t.type == 'keyword']

        self.assertTrue(any(t.value == 'processUserData' for t in identifiers))
        self.assertTrue(any(t.value == 'MAX_RETRY_COUNT' for t in identifiers))
        self.assertTrue(any(t.value == 'def' for t in keywords))
        self.assertTrue(any(t.value == 'return' for t in keywords))

    def test_operator_recognition(self):
        code = "a + b * c / d"
        tokens = self.lexer.tokenize(code)

        operators = [t for t in tokens if t.type == 'operator']
        self.assertEqual(len(operators), 3)
        self.assertEqual([op.value for op in operators], ['+', '*', '/'])

    def test_string_literals(self):
        code = '"test string" "another \\"quoted\\" string"'
        tokens = self.lexer.tokenize(code)

        strings = [t for t in tokens if t.type == 'string']
        self.assertEqual(len(strings), 2)
        self.assertEqual(strings[0].value, '"test string"')

    def test_number_literals(self):
        code = "42 3.14159 0.123"
        tokens = self.lexer.tokenize(code)

        numbers = [t for t in tokens if t.type == 'number']
        self.assertEqual(len(numbers), 3)
        self.assertEqual([n.value for n in numbers],
                         ['42', '3.14159', '0.123'])

    def test_morpheme_analysis(self):
        test_cases = {
            "preProcessedData": ["pre", "Processed", "Data"],
            "unvalidatedResult": ["un", "validated", "Result"],
            "postImplementationHook": ["post", "Implementation", "Hook"]
        }

        for identifier, expected_morphemes in test_cases.items():
            tokens = self.lexer.tokenize(identifier)
            self.assertEqual(len(tokens), 1)
            self.assertEqual(tokens[0].morphemes, expected_morphemes)

    def test_error_handling(self):
        code = "valid_identifier @ invalid_char #"
        tokens = self.lexer.tokenize(code)

        # Should still tokenize valid parts
        self.assertTrue(any(t.value == 'valid_identifier' for t in tokens))
        self.assertEqual(self.lexer.error_count, 2)  # For @ and #

    def test_performance_metrics(self):
        code = "def test_function(): pass"
        self.lexer.tokenize(code)
        metrics = self.lexer.get_metrics()

        self.assertIn('average_processing_time', metrics)
        self.assertIn('total_tokens', metrics)
        self.assertIn('error_rate', metrics)


if __name__ == '__main__':
    unittest.main()
