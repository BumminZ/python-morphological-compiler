
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from collections import defaultdict
import re
import time
import statistics
import tracemalloc
from datetime import datetime


@dataclass
class Token:
    """Class representing a token with its properties"""
    type: str
    value: str
    start: int
    end: int
    morphemes: List[str] = field(default_factory=list)
    convention: str = None
    line_number: int = 1
    column: int = 0

    def __str__(self) -> str:
        return f"Token(type='{self.type}', value='{self.value}', morphemes={self.morphemes}, convention='{self.convention}')"

    def __repr__(self) -> str:
        return self.__str__()


class MorphologicalLexer:
    """Lexical analyzer with morphological analysis capabilities"""

    def __init__(self):
        # Token patterns
        self.patterns = {
            'keyword': r'\b(def|class|return|if|while|for|import|from|as)\b',
            'identifier': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'operator': r'[+\-*/=<>!&|^%]+',
            'number': r'\d+(\.\d+)?',
            'string': r'\"([^\"\\]|\\.)*\"',
            'delimiter': r'[\(\)\[\]\{\},;:]',
            'whitespace': r'\s+'
        }

        # Compile patterns for performance
        self.compiled_patterns = {
            name: re.compile(pattern)
            for name, pattern in self.patterns.items()
        }

        # Morpheme analysis configuration
        self.morpheme_patterns = {
            'prefix': ['un', 'pre', 'post', 'sub', 'super', 'inter'],
            'suffix': ['able', 'ible', 'er', 'or', 'tion', 'sion', 'ment'],
            'compound_separator': ['_', r'(?=[A-Z])']
        }

        # Performance metrics
        self.metrics = defaultdict(list)
        self.token_count = 0
        self.error_count = 0

    def tokenize(self, code: str) -> List[Token]:
        """
        Tokenize input code and perform morphological analysis.

        Args:
            code (str): Source code to analyze

        Returns:
            List[Token]: List of analyzed tokens
        """
        tokens = []
        position = 0
        line = 1
        column = 0

        # Initialize performance monitoring
        start_time = time.time()
        tracemalloc.start()

        while position < len(code):
            # Handle newlines
            if code[position] == '\n':
                line += 1
                column = 0
                position += 1
                continue

            # Skip whitespace
            if code[position].isspace():
                position += 1
                column += 1
                continue

            # Try matching patterns
            token = None
            for token_type, pattern in self.compiled_patterns.items():
                if token_type == 'whitespace':
                    continue

                match = pattern.match(code, position)
                if match:
                    value = match.group(0)
                    token = Token(
                        type=token_type,
                        value=value,
                        start=position,
                        end=position + len(value),
                        line_number=line,
                        column=column
                    )

                    # Perform morphological analysis for identifiers
                    if token_type == 'identifier':
                        token.morphemes = self._analyze_morphemes(value)
                        token.convention = self._detect_naming_convention(
                            value)

                    tokens.append(token)
                    position = match.end()
                    column += len(value)
                    break

            # Handle unrecognized characters
            if not token:
                position += 1
                column += 1
                self.error_count += 1

        # Update performance metrics
        self._update_metrics(start_time)
        tracemalloc.stop()
        self.token_count += len(tokens)

        return tokens

    def _analyze_morphemes(self, identifier: str) -> List[str]:
        """
        Analyze identifier into morphological components.

        Args:
            identifier (str): Identifier to analyze

        Returns:
            List[str]: List of identified morphemes
        """
        if not identifier:
            return []

        # Split on boundaries (camelCase and snake_case)
        parts = re.split('_|(?=[A-Z])', identifier)
        parts = [p for p in parts if p]

        if not parts:
            return [identifier]

        morphemes = []
        for part in parts:
            if not part:
                continue

            part_lower = part.lower()

            # Check for prefixes
            prefix_found = False
            for prefix in self.morpheme_patterns['prefix']:
                if part_lower.startswith(prefix) and len(part) > len(prefix):
                    morphemes.append(prefix)
                    part = part[len(prefix):]
                    part_lower = part.lower()
                    prefix_found = True
                    break

            # Check for suffixes
            suffix_found = False
            for suffix in self.morpheme_patterns['suffix']:
                if part_lower.endswith(suffix) and len(part) > len(suffix):
                    remaining = part[:-len(suffix)]
                    if remaining:
                        morphemes.append(remaining)
                    morphemes.append(suffix)
                    suffix_found = True
                    break

            # Add remaining part if no suffix found
            if not suffix_found and part:
                morphemes.append(part)

        return morphemes

    def _detect_naming_convention(self, identifier: str) -> str:
        """
        Detect naming convention used in identifier.

        Args:
            identifier (str): Identifier to analyze

        Returns:
            str: Detected naming convention
        """
        if not identifier:
            return None

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

    def _update_metrics(self, start_time: float) -> None:
        """
        Update performance metrics.

        Args:
            start_time (float): Processing start time
        """
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()

        self.metrics['processing_time'].append(end_time - start_time)
        self.metrics['memory_usage'].append(
            current / 1024 / 1024)  # Convert to MB
        self.metrics['peak_memory'].append(peak / 1024 / 1024)  # Convert to MB

    def get_metrics(self) -> Dict:
        """
        Get performance metrics.

        Returns:
            Dict: Dictionary of performance metrics
        """
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
