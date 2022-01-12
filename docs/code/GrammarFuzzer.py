#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Efficient Grammar Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/GrammarFuzzer.html
# Last change: 2022-01-12 14:43:50+01:00
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
The Fuzzing Book - Efficient Grammar Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python GrammarFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.GrammarFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/GrammarFuzzer.html

### Efficient Grammar Fuzzing

This chapter introduces `GrammarFuzzer`, an efficient grammar fuzzer that takes a grammar to produce syntactically valid input strings.  Here's a typical usage:

>>> from Grammars import US_PHONE_GRAMMAR
>>> phone_fuzzer = GrammarFuzzer(US_PHONE_GRAMMAR)
>>> phone_fuzzer.fuzz()
'(855)846-4471'

The `GrammarFuzzer` constructor takes a number of keyword arguments to control its behavior.  `start_symbol`, for instance, allows to set the symbol that expansion starts with (instead of ``):

>>> area_fuzzer = GrammarFuzzer(US_PHONE_GRAMMAR, start_symbol='')
>>> area_fuzzer.fuzz()
'796'

Here's how to parameterize the `GrammarFuzzer` constructor:

Produce strings from `grammar`, starting with `start_symbol`.
If `min_nonterminals` or `max_nonterminals` is given, use them as limits 
for the number of nonterminals produced.  
If `disp` is set, display the intermediate derivation trees.
If `log` is set, show intermediate steps as text on standard output.
### Derivation Trees

Internally, `GrammarFuzzer` makes use of [derivation trees](#Derivation-Trees), which it expands step by step.  After producing a string, the tree produced can be accessed in the `derivation_tree` attribute.

>>> display_tree(phone_fuzzer.derivation_tree)
In the internal representation of a derivation tree, a _node_ is a pair (`symbol`, `children`).  For nonterminals, `symbol` is the symbol that is being expanded, and `children` is a list of further nodes.  For terminals, `symbol` is the terminal string, and `children` is empty.

>>> phone_fuzzer.derivation_tree
('',
 [('',
   [('(', []),
    ('',
     [('', [('8', [])]),
      ('', [('5', [])]),
      ('', [('5', [])])]),
    (')', []),
    ('',
     [('', [('8', [])]),
      ('', [('4', [])]),
      ('', [('6', [])])]),
    ('-', []),
    ('',
     [('', [('4', [])]),
      ('', [('4', [])]),
      ('', [('7', [])]),
      ('', [('1', [])])])])])

The chapter contains various helpers to work with derivation trees, including visualization tools – notably, `display_tree()`, above.


For more details, source, and documentation, see
"The Fuzzing Book - Efficient Grammar Fuzzing"
at https://www.fuzzingbook.org/html/GrammarFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Efficient Grammar Fuzzing
# =========================

if __name__ == '__main__':
    print('# Efficient Grammar Fuzzing')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo('84k8AO_3ChY')

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## An Insufficient Algorithm
## -------------------------

if __name__ == '__main__':
    print('\n## An Insufficient Algorithm')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .bookutils import quiz

from typing import Tuple, List, Optional, Any, Union, Set, Callable, Dict

from .bookutils import unicode_escape

from .Grammars import EXPR_EBNF_GRAMMAR, convert_ebnf_grammar, Grammar, Expansion
from .Grammars import simple_grammar_fuzzer, is_valid_grammar, exp_string

if __name__ == '__main__':
    expr_grammar = convert_ebnf_grammar(EXPR_EBNF_GRAMMAR)
    expr_grammar

from .ExpectError import ExpectTimeout

if __name__ == '__main__':
    with ExpectTimeout(1):
        simple_grammar_fuzzer(grammar=expr_grammar, max_nonterminals=3)

if __name__ == '__main__':
    quiz("Why does `simple_grammar_fuzzer()` hang?",
         [
             "It produces an infinite number of additions",
             "It produces an infinite number of digits",
             "It produces an infinite number of parentheses",
             "It produces an infinite number of signs",
         ], '(3 * 3 * 3) ** (3 / (3 * 3))')

if __name__ == '__main__':
    expr_grammar['<factor>']

from .Grammars import simple_grammar_fuzzer

from .Grammars import START_SYMBOL, EXPR_GRAMMAR, URL_GRAMMAR, CGI_GRAMMAR

from .Grammars import RE_NONTERMINAL, nonterminals, is_nonterminal

from .Timer import Timer

if __name__ == '__main__':
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

if __name__ == '__main__':
    average_time = sum(ys) / trials
    print("Average time:", average_time)

# %matplotlib inline
# 
# import matplotlib.pyplot as plt
# plt.scatter(xs, ys)
# plt.title('Time required for generating an output');

## Derivation Trees
## ----------------

if __name__ == '__main__':
    print('\n## Derivation Trees')



from graphviz import Digraph

if __name__ == '__main__':
    tree = Digraph("root")
    tree.attr('node', shape='plain')
    tree.node(r"\<start\>")

if __name__ == '__main__':
    tree

if __name__ == '__main__':
    tree.edge(r"\<start\>", r"\<expr\>")

if __name__ == '__main__':
    tree

if __name__ == '__main__':
    tree.edge(r"\<expr\>", r"\<expr\> ")
    tree.edge(r"\<expr\>", r"+")
    tree.edge(r"\<expr\>", r"\<term\>")

if __name__ == '__main__':
    tree

if __name__ == '__main__':
    tree.edge(r"\<expr\> ", r"\<term\> ")
    tree.edge(r"\<term\> ", r"\<factor\> ")
    tree.edge(r"\<factor\> ", r"\<integer\> ")
    tree.edge(r"\<integer\> ", r"\<digit\> ")
    tree.edge(r"\<digit\> ", r"2 ")

    tree.edge(r"\<term\>", r"\<factor\>")
    tree.edge(r"\<factor\>", r"\<integer\>")
    tree.edge(r"\<integer\>", r"\<digit\>")
    tree.edge(r"\<digit\>", r"2")

if __name__ == '__main__':
    tree

## Representing Derivation Trees
## -----------------------------

if __name__ == '__main__':
    print('\n## Representing Derivation Trees')



DerivationTree = Tuple[str, Optional[List[Any]]]

if __name__ == '__main__':
    derivation_tree: DerivationTree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])

