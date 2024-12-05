from typing import List, Dict
from .morphological_lexer import MorphologicalLexer, Token


class TestingFramework:
    def __init__(self):
        self.lexer = MorphologicalLexer()
        self.test_cases = []
        self.results = []

    def add_test_case(self, code: str, expected_tokens: List[Dict]):
        """Add a test case with expected results"""
        self.test_cases.append({
            'code': code,
            'expected': expected_tokens
        })

    def run_tests(self) -> Dict:
        """Run all test cases and return results"""
        self.results = []

        for test_case in self.test_cases:
            result = self._run_single_test(test_case)
            self.results.append(result)

        return self._compile_test_results()

    def _run_single_test(self, test_case: Dict) -> Dict:
        """Run a single test case"""
        actual_tokens = self.lexer.tokenize(test_case['code'])
        expected_tokens = test_case['expected']

        matches = self._compare_tokens(actual_tokens, expected_tokens)

        return {
            'code': test_case['code'],
            'passed': matches,
            'actual_tokens': [str(token) for token in actual_tokens],
            'expected_tokens': expected_tokens,
            'metrics': self.lexer.get_metrics()
        }

    def _compare_tokens(self, actual: List[Token], expected: List[Dict]) -> bool:
        """Compare actual tokens with expected results"""
        if len(actual) != len(expected):
            return False

        for act, exp in zip(actual, expected):
            if act.type != exp.get('type') or act.value != exp.get('value'):
                return False

        return True

    def _compile_test_results(self) -> Dict:
        """Compile overall test results"""
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results if result['passed'])

        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': passed_tests / total_tests if total_tests > 0 else 0,
            'detailed_results': self.results
        }
