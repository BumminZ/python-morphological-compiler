from .morphological_lexer import MorphologicalLexer


class ValidationFramework:
    def __init__(self):
        self.lexer = MorphologicalLexer()

    def validate_code(self, code):
        metrics = {
            'syntax': self._validate_syntax(code),
            'tokens': self._validate_tokens(self.lexer.tokenize(code)),
            'linguistics': self._validate_linguistics(code)
        }
        return metrics

    def _validate_syntax(self, code):
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False

    def _validate_tokens(self, tokens):
        valid_tokens = 0
        total_tokens = len(tokens)

        for token in tokens:
            if self._is_valid_token(token):
                valid_tokens += 1

        return valid_tokens / total_tokens if total_tokens > 0 else 0

    def _is_valid_token(self, token):
        return (
            token['type'] in self.lexer.patterns and
            token['value'] and
            isinstance(token['position'], tuple) and
            len(token['position']) == 2
        )

    def _validate_linguistics(self, code):
        tokens = self.lexer.tokenize(code)
        linguistic_validity = {
            'naming_conventions': 0,
            'morpheme_analysis': 0
        }

        for token in tokens:
            if token['type'] == 'identifiers':
                analysis = self.lexer.analyze_linguistics(token)
                if analysis:
                    linguistic_validity['naming_conventions'] += self._check_naming_convention(
                        analysis)
                    linguistic_validity['morpheme_analysis'] += self._check_morphemes(
                        analysis)

        return linguistic_validity

    def _check_naming_convention(self, analysis):
        return 1 if analysis['pattern'] in ['snake_case', 'camelCase', 'PascalCase'] else 0

    def _check_morphemes(self, analysis):
        return 1 if analysis['morphemes']['root'] else 0
