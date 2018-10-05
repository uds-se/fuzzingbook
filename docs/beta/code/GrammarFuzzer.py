#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/GrammarFuzzer.html
# Last change: 2018-09-27 15:22:22+02:00
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

if __name__ == "__main__":
    print('# Efficient Grammar Fuzzing')




# ## An Insufficient Algorithm

if __name__ == "__main__":
    print('\n## An Insufficient Algorithm')




# import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from Grammars import EXPR_GRAMMAR_EBNF, convert_ebnf_grammar, simple_grammar_fuzzer
else:
    from .Grammars import EXPR_GRAMMAR_EBNF, convert_ebnf_grammar, simple_grammar_fuzzer


if __name__ == "__main__":
    expr_grammar = convert_ebnf_grammar(EXPR_GRAMMAR_EBNF)
    expr_grammar


if __package__ is None or __package__ == "":
    from ExpectError import ExpectTimeout
else:
    from .ExpectError import ExpectTimeout


if __name__ == "__main__":
    with ExpectTimeout(1):
        simple_grammar_fuzzer(grammar=expr_grammar, max_nonterminals=3)


if __name__ == "__main__":
    expr_grammar['<factor>']


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


if __name__ == "__main__":
    trials = 50
    xs = []
    ys = []
    for i in range(trials):
        with Timer() as t:
            s = simple_grammar_fuzzer(EXPR_GRAMMAR, max_nonterminals=15)
        xs.append(len(s))
        ys.append(t.elapsed_time())
        print(i, end=" ")
    print()


if __name__ == "__main__":
    average_time = sum(ys) / trials
    print("Average time:", average_time)


# %matplotlib inline
# 
# import matplotlib.pyplot as plt
# plt.scatter(xs, ys)
# plt.title('Time required for generating an output');

# ## Derivation Trees

if __name__ == "__main__":
    print('\n## Derivation Trees')




from graphviz import Digraph

if __name__ == "__main__":
    tree = Digraph("root")
    tree.attr('node', shape='plain')
    tree.node(r"\<start\>")


if __name__ == "__main__":
    tree


if __name__ == "__main__":
    tree.edge(r"\<start\>", r"\<expr\>")


if __name__ == "__main__":
    tree


if __name__ == "__main__":
    tree.edge(r"\<expr\>", r"\<expr\> ")
    tree.edge(r"\<expr\>", r"+")
    tree.edge(r"\<expr\>", r"\<term\>")


if __name__ == "__main__":
    tree


if __name__ == "__main__":
    tree.edge(r"\<expr\> ", r"\<term\> ")
    tree.edge(r"\<term\> ", r"\<factor\> ")
    tree.edge(r"\<factor\> ", r"\<integer\> ")
    tree.edge(r"\<integer\> ", r"\<digit\> ")
    tree.edge(r"\<digit\> ", r"2 ")

    tree.edge(r"\<term\>", r"\<factor\>")
    tree.edge(r"\<factor\>", r"\<integer\>")
    tree.edge(r"\<integer\>", r"\<digit\>")
    tree.edge(r"\<digit\>", r"2")


if __name__ == "__main__":
    tree


# ## Representing Derivation Trees

if __name__ == "__main__":
    print('\n## Representing Derivation Trees')




if __name__ == "__main__":
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])



from graphviz import Digraph

from IPython.display import display

import re

def dot_escape(s):
    """Return s in a form suitable for dot"""
    # s = s.replace("\\", "\\\\")
    s = re.sub(r"([^a-zA-Z0-9 ])", r"\\\1", s)
    return s

if __name__ == "__main__":
    assert dot_escape("hello") == "hello"
    assert dot_escape("<hello>, world") == "\\<hello\\>\\, world"
    assert dot_escape("\\n") == "\\\\n"


def display_tree(derivation_tree):
    """Visualize a derivation tree as SVG using the graphviz/dot package."""

    counter = 0

    def traverse_tree(dot, tree, id=0):
        (symbol, children) = tree
        dot.node(repr(id), dot_escape(symbol))

        if children is not None:
            for child in children:
                nonlocal counter  # Assign each node a unique identifier
                counter += 1
                child_id = counter
                dot.edge(repr(id), repr(child_id))
                traverse_tree(dot, child, child_id)

    dot = Digraph(comment="Derivation Tree")
    dot.attr('node', shape='plain')
    traverse_tree(dot, derivation_tree)
    display(dot)


