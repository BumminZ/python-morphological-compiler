from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import defaultdict
import re
import time
import statistics
import tracemalloc


@dataclass
class Token:
    """Represents a token with its morphological properties"""
    type: str
    value: str
    start: int
    end: int
    morphemes: List[str] = field(default_factory=list)
    convention: str = None

    def __str__(self):
        return f"Token(type='{self.type}', value='{self.value}', morphemes={self.morphemes}, convention='{self.convention}')"


class MorphologicalLexer:
    def __init__(self):
        # Initialize token patterns
        self.patterns = {
            'keyword': r'\b(def|class|return|if|while|for|import|from|as)\b',
            'identifier': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'operator': r'[+\-*/=<>!&|^%]+',
            'number': r'\d+(\.\d+)?',
            'string': r'\"([^\"\\]|\\.)*\"',
            'delimiter': r'[\(\)\[\]\{\},;:]',
            'whitespace': r'\s+'
        }

        self.compiled_patterns = {
            name: re.compile(pattern)
            for name, pattern in self.patterns.items()
        }

        self.morpheme_patterns = {
            'prefix': ['un', 'pre', 'post', 'sub', 'super', 'inter'],
            'suffix': ['able', 'ible', 'er', 'or', 'tion', 'sion', 'ment'],
            'compound_separator': ['_', r'(?=[A-Z])']
        }

        self.metrics = defaultdict(list)
        self.token_count = 0
        self.error_count = 0

    def tokenize(self, code: str) -> List[Token]:
        """Tokenize the input code and perform morphological analysis"""
        tokens = []
        pos = 0
        start_time = time.time()
        tracemalloc.start()

        while pos < len(code):
            token = None
            for token_type, pattern in self.compiled_patterns.items():
                match = pattern.match(code, pos)
                if match:
                    value = match.group(0)
                    if token_type != 'whitespace':
                        token = Token(
                            type=token_type,
                            value=value,
                            start=pos,
                            end=pos + len(value)
                        )

                        if token_type == 'identifier':
                            token.morphemes = self._analyze_morphemes(value)
                            token.convention = self._detect_naming_convention(
                                value)

                        tokens.append(token)

                    pos = match.end()
                    break

            if token is None:
                pos += 1
                self.error_count += 1

        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.metrics['processing_time'].append(end_time - start_time)
        self.metrics['memory_usage'].append(current / 1024 / 1024)
        self.metrics['peak_memory'].append(peak / 1024 / 1024)
        self.token_count += len(tokens)

        return tokens

    def _analyze_morphemes(self, identifier: str) -> List[str]:
        """Break down an identifier into its morphological components"""
        morphemes = []
        parts = re.split('_|(?=[A-Z])', identifier)
        parts = [p for p in parts if p]

        for part in parts:
            part_lower = part.lower()

            prefix_found = False
            for prefix in self.morpheme_patterns['prefix']:
                if part_lower.startswith(prefix):
                    morphemes.append(prefix)
                    part = part[len(prefix):]
                    prefix_found = True
                    break

            suffix_found = False
            for suffix in self.morpheme_patterns['suffix']:
                if part_lower.endswith(suffix):
                    morphemes.append(suffix)
                    part = part[:-len(suffix)]
                    suffix_found = True
                    break

            if part:
                morphemes.append(part)

        return morphemes

    def _detect_naming_convention(self, identifier: str) -> str:
        """Detect the naming convention used in the identifier"""
        if '_' in identifier:
            if identifier.isupper():
                return 'CONSTANT_CASE'
            if identifier.startswith('_'):
                if identifier[1:].isupper():
                    return 'PRIVATE_CONSTANT_CASE'
                return 'private_snake_case'
            return 'snake_case'
        elif re.search('[A-Z]', identifier):
            if identifier[0].isupper():
                return 'PascalCase'
            return 'camelCase'
        return 'lowercase'

    def get_metrics(self) -> Dict:
        """Return performance metrics"""
        if not self.metrics['processing_time']:
            return {}

        return {
            'average_processing_time': statistics.mean(self.metrics['processing_time']),
            'total_tokens': self.token_count,
            'error_rate': self.error_count / max(1, self.token_count),
            'average_memory_usage': statistics.mean(self.metrics['memory_usage']),
            'peak_memory_usage': max(self.metrics['peak_memory']),
            'tokens_per_second': self.token_count / sum(self.metrics['processing_time'])
        }