#### Excursion: Implementing `display_tree()`

if __name__ == '__main__':
    print('\n#### Excursion: Implementing `display_tree()`')



from graphviz import Digraph

if __name__ == '__main__':
    from IPython.display import display

import re

def dot_escape(s: str) -> str:
    """Return s in a form suitable for dot"""
    s = re.sub(r'([^a-zA-Z0-9" ])', r"\\\1", s)
    return s

if __name__ == '__main__':
    assert dot_escape("hello") == "hello"
    assert dot_escape("<hello>, world") == "\\<hello\\>\\, world"
    assert dot_escape("\\n") == "\\\\n"

def extract_node(node, id):
    symbol, children, *annotation = node
    return symbol, children, ''.join(str(a) for a in annotation)

def default_node_attr(dot, nid, symbol, ann):
    dot.node(repr(nid), dot_escape(unicode_escape(symbol)))

def default_edge_attr(dot, start_node, stop_node):
    dot.edge(repr(start_node), repr(stop_node))

def default_graph_attr(dot):
    dot.attr('node', shape='plain')

def display_tree(derivation_tree: DerivationTree,
                 log: bool = False,
                 extract_node: Callable = extract_node,
                 node_attr: Callable = default_node_attr,
                 edge_attr: Callable = default_edge_attr,
                 graph_attr: Callable = default_graph_attr) -> Any:

    # If we import display_tree, we also have to import its functions
    from graphviz import Digraph

    counter = 0

    def traverse_tree(dot, tree, id=0):
        (symbol, children, annotation) = extract_node(tree, id)
        node_attr(dot, id, symbol, annotation)

        if children:
            for child in children:
                nonlocal counter
                counter += 1
                child_id = counter
                edge_attr(dot, id, child_id)
                traverse_tree(dot, child, child_id)

    dot = Digraph(comment="Derivation Tree")
    graph_attr(dot)
    traverse_tree(dot, derivation_tree)
    if log:
        print(dot)
    return dot

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    display_tree(derivation_tree)