if __name__ == "__main__":
    display_tree(derivation_tree)


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

if __name__ == "__main__":
    all_terminals(derivation_tree)


# ## Expanding a Node

if __name__ == "__main__":
    print('\n## Expanding a Node')




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


class GrammarFuzzer(GrammarFuzzer):
    def init_tree(self):
        return (self.start_symbol, None)

if __name__ == "__main__":
    f = GrammarFuzzer(EXPR_GRAMMAR)
    display_tree(f.init_tree())


class GrammarFuzzer(GrammarFuzzer):
    def expansion_to_children(self, expansion):
        # print("Converting " + repr(expansion))
        # strings contains all substrings -- both terminals and non-terminals such
        # that ''.join(strings) == expansion

        # See nonterminals() in Grammars.py
        if isinstance(expansion, tuple):
            expansion = expansion[0]

        if expansion == "":  # Special case: empty expansion
            return [("", [])]

        strings = re.split(RE_NONTERMINAL, expansion)
        return [(s, None) if is_nonterminal(s) else (s, [])
                for s in strings if len(s) > 0]


if __name__ == "__main__":
    f = GrammarFuzzer(EXPR_GRAMMAR)
    f.expansion_to_children("<term> + <expr>")


if __name__ == "__main__":
    f.expansion_to_children("")


if __name__ == "__main__":
    f.expansion_to_children(("+<term>", ["extra_data"]))


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
        possible_children = [self.expansion_to_children(
            expansion) for expansion in expansions]

        # ... and select a random expansion
        index = self.choose_node_expansion(node, possible_children)
        children = possible_children[index]

        # Return with new children
        return (symbol, children)


class GrammarFuzzer(GrammarFuzzer):
    def expand_node(self, node):
        return self.expand_node_randomly(node)

if __name__ == "__main__":
    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)

    print("Before:")
    tree = ("<term>", None)
    display_tree(tree)

    print("After:")
    tree = f.expand_node_randomly(tree)
    display_tree(tree)


# ## Expanding a Tree

if __name__ == "__main__":
    print('\n## Expanding a Tree')




class GrammarFuzzer(GrammarFuzzer):
    def possible_expansions(self, node):
        (symbol, children) = node
        if children is None:
            return 1

        return sum(self.possible_expansions(c) for c in children)

if __name__ == "__main__":
    f = GrammarFuzzer(EXPR_GRAMMAR)
    print(f.possible_expansions(derivation_tree))


class GrammarFuzzer(GrammarFuzzer):
    def any_possible_expansions(self, node):
        (symbol, children) = node
        if children is None:
            return True

        return any(self.any_possible_expansions(c) for c in children)

if __name__ == "__main__":
    f = GrammarFuzzer(EXPR_GRAMMAR)
    f.any_possible_expansions(derivation_tree)


class GrammarFuzzer(GrammarFuzzer):
    def choose_tree_expansion(self, tree, children):
        """Return index of subtree in `children` to be selected for expansion.  Defaults to random."""
        return random.randrange(0, len(children))

    def expand_tree_once(self, tree):
        # print("Expanding " + repr(tree))

        (symbol, children) = tree
        if children is None:
            # Expand this node
            return self.expand_node(tree)

        # Find all children with possible expansions
        expandable_children = [
            c for c in children if self.any_possible_expansions(c)]

        # `index_map` translates an index in `expandable_children` back into the original index in `children`
        index_map = [i for (i, c) in enumerate(children)
                     if self.any_possible_expansions(c)]

        # print("expandable_children =", expandable_children)
        # print("index_map =", index_map)

        # Select a random child
        child_to_be_expanded = self.choose_tree_expansion(
            tree, expandable_children)

        # Expand in place
        children[index_map[child_to_be_expanded]] = \
            self.expand_tree_once(expandable_children[child_to_be_expanded])

        return tree


