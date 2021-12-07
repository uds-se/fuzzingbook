#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Grammar Coverage" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/GrammarCoverageFuzzer.html
# Last change: 2021-12-07 13:37:08+01:00
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

This chapter introduces `GrammarCoverageFuzzer`, an efficient grammar fuzzer extending `GrammarFuzzer` from the [chapter on efficient grammar fuzzing](GrammarFuzzer.ipynb).  It strives to _cover all expansions at least once,_ thus ensuring coverage of functionality.

In the following example, for instance, we use `GrammarCoverageFuzzer` to produce an expression. We see that the resulting expression covers all digits and all operators in a single expression.

>>> from Grammars import EXPR_GRAMMAR
>>> expr_fuzzer = GrammarCoverageFuzzer(EXPR_GRAMMAR)
>>> expr_fuzzer.fuzz()
'-(2 + 3) * 4.5 / 6 - 2.0 / +8 + 7 + 3'

After fuzzing, the `expansion_coverage()` method returns a mapping of grammar expansions covered.

>>> expr_fuzzer.expansion_coverage()
{' -> 0',
 ' -> 1',
 ' -> 2',
 ' -> 3',
 ' -> 4',
 ' -> 5',
 ' -> 6',
 ' -> 7',
 ' -> 8',
 ' -> 9',
 ' -> ',
 ' ->  + ',
 ' ->  - ',
 ' -> ()',
 ' -> +',
 ' -> -',
 ' -> ',
 ' -> .',
 ' -> ',
 ' -> ',
 ' -> ',
 ' -> ',
 ' ->  * ',
 ' ->  / '}

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



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo('yq1orQJF6ys')

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

from .bookutils import quiz

from .Fuzzer import Fuzzer

from typing import Dict, List, Set, Union, Optional

from .Grammars import EXPR_GRAMMAR, CGI_GRAMMAR, URL_GRAMMAR, START_SYMBOL
from .Grammars import is_valid_grammar, extend_grammar, Grammar

if __name__ == '__main__':
    EXPR_GRAMMAR["<factor>"]

if __name__ == '__main__':
    quiz("Which expansions of `EXPR_GRAMMAR` does the expression `1 + 2` cover?",
         [
             "`<start> -> <expr>`",
             "`<integer> -> <digit><integer>`",
             "`<integer> -> <digit>`",
             "`<factor> -> +<factor>`"
         ], [1, 3])

### Tracking Grammar Coverage

if __name__ == '__main__':
    print('\n### Tracking Grammar Coverage')



from .Grammars import Grammar, Expansion
from .GrammarFuzzer import GrammarFuzzer, all_terminals, nonterminals, \
    display_tree, DerivationTree

import random

class TrackingGrammarCoverageFuzzer(GrammarFuzzer):
    """Track grammar coverage during production"""

    def __init__(self, *args, **kwargs) -> None:
        # invoke superclass __init__(), passing all arguments
        super().__init__(*args, **kwargs)
        self.reset_coverage()

#### Keeping Track of Expansions

if __name__ == '__main__':
    print('\n#### Keeping Track of Expansions')



class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def expansion_coverage(self) -> Set[str]:
        """Return the set of covered expansions as strings SYMBOL -> EXPANSION"""
        return self.covered_expansions

    def reset_coverage(self) -> None:
        """Clear coverage info tracked so far"""
        self.covered_expansions: Set[str] = set()

def expansion_key(symbol: str, 
                  expansion: Union[Expansion,
                                   DerivationTree, 
                                   List[DerivationTree]]) -> str:
    """Convert (symbol, `expansion`) into a key "SYMBOL -> EXPRESSION". 
      `expansion` can be an expansion string, a derivation tree,
         or a list of derivation trees."""

    if isinstance(expansion, tuple):
        # Expansion or single derivation tree
        expansion, _ = expansion

    if not isinstance(expansion, str):
        # Derivation tree
        children = expansion
        expansion = all_terminals((symbol, children))

    assert isinstance(expansion, str)

    return symbol + " -> " + expansion

if __name__ == '__main__':
    expansion_key(START_SYMBOL, EXPR_GRAMMAR[START_SYMBOL][0])

if __name__ == '__main__':
    children: List[DerivationTree] = [("<expr>", None), (" + ", []), ("<term>", None)]
    expansion_key("<expr>", children)