if __name__ == '__main__':
    quiz("And which of these is the internal representation of `derivation_tree`?",
        [
            "`('<start>', [('<expr>', (['<expr> + <term>']))])`",
            "`('<start>', [('<expr>', (['<expr>', ' + ', <term>']))])`",
            "`" + repr(derivation_tree) + "`",
            "`(" + repr(derivation_tree) + ", None)`"
        ], len("eleven") - len("one"))

if __name__ == '__main__':
    derivation_tree

#### Excursion: Source code and example for `display_annotated_tree()`

if __name__ == '__main__':
    print('\n#### Excursion: Source code and example for `display_annotated_tree()`')



def display_annotated_tree(tree: DerivationTree,
                           a_nodes: Dict[int, str],
                           a_edges: Dict[Tuple[int, int], str],
                           log: bool = False):
    def graph_attr(dot):
        dot.attr('node', shape='plain')
        dot.graph_attr['rankdir'] = 'LR'

    def annotate_node(dot, nid, symbol, ann):
        if nid in a_nodes:
            dot.node(repr(nid), 
                     "%s (%s)" % (dot_escape(unicode_escape(symbol)),
                                  a_nodes[nid]))
        else:
            dot.node(repr(nid), dot_escape(unicode_escape(symbol)))

    def annotate_edge(dot, start_node, stop_node):
        if (start_node, stop_node) in a_edges:
            dot.edge(repr(start_node), repr(stop_node),
                     a_edges[(start_node, stop_node)])
        else:
            dot.edge(repr(start_node), repr(stop_node))

    return display_tree(tree, log=log,
                        node_attr=annotate_node,
                        edge_attr=annotate_edge,
                        graph_attr=graph_attr)

if __name__ == '__main__':
    display_annotated_tree(derivation_tree, {3: 'plus'}, {(1, 3): 'op'}, log=False)

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



def all_terminals(tree: DerivationTree) -> str:
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

if __name__ == '__main__':
    all_terminals(derivation_tree)

def tree_to_string(tree: DerivationTree) -> str:
    symbol, children, *_ = tree
    if children:
        return ''.join(tree_to_string(c) for c in children)
    else:
        return '' if is_nonterminal(symbol) else symbol

if __name__ == '__main__':
    tree_to_string(derivation_tree)

## Expanding a Node
## ----------------

if __name__ == '__main__':
    print('\n## Expanding a Node')



from .Fuzzer import Fuzzer

class GrammarFuzzer(Fuzzer):
    """Produce strings from grammars efficiently, using derivation trees."""

    def __init__(self,
                 grammar: Grammar,
                 start_symbol: str = START_SYMBOL,
                 min_nonterminals: int = 0,
                 max_nonterminals: int = 10,
                 disp: bool = False,
                 log: Union[bool, int] = False) -> None:
        """Produce strings from `grammar`, starting with `start_symbol`.
        If `min_nonterminals` or `max_nonterminals` is given, use them as limits 
        for the number of nonterminals produced.  
        If `disp` is set, display the intermediate derivation trees.
        If `log` is set, show intermediate steps as text on standard output."""

        self.grammar = grammar
        self.start_symbol = start_symbol
        self.min_nonterminals = min_nonterminals
        self.max_nonterminals = max_nonterminals
        self.disp = disp
        self.log = log
        self.check_grammar()  # Invokes is_valid_grammar()

#### Excursion: `check_grammar()` implementation

if __name__ == '__main__':
    print('\n#### Excursion: `check_grammar()` implementation')



class GrammarFuzzer(GrammarFuzzer):
    def check_grammar(self) -> None:
        """Check the grammar passed"""
        assert self.start_symbol in self.grammar
        assert is_valid_grammar(
            self.grammar,
            start_symbol=self.start_symbol,
            supported_opts=self.supported_opts())

    def supported_opts(self) -> Set[str]:
        """Set of supported options. To be overloaded in subclasses."""
        return set()  # We don't support specific options

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



