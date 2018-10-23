#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Parser.html
# Last change: 2018-10-23 08:08:30+02:00
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




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    from fuzzingbook_utils import set_fixed_seed
    set_fixed_seed.set_fixed_seed()



if __package__ is None or __package__ == "":
    from Grammars import EXPR_GRAMMAR, START_SYMBOL
else:
    from .Grammars import EXPR_GRAMMAR, START_SYMBOL


if __package__ is None or __package__ == "":
    from GrammarFuzzer import display_tree
else:
    from .GrammarFuzzer import display_tree


import functools
import re

RE_NONTERMINAL = re.compile(r'(<[a-zA-Z_]*>)')

def split(rule):
    return [s for s in re.split(RE_NONTERMINAL, rule) if s]

class PEGParser:
    def __init__(self, grammar):
        self.grammar = {k: [split(l) for l in rules]
                        for k, rules in grammar.items()}
    # memoize repeated calls.
    @functools.lru_cache(maxsize=None)
    def unify_key(self, key, text, at=0):
        if key not in self.grammar:
            if text[at:].startswith(key): return at + len(key), (key, [])
            else: return at, None
        rules = self.grammar[key]
        for rule in rules:
            l, res = self.unify_line(rule, text, at)
            if res: return (l, (key, res))
        return 0, None

    def unify_line(self, rule, text, at):
        results = []
        for token in rule:
            at, res = self.unify_key(token, text, at)
            if res is None: return at, None
            results.append(res)
        return at, results

def parse(text, grammar, start_symbol=START_SYMBOL):
    peg = PEGParser(grammar)
    return peg.unify_key(start_symbol, text)

if __name__ == "__main__":
    cursor, tree = parse("1 + (2 * 3)", EXPR_GRAMMAR)
    display_tree(tree)


if __name__ == "__main__":
    cursor, tree = parse("1 * (2 + 3.45)", EXPR_GRAMMAR)
    display_tree(tree)


# ## Table driven parsers

if __name__ == "__main__":
    print('\n## Table driven parsers')




# ### LL(1) parser

if __name__ == "__main__":
    print('\n### LL(1) parser')




EOF = '\0'
EPSILON = ''

