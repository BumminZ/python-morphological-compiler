from dataclasses import dataclass
from typing import List, Dict, Optional
from collections import defaultdict, Counter
from datetime import datetime
from .morphological_lexer import Token


@dataclass
class AnalysisMetrics:
    """Data class to hold analysis metrics"""
    total_tokens: int
    unique_morphemes: int
    avg_token_length: float
    convention_distribution: Dict[str, float]
    pattern_accuracy: Dict[str, float]


class ResultAnalyzer:
    def __init__(self):
        self.token_stats = defaultdict(int)
        self.convention_stats = defaultdict(int)
        self.morpheme_stats = defaultdict(int)
        self.pattern_stats = defaultdict(list)
        self.analysis_timestamp = None

    def analyze_tokens(self, tokens: List[Token]) -> Dict:
        """Analyze token distribution and patterns with enhanced metrics"""
        self._reset_stats()
        self.analysis_timestamp = datetime.now()

        total_length = 0
        identifier_count = 0

        for token in tokens:
            # Basic token statistics
            self.token_stats[token.type] += 1
            total_length += len(token.value)

            if token.type == 'identifier':
                identifier_count += 1
                self._analyze_identifier(token)

        # Calculate advanced metrics
        metrics = self._calculate_metrics(
            total_length, len(tokens), identifier_count)

        return self._compile_results(metrics)

    def _analyze_identifier(self, token: Token) -> None:
        """Analyze individual identifier patterns and conventions"""
        # Convention analysis
        self.convention_stats[token.convention] += 1

        # Morpheme analysis
        for morpheme in token.morphemes:
            self.morpheme_stats[morpheme] += 1

        # Pattern analysis
        self._analyze_patterns(token)

    def _analyze_patterns(self, token: Token) -> None:
        """Analyze identifier patterns in detail"""
        # Length pattern
        self.pattern_stats['length'].append(len(token.value))

        # Complexity patterns
        has_number = any(c.isdigit() for c in token.value)
        has_underscore = '_' in token.value
        has_camel_case = any(c.isupper() for c in token.value[1:])

        self.pattern_stats['complexity'].append({
            'has_number': has_number,
            'has_underscore': has_underscore,
            'has_camel_case': has_camel_case
        })

    def _calculate_metrics(self, total_length: int, token_count: int,
                           identifier_count: int) -> AnalysisMetrics:
        """Calculate comprehensive analysis metrics"""
        if token_count == 0:
            return AnalysisMetrics(0, 0, 0.0, {}, {})

        # Calculate averages and distributions
        avg_token_length = total_length / token_count

        # Convention distribution
        total_conventions = sum(self.convention_stats.values())
        convention_dist = {
            conv: (count / total_conventions *
                   100) if total_conventions > 0 else 0
            for conv, count in self.convention_stats.items()
        }

        # Pattern accuracy
        pattern_accuracy = self._calculate_pattern_accuracy()

        return AnalysisMetrics(
            total_tokens=token_count,
            unique_morphemes=len(self.morpheme_stats),
            avg_token_length=avg_token_length,
            convention_distribution=convention_dist,
            pattern_accuracy=pattern_accuracy
        )

    def _calculate_pattern_accuracy(self) -> Dict[str, float]:
        """Calculate pattern recognition accuracy"""
        if not self.pattern_stats['complexity']:
            return {}

        total_patterns = len(self.pattern_stats['complexity'])
        accuracies = {
            'number_usage': sum(1 for p in self.pattern_stats['complexity']
                                if p['has_number']) / total_patterns * 100,
            'underscore_usage': sum(1 for p in self.pattern_stats['complexity']
                                    if p['has_underscore']) / total_patterns * 100,
            'camel_case_usage': sum(1 for p in self.pattern_stats['complexity']
                                    if p['has_camel_case']) / total_patterns * 100
        }
        return accuracies

    def _reset_stats(self) -> None:
        """Reset all statistics counters"""
        self.token_stats.clear()
        self.convention_stats.clear()
        self.morpheme_stats.clear()
        self.pattern_stats = defaultdict(list)
        self.analysis_timestamp = None

    def _compile_results(self, metrics: AnalysisMetrics) -> Dict:
        """Compile and return comprehensive analysis results"""
        return {
            'timestamp': self.analysis_timestamp,
            'token_distribution': dict(self.token_stats),
            'naming_conventions': dict(self.convention_stats),
            'morpheme_frequency': dict(self.morpheme_stats),
            'total_tokens': metrics.total_tokens,
            'unique_morphemes': metrics.unique_morphemes,
            'average_token_length': round(metrics.avg_token_length, 2),
            'convention_distribution': metrics.convention_distribution,
            'pattern_accuracy': metrics.pattern_accuracy,
            'convention_summary': {
                'most_common': max(self.convention_stats.items(),
                                   key=lambda x: x[1])[0] if self.convention_stats else None,
                'convention_counts': dict(self.convention_stats)
            }
        }
