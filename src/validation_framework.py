from typing import List, Dict
from .morphological_lexer import Token


class ValidationFramework:
    def __init__(self):
        self.validation_rules = {
            'naming_convention': self._validate_naming_convention,
            'morpheme_structure': self._validate_morpheme_structure,
            'token_sequence': self._validate_token_sequence
        }

    def validate_tokens(self, tokens: List[Token]) -> Dict:
        """Validate tokens against all rules"""
        results = {}
        for rule_name, validator in self.validation_rules.items():
            results[rule_name] = validator(tokens)
        return results

    def _validate_naming_convention(self, tokens: List[Token]) -> Dict:
        """Validate naming conventions"""
        violations = []
        for token in tokens:
            if token.type == 'identifier':
                if not self._is_valid_convention(token):
                    violations.append({
                        'token': str(token),
                        'issue': 'Invalid naming convention'
                    })

        return {
            'valid': len(violations) == 0,
            'violations': violations
        }

    def _validate_morpheme_structure(self, tokens: List[Token]) -> Dict:
        """Validate morpheme structure"""
        violations = []
        for token in tokens:
            if token.type == 'identifier' and token.morphemes:
                if not self._is_valid_morpheme_structure(token):
                    violations.append({
                        'token': str(token),
                        'issue': 'Invalid morpheme structure'
                    })

        return {
            'valid': len(violations) == 0,
            'violations': violations
        }

    def _validate_token_sequence(self, tokens: List[Token]) -> Dict:
        """Validate token sequence"""
        violations = []
        for i in range(len(tokens) - 1):
            if not self._is_valid_sequence(tokens[i], tokens[i + 1]):
                violations.append({
                    'tokens': f"{tokens[i]} -> {tokens[i + 1]}",
                    'issue': 'Invalid token sequence'
                })

        return {
            'valid': len(violations) == 0,
            'violations': violations
        }

    def _is_valid_convention(self, token: Token) -> bool:
        """Check if token follows valid naming conventions"""
        if token.convention == 'snake_case':
            return '_' in token.value and token.value.islower()
        elif token.convention == 'camelCase':
            return token.value[0].islower() and not '_' in token.value
        elif token.convention == 'PascalCase':
            return token.value[0].isupper() and not '_' in token.value
        return True

    def _is_valid_morpheme_structure(self, token: Token) -> bool:
        """Check if morpheme structure is valid"""
        return len(token.morphemes) > 0

    def _is_valid_sequence(self, token1: Token, token2: Token) -> bool:
        """Check if token sequence is valid"""
        # Add your sequence validation rules here
        return True
