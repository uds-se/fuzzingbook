#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/GrammarFuzzer.html
# Last change: 2018-11-27 02:24:06-08:00
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


# # Efficient Grammar Fuzzing


import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from Grammars import EXPR_EBNF_GRAMMAR, convert_ebnf_grammar, simple_grammar_fuzzer
else:
    from .Grammars import EXPR_EBNF_GRAMMAR, convert_ebnf_grammar, simple_grammar_fuzzer


if __package__ is None or __package__ == "":
    from ExpectError import ExpectTimeout
else:
    from .ExpectError import ExpectTimeout


if __package__ is None or __package__ == "":
    from Grammars import simple_grammar_fuzzer
else:
    from .Grammars import simple_grammar_fuzzer


if __package__ is None or __package__ == "":
    from Grammars import START_SYMBOL, EXPR_GRAMMAR, URL_GRAMMAR, CGI_GRAMMAR
else:
    from .Grammars import START_SYMBOL, EXPR_GRAMMAR, URL_GRAMMAR, CGI_GRAMMAR


if __package__ is None or __package__ == "":
    from Grammars import RE_NONTERMINAL, nonterminals, is_nonterminal
else:
    from .Grammars import RE_NONTERMINAL, nonterminals, is_nonterminal


if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


import re

def dot_escape(s):
    """Return s in a form suitable for dot"""
    # s = s.replace("\\", "\\\\")
    s = re.sub(r'([^a-zA-Z0-9" ])', r"\\\1", s)
    return s

def all_terminals(tree):
    (symbol, children) = tree
    if children is None:
        # This is a nonterminal symbol not expanded yet
        return symbol

    if len(children) == 0:
        # This is a terminal symbol
        return symbol

    # This is an expanded symbol:
    # Concatenate all terminal symbols from all children
    return ''.join([all_terminals(c) for c in children])

def tree_to_string(tree):
    symbol, children, *_ = tree
    if children:
        return ''.join(tree_to_string(c) for c in children)
    else:
        return '' if is_nonterminal(symbol) else symbol

# ## Expanding a Node



if __package__ is None or __package__ == "":
    from Fuzzer import Fuzzer
else:
    from .Fuzzer import Fuzzer


class GrammarFuzzer(Fuzzer):
    def __init__(self, grammar, start_symbol=START_SYMBOL,
                 min_nonterminals=0, max_nonterminals=10, disp=False, log=False):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.min_nonterminals = min_nonterminals
        self.max_nonterminals = max_nonterminals
        self.disp = disp
        self.log = log
        self._expansion_cache = {}


class GrammarFuzzer(GrammarFuzzer):
    def init_tree(self):
        return (self.start_symbol, None)

def expansion_to_children(expansion):
    # print("Converting " + repr(expansion))
    # strings contains all substrings -- both terminals and nonterminals such
    # that ''.join(strings) == expansion

    # See nonterminals() in Grammars.py
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    if expansion == "":  # Special case: epsilon expansion
        return [("", [])]

    strings = re.split(RE_NONTERMINAL, expansion)
    return [(s, None) if is_nonterminal(s) else (s, [])
            for s in strings if len(s) > 0]


class GrammarFuzzer(GrammarFuzzer):
    def expansion_to_children(self, expansion):
        result =  expansion_to_children(expansion)
        if expansion not in self._expansion_cache:
            self._expansion_cache[expansion] = []
        self._expansion_cache[expansion].append(result)
        return result

import random

class GrammarFuzzer(GrammarFuzzer):
    def choose_node_expansion(self, node, possible_children):
        """Return index of expansion in `possible_children` to be selected.  Defaults to random."""
        return random.randrange(0, len(possible_children))

    def expand_node_randomly(self, node):
        (symbol, children) = node
        assert children is None

        if self.log:
            print("Expanding", all_terminals(node), "randomly")

        # Fetch the possible expansions from grammar...
        expansions = self.grammar[symbol]
        possible_children = [self.expansion_to_children(expansion) for expansion in expansions]

        # ... and select a random expansion
        index = self.choose_node_expansion(node, possible_children)
        children = possible_children[index]

        # Return with new children
        return (symbol, children)


class GrammarFuzzer(GrammarFuzzer):
    def expand_node(self, node):
        return self.expand_node_randomly(node)


class GrammarFuzzer(GrammarFuzzer):
    def possible_expansions(self, node):
        (symbol, children) = node
        if children is None:
            return 1

        return sum(self.possible_expansions(c) for c in children)

class GrammarFuzzer(GrammarFuzzer):
    def any_possible_expansions(self, node):
        (symbol, children) = node
        if children is None:
            return True

        return any(self.any_possible_expansions(c) for c in children)

class GrammarFuzzer(GrammarFuzzer):
    def choose_tree_expansion(self, tree, children):
        """Return index of subtree in `children` to be selected for expansion.  Defaults to random."""
        return random.randrange(0, len(children))

    def expand_tree_once(self, tree):
        (symbol, children) = tree
        if children is None:
            # Expand this node
            return self.expand_node(tree)

        # Find all children with possible expansions
        expandable_children = [
            c for c in children if self.any_possible_expansions(c)]

        # `index_map` translates an index in `expandable_children`
        # back into the original index in `children`
        index_map = [i for (i, c) in enumerate(children)
                     if c in expandable_children]

        # Select a random child
        child_to_be_expanded = \
            self.choose_tree_expansion(tree, expandable_children)

        # Expand in place
        children[index_map[child_to_be_expanded]] = \
            self.expand_tree_once(expandable_children[child_to_be_expanded])

        return tree