class GrammarFuzzer(GrammarFuzzer):
    def init_tree(self) -> DerivationTree:
        return (self.start_symbol, None)

if __name__ == '__main__':
    f = GrammarFuzzer(EXPR_GRAMMAR)
    display_tree(f.init_tree())

### Picking a Children Alternative to be Expanded

if __name__ == '__main__':
    print('\n### Picking a Children Alternative to be Expanded')



class GrammarFuzzer(GrammarFuzzer):
    def choose_node_expansion(self, node: DerivationTree,
                              children_alternatives: List[List[DerivationTree]]) -> int:
        """Return index of expansion in `children_alternatives` to be selected.
           'children_alternatives`: a list of possible children for `node`.
           Defaults to random. To be overloaded in subclasses."""
        return random.randrange(0, len(children_alternatives))

### Getting a List of Possible Expansions

if __name__ == '__main__':
    print('\n### Getting a List of Possible Expansions')



#### Excursion: Implementing `expansion_to_children()`

if __name__ == '__main__':
    print('\n#### Excursion: Implementing `expansion_to_children()`')



def expansion_to_children(expansion: Expansion) -> List[DerivationTree]:
    # print("Converting " + repr(expansion))
    # strings contains all substrings -- both terminals and nonterminals such
    # that ''.join(strings) == expansion

    expansion = exp_string(expansion)
    assert isinstance(expansion, str)

    if expansion == "":  # Special case: epsilon expansion
        return [("", [])]

    strings = re.split(RE_NONTERMINAL, expansion)
    return [(s, None) if is_nonterminal(s) else (s, [])
            for s in strings if len(s) > 0]

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    expansion_to_children("<term> + <expr>")

if __name__ == '__main__':
    expansion_to_children("")

if __name__ == '__main__':
    expansion_to_children(("+<term>", {"extra_data": 1234}))

class GrammarFuzzer(GrammarFuzzer):
    def expansion_to_children(self, expansion: Expansion) -> List[DerivationTree]:
        return expansion_to_children(expansion)

### Putting Things Together

if __name__ == '__main__':
    print('\n### Putting Things Together')



#### Excursion: `expand_node_randomly()` implementation

if __name__ == '__main__':
    print('\n#### Excursion: `expand_node_randomly()` implementation')



import random

class GrammarFuzzer(GrammarFuzzer):
    def expand_node_randomly(self, node: DerivationTree) -> DerivationTree:
        """Choose a random expansion for `node` and return it"""
        (symbol, children) = node
        assert children is None

        if self.log:
            print("Expanding", all_terminals(node), "randomly")

        # Fetch the possible expansions from grammar...
        expansions = self.grammar[symbol]
        children_alternatives: List[List[DerivationTree]] = [
            self.expansion_to_children(expansion) for expansion in expansions
        ]

        # ... and select a random expansion
        index = self.choose_node_expansion(node, children_alternatives)
        chosen_children = children_alternatives[index]

        # Process children (for subclasses)
        chosen_children = self.process_chosen_children(chosen_children,
                                                       expansions[index])

        # Return with new children
        return (symbol, chosen_children)

class GrammarFuzzer(GrammarFuzzer):
    def expand_node(self, node: DerivationTree) -> DerivationTree:
        return self.expand_node_randomly(node)

class GrammarFuzzer(GrammarFuzzer):
    def process_chosen_children(self,
                                chosen_children: List[DerivationTree],
                                expansion: Expansion) -> List[DerivationTree]:
        """Process children after selection.  By default, does nothing."""
        return chosen_children

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)

    print("Before expand_node_randomly():")
    expr_tree = ("<integer>", None)
    display_tree(expr_tree)

if __name__ == '__main__':
    print("After expand_node_randomly():")
    expr_tree = f.expand_node_randomly(expr_tree)
    display_tree(expr_tree)

