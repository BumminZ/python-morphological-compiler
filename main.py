from src.morphological_lexer import MorphologicalLexer
from src.result_analyzer import ResultAnalyzer
from src.validation_framework import ValidationFramework
import sys


def main():
    # Initialize components
    lexer = MorphologicalLexer()
    analyzer = ResultAnalyzer()
    validator = ValidationFramework()

    # Sample code
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

    # Perform lexical analysis
    print("Performing lexical analysis...")
    tokens = lexer.tokenize(code)

    # Display tokens
    print("\nTokens found:")
    for token in tokens:
        if token.type == 'identifier':
            print(f"\nIdentifier: {token.value}")
            print(f"Convention: {token.convention}")
            print(f"Morphemes: {token.morphemes}")

    # Analyze results
    print("\nAnalyzing results...")
    analysis = analyzer.analyze_tokens(tokens)
    print("\nAnalysis results:")
    for key, value in analysis.items():
        print(f"{key}: {value}")

    # Validate tokens
    print("\nValidating tokens...")
    validation_results = validator.validate_tokens(tokens)
    print("\nValidation results:")
    for rule, result in validation_results.items():
        print(f"\n{rule}:")
        print(f"Valid: {result['valid']}")
        if not result['valid']:
            print("Violations:")
            for violation in result['violations']:
                print(f"- {violation}")

    # Display performance metrics
    print("\nPerformance Metrics:")
    metrics = lexer.get_metrics()
    for metric, value in metrics.items():
        print(f"{metric}: {value}")


if __name__ == "__main__":
    main()
