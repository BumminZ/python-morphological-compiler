import time
from morphological_lexer import MorphologicalLexer
from memory_profiler import memory_usage


class TestingFramework:
    def __init__(self):
        self.lexer = MorphologicalLexer()

    def performance_test(self, test_cases):
        metrics = {
            'accuracy': 0,
            'processing_time': [],
            'memory_usage': [],
            'error_rate': 0
        }

        for code in test_cases:
            start_time = time.time()
            memory_start = memory_usage()[0]

            try:
                tokens = self.lexer.tokenize(code)
                metrics['accuracy'] += self.validate_tokens(tokens)
            except Exception as e:
                metrics['error_rate'] += 1

            metrics['processing_time'].append(time.time() - start_time)
            metrics['memory_usage'].append(memory_usage()[0] - memory_start)

        return self.calculate_final_metrics(metrics)

    def calculate_final_metrics(self, metrics):
        return {
            'avg_accuracy': metrics['accuracy'] / len(metrics['processing_time']),
            'avg_time': sum(metrics['processing_time']) / len(metrics['processing_time']),
            'avg_memory': sum(metrics['memory_usage']) / len(metrics['memory_usage']),
            'error_rate': metrics['error_rate']
        }

    def validate_tokens(self, tokens):
        return len([t for t in tokens if t['type'] in self.lexer.patterns]) / len(tokens)