if __name__ == "__main__":
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])
    display_tree(derivation_tree)


if __name__ == "__main__":
    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)
    derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)


if __name__ == "__main__":
    derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)


# ## Closing the Expansion

if __name__ == "__main__":
    print('\n## Closing the Expansion')




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


if __name__ == "__main__":
    f = GrammarFuzzer(EXPR_GRAMMAR)
    assert f.symbol_cost("<digit>") == 1


if __name__ == "__main__":
    assert f.symbol_cost("<expr>") == 5


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

if __name__ == "__main__":
    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)
    display_tree(derivation_tree)

    step = 1
    while f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
        if step < 3:
            display_tree(derivation_tree)
        step += 1
    display_tree(derivation_tree)


# ## Node Inflation

if __name__ == "__main__":
    print('\n## Node Inflation')




class GrammarFuzzer(GrammarFuzzer):
    def expand_node_max_cost(self, node):
        if self.log:
            print("Expanding", all_terminals(node), "at maximum cost")

        return self.expand_node_by_cost(node, max)

class GrammarFuzzer(GrammarFuzzer):
    def expand_node(self, node):
        return self.expand_node_max_cost(node)

if __name__ == "__main__":
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])

    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)
    display_tree(derivation_tree)

    step = 1
    while step < 3 and f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
        display_tree(derivation_tree)
        step += 1



# ## Three Expansion Phases

if __name__ == "__main__":
    print('\n## Three Expansion Phases')




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


if __name__ == "__main__":
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])

    f = GrammarFuzzer(
        EXPR_GRAMMAR,
        min_nonterminals=3,
        max_nonterminals=5,
        log=True)
    derivation_tree = f.expand_tree(derivation_tree)
    display_tree(derivation_tree)



if __name__ == "__main__":
    all_terminals(derivation_tree)


# ## Putting it all Together

if __name__ == "__main__":
    print('\n## Putting it all Together')




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

if __name__ == "__main__":
    f = GrammarFuzzer(EXPR_GRAMMAR)
    f.fuzz()


if __name__ == "__main__":
    display_tree(f.derivation_tree)


if __name__ == "__main__":
    f = GrammarFuzzer(URL_GRAMMAR)
    f.fuzz()


if __name__ == "__main__":
    display_tree(f.derivation_tree)


if __name__ == "__main__":
    f = GrammarFuzzer(CGI_GRAMMAR, min_nonterminals=3, max_nonterminals=5)
    f.fuzz()


if __name__ == "__main__":
    display_tree(f.derivation_tree)


if __name__ == "__main__":
    trials = 50
    xs = []
    ys = []
    f = GrammarFuzzer(EXPR_GRAMMAR, max_nonterminals=20)
    for i in range(trials):
        with Timer() as t:
            s = f.fuzz()
        xs.append(len(s))
        ys.append(t.elapsed_time())
        print(i, end=" ")
    print()


if __name__ == "__main__":
    average_time = sum(ys) / trials
    print("Average time:", average_time)


# %matplotlib inline
# 
# import matplotlib.pyplot as plt
# plt.scatter(xs, ys)
# plt.title('Time required for generating an output');

if __name__ == "__main__":
    f = GrammarFuzzer(expr_grammar, max_nonterminals=10)
    f.fuzz()


# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1

if __name__ == "__main__":
    print('\n### Exercise 1')




def memoize(argnum):
    # cache the function calls. We only cache a given call based on the
    # indicated argument number per function.
    def fn_wrap(function):
        memo = {}

        def wrapper(*args):
            if args[argnum] in memo:
                return memo[args[argnum]]
            rv = function(*args)
            memo[args[argnum]] = rv
            return rv
        return wrapper
    return fn_wrap

# ### Exercise 2

if __name__ == "__main__":
    print('\n### Exercise 2')




# ### Exercise 3

if __name__ == "__main__":
    print('\n### Exercise 3')




class ExerciseGrammarFuzzer(GrammarFuzzer):
    def expand_node_randomly(self, node):
        if self.log:
            print("Expanding", all_terminals(node), "randomly by cost")

        return self.expand_node_by_cost(node, random.choice)