if __name__ == '__main__':
    quiz("What tree do we get if we expand the `<digit>` subtree?",
         [
             "We get another `<digit>` as new child of `<digit>`",
             "We get some digit as child of `<digit>`",
             "We get another `<digit>` as second child of `<integer>`",
             "The entire tree becomes a single node with a digit"
         ], 'len("2") + len("2")')

if __name__ == '__main__':
    digit_subtree = expr_tree[1][0]  # type: ignore
    display_tree(digit_subtree)

if __name__ == '__main__':
    print("After expanding the <digit> subtree:")
    digit_subtree = f.expand_node_randomly(digit_subtree)
    display_tree(digit_subtree)

if __name__ == '__main__':
    quiz("Is the original `expr_tree` affected by this change?",
         [
             "Yes, it has also gained a new child",
             "No, it is unchanged"
         ], "1 ** (1 - 1)")

if __name__ == '__main__':
    display_tree(expr_tree)

## Expanding a Tree
## ----------------

if __name__ == '__main__':
    print('\n## Expanding a Tree')



class GrammarFuzzer(GrammarFuzzer):
    def possible_expansions(self, node: DerivationTree) -> int:
        (symbol, children) = node
        if children is None:
            return 1

        return sum(self.possible_expansions(c) for c in children)

if __name__ == '__main__':
    f = GrammarFuzzer(EXPR_GRAMMAR)
    print(f.possible_expansions(derivation_tree))

class GrammarFuzzer(GrammarFuzzer):
    def any_possible_expansions(self, node: DerivationTree) -> bool:
        (symbol, children) = node
        if children is None:
            return True

        return any(self.any_possible_expansions(c) for c in children)

if __name__ == '__main__':
    f = GrammarFuzzer(EXPR_GRAMMAR)
    f.any_possible_expansions(derivation_tree)

#### Excursion: `expand_tree_once()` implementation

if __name__ == '__main__':
    print('\n#### Excursion: `expand_tree_once()` implementation')



class GrammarFuzzer(GrammarFuzzer):
    def choose_tree_expansion(self,
                              tree: DerivationTree,
                              children: List[DerivationTree]) -> int:
        """Return index of subtree in `children` to be selected for expansion.
           Defaults to random."""
        return random.randrange(0, len(children))

    def expand_tree_once(self, tree: DerivationTree) -> DerivationTree:
        """Choose an unexpanded symbol in tree; expand it.
           Can be overloaded in subclasses."""
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

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])
    display_tree(derivation_tree)

if __name__ == '__main__':
    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)
    derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)

if __name__ == '__main__':
    derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)

## Closing the Expansion
## ---------------------

if __name__ == '__main__':
    print('\n## Closing the Expansion')



### Excursion: Implementing Cost Functions

if __name__ == '__main__':
    print('\n### Excursion: Implementing Cost Functions')



class GrammarFuzzer(GrammarFuzzer):
    def symbol_cost(self, symbol: str, seen: Set[str] = set()) \
            -> Union[int, float]:
        expansions = self.grammar[symbol]
        return min(self.expansion_cost(e, seen | {symbol}) for e in expansions)

    def expansion_cost(self, expansion: Expansion,
                       seen: Set[str] = set()) -> Union[int, float]:
        symbols = nonterminals(expansion)
        if len(symbols) == 0:
            return 1  # no symbol

        if any(s in seen for s in symbols):
            return float('inf')

        # the value of a expansion is the sum of all expandable variables
        # inside + 1
        return sum(self.symbol_cost(s, seen) for s in symbols) + 1

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



if __name__ == '__main__':
    f = GrammarFuzzer(EXPR_GRAMMAR)
    assert f.symbol_cost("<digit>") == 1

if __name__ == '__main__':
    assert f.symbol_cost("<expr>") == 5

#### Excursion: `expand_node_by_cost()` implementation

if __name__ == '__main__':
    print('\n#### Excursion: `expand_node_by_cost()` implementation')



