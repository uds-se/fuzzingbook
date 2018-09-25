#!/usr/bin/env python
# Run spellchecker on notebook
"""
usage:

python nbspellcheck.py notebooks...
"""

import io, os, sys, types, re
import string
import nbformat

# from https://github.com/barrust/pyspellchecker - `pip install pyspellchecker` 
from spellchecker import SpellChecker

KNOWN_WORDS = [
    'microsoft', 'google', 'fuzzer', 'fuzzed', 'fuzzing', 'sanitizer', 'openssl', 'heartbleed',
    'xkcd', 'codenomicon', 'redblack', 'mypy', 'newline', 'nonprintable', 'llvm', 'cryptographic',
    "you'll", "we'd", "here's", "memory-checking", 'fuzzers', 'placeholder', 'uninitialized',
    'cannot', 'sqrt', 'url', 'urls', 'iterable', "that's", "won't", "search-based", "mutation-based",
    "non-executable", "you're", "isn't", 'lowercase', "grammar-based", "blog", "wikipedia",
    "comma-separated", "turing-complete", "nonterminal", 'backus-naur', 'json', 'whitespace',
    'bnf', 'ebnf', 'nonterminals', 'string-based', 'tree-based', 'grammar-generated',
    'infty', 'algorithmically', 'subtree', 'visualizes', 'mutates', 'cgi-encoded',
    'white-box', 'black-box', 'initialization', 'non-implemented', 'jupyter', 'javascript',
    'firefox', 'debug', 'shellsort', 'quintillions', "we'll", 'zeller', 'rahul', 'gopinath',
    'iterates', 'parenthesized', 'metadata', 'html', 'github', 'makefile', "hasn't",
    'comprehensions', 'subclassing', 'subclassed', 'inline', 'markdown', 'bulleted',
    'cheatsheet', 'timeout', 'timeouts'
]

spell = SpellChecker()
spell.word_frequency.load_words(KNOWN_WORDS)

def print_utf8(s):
    sys.stdout.buffer.write(s.encode('utf-8'))
    
def normalize(word):
    # print(repr(word))
    word = word.lower()
    word = "".join([c for c in word if c in string.ascii_letters + "'-" ])
    return word

def get_words(text):
    words = text.split()
    ws = []
    for word in words:
        w = normalize(word)
        if w == '' or len(w) > 20:
            continue
        ws.append(w)
    return ws

RE_STUFF = re.compile(r'\([htf]*tp[^)]*\)|\([^)]*.[^).]+\)|`[^`]*`')

def strip_stuff(text):
    return re.sub(RE_STUFF, '', text)

def spellcheck_notebook(notebook_path):
    # load the notebook
    if notebook_path == '-':
        notebook = nbformat.read(sys.stdin, 4)
    else:
        with io.open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, 4)

    for cell in notebook.cells:
        if cell.cell_type != 'markdown':
            continue
        
        text = strip_stuff(cell.source)
        words = get_words(text)
        misspelled = spell.unknown(words)
        if len(misspelled) > 0:
            # print(cell.source)
            for word in misspelled:
                correction = spell.correction(word)
                if word == correction:
                    print("%s: unknown word %s" % (notebook_path, repr(word)))
                else:
                    print("%s: unknown word %s (did you mean %s?)" % 
                        (notebook_path, repr(word), repr(correction)))

if __name__ == "__main__":
    for notebook in sys.argv[1:]:
        spellcheck_notebook(notebook)
