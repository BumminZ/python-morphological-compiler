from src.morphological_lexer import MorphologicalLexer
from src.result_analyzer import ResultsAnalyzer
from src.testing_framework import TestingFramework
from src.validation_framework import ValidationFramework


def main():
    # Initialize components
    lexer = MorphologicalLexer()
    test_framework = TestingFramework()
    validator = ValidationFramework()
    analyzer = ResultsAnalyzer()

    # Test code sample
    test_code = """
   def calculate_area(radius):
       PI = 3.14159
       return PI * radius ** 2
   """

    # Process and analyze
    tokens = lexer.tokenize(test_code)
    results = test_framework.performance_test([test_code])
    analysis = analyzer.analyze_performance(results)
    validation = validator.validate_code(test_code)

    # Print results
    print("\nTokens found:")
    for token in tokens:
        print(f"Type: {token['type']}, Value: {
              token['value']}, Position: {token['position']}")

    analyzer.format_results(analysis)
    print("\nAnalysis Results:", analysis)
    print("\nValidation Results:", validation)


if __name__ == "__main__":
    main()