class GrammarFuzzer(GrammarFuzzer):
    def expand_node_by_cost(self, node: DerivationTree, 
                            choose: Callable = min) -> DerivationTree:
        (symbol, children) = node
        assert children is None

        # Fetch the possible expansions from grammar...
        expansions = self.grammar[symbol]

        children_alternatives_with_cost = [(self.expansion_to_children(expansion),
                                            self.expansion_cost(expansion, {symbol}),
                                            expansion)
                                           for expansion in expansions]

        costs = [cost for (child, cost, expansion)
                 in children_alternatives_with_cost]
        chosen_cost = choose(costs)
        children_with_chosen_cost = [child for (child, child_cost, _) 
                                     in children_alternatives_with_cost
                                     if child_cost == chosen_cost]
        expansion_with_chosen_cost = [expansion for (_, child_cost, expansion)
                                      in children_alternatives_with_cost
                                      if child_cost == chosen_cost]

        index = self.choose_node_expansion(node, children_with_chosen_cost)

        chosen_children = children_with_chosen_cost[index]
        chosen_expansion = expansion_with_chosen_cost[index]
        chosen_children = self.process_chosen_children(
            chosen_children, chosen_expansion)

        # Return with a new list
        return (symbol, chosen_children)

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



class GrammarFuzzer(GrammarFuzzer):
    def expand_node_min_cost(self, node: DerivationTree) -> DerivationTree:
        if self.log:
            print("Expanding", all_terminals(node), "at minimum cost")

        return self.expand_node_by_cost(node, min)

class GrammarFuzzer(GrammarFuzzer):
    def expand_node(self, node: DerivationTree) -> DerivationTree:
        return self.expand_node_min_cost(node)

if __name__ == '__main__':
    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)
    display_tree(derivation_tree)

if __name__ == '__main__':
    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)

if __name__ == '__main__':
    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)

if __name__ == '__main__':
    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)

if __name__ == '__main__':
    while f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)    

if __name__ == '__main__':
    display_tree(derivation_tree)

## Node Inflation
## --------------

if __name__ == '__main__':
    print('\n## Node Inflation')



class GrammarFuzzer(GrammarFuzzer):
    def expand_node_max_cost(self, node: DerivationTree) -> DerivationTree:
        if self.log:
            print("Expanding", all_terminals(node), "at maximum cost")

        return self.expand_node_by_cost(node, max)

class GrammarFuzzer(GrammarFuzzer):
    def expand_node(self, node: DerivationTree) -> DerivationTree:
        return self.expand_node_max_cost(node)

if __name__ == '__main__':
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])

if __name__ == '__main__':
    f = GrammarFuzzer(EXPR_GRAMMAR, log=True)
    display_tree(derivation_tree)

if __name__ == '__main__':
    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)

if __name__ == '__main__':
    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)

if __name__ == '__main__':
    if f.any_possible_expansions(derivation_tree):
        derivation_tree = f.expand_tree_once(derivation_tree)
    display_tree(derivation_tree)

## Three Expansion Phases
## ----------------------

if __name__ == '__main__':
    print('\n## Three Expansion Phases')



#### Excursion: Implementation of three-phase `expand_tree()`

if __name__ == '__main__':
    print('\n#### Excursion: Implementation of three-phase `expand_tree()`')



class GrammarFuzzer(GrammarFuzzer):
    def log_tree(self, tree: DerivationTree) -> None:
        """Output a tree if self.log is set; if self.display is also set, show the tree structure"""
        if self.log:
            print("Tree:", all_terminals(tree))
            if self.disp:
                display(display_tree(tree))
            # print(self.possible_expansions(tree), "possible expansion(s) left")

    def expand_tree_with_strategy(self, tree: DerivationTree,
                                  expand_node_method: Callable,
                                  limit: Optional[int] = None):
        """Expand tree using `expand_node_method` as node expansion function
        until the number of possible expansions reaches `limit`."""
        self.expand_node = expand_node_method  # type: ignore
        while ((limit is None
                or self.possible_expansions(tree) < limit)
               and self.any_possible_expansions(tree)):
            tree = self.expand_tree_once(tree)
            self.log_tree(tree)
        return tree

    def expand_tree(self, tree: DerivationTree) -> DerivationTree:
        """Expand `tree` in a three-phase strategy until all expansions are complete."""
        self.log_tree(tree)
        tree = self.expand_tree_with_strategy(
            tree, self.expand_node_max_cost, self.min_nonterminals)
        tree = self.expand_tree_with_strategy(
            tree, self.expand_node_randomly, self.max_nonterminals)
        tree = self.expand_tree_with_strategy(
            tree, self.expand_node_min_cost)

        assert self.possible_expansions(tree) == 0

        return tree

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    initial_derivation_tree: DerivationTree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])