if __name__ == "__main__":
    grammar = {'<start>': ['<expr>'],
               '<expr>': ['<term><expr_>'],
               '<expr_>': ['+<expr>',
                           '-<expr>',
                           ''],
               '<term>': ['<factor><term_>'],
               '<term_>': ['*<term>',
                           '/<term>',
                           ''],
               '<factor>': ['+<factor>',
                            '-<factor>',
                            '(<expr>)',
                            '<int>'],
               '<int>': ['<integer><integer_>'],
               '<integer_>': ['',
                              '.<integer>'],
               '<integer>': ['<digit><I>'],
               '<I>': ['<integer>',
                       ''],
               '<digit>': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']}


if __name__ == "__main__":
    new_grammar = {k: [split(e) for e in grammar[k]] for k in grammar}
    new_grammar


def rules(g): return [(k, e) for k, a in g.items() for e in a]

def terminals(g):
    return set(t for k, expr in rules(g) for t in expr if t not in g)

# ### First and Follow sets

if __name__ == "__main__":
    print('\n### First and Follow sets')




def fixpoint(f):
    def helper(*args):
        while True:
            sargs = repr(args)
            args_ = f(*args)
            if repr(args_) == sargs:
                return args
            args = args_
    return helper

@fixpoint
def nullable_(rules, e):
    for A, expression in rules:
        if all((token in e)  for token in expression): e |= {A}
    return (rules, e)

def nullable(grammar):
    return nullable_(rules(grammar), set())[1]


@fixpoint
def firstset_(rules, first, epsilon):
    for A, expression in rules:
        for token in expression:
            first[A] |= first[token]

            # update until the first token that is not nullable
            if token not in epsilon:
                break
    return (rules, first, epsilon)

def firstset(grammar, epsilon):
    # https://www.cs.umd.edu/class/spring2014/cmsc430/lectures/lec05.pdf p6
    # (1) If X is a terminal, then First(X) is just X
    first = {i:{i} for i in terminals(grammar)}

    # (2) if X ::= epsilon, then epsilon \in First(X)
    for k in grammar:
        first[k] = {EPSILON} if k in epsilon else set()
    return firstset_(rules(grammar), first, epsilon)[1]

@fixpoint
def followset_(grammar, epsilon, first, follow):
    for A, expression in rules(grammar):
        # https://www.cs.umd.edu/class/spring2014/cmsc430/lectures/lec05.pdf
        # https://www.cs.uaf.edu/~cs331/notes/FirstFollow.pdf
        # essentially, we start from the end of the expression. Then:
        # (3) if there is a production A -> aB, then every thing in
        # FOLLOW(A) is in FOLLOW(B)
        # note: f_B serves as both follow and first.
        f_B = follow[A]
        for t in reversed(expression):
            # update the follow for the current token. If this is the
            # first iteration, then here is the assignment
            if t in grammar:
                follow[t] |= f_B  # only bother with nt

            # computing the last follow symbols for each token t. This
            # will be used in the next iteration. If current token is
            # nullable, then previous follows can be a legal follow for
            # next. Else, only the first of current token is legal follow
            # essentially

            # (2) if there is a production A -> aBb then everything in FIRST(B)
            # except for epsilon is added to FOLLOW(B)
            f_B = f_B | first[t] if t in epsilon else (first[t] - {EPSILON})

    return (grammar, epsilon, first, follow)

def followset(grammar, start):
    # Initialize first and follow sets for non-terminals
    follow = {i: set() for i in grammar}
    follow[start] = {EOF}

    epsilon = nullable(grammar)
    first = firstset(grammar, epsilon)
    return followset_(grammar, epsilon, first, follow)

def rnullable(rule, epsilon):
    return all(token in epsilon for token in rule)

def rfirst(rule, first, epsilon):
    tokens = set()
    for token in rule:
        tokens |= first[token]
        if token not in epsilon: break
    return tokens

def predict(rulepair, first, follow, epsilon):
    A, rule = rulepair
    rf = rfirst(rule, first, epsilon)
    if rnullable(rule, epsilon):
        rf |= follow[A]
    return rf

def parse_table(grammar, start, my_rules):
    _, epsilon, first, follow = followset(grammar, start)

    ptable = [(rule, predict(rule, first, follow, epsilon))
              for rule in my_rules]

    parse_tbl = {k: {} for k in grammar}

    for (k, expr), pvals in ptable:
        parse_tbl[k].update({v: (k, expr) for v in pvals})
    return parse_tbl

def parse_helper(grammar, tbl, stack, inplst):
    inp, *inplst = inplst
    exprs = []
    while stack:
        val, *stack = stack
        if isinstance(val, tuple):
            exprs.append(val)
        elif val not in grammar:  # terminal
            assert val == inp
            exprs.append(val)
            inp, *inplst = inplst or [None]
        else:
            _, rhs = tbl[val][inp] if inp else (None, [])
            stack = rhs + [(val, len(rhs))] + stack
    return exprs

def parse(grammar, start, inp):
    my_rules = rules(grammar)
    parse_tbl = parse_table(grammar, start, my_rules)
    k, _ = my_rules[0]
    stack = [k]
    return parse_helper(grammar, parse_tbl, stack, list(inp))

def linear_to_tree(arr):
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
    tree = linear_to_tree(parse(new_grammar, START_SYMBOL, '(1+2)*3'))
    display_tree(tree)


# ### Earley parser

if __name__ == "__main__":
    print('\n### Earley parser')




def shrink(rule): return [i.strip() for i in rule]

if __name__ == "__main__":
    new_grammar = {k: [shrink(split(e)) for e in EXPR_GRAMMAR[k]] for k in EXPR_GRAMMAR}
    new_grammar


@fixpoint
def nullable_(rules, e):
    for A, expression in rules:
        if all((token in e)  for token in expression): e |= {A}
    return (rules, e)

def nullable(grammar):
    return nullable_(rules(grammar), set())[1]

class State(object):
    def __init__(self, name, expr, dot, origin, children=[]):
        self.name, self.expr, self.dot, self.origin = name, expr, dot, origin
        self.children = children[:]
    def finished(self): return self.dot >= len(self.expr)
    def shift(self):
        return State(self.name, self.expr, self.dot+1, self.origin, self.children)
    def symbol(self): return self.expr[self.dot]

    def _t(self): return (self.name, self.expr, self.dot, self.origin.i, tuple(self.children))
    def __hash__(self): return hash(self._t())
    def __eq__(self, other): return  self._t() == other._t()

class Column(object):
    def __init__(self, i, token):
        self.token, self.states, self._unique, self.i = token, [], {}, i

    def add(self, state):
        if state in self._unique: return self._unique[state]
        self._unique[state] = state
        self.states.append(state)
        return self._unique[state]

def predict(col, sym, grammar):
    for alt in grammar[sym]:
        col.add(State(sym, tuple(alt), 0, col))

def scan(col, state, token):
    if token == col.token:
        col.add(state.shift())

def complete(col, state, grammar):
    for st in state.origin.states:
        if st.finished(): continue
        if state.name != st.symbol(): continue
        col.add(st.shift()).children.append(state)

# http://courses.washington.edu/ling571/ling571_fall_2010/slides/parsing_earley.pdf
# https://github.com/tomerfiliba/tau/blob/master/earley3.py
def parse(words, grammar, start):
    # Aycock 2002 Practical Earley Parsing -- treatment of epsilon
    epsilon = nullable(grammar)
    alt = tuple(*grammar[start])
    chart = [Column(i, tok) for i,tok in enumerate([None, *words])]
    chart[0].add(State(start, alt, 0, chart[0], []))

    for i, col in enumerate(chart):
        for state in col.states:
            if state.finished():
                complete(col, state, grammar)
            else:
                sym = state.symbol()
                if sym in grammar:
                    predict(col, sym, grammar)
                    if sym in epsilon:
                        # note that precomputation of epsilon derivation can result in infinite
                        # loops for certain grammars. Hence, we mark a nullable non-terminal
                        # but do not expand it.
                        col.add(state.shift()).children.append(State(sym + '*', tuple(), 0, col))
                else:
                    if i + 1 >= len(chart): continue
                    scan(chart[i+1], state, sym)
    return chart

def process_expr(expr, children, grammar):
    terms = iter([(i,[]) for i in expr if i not in grammar])
    nts = iter([node_translator(i, grammar) for i in  children])
    return [next(terms if i not in grammar else nts) for i in expr]

def node_translator(state, grammar):
    return (state.name, process_expr(state.expr, state.children, grammar))

if __name__ == "__main__":
    new_grammar = {k: [shrink(split(e)) for e in EXPR_GRAMMAR[k]] for k in EXPR_GRAMMAR}
    table = parse(list('1+2+3'), new_grammar, '<start>')
    states = [st for st in table[-1].states if st.name == '<start>' and st.finished()]
    for state in states:
        display_tree(node_translator(state, new_grammar))


# #### Ambiguous grammars generates parse forests

if __name__ == "__main__":
    print('\n#### Ambiguous grammars generates parse forests')




if __name__ == "__main__":
    grammar= {
            '<start>': ['<A>'],
            '<A>': ['<A>+<A>', 'a'],
            }


if __name__ == "__main__":
    new_grammar = {k: [shrink(split(e)) for e in grammar[k]] for k in grammar}
    table = parse(list('a+a+a'), new_grammar, '<start>')
    states = [st for st in table[-1].states if st.name == '<start>' and st.finished()]
    for state in states:
        display_tree(node_translator(state, new_grammar))


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
    # Some code that is part of the exercise
    pass


if __name__ == "__main__":
    # Some code for the solution
    2 + 2


# ### Exercise 2

if __name__ == "__main__":
    print('\n### Exercise 2')



