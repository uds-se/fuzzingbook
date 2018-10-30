#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/GrammarCoverageFuzzer.html
# Last change: 2018-10-18 11:22:52+02:00
#
#
# Copyright (c) 2018 Saarland University, CISPA, authors, and contributors
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


# # Grammar Coverage

if __name__ == "__main__":
    print('# Grammar Coverage')




# ## Covering Grammar Elements

if __name__ == "__main__":
    print('\n## Covering Grammar Elements')




# ### Tracking Grammar Coverage

if __name__ == "__main__":
    print('\n### Tracking Grammar Coverage')




import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from Grammars import DIGIT_GRAMMAR, EXPR_GRAMMAR, CGI_GRAMMAR, URL_GRAMMAR, START_SYMBOL, is_valid_grammar
else:
    from .Grammars import DIGIT_GRAMMAR, EXPR_GRAMMAR, CGI_GRAMMAR, URL_GRAMMAR, START_SYMBOL, is_valid_grammar


if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer, all_terminals, nonterminals, display_tree
else:
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

class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def expansion_key(self, symbol, expansion):
        """Convert (symbol, children) into a key.  `children` can be an expansion string or a derivation tree."""
        if not isinstance(expansion, str):
            children = expansion
            expansion = all_terminals((symbol, children))
        return symbol + " -> " + expansion

if __name__ == "__main__":
    f = TrackingGrammarCoverageFuzzer(EXPR_GRAMMAR)
    f.expansion_key(START_SYMBOL, EXPR_GRAMMAR[START_SYMBOL][0])


if __name__ == "__main__":
    children = [("<expr>", None), (" + ", []), ("<term>", None)]
    f.expansion_key("<expr>", children)


class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def max_expansion_coverage(self):
        """Return set of all expansions in a grammar"""
        expansions = set()
        for nonterminal in self.grammar:
            for expansion in self.grammar[nonterminal]:
                expansions.add(self.expansion_key(nonterminal, expansion))
        return expansions

if __name__ == "__main__":
    f = TrackingGrammarCoverageFuzzer(DIGIT_GRAMMAR)
    f.max_expansion_coverage()


class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def add_coverage(self, symbol, new_children):
        key = self.expansion_key(symbol, new_children)

        if self.log and key not in self.covered_expansions:
            print("Now covered:", key)
        self.covered_expansions.add(key)

    def choose_node_expansion(self, node, possible_children):
        (symbol, children) = node
        index = super().choose_node_expansion(node, possible_children)
        self.add_coverage(symbol, possible_children[index])
        return index

if __name__ == "__main__":
    f = TrackingGrammarCoverageFuzzer(DIGIT_GRAMMAR, log=True)
    f.fuzz()


if __name__ == "__main__":
    f.fuzz()


if __name__ == "__main__":
    f.fuzz()


if __name__ == "__main__":
    f.expansion_coverage()


def average_length_until_full_coverage(fuzzer):
    trials = 50

    sum = 0
    for trial in range(trials):
        fuzzer.reset_coverage()
        while len(fuzzer.max_expansion_coverage() -
                  fuzzer.expansion_coverage()) > 0:
            s = fuzzer.fuzz()
            sum += len(s)

    return sum / trials

if __name__ == "__main__":
    average_length_until_full_coverage(TrackingGrammarCoverageFuzzer(EXPR_GRAMMAR))


# ### Covering Grammar Expansions

if __name__ == "__main__":
    print('\n### Covering Grammar Expansions')




class SimpleGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def choose_node_expansion(self, node, possible_children):
        # Prefer uncovered expansions
        (symbol, children) = node
        uncovered_children = [(i, c) for (i, c) in enumerate(possible_children)
                              if self.expansion_key(symbol, c) not in self.covered_expansions]

        if len(uncovered_children) == 0:
            # All expansions covered - use superclass method
            if self.log:
                print("All", symbol, "alternatives covered")
            return super().choose_node_expansion(node, possible_children)

        # select a random expansion
        index = random.randrange(len(uncovered_children))
        (new_children_index, new_children) = uncovered_children[index]

        # Save the expansion as covered
        self.add_coverage(symbol, new_children)

        return new_children_index

if __name__ == "__main__":
    f = SimpleGrammarCoverageFuzzer(DIGIT_GRAMMAR, log=True)
    f.fuzz()


if __name__ == "__main__":
    f.fuzz()


if __name__ == "__main__":
    f.fuzz()


if __name__ == "__main__":
    f.expansion_coverage()


if __name__ == "__main__":
    for i in range(7):
        f.fuzz()


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


