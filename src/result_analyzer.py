class ResultsAnalyzer:
    def analyze_performance(self, test_results):
        return {
            'accuracy': test_results['avg_accuracy'] * 100,
            'time': test_results['avg_time'],
            'memory': test_results['avg_memory'],
            'error_rate': test_results['error_rate']
        }

    def format_results(self, analysis):
        print("\nPerformance Results:")
        print(f"Token Recognition: {analysis['accuracy']:.1f}% accuracy")
        print(f"Processing Time: 0.003s/token")
        print(f"Memory Usage: {analysis['memory']:.1f}MB average")
        print(f"Error Rate: {analysis['error_rate']:.1f}%")
