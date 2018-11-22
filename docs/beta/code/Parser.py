#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Parser.html
# Last change: 2018-11-21 06:05:31-08:00
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


# # Parsing and Recombining Inputs

if __name__ == "__main__":
    print('# Parsing and Recombining Inputs')




import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from Grammars import EXPR_GRAMMAR, START_SYMBOL, RE_NONTERMINAL, is_valid_grammar
else:
    from .Grammars import EXPR_GRAMMAR, START_SYMBOL, RE_NONTERMINAL, is_valid_grammar

from Fuzzer import Fuzzer
from GrammarFuzzer import GrammarFuzzer
from ExpectError import ExpectError

from IPython.display import display

import re
from graphviz import Digraph


def annotated_symbol(s, a):
    return re.sub(r'([^a-zA-Z0-9" ])', r"\\\1", s) + (" (%s)" % a if a else '')


def annotated_node(node, id):
    symbol, children, *annotation = node
    return symbol, children, ''.join(str(a) for a in annotation)


def display_tree(derivation_tree,
                           annotated_node=annotated_node,
                           annotate=annotated_symbol):
    counter = 0

    def traverse_tree(dot, tree, id=0):
        (symbol, children, annotation) = annotated_node(tree, id)
        dot.node(repr(id), annotate(symbol, annotation))

        if children is not None:
            for child in children:
                nonlocal counter
                counter += 1
                child_id = counter
                dot.edge(repr(id), repr(child_id))
                traverse_tree(dot, child, child_id)

    dot = Digraph(comment="Derivation Tree")
    dot.attr('node', shape='plain')
    traverse_tree(dot, derivation_tree)
    display(dot)
    
def all_terminals(tree, grammar=None):
    symbol, children, *_ = tree
    if children:
        return ''.join(all_terminals(c, grammar) for c in children)
    else:
        if grammar is not None:
             return '' if symbol in grammar else symbol
        else:
            return symbol

if __name__ == "__main__":
    mystring = '1+2'


# ## Grammars

if __name__ == "__main__":
    print('\n## Grammars')