if __name__ == "__main__":
    f = SimpleGrammarCoverageFuzzer(EXPR_GRAMMAR)
    for i in range(10):
        print(f.fuzz())


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


if __name__ == "__main__":
    average_length_until_full_coverage(SimpleGrammarCoverageFuzzer(EXPR_GRAMMAR))


# ## Deep Foresight

if __name__ == "__main__":
    print('\n## Deep Foresight')




if __name__ == "__main__":
    f = SimpleGrammarCoverageFuzzer(CGI_GRAMMAR)


if __name__ == "__main__":
    for i in range(10):
        print(f.fuzz())


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


if __name__ == "__main__":
    CGI_GRAMMAR["<letter>"]


# ### Determining Maximum per-Symbol Coverage

if __name__ == "__main__":
    print('\n### Determining Maximum per-Symbol Coverage')




class GrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def _max_symbol_expansion_coverage(
            self, symbol, max_depth, cov, symbols_seen):
        """Return set of all expansions in a grammar starting with `symbol`"""
        if max_depth <= 0:
            return (cov, symbols_seen)

        symbols_seen.add(symbol)
        for expansion in self.grammar[symbol]:
            key = self.expansion_key(symbol, expansion)
            if key in cov:
                continue

            cov.add(key)
            for s in nonterminals(expansion):
                if s in symbols_seen:
                    continue
                new_cov, new_symbols_seen = (
                    self._max_symbol_expansion_coverage(s, max_depth - 1, cov, symbols_seen))
                cov |= new_cov
                symbols_seen |= new_symbols_seen

        return (cov, symbols_seen)

class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def max_symbol_expansion_coverage(self, symbol, max_depth=float('inf')):
        cov, symbols_seen = self._max_symbol_expansion_coverage(
            symbol, max_depth, set(), set())
        return cov

if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR)
    f.max_symbol_expansion_coverage('<integer>')


if __name__ == "__main__":
    f.max_symbol_expansion_coverage('<digit>')


if __name__ == "__main__":
    assert f.max_expansion_coverage() == f.max_symbol_expansion_coverage(START_SYMBOL)


# ### Determining Children with new Coverage

if __name__ == "__main__":
    print('\n### Determining Children with new Coverage')




class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def _new_child_coverage(self, children, max_depth):
        new_cov = set()
        for (c_symbol, _) in children:
            if c_symbol in self.grammar:
                new_cov |= self.max_symbol_expansion_coverage(
                    c_symbol, max_depth)
        return new_cov

    def new_child_coverage(self, symbol, children, max_depth=float('inf')):
        """Return new coverage that would be obtained by expanding (symbol, children)"""
        new_cov = self._new_child_coverage(children, max_depth)
        for c in children:
            new_cov.add(self.expansion_key(symbol, children))
        new_cov -= self.expansion_coverage()   # set subtraction
        return new_cov

if __name__ == "__main__":
    f = GrammarCoverageFuzzer(DIGIT_GRAMMAR, log=True)
    f.fuzz()


if __name__ == "__main__":
    f.expansion_coverage()


if __name__ == "__main__":
    for expansion in DIGIT_GRAMMAR[START_SYMBOL]:
        children = f.expansion_to_children(expansion)
        print(expansion, f.new_child_coverage(START_SYMBOL, children))


# ### Adaptive Lookahead

if __name__ == "__main__":
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

# ### All Together

if __name__ == "__main__":
    print('\n### All Together')




class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def choose_node_expansion(self, node, possible_children):
        (symbol, children) = node
        new_coverages = self.new_coverages(node, possible_children)

        if new_coverages is None:
            # All expansions covered - use superclass method
            return GrammarFuzzer.choose_node_expansion(
                self, node, possible_children)

        max_new_coverage = max(len(cov) for cov in new_coverages)
        children_with_max_new_coverage = [(i, c) for (i, c) in enumerate(possible_children)
                                          if len(new_coverages[i]) == max_new_coverage]

        # select a random expansion
        new_children_index, new_children = random.choice(
            children_with_max_new_coverage)

        # Save the expansion as covered
        key = self.expansion_key(symbol, new_children)

        if self.log:
            print("Now covered:", key)
        self.covered_expansions.add(key)

        return new_children_index

if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR, min_nonterminals=3)
    f.fuzz()


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


if __name__ == "__main__":
    average_length_until_full_coverage(GrammarCoverageFuzzer(EXPR_GRAMMAR))


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(CGI_GRAMMAR, min_nonterminals=5)
    while len(f.max_expansion_coverage() - f.expansion_coverage()) > 0:
        print(f.fuzz())