#### Computing Possible Expansions

if __name__ == '__main__':
    print('\n#### Computing Possible Expansions')



class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def _max_expansion_coverage(self, symbol: str, 
                                max_depth: Union[int, float]) -> Set[str]:
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

    def max_expansion_coverage(self, symbol: Optional[str] = None,
                               max_depth: Union[int, float] = float('inf')) \
            -> Set[str]:
        """Return set of all expansions in a grammar 
           starting with `symbol` (default: start symbol).
           If `max_depth` is given, expand only to that depth."""
        if symbol is None:
            symbol = self.start_symbol

        self._symbols_seen: Set[str] = set()
        cov = self._max_expansion_coverage(symbol, max_depth)

        if symbol == START_SYMBOL:
            assert len(self._symbols_seen) == len(self.grammar)

        return cov

if __name__ == '__main__':
    expr_fuzzer = TrackingGrammarCoverageFuzzer(EXPR_GRAMMAR)
    expr_fuzzer.max_expansion_coverage()

#### Tracking Expansions while Fuzzing

if __name__ == '__main__':
    print('\n#### Tracking Expansions while Fuzzing')



class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def add_coverage(self, symbol: str,
                     new_child: Union[Expansion, List[DerivationTree]]) -> None:
        key = expansion_key(symbol, new_child)

        if self.log and key not in self.covered_expansions:
            print("Now covered:", key)
        self.covered_expansions.add(key)

    def choose_node_expansion(self, node: DerivationTree,
                              children_alternatives: 
                              List[List[DerivationTree]]) -> int:
        (symbol, children) = node
        index = super().choose_node_expansion(node, children_alternatives)
        self.add_coverage(symbol, children_alternatives[index])
        return index

class TrackingGrammarCoverageFuzzer(TrackingGrammarCoverageFuzzer):
    def missing_expansion_coverage(self) -> Set[str]:
        """Return expansions not covered yet"""
        return self.max_expansion_coverage() - self.expansion_coverage()

#### Putting Things Together

if __name__ == '__main__':
    print('\n#### Putting Things Together')



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

def average_length_until_full_coverage(fuzzer: TrackingGrammarCoverageFuzzer) -> float:
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
    """When choosing expansions, prefer expansions not covered."""

    def choose_node_expansion(self,
                              node: DerivationTree,
                              children_alternatives: List[List[DerivationTree]]) -> int:
        """Return index of expansion in `children_alternatives` to be selected.
           Picks uncovered expansions, if any."""

        # Prefer uncovered expansions
        (symbol, children) = node
        uncovered_children = [c for (i, c) in enumerate(children_alternatives)
                              if expansion_key(symbol, c)
                              not in self.covered_expansions]
        index_map = [i for (i, c) in enumerate(children_alternatives)
                     if c in uncovered_children]

        if len(uncovered_children) == 0:
            # All expansions covered - use superclass method
            return self.choose_covered_node_expansion(node, children_alternatives)

        # Select from uncovered nodes
        index = self.choose_uncovered_node_expansion(node, uncovered_children)

        return index_map[index]

class SimpleGrammarCoverageFuzzer(SimpleGrammarCoverageFuzzer):
    def choose_uncovered_node_expansion(self,
                                        node: DerivationTree,
                                        children_alternatives: List[List[DerivationTree]]) \
            -> int:
        """Return index of expansion in _uncovered_ `children_alternatives`
           to be selected.
           To be overloaded in subclasses."""
        return TrackingGrammarCoverageFuzzer.choose_node_expansion(
            self, node, children_alternatives)

    def choose_covered_node_expansion(self,
                                      node: DerivationTree,
                                      children_alternatives: List[List[DerivationTree]]) \
            -> int:
        """Return index of expansion in _covered_ `children_alternatives`
           to be selected.
           To be overloaded in subclasses."""
        return TrackingGrammarCoverageFuzzer.choose_node_expansion(
            self, node, children_alternatives)

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
    quiz("How many productions would `f.max_expansion_coverage('<digit>')` return?",
         [
             "10",
             "11",
             "12",
             "13"
         ], "100 / 100")

if __name__ == '__main__':
    f.max_expansion_coverage('<digit>')

### Determining yet Uncovered Children

