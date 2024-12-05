
from morphological_lexer import MorphologicalLexer
from result_analyzer import ResultsAnalyzer
from testing_framework import TestingFramework


def main():
    lexer = MorphologicalLexer()
    test_framework = TestingFramework()
    analyzer = ResultsAnalyzer()

    # Test cases
    test_code = """
    def calculate_area(radius):
        PI = 3.14159
        return PI * radius ** 2
    """

    # Run tests
    tokens = lexer.tokenize(test_code)
    results = test_framework.performance_test([test_code])
    analysis = analyzer.analyze_performance(results)

    print("Analysis Results:", analysis)


if __name__ == "__main__":
    main()