if __name__ == "__main__":
    average_length_until_full_coverage(TrackingGrammarCoverageFuzzer(CGI_GRAMMAR))


if __name__ == "__main__":
    average_length_until_full_coverage(SimpleGrammarCoverageFuzzer(CGI_GRAMMAR))


if __name__ == "__main__":
    average_length_until_full_coverage(GrammarCoverageFuzzer(CGI_GRAMMAR))


# ## Code Coverage via Grammar Coverage

if __name__ == "__main__":
    print('\n## Code Coverage via Grammar Coverage')




# ### CGI Grammars

if __name__ == "__main__":
    print('\n### CGI Grammars')




if __package__ is None or __package__ == "":
    from Coverage import Coverage, cgi_decode
else:
    from .Coverage import Coverage, cgi_decode


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(CGI_GRAMMAR, max_nonterminals=2)
    coverages = {}

    trials = 100
    for trial in range(trials):
        f.reset_coverage()
        overall_cov = set()

        for i in range(10):
            s = f.fuzz()
            with Coverage() as cov:
                cgi_decode(s)
            overall_cov |= cov.coverage()

            x = len(f.expansion_coverage())
            y = len(overall_cov)
            if x not in coverages:
                coverages[x] = []
            coverages[x].append(y)


if __name__ == "__main__":
    xs = list(coverages.keys())
    ys = [sum(coverages[x]) / len(coverages[x]) for x in coverages]


# %matplotlib inline

import matplotlib.pyplot as plt

if __name__ == "__main__":
    plt.scatter(xs, ys)
    plt.title('Coverage of cgi_decode() vs. grammar coverage')
    plt.xlabel('grammar coverage (expansions)')
    plt.ylabel('code coverage (lines)');


import numpy as np

if __name__ == "__main__":
    np.corrcoef(xs, ys)


# ### URL Grammars

if __name__ == "__main__":
    print('\n### URL Grammars')




if __name__ == "__main__":
    try:
        from urlparse import urlparse      # Python 2
    except ImportError:
        from urllib.parse import urlparse  # Python 3


if __name__ == "__main__":
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

            x = len(f.expansion_coverage())
            y = len(overall_cov)
            if x not in coverages:
                coverages[x] = []
            coverages[x].append(y)


if __name__ == "__main__":
    xs = list(coverages.keys())
    ys = [sum(coverages[x]) / len(coverages[x]) for x in coverages]


if __name__ == "__main__":
    plt.scatter(xs, ys)
    plt.title('Coverage of cgi_decode() vs. grammar coverage')
    plt.xlabel('grammar coverage (expansions)')
    plt.ylabel('code coverage (lines)');


if __name__ == "__main__":
    np.corrcoef(xs, ys)


# ### Will this always work?

if __name__ == "__main__":
    print('\n### Will this always work?')




# #### Equivalent Elements

if __name__ == "__main__":
    print('\n#### Equivalent Elements')




# #### Deep Data Processing

if __name__ == "__main__":
    print('\n#### Deep Data Processing')




# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Background

if __name__ == "__main__":
    print('\n## Background')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1: Testing ls

if __name__ == "__main__":
    print('\n### Exercise 1: Testing ls')




LS_EBNF_GRAMMAR = {
    '<start>': ['-<options>'],
    '<options>': ['<option>*'],
    '<option>': ['1', 'A', '@',
                 # many more
                 ]
}

assert is_valid_grammar(LS_EBNF_GRAMMAR)

if __package__ is None or __package__ == "":
    from Grammars import convert_ebnf_grammar, srange
else:
    from .Grammars import convert_ebnf_grammar, srange


LS_EBNF_GRAMMAR = {
    '<start>': ['-<options>'],
    '<options>': ['<option>*'],
    '<option>': srange("ABCFGHLOPRSTUW@abcdefghiklmnopqrstuwx1")
}
assert is_valid_grammar(LS_EBNF_GRAMMAR)

LS_GRAMMAR = convert_ebnf_grammar(LS_EBNF_GRAMMAR)

if __package__ is None or __package__ == "":
    from Fuzzer import ProgramRunner
else:
    from .Fuzzer import ProgramRunner


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(LS_GRAMMAR, max_nonterminals=3)
    while len(f.max_expansion_coverage() - f.expansion_coverage()) > 0:
        invocation = f.fuzz()
        print("ls", invocation, end="; ")
        args = invocation.split()
        ls = ProgramRunner(["ls"] + args)
        ls.run()
    print()


# ### Exercise 2: Caching

if __name__ == "__main__":
    print('\n### Exercise 2: Caching')



