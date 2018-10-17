#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Parser.html
# Last change: 2018-10-16 12:54:11+02:00
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

class PEGParser:
    def __init__(self, grammar):
        def split(rule): return tuple(
            s for s in re.split(
                RE_NONTERMINAL, rule) if s)
        self.grammar = {k: [split(l) for l in rules]
                        for k, rules in grammar.items()}

    def literal_match(self, part, text, cursor):
        return (cursor + len(part), (part, [])
                ) if text[cursor:].startswith(part) else (cursor, None)

    # memoize repeated calls.
    @functools.lru_cache(maxsize=None)
    def unify_key(self, key, text, cursor=0):
        rules = self.grammar[key]
        # make a generator for matching rules. We dont want a list because
        # we want to be lazy and evaluate only until the first matching
        rets = (self.unify_line(rule, text, cursor) for rule in rules)
        # return the first non null (matching) rule's cursor and res
        cursor, res = next(
            (ret for ret in rets if ret[1] is not None), (cursor, None))
        return (cursor, (key, res) if res is not None else None)

    def unify_line(self, parts, text, cursor):
        def is_symbol(v): return v[0] == '<'

        results = []
        for part in parts:
            # get the matcher function
            matcher = (self.unify_key if is_symbol(
                part) else self.literal_match)
            # compute the cursor, and the result from it.
            cursor, res = matcher(part, text, cursor)
            if res is None:
                return (cursor, None)
            results.append(res)
        return cursor, results

def parse(text, grammar, start_symbol=START_SYMBOL):
    def readall(fn): return ''.join([f for f in open(fn, 'r')]).strip()

    result = PEGParser(grammar).unify_key(start_symbol, text)
    return result

if __name__ == "__main__":
    cursor, tree = parse("1 + 2 * 3", EXPR_GRAMMAR)
    display_tree(tree)


# ## Table driven parsers

if __name__ == "__main__":
    print('\n## Table driven parsers')




# ### LL(1) parser

if __name__ == "__main__":
    print('\n### LL(1) parser')




def split_tokens(rule):
    lst = [i for i in re.split(RE_NONTERMINAL, rule) if i != '']
    if lst == []:
        return ['']
    return lst

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
    new_grammar = {k: [split_tokens(e) for e in grammar[k]] for k in grammar}
    new_grammar


def rules(g): return [(k, e) for k, a in g.items() for e in a]

def terminals(g):
    return set(token for k, expr in rules(g)
               for token in expr if token not in g)

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
def compute_ff(grammar, first, follow, epsilon):
    for A, expression in rules(grammar):
        nullable = True
        for token in expression:
            first[A] |= first[token]

            # update until the first token that is not nullable
            if token not in epsilon:
                nullable = False
                break

        if nullable:
            epsilon |= {A}
            first[A] |= {''}

        # https://www.cs.uaf.edu/~cs331/notes/FirstFollow.pdf
        # essentially, we start from the end of the expression. Then:
        # (3) if there is a production A -> aB, then every thing in
        # FOLLOW(A) is in FOLLOW(B)
        follow_B = follow[A]
        for t in reversed(expression):
            if not t:
                continue
            # update the follow for the current token. If this is the
            # first iteration, then here is the assignment
            if t in grammar:
                follow[t] |= follow_B  # only bother with nt

            # computing the last follow symbols for each token t. This
            # will be used in the next iteration. If current token is
            # nullable, then previous follows can be a legal follow for
            # next. Else, only the first of current token is legal follow
            # essentially

            # (2) if there is a production A -> aBb then everything in FIRST(B)
            # except for epsilon is added to FOLLOW(B)
            follow_B = follow_B | (
                first[t] - {''}) if t in epsilon else first[t]

    return (grammar, first, follow, epsilon)

def process(grammar):
    # Initialize first and follow sets for non-terminals
    first = {i: set() for i in grammar}
    follow = {i: set() for i in grammar}

    # If X is a terminal, then First(X) is just X
    first.update((i, {i}) for i in terminals(grammar))
    epsilon = {''}
    return compute_ff(grammar, first, follow, epsilon)

def rnullable(rule, epsilon):
    return all(token in epsilon for token in rule)

def rfirst(rule, first, epsilon):
    tokens = set()
    for token in rule:
        tokens |= first[token]
        if token not in epsilon:
            break  # not nullable
    return tokens

def predict(rulepair, first, follow, epsilon):
    A, rule = rulepair
    rf = rfirst(rule, first, epsilon)
    if rnullable(rule, epsilon):
        rf |= follow[A] - {''}
    return rf

def parse_table(grammar, my_rules):
    _, first, follow, epsilon = process(grammar)

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
            continue
        if val not in grammar:  # terminal
            if val == '':
                exprs.append(val)
                continue
            if val != inp:
                raise Exception("%s != %s" % (val, inp))
            exprs.append(val)
            inp, *inplst = [*inplst, '']
        else:
            k, rhs = tbl[val][inp]
            assert k == val
            stack = rhs + [(val, len(rhs))] + stack
    return exprs

def parse(grammar, inp):
    my_rules = rules(grammar)
    parse_tbl = parse_table(grammar, my_rules)
    k, _ = my_rules[0]
    stack = [k]
    return parse_helper(grammar, parse_tbl, stack, list(inp))

def to_tree(arr):
    stack = []
    while arr:
        elt = arr.pop(0)
        if not isinstance(elt, tuple):
            stack.append((elt, []))
        else:
            # get the last n
            sym, n = elt
            elts = stack[-n:]
            stack = stack[0:len(stack) - n]
            stack.append((sym, elts))
    assert len(stack) == 1
    return stack[0]

if __name__ == "__main__":
    tree = to_tree(parse(new_grammar, '(1+2)'))
    display_tree(tree)


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