if __name__ == '__main__':
    display_tree(initial_derivation_tree)

if __name__ == '__main__':
    f = GrammarFuzzer(
        EXPR_GRAMMAR,
        min_nonterminals=3,
        max_nonterminals=5,
        log=True)
    derivation_tree = f.expand_tree(initial_derivation_tree)

if __name__ == '__main__':
    display_tree(derivation_tree)

if __name__ == '__main__':
    all_terminals(derivation_tree)

## Putting it all Together
## -----------------------

if __name__ == '__main__':
    print('\n## Putting it all Together')



class GrammarFuzzer(GrammarFuzzer):
    def fuzz_tree(self) -> DerivationTree:
        """Produce a derivation tree from the grammar."""
        tree = self.init_tree()
        # print(tree)

        # Expand all nonterminals
        tree = self.expand_tree(tree)
        if self.log:
            print(repr(all_terminals(tree)))
        if self.disp:
            display(display_tree(tree))
        return tree

    def fuzz(self) -> str:
        """Produce a string from the grammar."""
        self.derivation_tree = self.fuzz_tree()
        return all_terminals(self.derivation_tree)

if __name__ == '__main__':
    f = GrammarFuzzer(EXPR_GRAMMAR)
    f.fuzz()

if __name__ == '__main__':
    display_tree(f.derivation_tree)

if __name__ == '__main__':
    f = GrammarFuzzer(URL_GRAMMAR)
    f.fuzz()

if __name__ == '__main__':
    display_tree(f.derivation_tree)

if __name__ == '__main__':
    f = GrammarFuzzer(CGI_GRAMMAR, min_nonterminals=3, max_nonterminals=5)
    f.fuzz()

if __name__ == '__main__':
    display_tree(f.derivation_tree)

if __name__ == '__main__':
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

if __name__ == '__main__':
    average_time = sum(ys) / trials
    print("Average time:", average_time)

# %matplotlib inline
# 
# import matplotlib.pyplot as plt
# plt.scatter(xs, ys)
# plt.title('Time required for generating an output');

if __name__ == '__main__':
    f = GrammarFuzzer(expr_grammar, max_nonterminals=10)
    f.fuzz()

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



### Efficient Grammar Fuzzing

if __name__ == '__main__':
    print('\n### Efficient Grammar Fuzzing')



from .Grammars import US_PHONE_GRAMMAR

if __name__ == '__main__':
    phone_fuzzer = GrammarFuzzer(US_PHONE_GRAMMAR)
    phone_fuzzer.fuzz()

if __name__ == '__main__':
    area_fuzzer = GrammarFuzzer(US_PHONE_GRAMMAR, start_symbol='<area>')
    area_fuzzer.fuzz()

import inspect

if __name__ == '__main__':
    print(inspect.getdoc(GrammarFuzzer.__init__))

from .ClassDiagram import display_class_hierarchy

if __name__ == '__main__':
    display_class_hierarchy([GrammarFuzzer],
                            public_methods=[
                                Fuzzer.__init__,
                                Fuzzer.fuzz,
                                Fuzzer.run,
                                Fuzzer.runs,
                                GrammarFuzzer.__init__,
                                GrammarFuzzer.fuzz,
                                GrammarFuzzer.fuzz_tree,
                            ],
                            types={
                                'DerivationTree': DerivationTree,
                                'Expansion': Expansion,
                                'Grammar': Grammar
                            },
                            project='fuzzingbook')

