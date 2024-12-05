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
