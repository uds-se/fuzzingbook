#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Parser.html
# Last change: 2018-11-20 09:07:25-08:00
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
    
def all_terminals(tree):
    symbol, children, *_ = tree
    return ''.join(all_terminals(c) for c in children) if children else symbol


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


PEG1 = {
    '<start>': ['a','b']
}

PEG2 = {
    '<start>': ['ab','abc']
}


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

def pp_grammar(grammar):
    def show_symbol(s):
        return s if s in grammar else "'%s'" % s

    def show_alternative(alt):
        return " + ".join(show_symbol(symbol) for symbol in alt)

    def show_alternative_set(alts):
        return "\n\t| ".join([show_alternative(alt) for alt in alts])

    for key in grammar:
        print("%s = %s" % (key, show_alternative_set(grammar[key])))


class Parser(Parser):
    def __init__(self, grammar, **kwargs):
        self._grammar = grammar
        self.start_symbol=kwargs.get('start_symbol') or START_SYMBOL 
        self.log = kwargs.get('log') or False
        self.tokens = kwargs.get('tokens') or set()        
        self.cgrammar = canonical(grammar)


class PEGParser(Parser):
    def parse_prefix(self, text):
        cursor, tree = self.unify_key(self.start_symbol, text, 0)
        return cursor, [tree]

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


def rules(grammar):
    return [(key, choice)
            for key, choices in grammar.items()
            for choice in choices]

EXPR_GRAMMAR_NS = {}
for key, alts in canonical(EXPR_GRAMMAR).items():
    EXPR_GRAMMAR_NS[key] = [''.join(sym.strip() for sym in alt) for alt in alts]

def terminals(grammar):
    return set(token
               for key, choice in rules(grammar)
               for token in choice if token not in grammar)


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

class State(Item):
    def __init__(self, name, expr, dot, s_col):
        super().__init__(name, expr, dot)
        self.s_col, self.e_col = s_col, None
        self.left, self.right = None, None

    def __str__(self):
        return self.name + ':= ' + ' '.join([
            str(p)
            for p in [*self.expr[:self.dot], '|', *self.expr[self.dot:]]
        ]) + "(%d,%d)" % (self.s_col.index, self.e_col.index)

    def __repr__(self): return str(self)

    def _t(self):
        return (self.name, self.expr, self.dot, self.s_col.index)

    def __hash__(self):
        return hash(self._t())

    def __eq__(self, other):
        return self._t() == other._t()

    def advance(self):
        return State(self.name, self.expr, self.dot + 1, self.s_col)

class NearleyParser(Parser):
    def __init__(self, grammar, **kwargs):
        super().__init__(grammar, **kwargs)
        self.cgrammar = canonical(grammar, letters=True)

class NearleyParser(NearleyParser):
    def chart_parse(self, words, start):
        alt = tuple(*self.cgrammar[start])
        chart = [Column(i, tok) for i, tok in enumerate([None, *words])]
        chart[0].add(State(start, alt, 0, chart[0]))
        return self.fill_chart(chart)

class NearleyParser(NearleyParser):
    def predict(self, col, sym):
        for alt in self.cgrammar[sym]:
            col.add(State(sym, tuple(alt), 0, col))

class NearleyParser(NearleyParser):
    def scan(self, col, state, letter):
        if letter == col.letter:
            col.add(state.advance())


class NearleyParser(NearleyParser):
    def add_derivation(self, item, left, right):
        if not (left and right): return

        if left.dot <= 1:
            left = left.right

        if not (item.left and item.right):
            item.left, item.right = left, right

        elif (item.right):
            if not (item.left == left and item.right == right):
                old = {'left':item.left, 'right':item.right, 'next':None}
                item.left = {'left':left, 'right':right, 'next':old}
                item.right = None
        else:
            d = item.left
            while d:
                if d['left'] == left and d['right'] == right: return
                d = d.next
            item.left = {'left':left, 'right':right, 'next':item.left}

    def complete(self, col, state):
        return self.nearley_complete(col, state)

    def nearley_complete(self, col, state):
        parent_states = [
            st for st in state.s_col.states if st.at_dot() == state.name
        ]
        for st in parent_states:
            a = st.advance()
            a = col.add(a)
            self.add_derivation(a, st, state)


class NearleyParser(NearleyParser):
    def fill_chart(self, chart):
        for i, col in enumerate(chart):
            for state in col.states:
                if state.finished():
                    self.complete(col, state)
                else:
                    sym = state.at_dot()
                    if sym in self.cgrammar:
                        self.predict(col, sym)
                    else:
                        if i + 1 >= len(chart):
                            continue
                        self.scan(chart[i + 1], state, sym)
            if self.log:
                print(col)
        return chart

class NearleyParser(NearleyParser):
    def parse_prefix(self, text):
        table = self.chart_parse(text, self.start_symbol)
        for col in reversed(table):
            states = [st for st in col.states if st.name == self.start_symbol]
            if states:
                return col.index, states
        return -1, []

    def parse(self, text):
        cursor, states = self.parse_prefix(list(text))
        if cursor != len(text):
            return []
        for state in states:
            if state.finished():
                yield self.derivation_tree(state)

    def process_expr(self, expr, children):
        terms = iter([(i, []) for i in expr if i not in self.cgrammar])
        nts = iter([self.derivation_tree(i) for i in children])
        return [next(terms if i not in self.cgrammar else nts) for i in expr]

    def derivation_tree(self, state):
        return (state.name, self.process_expr(state.expr, state.children))

A1_GRAMMAR = {
        "<start>": ["<expr>"],
        "<expr>": ["<expr>+<expr>", "<expr>-<expr>", "<integer>"],
        "<integer>": ["<digit><integer>", "<digit>"],
        "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        }
S_G = {
        '<start>' : ['<A><B><C><D>'],
        '<A>': ['a'],
        '<B>': ['b'],
        '<C>': ['c'],
        '<D>': ['d']
}
S_G = {
        '<start>' : ['<S>'],
        '<S>': ['<S><S>', 'a', '']
}
E_G = {
        '<start>' : ['<E>'],
        '<E>': ['<E>+<E>', '1']
}
parser = NearleyParser(E_G, log=True)
for tree in parser.parse('1+1+1'):
        print(tree)