class GrammarFuzzer(GrammarFuzzer):
    def symbol_cost(self, symbol, seen=set()):
        expansions = self.grammar[symbol]
        return min(self.expansion_cost(e, seen | {symbol}) for e in expansions)

    def expansion_cost(self, expansion, seen=set()):
        symbols = nonterminals(expansion)
        if len(symbols) == 0:
            return 1  # no symbol

        if any(s in seen for s in symbols):
            return float('inf')

        # the value of a expansion is the sum of all expandable variables
        # inside + 1
        return sum(self.symbol_cost(s, seen) for s in symbols) + 1

class GrammarFuzzer(GrammarFuzzer):
    def expand_node_by_cost(self, node, choose=min):
        (symbol, children) = node
        assert children is None

        # Fetch the possible expansions from grammar...
        expansions = self.grammar[symbol]

        possible_children_with_cost = [(self.expansion_to_children(expansion),
                                        self.expansion_cost(expansion, {symbol}))
                                       for expansion in expansions]

        costs = [cost for (child, cost) in possible_children_with_cost]
        chosen_cost = choose(costs)
        children_with_chosen_cost = [child for (child, child_cost) in possible_children_with_cost
                                     if child_cost == chosen_cost]

        index = self.choose_node_expansion(node, children_with_chosen_cost)

        # Return with a new list
        return (symbol, children_with_chosen_cost[index])


class GrammarFuzzer(GrammarFuzzer):
    def expand_node_min_cost(self, node):
        if self.log:
            print("Expanding", all_terminals(node), "at minimum cost")

        return self.expand_node_by_cost(node, min)

class GrammarFuzzer(GrammarFuzzer):
    def expand_node(self, node):
        return self.expand_node_min_cost(node)

class GrammarFuzzer(GrammarFuzzer):
    def expand_node_max_cost(self, node):
        if self.log:
            print("Expanding", all_terminals(node), "at maximum cost")

        return self.expand_node_by_cost(node, max)

class GrammarFuzzer(GrammarFuzzer):
    def expand_node(self, node):
        return self.expand_node_max_cost(node)

class GrammarFuzzer(GrammarFuzzer):
    def log_tree(self, tree):
        """Output a tree if self.log is set; if self.display is also set, show the tree structure"""
        if self.log:
            print("Tree:", all_terminals(tree))
            if self.disp:
                display_tree(tree)
            # print(self.possible_expansions(tree), "possible expansion(s) left")

    def expand_tree_with_strategy(self, tree, expand_node_method, limit=None):
        """Expand tree using `expand_node_method` as node expansion function
        until the number of possible expansions reaches `limit`."""
        self.expand_node = expand_node_method
        while (limit is None or self.possible_expansions(tree)
               < limit) and self.any_possible_expansions(tree):
            tree = self.expand_tree_once(tree)
            self.log_tree(tree)
        return tree

    def expand_tree(self, tree):
        """Expand `tree` in a three-phase strategy until all expansions are complete."""
        self.log_tree(tree)
        tree = self.expand_tree_with_strategy(
            tree, self.expand_node_max_cost, self.min_nonterminals)
        tree = self.expand_tree_with_strategy(
            tree, self.expand_node_randomly, self.max_nonterminals)
        tree = self.expand_tree_with_strategy(tree, self.expand_node_min_cost)

        assert self.possible_expansions(tree) == 0

        return tree

class GrammarFuzzer(GrammarFuzzer):
    def fuzz_tree(self):
        # Create an initial derivation tree
        tree = self.init_tree()
        # print(tree)

        # Expand all nonterminals
        tree = self.expand_tree(tree)
        if self.log:
            print(repr(all_terminals(tree)))
        if self.disp:
            display_tree(tree)
        return tree

    def fuzz(self):
        self.derivation_tree = self.fuzz_tree()
        return all_terminals(self.derivation_tree)

from copy import deepcopy
import random

class FasterGrammarFuzzer(GrammarFuzzer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._expansion_cache = {}
        self._expansion_invocations = 0

    def expansion_to_children(self, expansion):
        self._expansion_invocations += 1
        if expansion in self._expansion_cache and random.randint(0,1) == 1:
            return deepcopy(random.choice(self._expansion_cache[expansion]))

        return super().expansion_to_children(expansion)

import string
CSV_GRAMMAR = {
    '<start>' : ['<csvline>'],
    '<csvline>': ['<items>'],
    '<items>' :  ['<item>,<items>', '<item>'],
    '<item>' : ['<letters>'],
    '<letters>': ['<letter><letters>', '<letter>'],
    '<letter>' : string.ascii_letters + string.digits + string.punctuation + ' \t\n'
}
fgf = FasterGrammarFuzzer(CSV_GRAMMAR, min_nonterminals=3)
fgf._expansion_cache['<letters>'] = [
      [('car', [])],
      [('van', [])],
]
trials = 100
valid = []
time = 0
for i in range(trials):
    with Timer() as t:
        vehicle_info = fgf.fuzz()
        print(vehicle_info)
        try:
            process_vehicle(vehicle_info)
            valid.append(vehicle_info)
        except:
            pass
        time += t.elapsed_time()
print("%d valid strings, that is GrammarFuzzer generated %f%% valid entries from %d inputs" % (len(valid), len(valid)*100.0/trials , trials))
print("Total time of %f seconds" % time)
#for k in fgf._expansion_cache:
#    print(k)
#    for i in fgf._expansion_cache[k]:
#        print("     ",i)
