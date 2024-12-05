import re


class MorphologicalLexer:
    def __init__(self):
        self.patterns = {
            'keywords': r'\b(def|class|return|if|while|for|in|import|from|as)\b',
            'identifiers': r'[a-zA-Z_][a-zA-Z0-9_]*',
            'operators': r'[\+\-\*/=<>!&|^%]',
            'numbers': r'\d+(\.\d+)?',
            'strings': r'\".*?\"|\'.*?\'',
            'comments': r'#.*$'
        }

    def tokenize(self, code):
        tokens = []
        for pattern_type, regex in self.patterns.items():
            matches = re.finditer(regex, code)
            for match in matches:
                tokens.append({
                    'type': pattern_type,
                    'value': match.group(),
                    'position': match.span()
                })
        return sorted(tokens, key=lambda x: x['position'][0])

    def analyze_linguistics(self, token):
        prefixes = ['un', 're', 'de', 'pre']
        suffixes = ['able', 'ize', 'ment', 'tion']

        if token['type'] == 'identifiers':
            value = token['value']
            return {
                'morphemes': {
                    'prefix': [p for p in prefixes if value.startswith(p)],
                    'suffix': [s for s in suffixes if value.endswith(s)],
                    'root': self._extract_root(value, prefixes, suffixes)
                },
                'pattern': self._detect_naming_pattern(value)
            }
        return None

    def _extract_root(self, word, prefixes, suffixes):
        for p in prefixes:
            if word.startswith(p):
                word = word[len(p):]
        for s in suffixes:
            if word.endswith(s):
                word = word[:-len(s)]
        return word

    def _detect_naming_pattern(self, identifier):
        if '_' in identifier:
            return 'snake_case'
        elif identifier[0].isupper():
            return 'PascalCase'
        elif any(c.isupper() for c in identifier[1:]):
            return 'camelCase'
        return 'lowercase'
