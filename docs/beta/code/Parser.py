#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Parser.html
# Last change: 2018-11-02 11:36:04+01:00
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

if __name__ == "__main__":
    canonical(EXPR_GRAMMAR)


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




PEG1 = {
    '<start>': [['a'],['b']]
}

PEG2 = {
    '<start>': [['ab'],['abc']]
}

# ### Packrat Parser for _PEGs_

if __name__ == "__main__":
    print('\n### Packrat Parser for _PEGs_')




# #### The Parser

if __name__ == "__main__":
    print('\n#### The Parser')




class PEGParser(Parser):
    def __init__(self, grammar, start_symbol):
        super().__init__(grammar, start_symbol)
        
    def parse_prefix(self, text):
        return self.unify_key(self.start_symbol, text, 0)

# ##### Unify Key

if __name__ == "__main__":
    print('\n##### Unify Key')




class PEGParser(PEGParser):
    def unify_key(self, key, text, at=0):
        if key not in self.grammar:
            if text[at:].startswith(key): return at + len(key), (key, [])
            else: return at, None
        for rule in self.grammar[key]:
            to, res = self.unify_rule(rule, text, at)
            if res: return (to, (key, res))
        return 0, None

# ##### Unify Rule

if __name__ == "__main__":
    print('\n##### Unify Rule')




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
    peg = PEGParser(canonical(grammar), START_SYMBOL)
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
    peg = PEGParser(canonical(PEG_SURPRISE), '<A>')
    for s in strings:
        with ExpectError():
            tree = peg.parse(s)
            display_tree(tree)
            print(s)


# ## Context Free Grammars

if __name__ == "__main__":
    print('\n## Context Free Grammars')




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


def shrink(rule):
    return [i.strip() for i in rule]

def canonical(grammar):
    return  {k: [shrink(split(l)) for l in rules]
             for k, rules in grammar.items()}

if __name__ == "__main__":
    canonical(EXPR_GRAMMAR)


# ### Nearley Parser

if __name__ == "__main__":
    print('\n### Nearley Parser')




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
        state.e_col = self
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
    def __hash__(self):
        return hash(self._t())
    def __eq__(self, other):
        return  self._t() == other._t()

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




class NearleyParser(Parser):
    def chart_parse(self, words, start):
        alt = tuple(*self.grammar[start])
        chart = [Column(i, tok) for i,tok in enumerate([None, *words])]
        chart[0].add(State(start, alt, 0, chart[0]))
        return self.fill_chart(chart)

# ##### Predict

if __name__ == "__main__":
    print('\n##### Predict')




class NearleyParser(NearleyParser):
    def predict(self, col, sym):
        for alt in self.grammar[sym]:
            col.add(State(sym, tuple(alt), 0, col))

# ##### Scan

if __name__ == "__main__":
    print('\n##### Scan')




class NearleyParser(NearleyParser):
    def scan(self, col, state, letter):
        if letter == col.letter:
            col.add(state.advance())

# ##### Complete

if __name__ == "__main__":
    print('\n##### Complete')




class NearleyParser(NearleyParser):
    def complete(self, col, state): return self.nearley_complete(col, state)
    def nearley_complete(self, col, state):
        parent_states = [st for st in state.s_col.states
                     if st.at_dot() == state.name]
        for st in parent_states:
            col.add(st.advance()).children.append(state)

# ##### Fill chart

if __name__ == "__main__":
    print('\n##### Fill chart')




class NearleyParser(NearleyParser):
    def fill_chart(self, chart):
        for i, col in enumerate(chart):
            for state in col.states:
                if state.finished():
                    self.complete(col, state)
                else:
                    sym = state.at_dot()
                    if sym in self.grammar:
                        self.predict(col, sym)
                    else:
                        if i + 1 >= len(chart): continue
                        self.scan(chart[i+1], state, sym)
        return chart


# ##### Parse

if __name__ == "__main__":
    print('\n##### Parse')




class NearleyParser(NearleyParser):
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
    ep = NearleyParser(grammar, start)
    return ep.parse(text)  

