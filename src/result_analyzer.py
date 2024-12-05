from typing import List, Dict
from collections import defaultdict
from .morphological_lexer import Token


class ResultAnalyzer:
    def __init__(self):
        self.token_stats = defaultdict(int)
        self.convention_stats = defaultdict(int)
        self.morpheme_stats = defaultdict(int)

    def analyze_tokens(self, tokens: List[Token]) -> Dict:
        """Analyze token distribution and patterns"""
        self._reset_stats()

        for token in tokens:
            self.token_stats[token.type] += 1

            if token.type == 'identifier':
                self.convention_stats[token.convention] += 1
                for morpheme in token.morphemes:
                    self.morpheme_stats[morpheme] += 1

        return self.get_analysis_results()

    def _reset_stats(self):
        """Reset all statistics counters"""
        self.token_stats.clear()
        self.convention_stats.clear()
        self.morpheme_stats.clear()

    def get_analysis_results(self) -> Dict:
        """Return compiled analysis results"""
        return {
            'token_distribution': dict(self.token_stats),
            'naming_conventions': dict(self.convention_stats),
            'morpheme_frequency': dict(self.morpheme_stats),
            'total_tokens': sum(self.token_stats.values()),
            'unique_morphemes': len(self.morpheme_stats),
            'convention_summary': {
                'convention_type': max(self.convention_stats.items(),
                                       key=lambda x: x[1])[0] if self.convention_stats else None,
                'convention_counts': dict(self.convention_stats)
            }
        }
