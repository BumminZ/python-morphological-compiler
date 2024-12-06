# Python Morphological Lexical Analyzer

A sophisticated lexical analyzer that incorporates linguistic morphological principles for enhanced token recognition and analysis in source code.

## Overview

This project implements a morphological lexical analyzer for programming languages, combining traditional compiler design techniques with linguistic analysis. It provides detailed token recognition, morpheme analysis, and performance metrics.

## Features

### Core Functionality

- Advanced token recognition with linguistic pattern analysis
- Morphological decomposition of identifiers
- Multiple naming convention detection (camelCase, snake_case. PascalCase)
- Comprehensive performance metrics tracking

### Analysis Capabilities

- Token pattern recognition
- Morpheme-based identifier analysis
- Statistical analysis of code structure
- Code convention validation

### Performance Features

- Real-time performance monitoring
- Memory usage tracking
- Processing speed optimization
- Error rate analysis

## Installation

### Prerequisites

Python 3.8 or higher
pip (Python package installer)

### Setup
1. Clone the repository

``` bash
git clone https://github.com/yourusername/python-morphological-lexer.git
cd python-morphological-lexer
```
2. Create and activate virtual environment (optional but recommended)


``` bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate 
```
3. Install required packages

```bash
pip install statistics
```

## Usage

### Basic Usage

``` python
from src.morphological_lexer import MorphologicalLexer

# Initialize lexer
lexer = MorphologicalLexer()

# Analyze code
code = """
def calculateTotalValue(pre_processed_data):
    unvalidated_result = 0
    return unvalidated_result
"""

tokens = lexer.tokenize(code)

# Print results
for token in tokens:
    if token.type == 'identifier':
        print(f"Identifier: {token.value}")
        print(f"Convention: {token.convention}")
        print(f"Morphemes: {token.morphemes}")
```

### Running Tests

``` bash
python -m unittest tests/test_lexer.py
```

## Features in Detail
### Token Recognition

- Keywords, identifiers, operators, numbers, strings
- Custom token type support
- Contextual token analysis

### Morphological Analysis

- Identifier decomposition
- Prefix/suffix recognition
- Compound word analysis
- Naming convention detection

### Performance Tracking

- Processing time per token
- Memory utilization
- Error rate monitoring
- Statistical analysis

## Requirements

Python 3.8+
statistics module (standard library)

## Author
Aung Tay Zar maung
Contact: aungtayzarmaung@gmail.com

## Acknowledgments

- Research paper: "Morphological Principles in Compiler Design: Improving Token Recognition and Processing Speed"
- Contributors and reviewers