if __name__ == '__main__':
    print('\n### Determining yet Uncovered Children')



class GrammarCoverageFuzzer(SimpleGrammarCoverageFuzzer):
    """Produce from grammars, aiming for coverage of all expansions."""

    def new_child_coverage(self,
                           symbol: str,
                           children: List[DerivationTree],
                           max_depth: Union[int, float] = float('inf')) -> Set[str]:
        """Return new coverage that would be obtained 
           by expanding (`symbol`, `children`)"""

        new_cov = self._new_child_coverage(children, max_depth)
        new_cov.add(expansion_key(symbol, children))
        new_cov -= self.expansion_coverage()   # -= is set subtraction
        return new_cov

    def _new_child_coverage(self, children: List[DerivationTree],
                            max_depth: Union[int, float]) -> Set[str]:
        new_cov: Set[str] = set()
        for (c_symbol, _) in children:
            if c_symbol in self.grammar:
                new_cov |= self.max_expansion_coverage(c_symbol, max_depth)

        return new_cov

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR, start_symbol="<digit>", log=True)
    f.fuzz()

if __name__ == '__main__':
    f.expansion_coverage()

if __name__ == '__main__':
    f.new_child_coverage("<digit>", [('0', [])])

if __name__ == '__main__':
    f.new_child_coverage("<digit>", [('2', [])])

if __name__ == '__main__':
    for expansion in EXPR_GRAMMAR["<digit>"]:
        children = f.expansion_to_children(expansion)
        print(expansion, f.new_child_coverage("<digit>", children))

### Adaptive Lookahead

if __name__ == '__main__':
    print('\n### Adaptive Lookahead')



#### Excursion: Implementing `new_coverage()`

if __name__ == '__main__':
    print('\n#### Excursion: Implementing `new_coverage()`')



class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def new_coverages(self, node: DerivationTree,
                      children_alternatives: List[List[DerivationTree]]) \
            -> Optional[List[Set[str]]]:
        """Return coverage to be obtained for each child at minimum depth"""

        (symbol, children) = node
        for max_depth in range(len(self.grammar)):
            new_coverages = [
                self.new_child_coverage(
                    symbol, c, max_depth) for c in children_alternatives]
            max_new_coverage = max(len(new_coverage)
                                   for new_coverage in new_coverages)
            if max_new_coverage > 0:
                # Uncovered node found
                return new_coverages

        # All covered
        return None

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



### All Together

if __name__ == '__main__':
    print('\n### All Together')



#### Excursion: Implementing `choose_node_expansion()`

if __name__ == '__main__':
    print('\n#### Excursion: Implementing `choose_node_expansion()`')



