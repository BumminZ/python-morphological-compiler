# result_analyzer.py
class ResultsAnalyzer:
    def analyze_performance(self, test_results):
        return {
            'accuracy': {
                'mean': test_results['avg_accuracy'],
                'std_dev': 0  # Add standard deviation calculation if needed
            },
            'processing_time': {
                'mean': test_results['avg_time'],
                # Divide by token count if needed
                'per_token': test_results['avg_time']
            },
            'memory_usage': {
                'mean': test_results['avg_memory'],
                'peak': test_results['avg_memory']
            }
        }