if __name__ == "__main__":
    new_grammar = canonical(EXPR_GRAMMAR)
    mystring = '12*(2+2)/31'
    for tree in parse(list(mystring), new_grammar):
        assert mystring == all_terminals(tree)
        display_tree(tree)


# #### Ambiguous parsing

if __name__ == "__main__":
    print('\n#### Ambiguous parsing')




if __name__ == "__main__":
    new_grammar = canonical(A1_GRAMMAR)
    mystring = '1+2+3'
    for tree in parse(list(mystring), new_grammar, '<start>'):
        assert mystring == all_terminals(tree)
        display_tree(tree)


# ### Earley Parser

if __name__ == "__main__":
    print('\n### Earley Parser')




# #### States

if __name__ == "__main__":
    print('\n#### States')




class State(State):
    def __init__(self, name, expr, dot, s_col):
        self.name, self.expr, self.dot = name, expr, dot
        self.s_col, self.e_col = s_col, None

    def _t(self):
        return (self.name, self.expr, self.dot, self.s_col.index)
    
    def advance(self):
        return State(self.name, self.expr, self.dot+1, self.s_col)

# #### The Parser

if __name__ == "__main__":
    print('\n#### The Parser')




class EarleyParser(NearleyParser):
    def complete(self, col, state): return self.earley_complete(col, state)
    def earley_complete(self, col, state):
        parent_states = [st for st in state.s_col.states
                     if st.at_dot() == state.name]
        for st in parent_states:
            col.add(st.advance())

# ##### Parse

if __name__ == "__main__":
    print('\n##### Parse')




class EarleyParser(EarleyParser):
    def reverse(self, table):
        f_table = [Column(c.index, c.letter) for c in table]
        for col in table:
            finished = [s for s in col.states if s.finished()]
            for s in finished:
                f_table[s.s_col.index].states.append(s)
        return f_table

class EarleyParser(EarleyParser):
    def extract_trees(self, forest):
        return [self.extract_a_tree(forest)]
    
    def parse(self, text):
        cursor, states = self.parse_prefix(text)
        if cursor != len(text): return []
        table = self.chart_parse(text, self.start_symbol)
        f_table = self.reverse(table)
        start = next(s for s in states if s.finished())
        return self.extract_trees(self.parse_forest(f_table, start))

# ##### Parse Forests

if __name__ == "__main__":
    print('\n##### Parse Forests')




class EarleyParser(EarleyParser):
    def parse_forest(self, chart, state):
        if not state.expr: return (state.name, [])
        pathexprs = self.parse_paths(state.expr, chart, state.s_col.index, state.e_col.index)
        paths_ = []
        for pathexpr in pathexprs:
            pathexpr_ = []
            for varexpr in pathexpr:
                completion = (self.parse_forest(chart, varexpr)
                              if isinstance(varexpr, State)
                              else (varexpr, []))
                pathexpr_.append(completion)
            paths_.append(pathexpr_)
        return (state.name, paths_)

# ##### Parse Paths

if __name__ == "__main__":
    print('\n##### Parse Paths')




class EarleyParser(EarleyParser):
    def parse_paths(self, expr_, chart, frm, til):
        var,*expr = expr_
        starts = None
        if var not in self.grammar:
            starts = ([(var, frm + len(var))] if
                      frm<til and chart[frm+1].letter == var else [])
        else:
            starts = [(s, s.e_col.index)
                      for s in chart[frm].states if s.name == var]

        paths = []
        for state,start in starts:
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
        if not paths: return (name, [])
        return (name, [self.extract_a_tree(p) for p in paths[0]])