class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def choose_node_expansion(self, node: DerivationTree,
                              children_alternatives: List[List[DerivationTree]]) -> int:
        """Choose an expansion of `node` among `children_alternatives`.
           Return `n` such that expanding `children_alternatives[n]`
           yields the highest additional coverage."""

        (symbol, children) = node
        new_coverages = self.new_coverages(node, children_alternatives)

        if new_coverages is None:
            # All expansions covered - use superclass method
            return self.choose_covered_node_expansion(node, children_alternatives)

        max_new_coverage = max(len(cov) for cov in new_coverages)

        children_with_max_new_coverage = [c for (i, c) in enumerate(children_alternatives)
                                          if len(new_coverages[i]) == max_new_coverage]
        index_map = [i for (i, c) in enumerate(children_alternatives)
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

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



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

def duplicate_context(grammar: Grammar, 
                      symbol: str,
                      expansion: Optional[Expansion] = None, 
                      depth: Union[float, int] = float('inf')):
    """Duplicate an expansion within a grammar.

    In the given grammar, take the given expansion of the given `symbol`
    (if `expansion` is omitted: all symbols), and replace it with a
    new expansion referring to a duplicate of all originally referenced rules.

    If `depth` is given, limit duplication to `depth` references
    (default: unlimited)
    """
    orig_grammar = extend_grammar(grammar)
    _duplicate_context(grammar, orig_grammar, symbol,
                       expansion, depth, seen={})

    # After duplication, we may have unreachable rules; delete them
    for nonterminal in unreachable_nonterminals(grammar):
        del grammar[nonterminal]

#### Excursion: Implementing `_duplicate_context()`

if __name__ == '__main__':
    print('\n#### Excursion: Implementing `_duplicate_context()`')



import copy

def _duplicate_context(grammar: Grammar,
                       orig_grammar: Grammar,
                       symbol: str,
                       expansion: Optional[Expansion],
                       depth: Union[float, int],
                       seen: Dict[str, str]) -> None:
    """Helper function for `duplicate_context()`"""

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

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



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



#### Excursion: Creating the Plot

if __name__ == '__main__':
    print('\n#### Excursion: Creating the Plot')



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
    coverages: Dict[float, List[float]] = {}

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
    import matplotlib.pyplot as plt  # type: ignore

if __name__ == '__main__':
    import matplotlib.ticker as mtick  # type: ignore

if __name__ == '__main__':
    ax = plt.axes(label="CGI coverage")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    plt.xlim(0, max(xs))
    plt.ylim(0, max(ys))

    plt.title('Coverage of cgi_decode() vs. grammar coverage')
    plt.xlabel('grammar coverage (expansions)')
    plt.ylabel('code coverage (lines)')

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    plt.scatter(xs, ys);

if __name__ == '__main__':
    import numpy as np

if __name__ == '__main__':
    np.corrcoef(xs, ys)

if __name__ == '__main__':
    from scipy.stats import spearmanr  # type: ignore

if __name__ == '__main__':
    spearmanr(xs, ys)

### URL Grammars

if __name__ == '__main__':
    print('\n### URL Grammars')



from urllib.parse import urlparse

#### Excursion: Creating the Plot

if __name__ == '__main__':
    print('\n#### Excursion: Creating the Plot')



if __name__ == '__main__':
    with Coverage() as cov_max:
        urlparse("http://foo.bar/path")
        urlparse("https://foo.bar#fragment")
        urlparse("ftp://user:password@foo.bar?query=value")
        urlparse("ftps://127.0.0.1/?x=1&y=2")

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(URL_GRAMMAR, max_nonterminals=2)
    coverages: Dict[float, List[float]] = {}

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

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
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



from .Grammars import EXPR_GRAMMAR

if __name__ == '__main__':
    expr_fuzzer = GrammarCoverageFuzzer(EXPR_GRAMMAR)

if __name__ == '__main__':
    expr_fuzzer.fuzz();

if __name__ == '__main__':
    expr_fuzzer.fuzz()

if __name__ == '__main__':
    expr_fuzzer.expansion_coverage()

from .ClassDiagram import display_class_hierarchy

if __name__ == '__main__':
    display_class_hierarchy([GrammarCoverageFuzzer],
                            public_methods=[
                                Fuzzer.run,
                                Fuzzer.runs,
                                GrammarFuzzer.__init__,
                                GrammarFuzzer.fuzz,
                                GrammarFuzzer.fuzz_tree,
                                TrackingGrammarCoverageFuzzer.max_expansion_coverage,
                                TrackingGrammarCoverageFuzzer.missing_expansion_coverage,
                                TrackingGrammarCoverageFuzzer.reset_coverage,
                                GrammarCoverageFuzzer.__init__,
                                GrammarCoverageFuzzer.fuzz,
                                GrammarCoverageFuzzer.expansion_coverage,
                            ],
                            types={
                                'DerivationTree': DerivationTree,
                                'Expansion': Expansion,
                                'Grammar': Grammar
                            },
                            project='fuzzingbook')

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



LS_EBNF_GRAMMAR: Grammar = {
    '<start>': ['-<options>'],
    '<options>': ['<option>*'],
    '<option>': ['1', 'A', '@',
                 # many more
                 ]
}

if __name__ == '__main__':
    assert is_valid_grammar(LS_EBNF_GRAMMAR)

from .Grammars import convert_ebnf_grammar, srange

LS_EBNF_GRAMMAR: Grammar = {
    '<start>': ['-<options>'],
    '<options>': ['<option>*'],
    '<option>': srange("ABCFGHLOPRSTUW@abcdefghiklmnopqrstuwx1")
}

if __name__ == '__main__':
    assert is_valid_grammar(LS_EBNF_GRAMMAR)

LS_GRAMMAR: Grammar = convert_ebnf_grammar(LS_EBNF_GRAMMAR)

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