### Derivation Trees

if __name__ == '__main__':
    print('\n### Derivation Trees')



if __name__ == '__main__':
    display_tree(phone_fuzzer.derivation_tree)

if __name__ == '__main__':
    phone_fuzzer.derivation_tree

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



### Extending Grammars

if __name__ == '__main__':
    print('\n### Extending Grammars')



### Applying Grammars

if __name__ == '__main__':
    print('\n### Applying Grammars')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Caching Method Results

if __name__ == '__main__':
    print('\n### Exercise 1: Caching Method Results')



import copy

class FasterGrammarFuzzer(GrammarFuzzer):
    """Variant of `GrammarFuzzer` with memoized values"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._expansion_cache: Dict[Expansion, List[DerivationTree]] = {}
        self._expansion_invocations = 0
        self._expansion_invocations_cached = 0

    def expansion_to_children(self, expansion: Expansion) \
            -> List[DerivationTree]:
        self._expansion_invocations += 1
        if expansion in self._expansion_cache:
            self._expansion_invocations_cached += 1
            cached_result = copy.deepcopy(self._expansion_cache[expansion])
            return cached_result

        result = super().expansion_to_children(expansion)
        self._expansion_cache[expansion] = result
        return result

if __name__ == '__main__':
    f = FasterGrammarFuzzer(EXPR_GRAMMAR, min_nonterminals=3, max_nonterminals=5)
    f.fuzz()

if __name__ == '__main__':
    f._expansion_invocations

if __name__ == '__main__':
    f._expansion_invocations_cached

if __name__ == '__main__':
    print("%.2f%% of invocations can be cached" %
          (f._expansion_invocations_cached * 100 / f._expansion_invocations))

### Exercise 2: Grammar Pre-Compilation

if __name__ == '__main__':
    print('\n### Exercise 2: Grammar Pre-Compilation')



class EvenFasterGrammarFuzzer(GrammarFuzzer):
    """Variant of `GrammarFuzzer` with precomputed costs"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._symbol_costs: Dict[str, Union[int, float]] = {}
        self._expansion_costs: Dict[Expansion, Union[int, float]] = {}
        self.precompute_costs()

    def new_symbol_cost(self, symbol: str,
                        seen: Set[str] = set()) -> Union[int, float]:
        return self._symbol_costs[symbol]

    def new_expansion_cost(self, expansion: Expansion,
                           seen: Set[str] = set()) -> Union[int, float]:
        return self._expansion_costs[expansion]

    def precompute_costs(self) -> None:
        for symbol in self.grammar:
            self._symbol_costs[symbol] = super().symbol_cost(symbol)
            for expansion in self.grammar[symbol]:
                self._expansion_costs[expansion] = \
                    super().expansion_cost(expansion)

        # Make sure we now call the caching methods
        self.symbol_cost = self.new_symbol_cost  # type: ignore
        self.expansion_cost = self.new_expansion_cost  # type: ignore

if __name__ == '__main__':
    f = EvenFasterGrammarFuzzer(EXPR_GRAMMAR)

if __name__ == '__main__':
    f._symbol_costs

if __name__ == '__main__':
    f._expansion_costs

if __name__ == '__main__':
    f = EvenFasterGrammarFuzzer(EXPR_GRAMMAR)
    f.fuzz()

### Exercise 3: Maintaining Trees to be Expanded

if __name__ == '__main__':
    print('\n### Exercise 3: Maintaining Trees to be Expanded')



### Exercise 4: Alternate Random Expansions

if __name__ == '__main__':
    print('\n### Exercise 4: Alternate Random Expansions')



class ExerciseGrammarFuzzer(GrammarFuzzer):
    def expand_node_randomly(self, node: DerivationTree) -> DerivationTree:
        if self.log:
            print("Expanding", all_terminals(node), "randomly by cost")

        return self.expand_node_by_cost(node, random.choice)