A3_GRAMMAR = {
        "<start>":
        ["<expr>"],
        "<expr>":
        ["<expr>+<expr>", "<expr>-<expr>","(<expr>)", "<integer>"],
        "<integer>":
        ["<digit><integer>", "<digit>"],
        "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        }

def parse(text, grammar, start=START_SYMBOL):
    ep = EarleyParser(canonical(grammar), start)
    return ep.parse(text)  

if __name__ == "__main__":
    mystring = '(1+24)-33'
    tree = parse(mystring, A3_GRAMMAR)[0]
    assert all_terminals(tree) == mystring
    display_tree(tree)


# ##### extract_trees

if __name__ == "__main__":
    print('\n##### extract_trees')




class EarleyParser(EarleyParser):
    def extract_trees(self, forest_node):
        name, paths = forest_node
        if not paths: return [(name, [])]
        results = []
        for path in paths:
            ptrees = zip(*[self.extract_trees(p) for p in path])
            results.extend([(name, p) for p in ptrees])
        return results

if __name__ == "__main__":
    mystring = '12+23-34'
    for tree in parse(mystring, A1_GRAMMAR):
        assert mystring == all_terminals(tree)
        display_tree(tree)


# #### The Aycock Epsilon fix

if __name__ == "__main__":
    print('\n#### The Aycock Epsilon fix')




if __name__ == "__main__":
    my_grammar = {
        '<start>': [['<A>'], ['<B>']],
        '<A>': [['a'],['']],
        '<B>': [['b']]
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
    tree = parse(mystring, E_GRAMMAR)
    print(tree)


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




def nullable_expr(expr, nullables): return all(token in nullables for token in expr)

def nullable(grammar):
    productions = rules(grammar)
    @fixpoint
    def nullable_(nullables):
        for A, expr in productions:
            if nullable_expr(expr, nullables): nullables |= {A}
        return (nullables)
    return nullable_({EPSILON})

if __name__ == "__main__":
    nullable(canonical(E_GRAMMAR))


class EarleyParser(EarleyParser):
    def fill_chart(self, chart):
        epsilon = nullable(self.grammar)
        for i, col in enumerate(chart):
            for state in col.states:
                if state.finished():
                    self.complete(col, state)
                else:
                    sym = state.at_dot()
                    if sym in self.grammar:
                        self.predict(col, sym)
                        if sym in epsilon:
                            col.add(state.advance())
                    else:
                        if i + 1 >= len(chart): continue
                        self.scan(chart[i+1], state, sym)
        return chart


if __name__ == "__main__":
    mystring = 'a'
    tree = parse(mystring, E_GRAMMAR)[0]
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




# ### Exercise 1 _More PEG Syntax_

if __name__ == "__main__":
    print('\n### Exercise 1 _More PEG Syntax_')




# ### Exercise 2 _PEG Predicates_

if __name__ == "__main__":
    print('\n### Exercise 2 _PEG Predicates_')




# ### Exercise 3 _Earley Fill Chart_

if __name__ == "__main__":
    print('\n### Exercise 3 _Earley Fill Chart_')




# ### Exercise 4 _Leo Parser_

if __name__ == "__main__":
    print('\n### Exercise 4 _Leo Parser_')




LR_GRAMMAR = {
        '<start>': ['<A>'],
        '<A>': ['<A>a', ''],
}

RR_GRAMMAR = {
        '<start>': ['<A>'],
        '<A>': ['a<A>', ''],
}

class Column(Column):
    def __str__(self):
        return "%s chart[%d]\n%s" % (
            self.letter, self.index, "\n".join(str(state)
                for state in self.states if state.finished()))
class State(State):
    def __str__(self):
        return self.name +':= '+ ' '.join([str(p) for p in
                [*self.expr[:self.dot],'|', *self.expr[self.dot:]]]) + "(%d,%d)" % (self.s_col.index, self.e_col.index)

class LoggingParser(EarleyParser):
    def fill_chart(self, chart):
        epsilon = nullable(self.grammar)
        for i, col in enumerate(chart):
            for state in col.states:
                if state.finished():
                    self.complete(col, state)
                else:
                    sym = state.at_dot()
                    if sym in self.grammar:
                        self.predict(col, sym)
                        if sym in epsilon:
                            col.add(state.advance())
                    else:
                        if i + 1 >= len(chart): continue
                        self.scan(chart[i+1], state, sym)
            print(str(col),"\n")
        print('_'*80)
        return chart

if __name__ == "__main__":
    result = LoggingParser(canonical(LR_GRAMMAR)).parse_prefix('aaaaaa')


if __name__ == "__main__":
    result = LoggingParser(canonical(RR_GRAMMAR)).parse_prefix('aaaaaa')


class State(State):
    def __init__(self, name, expr, dot, s_col, tag=None):
        super().__init__(name, expr, dot, s_col)
        self.tag = tag

    def copy(self, tag=None):
        return State(self.name, self.expr, self.dot, self.s_col, tag)

class LeoParser(LoggingParser):
    def complete(self, col, state): return self.leo_complete(col, state)
    
    def leo_complete(self, col, state):
        detred = self.deterministic_reduction(state)
        if detred:
            col.add(detred.copy())
        else:
            self.earley_complete(col, state)


def splitlst(predicate, iterable):
    return reduce(lambda res, e: res[predicate(e)].append(e)
                  or res, iterable, ([], []))

class LeoParser(LeoParser):
    def check_single_item(self, st, remain):
        res = [s for s in remain
                 if s.name == st.name and s.expr == st.expr and
                    s.s_col.index == st.s_col.index and s.dot == (st.dot - 1)]
        return len(res) == 1

    @lru_cache(maxsize=None)
    def get_above(self, state):
        remain, finished = splitlst(lambda s: s.finished(), state.s_col.states)
        res = [st for st in finished if len(st.expr) > 1 and state.name == st.expr[-1]]
        vals = [st for st in res if self.check_single_item(st, remain)]
        if vals:
            assert len(vals) == 1
            return vals[0]
        return None

    def deterministic_reduction(self, state):
        st = state
        while True:
            _st = self.get_above(st)
            if not _st: break
            st = _st
        return st if st != state else None
    
    def complete(self, col, state): return self.leo_complete(col, state)
    
    def leo_complete(self, col, state):
        detred = self.deterministic_reduction(state)
        if detred:
            col.add(detred.copy())
        else:
            self.earley_complete(col, state)


if __name__ == "__main__":
    result = LeoParser(canonical(RR_GRAMMAR)).parse_prefix('aaaaaa')


if __name__ == "__main__":
    result = LeoParser(canonical(LR_GRAMMAR)).parse_prefix('aaaaaa')
    result


# ### Exercise 5 _First set of a non-terminal_

if __name__ == "__main__":
    print('\n### Exercise 5 _First set of a non-terminal_')




def firstset(grammar, nullable):
    first = {i:{i} for i in terminals(grammar)}
    for k in grammar:
        first[k] = {EPSILON} if k in nullable else set()
    return firstset_((rules(grammar), first, nullable))[1]

def first_expr(expr, first, nullable):
    tokens = set()
    for token in expr:
        tokens |= first[token]
        if token not in nullable: break
    return tokens

@fixpoint
def firstset_(arg):
    (rules, first, epsilon) = arg
    for A, expression in rules:
        first[A] |= first_expr(expression, first,epsilon)
    return (rules, first, epsilon)

if __name__ == "__main__":
    firstset(canonical(EXPR_GRAMMAR), EPSILON)


# ### Exercise 6 _Follow set of a non-terminal_

if __name__ == "__main__":
    print('\n### Exercise 6 _Follow set of a non-terminal_')




if __name__ == "__main__":
    EOF='\0'
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
            if t in grammar: follow[t] |= f_B
            f_B = f_B | first[t] if t in epsilon else (first[t] - {EPSILON})

    return (grammar, epsilon, first, follow)

if __name__ == "__main__":
    followset(canonical(A1_GRAMMAR), START_SYMBOL)


# ### Exercise 7 _LL(1) parser_

if __name__ == "__main__":
    print('\n### Exercise 7 _LL(1) parser_')




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

# ### Exercise 8 _LR(1) parser_

if __name__ == "__main__":
    print('\n### Exercise 8 _LR(1) parser_')




from enum import Enum, auto
class Action(Enum):
    Goto = auto()
    Shift = auto()
    Accept = auto()
    Reduce = auto()

RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')

class PLine:
    cache = {}
    counter = 0
    fdict = None
    def __init__(self, key, production, cursor=0, lookahead=set(), pnum=0):
        self.key,self.production,self.cursor,self.lookahead = key,production,cursor,lookahead
        self.tokens = self.production
        self.pnum = pnum

    @classmethod
    def reset(cls):
        PLine.cache.clear()
        PLine.fdict = None
        PLine.counter = 0

    @classmethod
    def init_cache(cls, grammar, fdict):
        PLine.fdict = fdict
        for key in sorted(grammar.keys()):
            for production in grammar[key]:
                PLine.cache[str((key, production, 0))] = PLine(key, production,
                        cursor=0, lookahead=fdict[key], pnum=PLine.counter)
                PLine.counter += 1
        return len(PLine.cache.keys())

    @classmethod
    def get(cls, key, production, cursor):
        val = PLine.cache.get(str((key, production, cursor)))
        if val: return val

        seed = PLine.cache.get(str((key, production, 0)))
        val = PLine(key, production, cursor, seed.lookahead, seed.pnum)
        PLine.cache[str((key, production, cursor))] = val

        return val

    @classmethod
    def from_seed(cls, obj, cursor):
        return PLine.get(obj.key, obj.production, cursor)

    def production_number(self):
        return self.pnum

    def __repr__(self): return str(self)

    def __str__(self):
        return "[p%s]: %s -> %s \tcursor: %s %s" % (self.production_number(),
                self.key, ''.join([str(i) for i in self.tokens]), self.cursor, '@' + ''.join(sorted(self.lookahead)))

    def advance(self):
        if self.cursor >= len(self.tokens): return '', None
        if self.at(self.cursor) == EOF: return '', None
        token = self.at(self.cursor)
        return token, PLine.from_seed(self, self.cursor+1)

    def at(self, cursor):
        if cursor >= len(self.tokens): return None
        return self.tokens[cursor]

def lr1_closure(closure, cursor, grammar):
    items = closure[:] # copy
    seen = set()
    while items:
        item, *items = items
        token = item.at(item.cursor)
        if not token: continue
        if token in seen: continue
        if token in grammar:
            for ps in grammar[token]:
                pl = PLine.get(key=token, production=ps, cursor=0)
                items.append(pl)
                closure.append(pl)
                seen.add(pl.key)
    return closure

class State:
    counter = 1
    registry = {}
    cache = {}
    def reset():
        PLine.reset()
        State.counter = 1
        State.registry = {}
        State.cache = {}

    def __init__(self, plines, sfrom=None):
        self.plines = plines
        self.shifts = {}
        self.go_tos = {}
        self.i = State.counter
        self.row = []
        self.hrow = {}
        self.note = "*"
        if sfrom:
            self.grammar = sfrom.grammar
            self.start = sfrom.start
        State.counter += 1
        State.registry[self.i] = self
        self.key = ''.join([str(l) for l in plines])
        if State.cache.get(self.key): raise Exception("Cache already has the state. Use State.get")
        State.cache[self.key] = self

    @classmethod
    def get(cls, plines, sfrom=None):
        key = ''.join([str(l) for l in plines])
        val = State.cache.get(key)
        if val: return val
        State.cache[key] = State(plines, sfrom)
        return State.cache[key]

    def __str__(self):
        return "State(%s):\n\t%s" % (self.i, "\n\t".join([str(i) for i in self.plines]))

    def __repr__(self): return str(self)

    @classmethod
    def construct_initial_state(cls, grammar, start=START_SYMBOL):
        _, _epsilon, _first, follow = followset(grammar, start)
        PLine.init_cache(grammar, follow)
        production_str = grammar[start][0]

        pl = PLine.get(key=start, production=production_str, cursor=0)

        lr1_items = lr1_closure(closure=[pl], cursor=0, grammar=grammar)
        state =  cls(lr1_items, 0)
        # seed state
        state.start, state.grammar = start, grammar
        return state

    def go_to(self, token):
        if self.go_tos.get(token): return self.go_tos[token]
        if token not in self.grammar: return None
        new_plines = []
        for pline in self.plines:
            tadv, new_pline = pline.advance()
            if token == tadv:
                new_plines.append(new_pline)
        if not new_plines: return None
        s = self.form_closure(new_plines)
        self.go_tos[token] = s
        s.note = "%s -> [%s] -> " % (self.i,  token)
        return s

    def shift_to(self, token):
        if self.shifts.get(token): return self.shifts[token]
        if token in self.grammar: return None
        new_plines = []
        for pline in self.plines:
            tadv, new_pline = pline.advance()
            if token == tadv:
                new_plines.append(new_pline)
        if not new_plines: return None
        # each time we shift, we have to build a new closure, with cursor at 0
        # for the newly added rules.
        s = self.form_closure(new_plines)
        self.shifts[token] = s
        s.note = "%s -> [%s] -> " % (self.i,  token)
        return s

    def form_closure(self, plines):
        closure = lr1_closure(closure=plines, cursor=0, grammar=self.grammar)
        s = State.get(plines=plines, sfrom=self)
        return s

    def get_reduction(self, nxt_tok):
        # is the cursor at the end in any of the plines?
        for pline in self.plines:
            if pline.cursor + 1 >= len(pline.tokens):
                res = nxt_tok in pline.lookahead
                if res: return pline
        # return the production number too for this pline
        return None

    @classmethod
    def construct_states(cls, grammar, start=START_SYMBOL):
        state1 = State.construct_initial_state(grammar, start)
        states = [state1]
        follow = {}
        all_states = set()
        seen = set()
        while states:
            state, *states = states
            if state.i in seen: continue
            seen.add(state.i)
            all_states.add(state)
            sym = symbols(grammar)
            for key in sorted(sym): # needs terminal symbols too.
                if key not in grammar:
                    new_state = state.shift_to(key)
                    if new_state: # and new_state.i not in seen:
                        states.append(new_state)
                        state.hrow[key] = (Action.Shift, new_state.i)
                    else:
                        state.hrow[key] = ('_', None)
                else:
                    new_state = state.go_to(key)
                    if new_state: # and new_state.i not in seen:
                        states.append(new_state)
                        state.hrow[key] = (Action.Goto, new_state.i)
                    else:
                        state.hrow[key] = ('_', None)

        for state in all_states:
            for line in state.plines:
                if line.at(line.cursor) == EOF:
                    key = EOF 
                    state.hrow[key] = (Action.Accept, None)
                elif line.cursor + 1 > len(line.tokens):
                    for key in line.lookahead:
                        state.hrow[key] = (Action.Reduce, line)
        return state1

def parse(input_text, grammar):
    expr_stack = []
    state_stack = [State.registry[1].i]
    tokens = list(input_text)
    next_token = None
    tree = []
    while True:
        if not next_token:
            if not tokens:
                next_token = EOF
            else:
                next_token, *tokens = tokens
        # use the next_token on the state stack to decide what to do.
        (action, nxt) = State.registry[state_stack[-1]].hrow[next_token]
        if action == Action.Shift:
            next_state = State.registry[nxt]
            # this means we can shift.
            expr_stack.append(next_token)
            state_stack.append(next_state.i)
            next_token = None
        elif action == Action.Reduce:
            pline = nxt
            # Remove the matched topmost L symbols (and parse trees and
            # associated state numbers) from the parse stack.
            # pop the plines' rhs symbols off the stack
            pnum = len(pline.tokens)
            popped = expr_stack[-pnum:]
            expr_stack = expr_stack[:-pnum]
            # push the lhs symbol of pline
            expr_stack.append({pline.key: popped})
            # pop the same number of states.
            state_stack = state_stack[:-pnum]
            (action, nxt) = State.registry[state_stack[-1]].hrow[pline.key]
            next_state = State.registry[nxt]
            state_stack.append(next_state.i)
        elif action == Action.Goto:
            next_state = State.registry[nxt]
            state_stack.append(next_state.i)
        elif action == Action.Accept:
            break
        else:
            raise Exception("Syntax error")

    assert len(expr_stack) == 1
    return expr_stack[0]

def initialize(grammar, start):
    grammar[start][0].append(EOF)
    State.construct_states(grammar, start)
