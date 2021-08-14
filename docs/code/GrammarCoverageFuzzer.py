#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Grammar Coverage" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/GrammarCoverageFuzzer.html
# Last change: 2021-06-04 14:55:54+02:00
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r'''
The Fuzzing Book - Grammar Coverage

This file can be _executed_ as a script, running all experiments:

    $ python GrammarCoverageFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.GrammarCoverageFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/GrammarCoverageFuzzer.html

This chapter introduces `GrammarCoverageFuzzer`, an efficient grammar fuzzer extending `GrammarFuzzer` from the [chapter on efficient grammar fuzzing](GrammarFuzzer.ipynb).  It strives to cover all expansions at least once.  In the following example, for instance, all digits in the area code are different, as are the digits in the line number:

>>> from Grammars import US_PHONE_GRAMMAR
>>> phone_fuzzer = GrammarCoverageFuzzer(US_PHONE_GRAMMAR)
>>> phone_fuzzer.fuzz()
'(521)383-0695'

After fuzzing, the `expansion_coverage()` method returns a mapping of grammar expansions covered.

>>> phone_fuzzer.expansion_coverage()
{' -> ',
 ' -> 0',
 ' -> 1',
 ' -> 2',
 ' -> 3',
 ' -> 5',
 ' -> 6',
 ' -> 8',
 ' -> 9',
 ' -> ',
 ' -> 3',
 ' -> 5',
 ' -> ',
 ' -> ()-',
 ' -> '}

Subsequent calls to `fuzz()` will go for further coverage (i.e., covering the other area code digits, for example); a call to `reset()` clears the recored coverage, starting anew.

Since such coverage in inputs also yields higher code coverage, `GrammarCoverageFuzzer` is a recommended extension to `GrammarFuzzer`.


For more details, source, and documentation, see
"The Fuzzing Book - Grammar Coverage"
at https://www.fuzzingbook.org/html/GrammarCoverageFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Grammar Coverage
# ================

if __name__ == '__main__':
    print('# Grammar Coverage')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Covering Grammar Elements
## -------------------------

if __name__ == '__main__':
    print('\n## Covering Grammar Elements')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .Grammars import EXPR_GRAMMAR, CGI_GRAMMAR, URL_GRAMMAR, START_SYMBOL
from .Grammars import is_valid_grammar, extend_grammar

if __name__ == '__main__':
    EXPR_GRAMMAR["<factor>"]

### Tracking Grammar Coverage

if __name__ == '__main__':
    print('\n### Tracking Grammar Coverage')



from .GrammarFuzzer import GrammarFuzzer, all_terminals, nonterminals, display_tree

import random

class TrackingGrammarCoverageFuzzer(GrammarFuzzer):
    def __init__(self, *args, **kwargs):
        # invoke superclass __init__(), passing all arguments
        super().__init__(*args, **kwargs)
        self.reset_coverage()

    def reset_coverage(self):
        self.covered_expansions = set()

    def expansion_coverage(self):
        return self.covered_expansions

def expansion_key(symbol, expansion):
    """Convert (symbol, expansion) into a key.  `expansion` can be an expansion string or a derivation tree."""
    if isinstance(expansion, tuple):
        expansion = expansion[0]
    if not isinstance(expansion, str):
        children = expansion
        expansion = all_terminals((symbol, children))
    return symbol + " -> " + expansion

if __name__ == '__main__':
    expansion_key(START_SYMBOL, EXPR_GRAMMAR[START_SYMBOL][0])

if __name__ == '__main__':
    children = [("<expr>", None), (" + ", []), ("<term>", None)]
    expansion_key("<expr>", children)

class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def _max_expansion_coverage(self, symbol, max_depth):
        if max_depth <= 0:
            return set()

        self._symbols_seen.add(symbol)

        expansions = set()
        for expansion in self.grammar[symbol]:
            expansions.add(expansion_key(symbol, expansion))
            for nonterminal in nonterminals(expansion):
                if nonterminal not in self._symbols_seen:
                    expansions |= self._max_expansion_coverage(
                        nonterminal, max_depth - 1)

        return expansions

    def max_expansion_coverage(self, symbol=None, max_depth=float('inf')):
        """Return set of all expansions in a grammar starting with `symbol`"""
        if symbol is None:
            symbol = self.start_symbol

        self._symbols_seen = set()
        cov = self._max_expansion_coverage(symbol, max_depth)

        if symbol == START_SYMBOL:
            assert len(self._symbols_seen) == len(self.grammar)

        return cov

if __name__ == '__main__':
    expr_fuzzer = TrackingGrammarCoverageFuzzer(EXPR_GRAMMAR)
    expr_fuzzer.max_expansion_coverage()

class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def add_coverage(self, symbol, new_children):
        key = expansion_key(symbol, new_children)

        if self.log and key not in self.covered_expansions:
            print("Now covered:", key)
        self.covered_expansions.add(key)

    def choose_node_expansion(self, node, possible_children):
        (symbol, children) = node
        index = super().choose_node_expansion(node, possible_children)
        self.add_coverage(symbol, possible_children[index])
        return index

class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def missing_expansion_coverage(self):
        return self.max_expansion_coverage() - self.expansion_coverage()

if __name__ == '__main__':
    digit_fuzzer = TrackingGrammarCoverageFuzzer(
        EXPR_GRAMMAR, start_symbol="<digit>", log=True)
    digit_fuzzer.fuzz()

if __name__ == '__main__':
    digit_fuzzer.fuzz()

if __name__ == '__main__':
    digit_fuzzer.fuzz()

if __name__ == '__main__':
    digit_fuzzer.expansion_coverage()

if __name__ == '__main__':
    digit_fuzzer.max_expansion_coverage()

if __name__ == '__main__':
    digit_fuzzer.missing_expansion_coverage()

def average_length_until_full_coverage(fuzzer):
    trials = 50

    sum = 0
    for trial in range(trials):
        # print(trial, end=" ")
        fuzzer.reset_coverage()
        while len(fuzzer.missing_expansion_coverage()) > 0:
            s = fuzzer.fuzz()
            sum += len(s)

    return sum / trials

if __name__ == '__main__':
    digit_fuzzer.log = False
    average_length_until_full_coverage(digit_fuzzer)

if __name__ == '__main__':
    expr_fuzzer = TrackingGrammarCoverageFuzzer(EXPR_GRAMMAR)
    average_length_until_full_coverage(expr_fuzzer)

### Covering Grammar Expansions

if __name__ == '__main__':
    print('\n### Covering Grammar Expansions')



class SimpleGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def choose_node_expansion(self, node, possible_children):
        # Prefer uncovered expansions
        (symbol, children) = node
        uncovered_children = [c for (i, c) in enumerate(possible_children)
                              if expansion_key(symbol, c) not in self.covered_expansions]
        index_map = [i for (i, c) in enumerate(possible_children)
                     if c in uncovered_children]

        if len(uncovered_children) == 0:
            # All expansions covered - use superclass method
            return self.choose_covered_node_expansion(node, possible_children)

        # Select from uncovered nodes
        index = self.choose_uncovered_node_expansion(node, uncovered_children)

        return index_map[index]

class SimpleGrammarCoverageFuzzer(SimpleGrammarCoverageFuzzer):
    def choose_uncovered_node_expansion(self, node, possible_children):
        return TrackingGrammarCoverageFuzzer.choose_node_expansion(
            self, node, possible_children)

    def choose_covered_node_expansion(self, node, possible_children):
        return TrackingGrammarCoverageFuzzer.choose_node_expansion(
            self, node, possible_children)

if __name__ == '__main__':
    f = SimpleGrammarCoverageFuzzer(EXPR_GRAMMAR, start_symbol="<digit>")
    f.fuzz()

if __name__ == '__main__':
    f.fuzz()

if __name__ == '__main__':
    f.fuzz()

if __name__ == '__main__':
    f.expansion_coverage()

if __name__ == '__main__':
    for i in range(7):
        print(f.fuzz(), end=" ")

if __name__ == '__main__':
    f.missing_expansion_coverage()

if __name__ == '__main__':
    f = SimpleGrammarCoverageFuzzer(EXPR_GRAMMAR)
    for i in range(10):
        print(f.fuzz())

if __name__ == '__main__':
    f.missing_expansion_coverage()

if __name__ == '__main__':
    average_length_until_full_coverage(SimpleGrammarCoverageFuzzer(EXPR_GRAMMAR))

## Deep Foresight
## --------------

if __name__ == '__main__':
    print('\n## Deep Foresight')



if __name__ == '__main__':
    CGI_GRAMMAR

if __name__ == '__main__':
    f = SimpleGrammarCoverageFuzzer(CGI_GRAMMAR)
    for i in range(10):
        print(f.fuzz())

if __name__ == '__main__':
    f.missing_expansion_coverage()

if __name__ == '__main__':
    CGI_GRAMMAR["<letter>"]

### Determining Maximum per-Symbol Coverage

if __name__ == '__main__':
    print('\n### Determining Maximum per-Symbol Coverage')



if __name__ == '__main__':
    f = SimpleGrammarCoverageFuzzer(EXPR_GRAMMAR)
    f.max_expansion_coverage('<integer>')

if __name__ == '__main__':
    f.max_expansion_coverage('<digit>')

### Determining yet Uncovered Children

if __name__ == '__main__':
    print('\n### Determining yet Uncovered Children')



class GrammarCoverageFuzzer(SimpleGrammarCoverageFuzzer):
    def _new_child_coverage(self, children, max_depth):
        new_cov = set()
        for (c_symbol, _) in children:
            if c_symbol in self.grammar:
                new_cov |= self.max_expansion_coverage(
                    c_symbol, max_depth)
        return new_cov

    def new_child_coverage(self, symbol, children, max_depth=float('inf')):
        """Return new coverage that would be obtained by expanding (symbol, children)"""
        new_cov = self._new_child_coverage(children, max_depth)
        new_cov.add(expansion_key(symbol, children))
        new_cov -= self.expansion_coverage()   # -= is set subtraction
        return new_cov

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR, start_symbol="<digit>", log=True)
    f.fuzz()

if __name__ == '__main__':
    f.expansion_coverage()

if __name__ == '__main__':
    for expansion in EXPR_GRAMMAR["<digit>"]:
        children = f.expansion_to_children(expansion)
        print(expansion, f.new_child_coverage("<digit>", children))

### Adaptive Lookahead

if __name__ == '__main__':
    print('\n### Adaptive Lookahead')



class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def new_coverages(self, node, possible_children):
        """Return coverage to be obtained for each child at minimum depth"""
        (symbol, children) = node
        for max_depth in range(len(self.grammar)):
            new_coverages = [
                self.new_child_coverage(
                    symbol, c, max_depth) for c in possible_children]
            max_new_coverage = max(len(new_coverage)
                                   for new_coverage in new_coverages)
            if max_new_coverage > 0:
                # Uncovered node found
                return new_coverages

        # All covered
        return None

### All Together

if __name__ == '__main__':
    print('\n### All Together')



class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def choose_node_expansion(self, node, possible_children):
        (symbol, children) = node
        new_coverages = self.new_coverages(node, possible_children)

        if new_coverages is None:
            # All expansions covered - use superclass method
            return self.choose_covered_node_expansion(node, possible_children)

        max_new_coverage = max(len(cov) for cov in new_coverages)

        children_with_max_new_coverage = [c for (i, c) in enumerate(possible_children)
                                          if len(new_coverages[i]) == max_new_coverage]
        index_map = [i for (i, c) in enumerate(possible_children)
                     if len(new_coverages[i]) == max_new_coverage]

        # Select a random expansion
        new_children_index = self.choose_uncovered_node_expansion(
            node, children_with_max_new_coverage)
        new_children = children_with_max_new_coverage[new_children_index]

        # Save the expansion as covered
        key = expansion_key(symbol, new_children)

        if self.log:
            print("Now covered:", key)
        self.covered_expansions.add(key)

        return index_map[new_children_index]

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR, min_nonterminals=3)
    f.fuzz()

if __name__ == '__main__':
    f.max_expansion_coverage() - f.expansion_coverage()

if __name__ == '__main__':
    average_length_until_full_coverage(GrammarCoverageFuzzer(EXPR_GRAMMAR))

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(CGI_GRAMMAR, min_nonterminals=5)
    while len(f.max_expansion_coverage() - f.expansion_coverage()) > 0:
        print(f.fuzz())

if __name__ == '__main__':
    average_length_until_full_coverage(TrackingGrammarCoverageFuzzer(CGI_GRAMMAR))

if __name__ == '__main__':
    average_length_until_full_coverage(SimpleGrammarCoverageFuzzer(CGI_GRAMMAR))

if __name__ == '__main__':
    average_length_until_full_coverage(GrammarCoverageFuzzer(CGI_GRAMMAR))

## Coverage in Context
## -------------------

if __name__ == '__main__':
    print('\n## Coverage in Context')



if __name__ == '__main__':
    EXPR_GRAMMAR["<factor>"]

### Extending Grammars for Context Coverage Manually

if __name__ == '__main__':
    print('\n### Extending Grammars for Context Coverage Manually')



if __name__ == '__main__':
    dup_expr_grammar = extend_grammar(EXPR_GRAMMAR,
                                      {
                                          "<factor>": ["+<factor>", "-<factor>", "(<expr>)", "<integer-1>.<integer-2>", "<integer>"],
                                          "<integer-1>": ["<digit-1><integer-1>", "<digit-1>"],
                                          "<integer-2>": ["<digit-2><integer-2>", "<digit-2>"],
                                          "<digit-1>":
                                          ["0", "1", "2", "3", "4",
                                              "5", "6", "7", "8", "9"],
                                          "<digit-2>":
                                          ["0", "1", "2", "3", "4",
                                              "5", "6", "7", "8", "9"]
                                      }
                                      )

if __name__ == '__main__':
    assert is_valid_grammar(dup_expr_grammar)

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(dup_expr_grammar, start_symbol="<factor>")
    for i in range(10):
        print(f.fuzz())

### Extending Grammars for Context Coverage Programmatically

if __name__ == '__main__':
    print('\n### Extending Grammars for Context Coverage Programmatically')



from .Grammars import new_symbol, unreachable_nonterminals
from .GrammarFuzzer import expansion_to_children

def duplicate_context(grammar, symbol, expansion=None, depth=float('inf')):
    """Duplicate an expansion within a grammar.

    In the given grammar, take the given expansion of the given symbol
    (if expansion is omitted: all symbols), and replace it with a
    new expansion referring to a duplicate of all originally referenced rules.

    If depth is given, limit duplication to `depth` references (default: unlimited)
    """
    orig_grammar = extend_grammar(grammar)
    _duplicate_context(grammar, orig_grammar, symbol,
                       expansion, depth, seen={})

    # After duplication, we may have unreachable rules; delete them
    for nonterminal in unreachable_nonterminals(grammar):
        del grammar[nonterminal]

import copy

def _duplicate_context(grammar, orig_grammar, symbol, expansion, depth, seen):
    for i in range(len(grammar[symbol])):
        if expansion is None or grammar[symbol][i] == expansion:
            new_expansion = ""
            for (s, c) in expansion_to_children(grammar[symbol][i]):
                if s in seen:                 # Duplicated already
                    new_expansion += seen[s]
                elif c == [] or depth == 0:   # Terminal symbol or end of recursion
                    new_expansion += s
                else:                         # Nonterminal symbol - duplicate
                    # Add new symbol with copy of rule
                    new_s = new_symbol(grammar, s)
                    grammar[new_s] = copy.deepcopy(orig_grammar[s])

                    # Duplicate its expansions recursively
                    # {**seen, **{s: new_s}} is seen + {s: new_s}
                    _duplicate_context(grammar, orig_grammar, new_s, expansion=None,
                                       depth=depth - 1, seen={**seen, **{s: new_s}})
                    new_expansion += new_s

            grammar[symbol][i] = new_expansion

if __name__ == '__main__':
    dup_expr_grammar = extend_grammar(EXPR_GRAMMAR)
    duplicate_context(dup_expr_grammar, "<factor>", "<integer>.<integer>")
    dup_expr_grammar

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(dup_expr_grammar, start_symbol="<factor>")
    for i in range(10):
        print(f.fuzz())

if __name__ == '__main__':
    dup_expr_grammar = extend_grammar(EXPR_GRAMMAR)
    duplicate_context(dup_expr_grammar, "<factor>", "<integer>.<integer>", depth=1)
    dup_expr_grammar

if __name__ == '__main__':
    assert is_valid_grammar(dup_expr_grammar)

if __name__ == '__main__':
    dup_expr_grammar = extend_grammar(EXPR_GRAMMAR)
    duplicate_context(dup_expr_grammar, "<expr>")

if __name__ == '__main__':
    assert is_valid_grammar(dup_expr_grammar)
    len(dup_expr_grammar)

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(dup_expr_grammar)
    len(f.max_expansion_coverage())

if __name__ == '__main__':
    dup_expr_grammar = extend_grammar(EXPR_GRAMMAR)
    duplicate_context(dup_expr_grammar, "<expr>")
    duplicate_context(dup_expr_grammar, "<expr-1>")
    len(dup_expr_grammar)

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(dup_expr_grammar)
    len(f.max_expansion_coverage())

if __name__ == '__main__':
    dup_expr_grammar["<expr>"]

if __name__ == '__main__':
    dup_expr_grammar["<term-1-1>"]

if __name__ == '__main__':
    dup_expr_grammar["<factor-1-1>"]

## Covering Code by Covering Grammars
## ----------------------------------

if __name__ == '__main__':
    print('\n## Covering Code by Covering Grammars')



### CGI Grammars

if __name__ == '__main__':
    print('\n### CGI Grammars')



from .Coverage import Coverage, cgi_decode

if __name__ == '__main__':
    with Coverage() as cov_max:
        cgi_decode('+')
        cgi_decode('%20')
        cgi_decode('abc')
        try:
            cgi_decode('%?a')
        except:
            pass

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(CGI_GRAMMAR, max_nonterminals=2)
    coverages = {}

    trials = 100
    for trial in range(trials):
        f.reset_coverage()
        overall_cov = set()
        max_cov = 30

        for i in range(10):
            s = f.fuzz()
            with Coverage() as cov:
                cgi_decode(s)
            overall_cov |= cov.coverage()

            x = len(f.expansion_coverage()) * 100 / len(f.max_expansion_coverage())
            y = len(overall_cov) * 100 / len(cov_max.coverage())
            if x not in coverages:
                coverages[x] = []
            coverages[x].append(y)

if __name__ == '__main__':
    xs = list(coverages.keys())
    ys = [sum(coverages[x]) / len(coverages[x]) for x in coverages]

# %matplotlib inline

if __name__ == '__main__':
    import matplotlib.pyplot as plt

if __name__ == '__main__':
    import matplotlib.ticker as mtick

if __name__ == '__main__':
    ax = plt.axes(label="CGI coverage")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    plt.xlim(0, max(xs))
    plt.ylim(0, max(ys))

    plt.title('Coverage of cgi_decode() vs. grammar coverage')
    plt.xlabel('grammar coverage (expansions)')
    plt.ylabel('code coverage (lines)')
    plt.scatter(xs, ys);

if __name__ == '__main__':
    import numpy as np

if __name__ == '__main__':
    np.corrcoef(xs, ys)

if __name__ == '__main__':
    from scipy.stats import spearmanr

if __name__ == '__main__':
    spearmanr(xs, ys)

### URL Grammars

if __name__ == '__main__':
    print('\n### URL Grammars')



if __name__ == '__main__':
    try:
        from urlparse import urlparse      # Python 2
    except ImportError:
        from urllib.parse import urlparse  # Python 3

if __name__ == '__main__':
    with Coverage() as cov_max:
        urlparse("http://foo.bar/path")
        urlparse("https://foo.bar#fragment")
        urlparse("ftp://user:password@foo.bar?query=value")
        urlparse("ftps://127.0.0.1/?x=1&y=2")

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(URL_GRAMMAR, max_nonterminals=2)
    coverages = {}

    trials = 100
    for trial in range(trials):
        f.reset_coverage()
        overall_cov = set()

        for i in range(20):
            s = f.fuzz()
            with Coverage() as cov:
                urlparse(s)
            overall_cov |= cov.coverage()

            x = len(f.expansion_coverage()) * 100 / len(f.max_expansion_coverage())
            y = len(overall_cov) * 100 / len(cov_max.coverage())
            if x not in coverages:
                coverages[x] = []
            coverages[x].append(y)

if __name__ == '__main__':
    xs = list(coverages.keys())
    ys = [sum(coverages[x]) / len(coverages[x]) for x in coverages]

if __name__ == '__main__':
    ax = plt.axes(label="URL coverage")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    plt.xlim(0, max(xs))
    plt.ylim(0, max(ys))

    plt.title('Coverage of urlparse() vs. grammar coverage')
    plt.xlabel('grammar coverage (expansions)')
    plt.ylabel('code coverage (lines)')
    plt.scatter(xs, ys);

if __name__ == '__main__':
    np.corrcoef(xs, ys)

if __name__ == '__main__':
    spearmanr(xs, ys)

### Will this always work?

if __name__ == '__main__':
    print('\n### Will this always work?')



#### Equivalent Elements

if __name__ == '__main__':
    print('\n#### Equivalent Elements')



#### Deep Data Processing

if __name__ == '__main__':
    print('\n#### Deep Data Processing')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



from .Grammars import US_PHONE_GRAMMAR

if __name__ == '__main__':
    phone_fuzzer = GrammarCoverageFuzzer(US_PHONE_GRAMMAR)
    phone_fuzzer.fuzz()

if __name__ == '__main__':
    phone_fuzzer.expansion_coverage()

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Testing ls

if __name__ == '__main__':
    print('\n### Exercise 1: Testing ls')



LS_EBNF_GRAMMAR = {
    '<start>': ['-<options>'],
    '<options>': ['<option>*'],
    '<option>': ['1', 'A', '@',
                 # many more
                 ]
}

if __name__ == '__main__':
    assert is_valid_grammar(LS_EBNF_GRAMMAR)

from .Grammars import convert_ebnf_grammar, srange

LS_EBNF_GRAMMAR = {
    '<start>': ['-<options>'],
    '<options>': ['<option>*'],
    '<option>': srange("ABCFGHLOPRSTUW@abcdefghiklmnopqrstuwx1")
}

if __name__ == '__main__':
    assert is_valid_grammar(LS_EBNF_GRAMMAR)

LS_GRAMMAR = convert_ebnf_grammar(LS_EBNF_GRAMMAR)

from .Fuzzer import ProgramRunner

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(LS_GRAMMAR, max_nonterminals=3)
    while len(f.max_expansion_coverage() - f.expansion_coverage()) > 0:
        invocation = f.fuzz()
        print("ls", invocation, end="; ")
        args = invocation.split()
        ls = ProgramRunner(["ls"] + args)
        ls.run()
    print()

### Exercise 2: Caching

if __name__ == '__main__':
    print('\n### Exercise 2: Caching')


