#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Parser.html
# Last change: 2018-10-27 14:03:06+02:00
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
from Grammars import EXPR_GRAMMAR, START_SYMBOL, RE_NONTERMINAL
from GrammarFuzzer import display_tree, all_terminals, GrammarFuzzer
from ExpectError import ExpectError

if __name__ == "__main__":
    mystring = '1+2'


A1_GRAMMAR = {
   "<start>":
       ["<expr>"],
   "<expr>":
       ["<expr>+<expr>", "<expr>-<expr>", "<integer>"],
   "<integer>":
       ["<digit><integer>", "<digit>"],
   "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

if __name__ == "__main__":
    tree = ('<start>',[
        ('<expr>',[
            ('<expr>',[('<integer>',[('<digit>',[('1',[])])])]),
            ('+',[]),                           
            ('<expr>',[('<integer>',[('<digit>',[('2',[])])])])])])
    assert mystring == all_terminals(tree)
    display_tree(tree)


A2_GRAMMAR = {
   "<start>":
      ["<expr>"],
   "<expr>":
      ["<integer><expr_>"],
   "<expr_>":
      ["+<expr>", "-<expr>", ""],
   "<integer>":
      ["<digit><integer_>"],
   "<integer_>":
      ["<integer>", ""],
   "<digit>":
      ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

if __name__ == "__main__":
    tree = ('<start>', [
        ('<expr>', [('<integer>',
                     [('<digit>', [('1', [])]), ('<integer_>', [('',[])])]),
                    ('<expr_>', [('+', []), 
                                 ('<expr>', [
                                     ('<integer>', [
                                         ('<digit>', [('2', [])]),
                                         ('<integer_>', [('',[])])]),
                                     ('<expr_>', [('',[])])])])])])
    assert mystring == all_terminals(tree)
    display_tree(tree)


if __name__ == "__main__":
    mystring = '1+2+3'
    tree = ('<start>', [
        ('<expr>', [
            ('<expr>', [
                ('<expr>', [('<integer>', [('<digit>', [('1', [])])])]),
                ('+', []),
                ('<expr>', [('<integer>', [('<digit>', [('2', [])])])])]), 
            ('+', []), 
            ('<expr>', [('<integer>', [('<digit>', [('3', [])])])])])])
    assert mystring == all_terminals(tree)
    display_tree(tree)


if __name__ == "__main__":
    tree = ('<start>', [
        ('<expr>', [
            ('<expr>', [('<integer>', [('<digit>', [('1', [])])])]), 
            ('+', []), 
            ('<expr>', [
                ('<expr>', [('<integer>', [('<digit>', [('2', [])])])]), 
                ('+', []), 
                ('<expr>', [('<integer>', [('<digit>', [('3', [])])])])]) ])])
    assert all_terminals(tree) == mystring
    display_tree(tree)


from functools import reduce, lru_cache
import re

def split(rule):
    return [token
            for token in re.split(RE_NONTERMINAL, rule)
            if token]

def canonical(grammar):
    return  {key: [split(choice) for choice in choices]
             for key, choices in grammar.items()}

class Parser(object):
    def __init__(self, grammar, start_symbol=START_SYMBOL):
        self.start_symbol = start_symbol
        self.grammar = grammar
        
    def parse_prefix(self, text):
        """Return pair (cursor, forest) for longest prefix of text"""
        raise NotImplemented()
        
    def parse(self, text):
        cursor, forest = self.parse_prefix(text)
        if cursor < len(text):
            raise SyntaxError("at " + repr(text[cursor:]))
        return forest

# ## Parsing Expression Grammars

if __name__ == "__main__":
    print('\n## Parsing Expression Grammars')




if __name__ == "__main__":
    peg = {
        '<start>': [['a'],['b']]
    }


if __name__ == "__main__":
    peg = {
        '<start>': [['ab'],['abc']]
    }


# ### Packrat Parser for _PEGs_

if __name__ == "__main__":
    print('\n### Packrat Parser for _PEGs_')




class PEGParser(Parser):
    def __init__(self, grammar, start_symbol):
        super().__init__(canonical(grammar), start_symbol)
        
    def parse_prefix(self, text):
        return self.unify_key(self.start_symbol, text, 0)

class PEGParser(PEGParser):
    def unify_key(self, key, text, at=0):
        if key not in self.grammar:
            if text[at:].startswith(key): return at + len(key), (key, [])
            else: return at, None
        for rule in self.grammar[key]:
            to, res = self.unify_rule(rule, text, at)
            if res: return (to, (key, res))
        return 0, None

class PEGParser(PEGParser):
    def unify_rule(self, rule, text, at):
        results = []
        for token in rule:
            at, res = self.unify_key(token, text, at)
            if res is None: return at, None
            results.append(res)
        return at, results

class PEGParser(PEGParser):
    @lru_cache(maxsize=None)
    def unify_key(self, key, text, at=0):
        if key not in self.grammar:
            if text[at:].startswith(key): return at + len(key), (key, [])
            else: return at, None
        for rule in self.grammar[key]:
            to, res = self.unify_rule(rule, text, at)
            if res: return (to, (key, res))
        return 0, None

def parse(text, grammar):
    peg = PEGParser(grammar, START_SYMBOL)
    return peg.parse(text)  

if __name__ == "__main__":
    mystring = "1 + (2 * 3)"
    tree = parse(mystring, EXPR_GRAMMAR)
    assert all_terminals(tree) == mystring
    display_tree(tree)


if __name__ == "__main__":
    mystring = "1 * (2 + 3.35)"
    tree = parse(mystring, EXPR_GRAMMAR)
    assert all_terminals(tree) == mystring
    display_tree(tree)


PEG_SURPRISE = {
    "<A>": ["a<A>a","aa"]
}

if __name__ == "__main__":
    strings = []
    for e in range(4):
        f = GrammarFuzzer(PEG_SURPRISE, '<A>')
        tree = ('<A>',None)
        for _ in range(e):
            tree = f.expand_tree_once(tree)
        tree = f.expand_tree_with_strategy(tree, f.expand_node_min_cost)
        strings.append(all_terminals(tree))
        display_tree(tree)
    strings


if __name__ == "__main__":
    peg = PEGParser(PEG_SURPRISE, '<A>')
    for s in strings:
        with ExpectError():
            tree = peg.parse(s)
            display_tree(tree)
            print(s)


# ## Context Free Grammars

if __name__ == "__main__":
    print('\n## Context Free Grammars')




EOF = '\0'
EPSILON = ''

def rules(grammar):
    return [(key, choice)
            for key, choices in grammar.items()
            for choice in choices]

if __name__ == "__main__":
    rules(canonical(EXPR_GRAMMAR))


def terminals(grammar):
    return set(token
               for key, choice in rules(grammar)
               for token in choice if token not in grammar)

if __name__ == "__main__":
    terminals(canonical(EXPR_GRAMMAR))


if __name__ == "__main__":
    my_grammar = {
        '<start>': [['<A>'], ['<B>']],
        '<A>': [['a'],['']],
        '<B>': [['b']]
    }


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


def nullable(grammar):
    productions = rules(grammar)
    @fixpoint
    def nullable_(nullables):
        for A, expr in productions:
            if all(token in nullables for token in expr):
                nullables |= {A}
        return (nullables)
    return nullable_({EPSILON})

if __name__ == "__main__":
    nullable(my_grammar)


def shrink(rule):
    return [i.strip() for i in rule]

def canonical(grammar):
    return  {k: [shrink(split(l)) for l in rules]
             for k, rules in grammar.items()}

if __name__ == "__main__":
    canonical(EXPR_GRAMMAR)


# ### Earley parser

if __name__ == "__main__":
    print('\n### Earley parser')




# #### Columns

if __name__ == "__main__":
    print('\n#### Columns')




class Column(object):
    def __init__(self, index, letter):
        self.index, self.letter = index, letter
        self.states, self._unique =  [], {}

class Column(Column):
    def add(self, state):
        if state in self._unique: return self._unique[state]
        self._unique[state] = state
        self.states.append(state)
        return self._unique[state]

# #### States

if __name__ == "__main__":
    print('\n#### States')




class State(object):
    def __init__(self, name, expr, dot, s_col, children=[]):
        self.name, self.expr, self.dot = name, expr, dot
        self.s_col, self.e_col = s_col, None
        self.children = children[:]
        
    def _t(self):
        return (self.name, self.expr, self.dot, self.s_col.index, tuple(self.children))
    def __hash__(self): return hash(self._t())
    def __eq__(self, other): return  self._t() == other._t()

class State(State):
    def finished(self):
        return self.dot >= len(self.expr)
    def advance(self):
        return State(self.name, self.expr, self.dot+1, self.s_col, self.children)
    def at_dot(self):
        return self.expr[self.dot] if self.dot < len(self.expr) else None

# #### The Parser

if __name__ == "__main__":
    print('\n#### The Parser')




class EarleyParser(Parser):
    def __init__(self, grammar, start_symbol):
        super().__init__(grammar, start_symbol)
        self.epsilon = nullable(self.grammar)

class EarleyParser(EarleyParser):
    def chart_parse(self, words, start):
        alt = tuple(*self.grammar[start])
        chart = [Column(i, tok) for i,tok in enumerate([None, *words])]
        chart[0].add(State(start, alt, 0, chart[0], []))
        return self.fill_chart(chart)

class EarleyParser(EarleyParser):
    def predict(self, col, sym):
        for alt in self.grammar[sym]:
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
    def complete(self, col, state): return self.earley_complete(col, state)
    def earley_complete(self, col, state):
        parent_states = [st for st in state.s_col.states
                     if st.at_dot() == state.name]
        for st in parent_states:
            col.add(st.advance()).children.append(state)

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
                    if sym in self.grammar:
                        self.predict(col, sym)
                        if sym in self.epsilon:
                            c = col.add(state.advance())
                            c.children.append(State(sym + '*', tuple(), 0, col))
                    else:
                        if i + 1 >= len(chart): continue
                        self.scan(chart[i+1], state, sym)
        return chart


class EarleyParser(EarleyParser):
    def parse_prefix(self, text):
        table = self.chart_parse(text, self.start_symbol)
        for col in reversed(table):
            states = [st for st in col.states if st.name == self.start_symbol]
            if states: return col.index, states
        return -1, []

    def parse(self, text):
        cursor, states = self.parse_prefix(text)
        if cursor != len(text): return []
        for state in states:
            if state.finished():
                yield self.derivation_tree(state)

    def process_expr(self, expr, children):
        terms = iter([(i,[]) for i in expr if i not in self.grammar])
        nts = iter([self.derivation_tree(i) for i in  children])
        return [next(terms if i not in self.grammar else nts) for i in expr]

    def derivation_tree(self, state):
        return (state.name, self.process_expr(state.expr, state.children))

def parse(text, grammar, start=START_SYMBOL):
    ep = EarleyParser(grammar, start)
    return ep.parse(text)  

if __name__ == "__main__":
    new_grammar = canonical(EXPR_GRAMMAR)
    for tree in parse(list('1+2+3'), new_grammar):
        display_tree(tree)


# #### Ambiguous grammars

if __name__ == "__main__":
    print('\n#### Ambiguous grammars')




if __name__ == "__main__":
    grammar= {
            '<start>': ['<A>'],
            '<A>': ['<A>+<A>', 'a'],
            }


if __name__ == "__main__":
    new_grammar = canonical(A1_GRAMMAR)
    for tree in parse(list('1+2+3'), new_grammar, '<start>'):
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




# ### Exercise 1

if __name__ == "__main__":
    print('\n### Exercise 1')




if __name__ == "__main__":
    pass


# ### Exercise 2

if __name__ == "__main__":
    print('\n### Exercise 2')




if __name__ == "__main__":
    pass


# ### Exercise 3

if __name__ == "__main__":
    print('\n### Exercise 3')




if __name__ == "__main__":
    pass


# ### Exercise 4

if __name__ == "__main__":
    print('\n### Exercise 4')




if __name__ == "__main__":
    pass


# ### Exercise 5

if __name__ == "__main__":
    print('\n### Exercise 5')




if __name__ == "__main__":
    RE_NONTERMINAL


# ### Exercise 6

if __name__ == "__main__":
    print('\n### Exercise 6')




class LeoParser(EarleyParser):
    def check_single_item(self, st, remain):
        res = [s for s in remain
                 if s.name == st.name and s.expr == st.expr and
                    s.s_col.i == st.s_col.i and s.dot == (st.dot - 1)]
        return len(res) == 1

    @lru_cache(maxsize=None)
    def get_above(self, state):
        remain, finished = splitlst(lambda s: s.finished(), state.s_col.states)
        vals = [st for st in finished
                    if state.name == st.expr[-1] and
                       self.check_single_item(st, remain)]
        if vals:
            assert len(vals) == 1
            res = self.get_above(vals[0])
            return vals[0] if not res else res
        return None

    def leo_complete(self, col, state):
        detred = self.get_above(state)
        if detred:
            col.add(detred.copy()).children.append(state)
        else:
            self.earley_complete(col, state)

    def complete(self, col, state): return self.leo_complete(col, state)