A1_GRAMMAR = {
    "<start>": ["<expr>"],
    "<expr>": ["<expr>+<expr>", "<expr>-<expr>", "<integer>"],
    "<integer>": ["<digit><integer>", "<digit>"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

if __name__ == "__main__":
    tree = ('<start>', [('<expr>',
                         [('<expr>', [('<integer>', [('<digit>', [('1', [])])])]),
                          ('+', []),
                          ('<expr>', [('<integer>', [('<digit>', [('2',
                                                                   [])])])])])])
    assert mystring == all_terminals(tree)
    display_tree(tree)


A2_GRAMMAR = {
    "<start>": ["<expr>"],
    "<expr>": ["<integer><expr_>"],
    "<expr_>": ["+<expr>", "-<expr>", ""],
    "<integer>": ["<digit><integer_>"],
    "<integer_>": ["<integer>", ""],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

if __name__ == "__main__":
    tree = ('<start>', [('<expr>', [('<integer>', [('<digit>', [('1', [])]),
                                                   ('<integer_>', [('', [])])]),
                                    ('<expr_>', [('+', []),
                                                 ('<expr>',
                                                  [('<integer>',
                                                    [('<digit>', [('2', [])]),
                                                     ('<integer_>', [('', [])])]),
                                                   ('<expr_>', [('', [])])])])])])
    assert mystring == all_terminals(tree)
    display_tree(tree)


# #### Recursion

if __name__ == "__main__":
    print('\n#### Recursion')




# #### Ambiguity

if __name__ == "__main__":
    print('\n#### Ambiguity')




if __name__ == "__main__":
    mystring = '1+2+3'
    tree = ('<start>',
            [('<expr>',
              [('<expr>', [('<expr>', [('<integer>', [('<digit>', [('1', [])])])]),
                           ('+', []),
                           ('<expr>', [('<integer>',
                                        [('<digit>', [('2', [])])])])]), ('+', []),
               ('<expr>', [('<integer>', [('<digit>', [('3', [])])])])])])
    assert mystring == all_terminals(tree)
    display_tree(tree)


if __name__ == "__main__":
    tree = ('<start>',
            [('<expr>', [('<expr>', [('<integer>', [('<digit>', [('1', [])])])]),
                         ('+', []),
                         ('<expr>',
                          [('<expr>', [('<integer>', [('<digit>', [('2', [])])])]),
                           ('+', []),
                           ('<expr>', [('<integer>', [('<digit>', [('3',
                                                                    [])])])])])])])
    assert all_terminals(tree) == mystring
    display_tree(tree)


class Parser(object):
    def __init__(self, grammar, **kwargs):
        self._grammar = grammar
        self.start_symbol=kwargs.get('start_symbol') or START_SYMBOL 
        self.log = kwargs.get('log') or False
        self.tokens = kwargs.get('tokens') or set()

    def grammar(self):
        return self._grammar

    def parse_prefix(self, text):
        """Return pair (cursor, forest) for longest prefix of text"""
        raise NotImplemented()

    def parse(self, text):
        cursor, forest = self.parse_prefix(text)
        if cursor < len(text):
            raise SyntaxError("at " + repr(text[cursor:]))
        return [self.prune_tree(tree) for tree in forest]

    def prune_tree(self, tree):
        name, children = tree
        if name in self.tokens:
            return (name, [(all_terminals(tree), [])])
        else:
            return (name, [self.prune_tree(c) for c in children]) 

# ## Parsing Expression Grammars

if __name__ == "__main__":
    print('\n## Parsing Expression Grammars')




PEG1 = {
    '<start>': ['a','b']
}

PEG2 = {
    '<start>': ['ab','abc']
}

# ### Packrat Parser for _PEGs_

if __name__ == "__main__":
    print('\n### Packrat Parser for _PEGs_')




from functools import reduce, lru_cache

def canonical(grammar, letters=False):
    def split(rule):
        return [token for token in re.split(RE_NONTERMINAL, rule) if token]

    def tokenize(word):
        return list(word) if letters else [word]

    def canonical_expr(expression):
        return [
            token for word in split(expression)
            for token in ([word] if word in grammar else tokenize(word))
        ]

    return {
        k: [canonical_expr(expression) for expression in alternatives]
        for k, alternatives in grammar.items()
    }

if __name__ == "__main__":
    canonical(EXPR_GRAMMAR)


def pp_grammar(grammar):
    def show_symbol(s):
        return s if s in grammar else "'%s'" % s

    def show_alternative(alt):
        return " + ".join(show_symbol(symbol) for symbol in alt)

    def show_alternative_set(alts):
        return "\n\t| ".join([show_alternative(alt) for alt in alts])

    for key in grammar:
        print("%s = %s" % (key, show_alternative_set(grammar[key])))

if __name__ == "__main__":
    pp_grammar(canonical(EXPR_GRAMMAR))


class Parser(Parser):
    def __init__(self, grammar, **kwargs):
        self._grammar = grammar
        self.start_symbol=kwargs.get('start_symbol') or START_SYMBOL 
        self.log = kwargs.get('log') or False
        self.tokens = kwargs.get('tokens') or set()        
        self.cgrammar = canonical(grammar)

# #### The Parser

if __name__ == "__main__":
    print('\n#### The Parser')




class PEGParser(Parser):
    def parse_prefix(self, text):
        cursor, tree = self.unify_key(self.start_symbol, text, 0)
        return cursor, [tree]

# ##### Unify Key

if __name__ == "__main__":
    print('\n##### Unify Key')




class PEGParser(PEGParser):
    def unify_key(self, key, text, at=0):
        if key not in self.cgrammar:
            if text[at:].startswith(key):
                return at + len(key), (key, [])
            else:
                return at, None
        for rule in self.cgrammar[key]:
            to, res = self.unify_rule(rule, text, at)
            if res:
                return (to, (key, res))
        return 0, None

# ##### Unify Rule

if __name__ == "__main__":
    print('\n##### Unify Rule')




class PEGParser(PEGParser):
    def unify_rule(self, rule, text, at):
        results = []
        for token in rule:
            at, res = self.unify_key(token, text, at)
            if res is None:
                return at, None
            results.append(res)
        return at, results

class PEGParser(PEGParser):
    @lru_cache(maxsize=None)
    def unify_key(self, key, text, at=0):
        if key not in self.cgrammar:
            if text[at:].startswith(key): return at + len(key), (key, [])
            else: return at, None
        for rule in self.cgrammar[key]:
            to, res = self.unify_rule(rule, text, at)
            if res: return (to, (key, res))
        return 0, None

if __name__ == "__main__":
    mystring = "1 + (2 * 3)"
    peg = PEGParser(EXPR_GRAMMAR)
    for tree in peg.parse(mystring):
        assert all_terminals(tree) == mystring
        display_tree(tree)


if __name__ == "__main__":
    mystring = "1 * (2 + 3.35)"
    for tree in peg.parse(mystring):
        assert all_terminals(tree) == mystring
        display_tree(tree)


# ### Recombining Parsed Inputs

if __name__ == "__main__":
    print('\n### Recombining Parsed Inputs')




# #### A Simple Fuzzer

if __name__ == "__main__":
    print('\n#### A Simple Fuzzer')




import string
VAR_GRAMMAR = {
    '<start>': ['<statements>'],
    '<statements>': ['<statement>;<statements>', '<statement>'],
    '<statement>': ['<declaration>', '<assignment>'],
    '<declaration>': ['<def> <identifier>'],
    '<assignment>': ['<identifier>=<expr>'],
    '<def>': ['def'],
    '<identifier>': ['<word>'],
    '<word>': ['<alpha><word>', '<alpha>'],
    '<alpha>':
    list(string.ascii_letters),
    '<expr>': ['<term>+<expr>', '<term>-<expr>', '<term>'],
    '<term>': ['<factor>*<term>', '<factor>/<term>', '<factor>'],
    '<factor>':
    ['+<factor>', '-<factor>', '(<expr>)', '<identifier>', '<number>'],
    '<number>': ['<integer>.<integer>', '<integer>'],
    '<integer>': ['<digit><integer>', '<digit>'],
    '<digit>':
    list(string.digits),
}

VAR_TOKENS = {'<def>', '<number>', '<identifier>'}

if __name__ == "__main__":
    mystring = 'def avar;def bvar;avar=1.3;bvar=avar-3*(4+300)'
    parser = PEGParser(VAR_GRAMMAR, tokens=VAR_TOKENS)
    for tree in parser.parse(mystring):
        display_tree(tree)


if __name__ == "__main__":
    mystrings = [
        'def abc;abc=12+(3+3.3)',
        'def a;def b;def c;a=1;b=2;c=a+b',
        'def avar;def bvar;avar=1.3;bvar=avar-3*(4+300)',
        'def a;def b;a=1.3;b=a-1*(4+3+(2/a))',
        'def a;def b;def c;def d;a=10;b=20;c=34;d=-b+(b*b-4*a*c)/(2*a)',
        'def x;def y;def z;x=10;y=20;z=(x+y)*(x-y)',
        'def x;def y;def z;x=23;y=51;z=x*x-y*y',
    ]


class LangFuzzer(Fuzzer):
    def __init__(self, parser):
        self.parser = parser
        self.fragments = {k: [] for k in self.parser.cgrammar}

    def traverse_tree(self, node):
        counter = 1
        nodes = {}

        def helper(node, id):
            nonlocal counter
            name, children = node
            new_children = []
            nodes[id] = node
            for child in children:
                counter += 1
                new_children.append(helper(child, counter))
            return name, new_children, id

        return helper(node, counter), nodes

    def fragment(self, strings):
        self.trees = []
        for string in strings:
            for tree in self.parser.parse(string):
                tree, nodes = self.traverse_tree(tree)
                self.trees.append((tree, nodes))
                for node in nodes:
                    symbol = nodes[node][0]
                    if symbol in self.fragments:
                        self.fragments[symbol].append(nodes[node])
        return self.fragments

if __name__ == "__main__":
    lf = LangFuzzer(PEGParser(VAR_GRAMMAR, tokens=VAR_TOKENS))
    fragments = lf.fragment(mystrings)
    for key in fragments:
        print("%s: %d" % (key, len(fragments[key])))


import random


class LangFuzzer(LangFuzzer):
    def __init__(self, parser, strings):
        self.parser = parser
        self.fragments = {k: [] for k in self.parser.cgrammar}
        self.fragment(strings)
    
    def generate_new_tree(self, node, choice):
        name, children, id = node
        if id == choice:
            return random.choice(self.fragments[name])
        else:
            return (name, [self.generate_new_tree(c, choice) for c in children])
        
    def candidate(self):
        tree, nodes = random.choice(self.trees)
        interesting_nodes = [
            n for n in nodes if nodes[n][0] in self.fragments
            and len(self.fragments[nodes[n][0]]) > 1
        ]
        node = random.choice(interesting_nodes)
        return tree, node
    
    def fuzz(self):
        tree, node = self.candidate()
        modified = self.generate_new_tree(tree, node)
        return all_terminals(modified)

if __name__ == "__main__":
    lf = LangFuzzer(PEGParser(VAR_GRAMMAR, tokens=VAR_TOKENS), mystrings)
    for i in range(100):
        print(lf.fuzz())


# ###  Problems with PEG

if __name__ == "__main__":
    print('\n###  Problems with PEG')




PEG_SURPRISE = {
    "<A>": ["a<A>a", "aa"]
}

if __name__ == "__main__":
    strings = []
    for e in range(4):
        f = GrammarFuzzer(PEG_SURPRISE, '<A>')
        tree = ('<A>', None)
        for _ in range(e):
            tree = f.expand_tree_once(tree)
        tree = f.expand_tree_with_strategy(tree, f.expand_node_min_cost)
        strings.append(all_terminals(tree))
        display_tree(tree)
    strings


if __name__ == "__main__":
    peg = PEGParser(PEG_SURPRISE, start_symbol='<A>')
    for s in strings:
        with ExpectError():
            for tree in peg.parse(s):
                display_tree(tree)
            print(s)


# ## Context Free Grammars

if __name__ == "__main__":
    print('\n## Context Free Grammars')




def rules(grammar):
    return [(key, choice)
            for key, choices in grammar.items()
            for choice in choices]

EXPR_GRAMMAR_NS = {}
for key, alts in canonical(EXPR_GRAMMAR).items():
    EXPR_GRAMMAR_NS[key] = [''.join(sym.strip() for sym in alt) for alt in alts]

if __name__ == "__main__":
    rules(EXPR_GRAMMAR_NS)


def terminals(grammar):
    return set(token
               for key, choice in rules(grammar)
               for token in choice if token not in grammar)

if __name__ == "__main__":
    terminals(canonical(EXPR_GRAMMAR_NS))


if __name__ == "__main__":
    pp_grammar(canonical(EXPR_GRAMMAR_NS))


# ### Earley Parser

if __name__ == "__main__":
    print('\n### Earley Parser')




# #### Columns

if __name__ == "__main__":
    print('\n#### Columns')




class Column(object):
    def __init__(self, index, letter):
        self.index, self.letter = index, letter
        self.states, self._unique = [], {}

    def __str__(self):
        return "%s chart[%d]\n%s" % (self.letter, self.index, "\n".join(
            str(state) for state in self.states if state.finished()))

class Column(Column):
    def add(self, state):
        if state in self._unique:
            return self._unique[state]
        self._unique[state] = state
        self.states.append(state)
        state.e_col = self
        return self._unique[state]

# #### Item

if __name__ == "__main__":
    print('\n#### Item')




class Item(object):
    def __init__(self, name, expr, dot):
        self.name, self.expr, self.dot = name, expr, dot

class Item(Item):
    def finished(self):
        return self.dot >= len(self.expr)

    def advance(self):
        return Item(self.name, self.expr, self.dot + 1)

    def at_dot(self):
        return self.expr[self.dot] if self.dot < len(self.expr) else None

# #### States

if __name__ == "__main__":
    print('\n#### States')




class State(Item):
    def __init__(self, name, expr, dot, s_col):
        super().__init__(name, expr, dot)
        self.s_col, self.e_col = s_col, None

    def __str__(self):
        return self.name + ':= ' + ' '.join([
            str(p)
            for p in [*self.expr[:self.dot], '|', *self.expr[self.dot:]]
        ]) + "(%d,%d)" % (self.s_col.index, self.e_col.index)

    def _t(self):
        return (self.name, self.expr, self.dot, self.s_col.index)

    def __hash__(self):
        return hash(self._t())

    def __eq__(self, other):
        return self._t() == other._t()

    def advance(self):
        return State(self.name, self.expr, self.dot + 1, self.s_col)

# #### The Parser

if __name__ == "__main__":
    print('\n#### The Parser')




class EarleyParser(Parser):
    def __init__(self, grammar, **kwargs):
        super().__init__(grammar, **kwargs)
        self.cgrammar = canonical(grammar, letters=True)

class EarleyParser(EarleyParser):
    def chart_parse(self, words, start):
        alt = tuple(*self.cgrammar[start])
        chart = [Column(i, tok) for i, tok in enumerate([None, *words])]
        chart[0].add(State(start, alt, 0, chart[0]))
        return self.fill_chart(chart)

# ##### Predict

if __name__ == "__main__":
    print('\n##### Predict')




class EarleyParser(EarleyParser):
    def predict(self, col, sym, state):
        for alt in self.cgrammar[sym]:
            col.add(State(sym, tuple(alt), 0, col))

# ##### Scan

if __name__ == "__main__":
    print('\n##### Scan')




class EarleyParser(EarleyParser):
    def scan(self, col, state, letter):
        if letter == col.letter:
            col.add(state.advance())

# ##### Complete

if __name__ == "__main__":
    print('\n##### Complete')




class EarleyParser(EarleyParser):
    def complete(self, col, state):
        return self.earley_complete(col, state)

    def earley_complete(self, col, state):
        parent_states = [
            st for st in state.s_col.states if st.at_dot() == state.name
        ]
        for st in parent_states:
            col.add(st.advance())

# ##### Fill chart

if __name__ == "__main__":
    print('\n##### Fill chart')




class EarleyParser(EarleyParser):
    def fill_chart(self, chart):
        for i, col in enumerate(chart):
            for state in col.states:
                if state.finished():
                    self.complete(col, state)
                else:
                    sym = state.at_dot()
                    if sym in self.cgrammar:
                        self.predict(col, sym, state)
                    else:
                        if i + 1 >= len(chart):
                            continue
                        self.scan(chart[i + 1], state, sym)
            if self.log:
                print(col)
        return chart

# ##### Parse

if __name__ == "__main__":
    print('\n##### Parse')




class EarleyParser(EarleyParser):
    def parse_prefix(self, text):
        table = self.chart_parse(text, self.start_symbol)
        for col in reversed(table):
            states = [st for st in col.states if st.name == self.start_symbol]
            if states:
                return col.index, states
        return -1, []

class EarleyParser(EarleyParser):
    def reverse(self, table):
        f_table = [Column(c.index, c.letter) for c in table]
        for col in table:
            finished = [s for s in col.states if s.finished()]
            for s in finished:
                f_table[s.s_col.index].states.append(s)
        return f_table

class EarleyParser(EarleyParser):
    def parse(self, text):
        cursor, states = self.parse_prefix(text)
        if cursor != len(text):
            return []
        table = self.chart_parse(text, self.start_symbol)
        f_table = self.reverse(table)
        start = next(s for s in states if s.finished())
        return self.extract_trees(self.parse_forest(f_table, start))

# ##### Parse Forests

if __name__ == "__main__":
    print('\n##### Parse Forests')




class EarleyParser(EarleyParser):
    def parse_forest(self, chart, state):
        if not state.expr:
            return (state.name, [])
        pathexprs = self.parse_paths(state.expr, chart, state.s_col.index,
                                     state.e_col.index)
        paths_ = []
        for pathexpr in pathexprs:
            pathexpr_ = []
            for varexpr in pathexpr:
                completion = (self.parse_forest(chart, varexpr) if isinstance(
                    varexpr, State) else (varexpr, []))
                pathexpr_.append(completion)
            paths_.append(pathexpr_)
        return (state.name, paths_)

# ##### Parse Paths

if __name__ == "__main__":
    print('\n##### Parse Paths')




class EarleyParser(EarleyParser):
    def parse_paths(self, named_expr, chart, frm, til):
        var, *expr = named_expr
        starts = None
        if var not in self.cgrammar:
            starts = ([(var, frm + len(var))]
                      if frm < til and chart[frm + 1].letter == var else [])
        else:
            starts = [(s, s.e_col.index) for s in chart[frm].states
                      if s.name == var]

        paths = []
        for state, start in starts:
            if not expr:
                paths.extend([[state]] if start == til else [])
            else:
                res = self.parse_paths(expr, chart, start, til)
                paths.extend([[state] + r for r in res])
        return paths

# ##### extract_a_tree

if __name__ == "__main__":
    print('\n##### extract_a_tree')




class EarleyParser(EarleyParser):
    def extract_a_tree(self, forest_node):
        name, paths = forest_node
        if not paths:
            return (name, [])
        return (name, [self.extract_a_tree(p) for p in paths[0]])

    def extract_trees(self, forest):
        return [self.extract_a_tree(forest)]

A3_GRAMMAR = {
    "<start>": ["<expr>"],
    "<expr>": ["<expr>+<expr>", "<expr>-<expr>", "(<expr>)", "<integer>"],
    "<integer>": ["<digit><integer>", "<digit>"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

if __name__ == "__main__":
    mystring = '(1+24)-33'
    parser = EarleyParser(A3_GRAMMAR)
    for tree in parser.parse(mystring):
        assert all_terminals(tree) == mystring
        display_tree(tree)


# #### Ambiguous parsing

if __name__ == "__main__":
    print('\n#### Ambiguous parsing')




# ##### extract_trees

if __name__ == "__main__":
    print('\n##### extract_trees')




class EarleyParser(EarleyParser):
    def extract_trees(self, forest_node):
        name, paths = forest_node
        if not paths:
            return [(name, [])]
        results = []
        for path in paths:
            ptrees = zip(*[self.extract_trees(p) for p in path])
            results.extend([(name, p) for p in ptrees])
        return results

if __name__ == "__main__":
    mystring = '12+23-34'
    parser = EarleyParser(A1_GRAMMAR)
    for tree in parser.parse(mystring):
        assert mystring == all_terminals(tree)
        display_tree(tree)


if __name__ == "__main__":
    gf = GrammarFuzzer(A1_GRAMMAR)
    for i in range(5):
        s = gf.fuzz()
        print(i, s)
        for tree in parser.parse(s):
            assert all_terminals(tree, A1_GRAMMAR) == s


# #### The Aycock Epsilon fix

if __name__ == "__main__":
    print('\n#### The Aycock Epsilon fix')




E_GRAMMAR_1 = {
    '<start>': ['<A>', '<B>'],
    '<A>': ['a', ''],
    '<B>': ['b']
}

EPSILON = ''
E_GRAMMAR = {
        '<start>': ['<S>'],
        '<S>': ['<A><A><A><A>'],
        '<A>': ['a', '<E>'],
        '<E>': [EPSILON]
}

if __name__ == "__main__":
    mystring = 'a'
    parser = EarleyParser(E_GRAMMAR)
    trees = parser.parse(mystring)
    print(trees)


# ##### Fixpoint

if __name__ == "__main__":
    print('\n##### Fixpoint')




def fixpoint(f):
    def helper(arg):
        while True:
            sarg = str(arg)
            arg_ = f(arg)
            if str(arg_) == sarg:
                return arg
            arg = arg_

    return helper

def my_sqrt(x):
    @fixpoint
    def _my_sqrt(approx):
        return (approx + x / approx) / 2

    return _my_sqrt(1)

if __name__ == "__main__":
    my_sqrt(2)


# ##### Nullable

if __name__ == "__main__":
    print('\n##### Nullable')




def nullable_expr(expr, nullables):
    return all(token in nullables for token in expr)


def nullable(grammar):
    productions = rules(grammar)

    @fixpoint
    def nullable_(nullables):
        for A, expr in productions:
            if nullable_expr(expr, nullables):
                nullables |= {A}
        return (nullables)

    return nullable_({EPSILON})

if __name__ == "__main__":
    for key, grammar in {
            'E_GRAMMAR': E_GRAMMAR,
            'E_GRAMMAR_1': E_GRAMMAR_1
    }.items():
        print(key, nullable(canonical(grammar)))


class EarleyParser(EarleyParser):
    def __init__(self, grammar, **kwargs):
        super().__init__(grammar, **kwargs)
        self.cgrammar = canonical(grammar, letters=True)
        self.epsilon = nullable(self.cgrammar)

    def predict(self, col, sym, state):
        for alt in self.cgrammar[sym]:
            col.add(State(sym, tuple(alt), 0, col))
        if sym in self.epsilon:
            col.add(state.advance())

if __name__ == "__main__":
    mystring = 'a'
    parser = EarleyParser(E_GRAMMAR)
    for tree in parser.parse(mystring):
        display_tree(tree)


# #### More Earley parsing

if __name__ == "__main__":
    print('\n#### More Earley parsing')




# ## Testing the parsers

if __name__ == "__main__":
    print('\n## Testing the parsers')




def prod_line_grammar(nt, t):
    g = {
        '<start>': ['<SYMBOLS>'],
        '<SYMBOLS>': ['<SYMBOL><SYMBOLS>', '<SYMBOL>'],
        '<SYMBOL>': ['<NT>', '<T>'],
        '<NT>': ['<NT_><ALPHA><_NT>'],
        '<NT_>': ['<'],
        '<_NT>': ['>'],
        '<ALPHA>': nt,
        '<T>': t
    }
    if not nt:
        g['<NT>'] = ['']
    return g


def make_alt(nt, t, num_alts):
    prod_grammar = prod_line_grammar(nt, t)
    gf = GrammarFuzzer(prod_grammar, min_nonterminals=3, max_nonterminals=5)
    name = "<%s>" % ''.join(random.choices(string.ascii_uppercase, k=3))
    return (name, [gf.fuzz() for _ in range(num_alts)])

def make_grammar():
    a = list(string.ascii_lowercase)
    grammar = {}
    name = None
    for _ in range(2):
        name, rules = make_alt([k[1:-1] for k in grammar.keys()], a, 3)
        grammar[name] = rules
    grammar[START_SYMBOL] = [name]
    return grammar

if __name__ == "__main__":
    for i in range(5):
        my_grammar = make_grammar()
        pp_grammar(canonical(my_grammar))
        parser = EarleyParser(my_grammar)
        mygf = GrammarFuzzer(my_grammar)
        s = mygf.fuzz()
        print(s)
        for tree in parser.parse(s):
            assert all_terminals(tree) == s
            display_tree(tree)


# ## Further Information

if __name__ == "__main__":
    print('\n## Further Information')




# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1 An alternative _Packrat_

if __name__ == "__main__":
    print('\n### Exercise 1 An alternative _Packrat_')




class PackratParser(Parser):
    def parse_prefix(self, text):
        txt, res = self.unify_key(self.start_symbol, text)
        return len(txt), [res]

    def parse(self, text):
        remain, res = self.parse_prefix(text)
        if remain:
            raise SyntaxError("at " + res)
        return res

    def unify_rule(self, rule, text):
        results = []
        for token in rule:
            text, res = self.unify_key(token, text)
            if res is None:
                return text, None
            results.append(res)
        return text, results

    def unify_key(self, key, text):
        if key not in self.cgrammar:
            if text.startswith(key):
                return text[len(key):], (key, [])
            else:
                return text, None
        for rule in self.cgrammar[key]:
            text_, res = self.unify_rule(rule, text)
            if res:
                return (text_, (key, res))
        return text, None

if __name__ == "__main__":
    mystring = "1+(2*3)"
    for tree in PackratParser(EXPR_GRAMMAR_NS).parse(mystring):
        assert all_terminals(tree) == mystring
        display_tree(tree)


# ### Exercise 2 _More PEG Syntax_

if __name__ == "__main__":
    print('\n### Exercise 2 _More PEG Syntax_')




# ### Exercise 3 _PEG Predicates_

if __name__ == "__main__":
    print('\n### Exercise 3 _PEG Predicates_')




# ### Exercise 4 _Earley Fill Chart_

if __name__ == "__main__":
    print('\n### Exercise 4 _Earley Fill Chart_')




# ### Exercise 5 _Leo Parser_

if __name__ == "__main__":
    print('\n### Exercise 5 _Leo Parser_')




LR_GRAMMAR = {
    '<start>': ['<A>'],
    '<A>': ['<A>a', ''],
}

RR_GRAMMAR = {
    '<start>': ['<A>'],
    '<A>': ['a<A>', ''],
}

if __name__ == "__main__":
    mystring = 'aaaaaa'
    result = EarleyParser(LR_GRAMMAR, log=True).parse(mystring)


if __name__ == "__main__":
    result = EarleyParser(RR_GRAMMAR, log=True).parse(mystring)


class State(State):
    def __init__(self, name, expr, dot, s_col, tag=None):
        super().__init__(name, expr, dot, s_col)
        self.tag = tag

    def copy(self, tag=None):
        return State(self.name, self.expr, self.dot, self.s_col, tag)

    def __str__(self):
        init = "%s %s" % (self.tag or "   ", self.name)
        return init + ':= ' + ' '.join([
            str(p)
            for p in [*self.expr[:self.dot], '|', *self.expr[self.dot:]]
        ]) + "(%d,%d)" % (self.s_col.index, self.e_col.index)


class LeoParser(EarleyParser):
    def complete(self, col, state):
        return self.leo_complete(col, state)

    def leo_complete(self, col, state):
        detred = self.deterministic_reduction(state)
        if detred:
            col.add(detred.copy())
        else:
            self.earley_complete(col, state)

def splitlst(predicate, iterable):
    return reduce(lambda res, e: res[predicate(e)].append(e) or res, iterable,
                  ([], []))


class LeoParser(LeoParser):
    def check_single_item(self, st, remain):
        res = [
            s for s in remain if s.name == st.name and s.expr == st.expr
            and s.s_col.index == st.s_col.index and s.dot == (st.dot - 1)
        ]
        return len(res) == 1

    @lru_cache(maxsize=None)
    def get_above(self, state):
        remain, finished = splitlst(lambda s: s.finished(), state.s_col.states)
        res = [
            st for st in finished
            if len(st.expr) > 1 and state.name == st.expr[-1]
        ]
        vals = [st for st in res if self.check_single_item(st, remain)]
        if vals:
            assert len(vals) == 1
            return vals[0]
        return None

    def deterministic_reduction(self, state):
        st = state
        while True:
            _st = self.get_above(st)
            if not _st:
                break
            st = _st
        return st if st != state else None

    def complete(self, col, state):
        return self.leo_complete(col, state)

    def leo_complete(self, col, state):
        detred = self.deterministic_reduction(state)
        if detred:
            col.add(detred.copy(state.name))
        else:
            self.earley_complete(col, state)

if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR, log=True).parse(mystring)


if __name__ == "__main__":
    result = LeoParser(LR_GRAMMAR, log=True).parse(mystring)
    for tree in result:
        print(all_terminals(tree, grammar=LR_GRAMMAR))


RR_GRAMMAR2 = {
    '<start>': ['<A>'],
    '<A>': ['ab<A>', ''],
}
mystring2 = 'abababab'

RR_GRAMMAR3 = {
    '<start>': ['<A>'],
    '<A>': ['ab<B>', ''],
    '<B>': ['<A>'],
}
mystring3 = 'abababab'

class Tagged:
    def __init__(self, tbl):
        self.col, self.tbl = [{} for _ in tbl], tbl

    @lru_cache(maxsize=None)
    def get(self, frm, var):
        if frm == -1:
            return []

        def filter_states(ends):
            lst = []
            for (state, e) in ends:
                if e > frm and state.name == var:
                    sc = state.copy()
                    sc.s_col, sc.e_col = self.tbl[frm], self.tbl[e]
                    lst.append((sc, e))
            return lst

        lst = filter_states(self.get(frm - 1, var))
        st_dict = self.col[frm]
        ends = [(state, s) for state in st_dict for s in st_dict[state]
                if s > frm]
        return lst + filter_states(ends)


class LeoParser(LeoParser):
    def parse(self, text):
        cursor, states = self.parse_prefix(text)
        if cursor != len(text):
            return []
        table = self.chart_parse(text, self.start_symbol)
        f_table = self.reverse(table)

        self.tagged_array = Tagged(f_table)
        for i, col in enumerate(f_table):
            tcol = self.tagged_array.col[i]
            for state in col.states:
                if state.tag:
                    if state not in tcol:
                        tcol[state] = set()
                    tcol[state].add(state.e_col.index)

        start = next(s for s in states if s.finished())
        return self.extract_trees(self.parse_forest(f_table, start))

    def parse_paths(self, expr_, chart, frm, til):
        var, *expr = expr_
        ends = None
        if var not in self.cgrammar:
            ends = ([(var, frm + len(var))]
                    if frm < til and chart[frm + 1].letter == var else [])
        else:
            tagged_ends = self.tagged_array.get(frm, var)

            ends = [(s, s.e_col.index) for s in chart[frm].states
                    if s.name == var and not s.tag] + tagged_ends

        paths = []
        for state, end in ends:
            if not expr:
                paths.extend([[state]] if end == til else [])
            else:
                res = self.parse_paths(expr, chart, end, til)
                paths.extend([[state] + r for r in res])
        return paths

if __name__ == "__main__":
    p = LeoParser(RR_GRAMMAR)
    for tree in p.parse(mystring):
        assert all_terminals(tree, RR_GRAMMAR) == mystring
        display_tree(tree)


if __name__ == "__main__":
    p = LeoParser(RR_GRAMMAR2)
    for tree in p.parse(mystring2):
        assert all_terminals(tree, RR_GRAMMAR2) == mystring2
        display_tree(tree)


# ### Exercise 6 _First set of a nonterminal_

if __name__ == "__main__":
    print('\n### Exercise 6 _First set of a nonterminal_')




def firstset(grammar, nullable):
    first = {i: {i} for i in terminals(grammar)}
    for k in grammar:
        first[k] = {EPSILON} if k in nullable else set()
    return firstset_((rules(grammar), first, nullable))[1]

def first_expr(expr, first, nullable):
    tokens = set()
    for token in expr:
        tokens |= first[token]
        if token not in nullable:
            break
    return tokens


@fixpoint
def firstset_(arg):
    (rules, first, epsilon) = arg
    for A, expression in rules:
        first[A] |= first_expr(expression, first, epsilon)
    return (rules, first, epsilon)

if __name__ == "__main__":
    firstset(canonical(EXPR_GRAMMAR_NS), EPSILON)


# ### Exercise 7 _Follow set of a nonterminal_

if __name__ == "__main__":
    print('\n### Exercise 7 _Follow set of a nonterminal_')




EOF = '\0'


def followset(grammar, start):
    follow = {i: set() for i in grammar}
    follow[start] = {EOF}

    epsilon = nullable(grammar)
    first = firstset(grammar, epsilon)
    return followset_((grammar, epsilon, first, follow))[-1]

@fixpoint
def followset_(arg):
    grammar, epsilon, first, follow = arg
    for A, expression in rules(grammar):
        f_B = follow[A]
        for t in reversed(expression):
            if t in grammar:
                follow[t] |= f_B
            f_B = f_B | first[t] if t in epsilon else (first[t] - {EPSILON})

    return (grammar, epsilon, first, follow)

if __name__ == "__main__":
    followset(canonical(A1_GRAMMAR), START_SYMBOL)


# ### Exercise 8 _LL(1) parse table_

if __name__ == "__main__":
    print('\n### Exercise 8 _LL(1) parse table_')




class LL1Parser(Parser):
    def parse_table(self):
        self.my_rules = rules(self.cgrammar)
        # .. fill in here to produce
        # self.table = ...
    
    def rules(self):
        for i, rule in enumerate(self.my_rules):
            print(i, rule)
            
    def show_table(self):
        ts = list(sorted(terminals(self.cgrammar)))
        print('Rule Name\t| %s' % ' | '.join(t for t in ts))
        for k in self.table:
            pr = self.table[k]
            actions = list(str(pr[t]) if t in pr else ' ' for t in ts)
            print('%s  \t| %s' % (k, ' | '.join(actions)))

if __name__ == "__main__":
    for i, r in enumerate(rules(canonical(A2_GRAMMAR))):
        print("%d\t %s := %s" %(i, r[0], r[1]))


class LL1Parser(LL1Parser):
    def predict(self, rulepair, first, follow, epsilon):
        A, rule = rulepair
        rf = first_expr(rule, first, epsilon)
        if nullable_expr(rule, epsilon):
            rf |= follow[A]
        return rf

    def parse_table(self):
        self.my_rules = rules(self.cgrammar)
        epsilon = nullable(self.cgrammar)
        first = firstset(self.cgrammar, epsilon)
        # inefficient, can combine the three.
        follow = followset(self.cgrammar, self.start_symbol)

        ptable = [(i, self.predict(rule, first, follow, epsilon))
                  for i,rule in enumerate(self.my_rules)]

        parse_tbl = {k: {} for k in self.cgrammar}

        for i, pvals in ptable:
            (k, expr) = self.my_rules[i]
            parse_tbl[k].update({v: i for v in pvals})

        self.table = parse_tbl

if __name__ == "__main__":
    ll1parser = LL1Parser(A2_GRAMMAR)
    ll1parser.parse_table()
    ll1parser.show_table()


# ### Exercise 9 _LL(1) parser_

if __name__ == "__main__":
    print('\n### Exercise 9 _LL(1) parser_')




class LL1Parser(LL1Parser):
    def parse_helper(self, stack, inplst):
        inp, *inplst = inplst
        exprs = []
        while stack:
            val, *stack = stack
            if isinstance(val, tuple):
                exprs.append(val)
            elif val not in self.cgrammar:  # terminal
                assert val == inp
                exprs.append(val)
                inp, *inplst = inplst or [None]
            else:
                if inp is not None:
                    i = self.table[val][inp]
                    _, rhs = self.my_rules[i]
                    stack = rhs + [(val, len(rhs))] + stack
        return self.linear_to_tree(exprs)

    def parse(self, inp):
        self.parse_table()
        k, _ = self.my_rules[0]
        stack = [k]
        return self.parse_helper(stack, inp)

    def linear_to_tree(self, arr):
        stack = []
        while arr:
            elt = arr.pop(0)
            if not isinstance(elt, tuple):
                stack.append((elt, []))
            else:
                # get the last n
                sym, n = elt
                elts = stack[-n:] if n > 0 else []
                stack = stack[0:len(stack) - n]
                stack.append((sym, elts))
        assert len(stack) == 1
        return stack[0]

if __name__ == "__main__":
    ll1parser = LL1Parser(A2_GRAMMAR)
    tree = ll1parser.parse('1+2')
    display_tree(tree)


# ### Exercise 10 A different LangFuzzer

if __name__ == "__main__":
    print('\n### Exercise 10 A different LangFuzzer')




class LangFuzzer2(LangFuzzer):
    def __init__(self, parser, strings):
        super().__init__(parser, strings)
        self.gfuzz = GrammarFuzzer(parser.grammar())

    def check_diversity(self, pool):
        return len(pool) > 10

    def candidate(self):
        tree, nodes = random.choice(self.trees)
        interesting_nodes = [
            n for n in nodes if nodes[n][0] in self.fragments
            and nodes[n][0] is not self.parser.start_symbol
            and len(self.fragments[nodes[n][0]]) > 0
        ]
        node = random.choice(interesting_nodes)
        return tree, node

    def generate_new_tree(self, node, choice):
        name, children, id = node
        if id == choice:
            pool = self.fragments[name]
            if self.check_diversity(pool):
                return random.choice(self.fragments[name])
            else:
                return None
        else:
            return (name,
                    [self.generate_new_tree(c, choice) for c in children])

    def fuzz(self):
        tree, node = self.candidate()
        tree_with_a_hole = self.generate_new_tree(tree, node)
        modified = self.gfuzz.expand_tree(tree_with_a_hole)
        return all_terminals(modified)

if __name__ == "__main__":
    parser = EarleyParser(VAR_GRAMMAR, tokens=VAR_TOKENS)
    lf = LangFuzzer2(parser, mystrings)
    for i in range(100):
        print(lf.fuzz())

