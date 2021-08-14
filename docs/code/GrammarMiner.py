#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Mining Input Grammars" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/GrammarMiner.html
# Last change: 2021-06-04 14:56:57+02:00
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
The Fuzzing Book - Mining Input Grammars

This file can be _executed_ as a script, running all experiments:

    $ python GrammarMiner.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.GrammarMiner import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/GrammarMiner.html

This chapter provides a number of classes to mine input grammars from existing programs.  The function `recover_grammar()` could be the easiest to use.  It takes a function and a set of inputs, and returns a grammar that describes its input language.

We apply `recover_grammar()` on a `url_parse()` function that takes and decomposes URLs:

>>> url_parse('https://www.fuzzingbook.org/')
>>> URLS
['http://user:pass@www.google.com:80/?q=path#ref',
 'https://www.cispa.saarland:80/',
 'http://www.fuzzingbook.org/#News']

We extract the input grammar for `url_parse()` using `recover_grammar()`:

>>> grammar = recover_grammar(url_parse, URLS)
>>> grammar
{'': [''],
 '': [':'],
 '': ['', 'http', 'https'],
 '': ['///',
  '//'],
 '': ['user:pass@www.google.com:80',
  'www.cispa.saarland:80',
  'www.fuzzingbook.org'],
 '': ['/#',
  '#'],
 '': ['/?'],
 '': ['q=path', ''],
 '': ['ref', 'News', '']}

The names of nonterminals are a bit technical; but the grammar nicely represents the structure of the input; for instance, the different schemes (`"http"`, `"https"`) are all identified.
The grammar can be immediately used for fuzzing, producing arbitrary combinations of input elements, which are all syntactically valid.

>>> from GrammarCoverageFuzzer import GrammarCoverageFuzzer
>>> fuzzer = GrammarCoverageFuzzer(grammar)
>>> [fuzzer.fuzz() for i in range(5)]
['http://user:pass@www.google.com:80/?q=path#News',
 'https://www.fuzzingbook.org/',
 'http://www.cispa.saarland:80/#ref',
 'http://user:pass@www.google.com:80/#News',
 'http://www.fuzzingbook.org/#News']

Being able to automatically extract a grammar and to use this grammar for fuzzing makes for very effective test generation with a minimum of manual work.


For more details, source, and documentation, see
"The Fuzzing Book - Mining Input Grammars"
at https://www.fuzzingbook.org/html/GrammarMiner.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Mining Input Grammars
# =====================

if __name__ == '__main__':
    print('# Mining Input Grammars')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## A Grammar Challenge
## -------------------

if __name__ == '__main__':
    print('\n## A Grammar Challenge')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .Parser import process_inventory, process_vehicle, process_car, process_van, lr_graph  # minor dependency

INVENTORY = """\
1997,van,Ford,E350
2000,car,Mercury,Cougar
1999,car,Chevy,Venture\
"""

if __name__ == '__main__':
    print(process_inventory(INVENTORY))

## A Simple Grammar Miner
## ----------------------

if __name__ == '__main__':
    print('\n## A Simple Grammar Miner')



VEHICLES = INVENTORY.split('\n')

INVENTORY_METHODS = {
    'process_inventory',
    'process_vehicle',
    'process_van',
    'process_car'}

### Tracer

if __name__ == '__main__':
    print('\n### Tracer')



from .Coverage import Coverage

import inspect

class Tracer(Coverage):
    def traceit(self, frame, event, arg):
        method_name = inspect.getframeinfo(frame).function
        if method_name not in INVENTORY_METHODS:
            return
        file_name = inspect.getframeinfo(frame).filename

        param_names = inspect.getargvalues(frame).args
        lineno = inspect.getframeinfo(frame).lineno
        local_vars = inspect.getargvalues(frame).locals
        print(event, file_name, lineno, method_name, param_names, local_vars)
        return self.traceit

if __name__ == '__main__':
    with Tracer() as tracer:
        process_vehicle(VEHICLES[0])

### Context

if __name__ == '__main__':
    print('\n### Context')



class Context:
    def __init__(self, frame, track_caller=True):
        self.method = inspect.getframeinfo(frame).function
        self.parameter_names = inspect.getargvalues(frame).args
        self.file_name = inspect.getframeinfo(frame).filename
        self.line_no = inspect.getframeinfo(frame).lineno

    def _t(self):
        return (self.file_name, self.line_no, self.method,
                ','.join(self.parameter_names))

    def __repr__(self):
        return "%s:%d:%s(%s)" % self._t()

class Context(Context):
    def extract_vars(self, frame):
        return inspect.getargvalues(frame).locals

    def parameters(self, all_vars):
        return {k: v for k, v in all_vars.items() if k in self.parameter_names}

    def qualified(self, all_vars):
        return {"%s:%s" % (self.method, k): v for k, v in all_vars.items()}

def log_event(event, var):
    print({'call': '->', 'return': '<-'}.get(event, '  '), var)

class Tracer(Tracer):
    def traceit(self, frame, event, arg):
        log_event(event, Context(frame))
        return self.traceit

if __name__ == '__main__':
    with Tracer() as tracer:
        process_vehicle(VEHICLES[0])

class Tracer(Tracer):
    def __init__(self, my_input, **kwargs):
        self.options(kwargs)
        self.my_input, self.trace = my_input, []

class Tracer(Tracer):
    def options(self, kwargs):
        self.files = kwargs.get('files', [])
        self.methods = kwargs.get('methods', [])
        self.log = log_event if kwargs.get('log') else lambda _evt, _var: None

class Tracer(Tracer):
    def tracing_context(self, cxt, event, arg):
        fres = not self.files or any(
            cxt.file_name.endswith(f) for f in self.files)
        mres = not self.methods or any(cxt.method == m for m in self.methods)
        return fres and mres

class Tracer(Tracer):
    def tracing_var(self, k, v):
        return isinstance(v, str)

class Tracer(Tracer):
    def on_event(self, event, arg, cxt, my_vars):
        self.trace.append((event, arg, cxt, my_vars))
        
    def create_context(self, frame):
        return Context(frame)

    def traceit(self, frame, event, arg):
        cxt = self.create_context(frame)
        if not self.tracing_context(cxt, event, arg):
            return self.traceit
        self.log(event, cxt)

        my_vars = {
            k: v
            for k, v in cxt.extract_vars(frame).items()
            if self.tracing_var(k, v)
        }
        self.on_event(event, arg, cxt, my_vars)
        return self.traceit

if __name__ == '__main__':
    with Tracer(VEHICLES[0], methods=INVENTORY_METHODS, log=True) as tracer:
        process_vehicle(VEHICLES[0])

if __name__ == '__main__':
    for t in tracer.trace:
        print(t[0], t[2].method, dict(t[3]))

if __name__ == '__main__':
    with Tracer(VEHICLES[0], methods=INVENTORY_METHODS, log=True) as tracer:
        process_vehicle(tracer.my_input)

### DefineTracker

if __name__ == '__main__':
    print('\n### DefineTracker')



class DefineTracker:
    def __init__(self, my_input, trace, **kwargs):
        self.options(kwargs)
        self.my_input = my_input
        self.trace = trace
        self.my_assignments = {}
        self.process()

FRAGMENT_LEN = 3

class DefineTracker(DefineTracker):
    def options(self, kwargs):
        self.log = log_event if kwargs.get('log') else lambda _evt, _var: None
        self.fragment_len = kwargs.get('fragment_len', FRAGMENT_LEN)

class DefineTracker(DefineTracker):
    def is_input_fragment(self, var, value):
        return len(value) >= self.fragment_len and value in self.my_input

class DefineTracker(DefineTracker):
    def fragments(self, variables):
        return {k: v for k, v in variables.items(
        ) if self.is_input_fragment(k, v)}

class DefineTracker(DefineTracker):
    def track_event(self, event, arg, cxt, my_vars):
        self.log(event, (cxt.method, my_vars))
        self.my_assignments.update(self.fragments(my_vars))

    def process(self):
        for event, arg, cxt, my_vars in self.trace:
            self.track_event(event, arg, cxt, my_vars)

if __name__ == '__main__':
    tracker = DefineTracker(tracer.my_input, tracer.trace, fragment_len=5)
    for k, v in tracker.my_assignments.items():
        print(k, '=', repr(v))

if __name__ == '__main__':
    tracker = DefineTracker(tracer.my_input, tracer.trace)
    for k, v in tracker.my_assignments.items():
        print(k, '=', repr(v))

class DefineTracker(DefineTracker):
    def assignments(self):
        return self.my_assignments.items()

### Assembling a Derivation Tree

if __name__ == '__main__':
    print('\n### Assembling a Derivation Tree')



from .Grammars import START_SYMBOL, syntax_diagram, is_nonterminal

from .GrammarFuzzer import GrammarFuzzer, FasterGrammarFuzzer, display_tree, tree_to_string

if __name__ == '__main__':
    derivation_tree = (START_SYMBOL, [("1997,van,Ford,E350", [])])

if __name__ == '__main__':
    display_tree(derivation_tree)

if __name__ == '__main__':
    derivation_tree = (START_SYMBOL, [('<vehicle>', [("1997,van,Ford,E350", [])],
                                       [])])

if __name__ == '__main__':
    display_tree(derivation_tree)

if __name__ == '__main__':
    derivation_tree = (START_SYMBOL, [('<vehicle>', [('<year>', [('1997', [])]),
                                                     (",van,Ford,E350", [])], [])])

if __name__ == '__main__':
    display_tree(derivation_tree)

if __name__ == '__main__':
    derivation_tree = (START_SYMBOL, [('<vehicle>', [('<year>', [('1997', [])]),
                                                     (",van,", []),
                                                     ('<company>', [('Ford', [])]),
                                                     (",E350", [])], [])])

if __name__ == '__main__':
    display_tree(derivation_tree)

if __name__ == '__main__':
    derivation_tree = (START_SYMBOL, [('<vehicle>', [('<year>', [('1997', [])]),
                                                     (",", []),
                                                     ("<kind>", [('van', [])]),
                                                     (",", []),
                                                     ('<company>', [('Ford', [])]),
                                                     (",", []),
                                                     ("<model>", [('E350', [])])
                                                     ], [])])

if __name__ == '__main__':
    display_tree(derivation_tree)

class TreeMiner:
    def __init__(self, my_input, my_assignments, **kwargs):
        self.options(kwargs)
        self.my_input = my_input
        self.my_assignments = my_assignments
        self.tree = self.get_derivation_tree()

    def options(self, kwargs):
        self.log = log_call if kwargs.get('log') else lambda _i, _v: None

    def get_derivation_tree(self):
        return (START_SYMBOL, [])

def log_call(indent, var):
    print('\t' * indent, var)

def to_nonterminal(var):
    return "<" + var.lower() + ">"

class TreeMiner(TreeMiner):
    def string_part_of_value(self, part, value):
        return (part in value)

class TreeMiner(TreeMiner):
    def partition(self, part, value):
        return value.partition(part)

class TreeMiner(TreeMiner):
    def partition_by_part(self, pair, value):
        k, part = pair
        prefix_k_suffix = [
                    (k, [[part, []]]) if i == 1 else (e, [])
                    for i, e in enumerate(self.partition(part, value))
                    if e]
        return prefix_k_suffix

class TreeMiner(TreeMiner):
    def insert_into_tree(self, my_tree, pair):
        var, values = my_tree
        k, v = pair
        self.log(1, "- Node: %s\t\t? (%s:%s)" % (var, k, repr(v)))
        applied = False
        for i, value_ in enumerate(values):
            value, arr = value_
            self.log(2, "-> [%d] %s" % (i, repr(value)))
            if is_nonterminal(value):
                applied = self.insert_into_tree(value_, pair)
                if applied:
                    break
            elif self.string_part_of_value(v, value):
                prefix_k_suffix = self.partition_by_part(pair, value)
                del values[i]
                for j, rep in enumerate(prefix_k_suffix):
                    values.insert(j + i, rep)
                applied = True

                self.log(2, " > %s" % (repr([i[0] for i in prefix_k_suffix])))
                break
            else:
                continue
        return applied

if __name__ == '__main__':
    tree = (START_SYMBOL, [("1997,van,Ford,E350", [])])
    m = TreeMiner('', {}, log=True)

if __name__ == '__main__':
    display_tree(tree)

if __name__ == '__main__':
    v = m.insert_into_tree(tree, ('<vehicle>', "1997,van,Ford,E350"))

if __name__ == '__main__':
    display_tree(tree)

if __name__ == '__main__':
    v = m.insert_into_tree(tree, ('<model>', 'E350'))

if __name__ == '__main__':
    display_tree((tree))

if __name__ == '__main__':
    v = m.insert_into_tree(tree, ('<company>', 'Ford'))

if __name__ == '__main__':
    display_tree(tree)

if __name__ == '__main__':
    v = m.insert_into_tree(tree, ('<kind>', 'van'))

if __name__ == '__main__':
    display_tree(tree)

if __name__ == '__main__':
    v = m.insert_into_tree(tree, ('<year>', '1997'))

if __name__ == '__main__':
    display_tree(tree)

class TreeMiner(TreeMiner):
    def nt_var(self, var):
        return var if is_nonterminal(var) else to_nonterminal(var)

class TreeMiner(TreeMiner):
    def apply_new_definition(self, tree, var, value):
        nt_var = self.nt_var(var)
        return self.insert_into_tree(tree, (nt_var, value))

class TreeMiner(TreeMiner):
    def get_derivation_tree(self):
        tree = (START_SYMBOL, [(self.my_input, [])])

        for var, value in self.my_assignments:
            self.log(0, "%s=%s" % (var, repr(value)))
            self.apply_new_definition(tree, var, value)
        return tree

if __name__ == '__main__':
    with Tracer(VEHICLES[0]) as tracer:
        process_vehicle(tracer.my_input)
    assignments = DefineTracker(tracer.my_input, tracer.trace).assignments()
    dt = TreeMiner(tracer.my_input, assignments, log=True)
    dt.tree

if __name__ == '__main__':
    display_tree(TreeMiner(tracer.my_input, assignments).tree)

if __name__ == '__main__':
    trees = []
    for vehicle in VEHICLES:
        print(vehicle)
        with Tracer(vehicle) as tracer:
            process_vehicle(tracer.my_input)
        assignments = DefineTracker(tracer.my_input, tracer.trace).assignments()
        trees.append((tracer.my_input, assignments))
        for var, val in assignments:
            print(var + " = " + repr(val))
        print()

if __name__ == '__main__':
    csv_dt = []
    for inputstr, assignments in trees:
        print(inputstr)
        dt = TreeMiner(inputstr, assignments)
        csv_dt.append(dt)
        display_tree(dt.tree)

### Recovering Grammars from Derivation Trees

if __name__ == '__main__':
    print('\n### Recovering Grammars from Derivation Trees')



class GrammarMiner:
    def __init__(self):
        self.grammar = {}

class GrammarMiner(GrammarMiner):
    def tree_to_grammar(self, tree):
        node, children = tree
        one_alt = [ck for ck, gc in children]
        hsh = {node: [one_alt] if one_alt else []}
        for child in children:
            if not is_nonterminal(child[0]):
                continue
            chsh = self.tree_to_grammar(child)
            for k in chsh:
                if k not in hsh:
                    hsh[k] = chsh[k]
                else:
                    hsh[k].extend(chsh[k])
        return hsh

if __name__ == '__main__':
    gm = GrammarMiner()
    gm.tree_to_grammar(csv_dt[0].tree)

def readable(grammar):
    def readable_rule(rule):
        return ''.join(rule)

    return {k: list(set(readable_rule(a) for a in grammar[k]))
            for k in grammar}

if __name__ == '__main__':
    syntax_diagram(readable(gm.tree_to_grammar(csv_dt[0].tree)))

import itertools

class GrammarMiner(GrammarMiner):
    def add_tree(self, t):
        t_grammar = self.tree_to_grammar(t.tree)
        self.grammar = {
            key: self.grammar.get(key, []) + t_grammar.get(key, [])
            for key in itertools.chain(self.grammar.keys(), t_grammar.keys())
        }

if __name__ == '__main__':
    inventory_grammar = GrammarMiner()
    for dt in csv_dt:
        inventory_grammar.add_tree(dt)

if __name__ == '__main__':
    syntax_diagram(readable(inventory_grammar.grammar))

class GrammarMiner(GrammarMiner):
    def update_grammar(self, inputstr, trace):
        at = self.create_tracker(inputstr, trace)
        dt = self.create_tree_miner(inputstr, at.assignments())
        self.add_tree(dt)
        return self.grammar

    def create_tracker(self, *args):
        return DefineTracker(*args)

    def create_tree_miner(self, *args):
        return TreeMiner(*args)

def recover_grammar(fn, inputs, **kwargs):
    miner = GrammarMiner()
    for inputstr in inputs:
        with Tracer(inputstr, **kwargs) as tracer:
            fn(tracer.my_input)
        miner.update_grammar(tracer.my_input, tracer.trace)
    return readable(miner.grammar)

#### Example 1. Recovering the Inventory Grammar

if __name__ == '__main__':
    print('\n#### Example 1. Recovering the Inventory Grammar')



if __name__ == '__main__':
    inventory_grammar = recover_grammar(process_vehicle, VEHICLES)

if __name__ == '__main__':
    inventory_grammar

#### Example 2. Recovering URL Grammar

if __name__ == '__main__':
    print('\n#### Example 2. Recovering URL Grammar')



URLS = [
    'http://user:pass@www.google.com:80/?q=path#ref',
    'https://www.cispa.saarland:80/',
    'http://www.fuzzingbook.org/#News',
]

from urllib.parse import urlparse, clear_cache

def url_parse(url):
    clear_cache()
    urlparse(url)

if __name__ == '__main__':
    trees = []
    for url in URLS:
        print(url)
        with Tracer(url) as tracer:
            url_parse(tracer.my_input)
        assignments = DefineTracker(tracer.my_input, tracer.trace).assignments()
        trees.append((tracer.my_input, assignments))
        for var, val in assignments:
            print(var + " = " + repr(val))
        print()


    url_dt = []
    for inputstr, assignments in trees:
        print(inputstr)
        dt = TreeMiner(inputstr, assignments)
        url_dt.append(dt)
        display_tree(dt.tree)

if __name__ == '__main__':
    url_grammar = recover_grammar(url_parse, URLS, files=['urllib/parse.py'])

if __name__ == '__main__':
    syntax_diagram(url_grammar)

### Fuzzing

if __name__ == '__main__':
    print('\n### Fuzzing')



if __name__ == '__main__':
    f = GrammarFuzzer(inventory_grammar)
    for _ in range(10):
        print(f.fuzz())

if __name__ == '__main__':
    f = GrammarFuzzer(url_grammar)
    for _ in range(10):
        print(f.fuzz())

### Problems with the Simple Miner

if __name__ == '__main__':
    print('\n### Problems with the Simple Miner')



URLS_X = URLS + ['ftp://freebsd.org/releases/5.8']

if __name__ == '__main__':
    url_grammar = recover_grammar(url_parse, URLS_X, files=['urllib/parse.py'])

if __name__ == '__main__':
    syntax_diagram(url_grammar)

if __name__ == '__main__':
    clear_cache()
    with Tracer(URLS_X[0]) as tracer:
        urlparse(tracer.my_input)
    for i, t in enumerate(tracer.trace):
        if t[0] in {'call', 'line'} and 'parse.py' in str(t[2]) and t[3]:
            print(i, t[2]._t()[1], t[3:])

## Grammar Miner with Reassignment
## -------------------------------

if __name__ == '__main__':
    print('\n## Grammar Miner with Reassignment')



### Tracking variable assignment locations

if __name__ == '__main__':
    print('\n### Tracking variable assignment locations')



def C(cp_1):
    c_2 = cp_1 + '@2'
    c_3 = c_2 + '@3'
    return c_3


def B(bp_7):
    b_8 = bp_7 + '@8'
    return C(b_8)


def A(ap_12):
    a_13 = ap_12 + '@13'
    a_14 = B(a_13) + '@14'
    a_14 = a_14 + '@15'
    a_13 = a_14 + '@16'
    a_14 = B(a_13) + '@17'
    a_14 = B(a_13) + '@18'

if __name__ == '__main__':
    with Tracer('____') as tracer:
        A(tracer.my_input)

    for t in tracer.trace:
        print(t[0], "%d:%s" % (t[2].line_no, t[2].method), t[3])

### CallStack

if __name__ == '__main__':
    print('\n### CallStack')



class CallStack:
    def __init__(self, **kwargs):
        self.options(kwargs)
        self.method_id = (START_SYMBOL, 0)
        self.method_register = 0
        self.mstack = [self.method_id]

    def enter(self, method):
        self.method_register += 1
        self.method_id = (method, self.method_register)
        self.log('call', "%s%s" % (self.indent(), str(self)))
        self.mstack.append(self.method_id)

    def leave(self):
        self.mstack.pop()
        self.log('return', "%s%s" % (self.indent(), str(self)))
        self.method_id = self.mstack[-1]

class CallStack(CallStack):
    def options(self, kwargs):
        self.log = log_event if kwargs.get('log') else lambda _evt, _var: None

    def indent(self):
        return len(self.mstack) * "\t"

    def at(self, n):
        return self.mstack[n]

    def __len__(self):
        return len(mstack) - 1

    def __str__(self):
        return "%s:%d" % self.method_id

    def __repr__(self):
        return repr(self.method_id)

def display_stack(istack):
    def stack_to_tree(stack):
        current, *rest = stack
        if not rest:
            return (repr(current), [])
        return (repr(current), [stack_to_tree(rest)])
    display_tree(stack_to_tree(istack.mstack), graph_attr=lr_graph)

if __name__ == '__main__':
    cs = CallStack()
    display_stack(cs)
    cs

if __name__ == '__main__':
    cs.enter('hello')
    display_stack(cs)
    cs

if __name__ == '__main__':
    cs.enter('world')
    display_stack(cs)
    cs

if __name__ == '__main__':
    cs.leave()
    display_stack(cs)
    cs

if __name__ == '__main__':
    cs.enter('world')
    display_stack(cs)
    cs

if __name__ == '__main__':
    cs.leave()
    display_stack(cs)
    cs

### Vars

if __name__ == '__main__':
    print('\n### Vars')



class Vars:
    def __init__(self, original):
        self.defs = {}
        self.my_input = original

class Vars(Vars):
    def _set_kv(self, k, v):
        self.defs[k] = v

    def __setitem__(self, k, v):
        self._set_kv(k, v)

    def update(self, v):
        for k, v in v.items():
            self._set_kv(k, v)

if __name__ == '__main__':
    v = Vars('')
    v.defs

if __name__ == '__main__':
    v['x'] = 'X'
    v.defs

if __name__ == '__main__':
    v.update({'x': 'x', 'y': 'y'})
    v.defs

### AssignmentVars

if __name__ == '__main__':
    print('\n### AssignmentVars')



class AssignmentVars(Vars):
    def __init__(self, original):
        super().__init__(original)
        self.accessed_seq_var = {}
        self.var_def_lines = {}
        self.current_event = None
        self.new_vars = set()
        self.method_init()

class AssignmentVars(AssignmentVars):
    def method_init(self):
        self.call_stack = CallStack()
        self.event_locations = {self.call_stack.method_id: []}

class AssignmentVars(AssignmentVars):
    def update(self, v):
        for k, v in v.items():
            self._set_kv(k, v)
        self.var_location_register(self.new_vars)
        self.new_vars = set()

class AssignmentVars(AssignmentVars):
    def var_name(self, var):
        return (var, self.accessed_seq_var[var])

class AssignmentVars(AssignmentVars):
    def var_access(self, var):
        if var not in self.accessed_seq_var:
            self.accessed_seq_var[var] = 0
        return self.var_name(var)

class AssignmentVars(AssignmentVars):
    def var_assign(self, var):
        self.accessed_seq_var[var] += 1
        self.new_vars.add(self.var_name(var))
        return self.var_name(var)

if __name__ == '__main__':
    sav = AssignmentVars('')
    sav.defs

if __name__ == '__main__':
    sav.var_access('v1')

if __name__ == '__main__':
    sav.var_assign('v1')

if __name__ == '__main__':
    sav.var_assign('v1')

class AssignmentVars(AssignmentVars):
    def _set_kv(self, var, val):
        s_var = self.var_access(var)
        if s_var in self.defs and self.defs[s_var] == val:
            return
        self.defs[self.var_assign(var)] = val

if __name__ == '__main__':
    sav = AssignmentVars('')
    sav['x'] = 'X'
    sav.defs

if __name__ == '__main__':
    sav['x'] = 'X'
    sav.defs

if __name__ == '__main__':
    sav['x'] = 'Y'
    sav.defs

class AssignmentVars(AssignmentVars):
    def method_enter(self, cxt, my_vars):
        self.current_event = 'call'
        self.call_stack.enter(cxt.method)
        self.event_locations[self.call_stack.method_id] = []
        self.register_event(cxt)
        self.update(my_vars)

    def method_exit(self, cxt, my_vars):
        self.current_event = 'return'
        self.register_event(cxt)
        self.update(my_vars)
        self.call_stack.leave()

    def method_statement(self, cxt, my_vars):
        self.current_event = 'line'
        self.register_event(cxt)
        self.update(my_vars)

class AssignmentVars(AssignmentVars):
    def register_event(self, cxt):
        self.event_locations[self.call_stack.method_id].append(cxt.line_no)

class AssignmentVars(AssignmentVars):
    def var_location_register(self, my_vars):
        def loc(mid):
            if self.current_event == 'call':
                return self.event_locations[mid][-1]
            elif self.current_event == 'line':
                return self.event_locations[mid][-2]
            elif self.current_event == 'return':
                return self.event_locations[mid][-2]
            else:
                assert False

        my_loc = loc(self.call_stack.method_id)
        for var in my_vars:
            self.var_def_lines[var] = my_loc

class AssignmentVars(AssignmentVars):
    def defined_vars(self, formatted=True):
        def fmt(k):
            v = (k[0], self.var_def_lines[k])
            return "%s@%s" % v if formatted else v

        return [(fmt(k), v) for k, v in self.defs.items()]

class AssignmentVars(AssignmentVars):
    def seq_vars(self, formatted=True):
        def fmt(k):
            v = (k[0], self.var_def_lines[k], k[1])
            return "%s@%s:%s" % v if formatted else v

        return {fmt(k): v for k, v in self.defs.items()}

### AssignmentTracker

if __name__ == '__main__':
    print('\n### AssignmentTracker')



class AssignmentTracker(DefineTracker):
    def __init__(self, my_input, trace, **kwargs):
        self.options(kwargs)
        self.my_input = my_input

        self.my_assignments = self.create_assignments(my_input)

        self.trace = trace
        self.process()

    def create_assignments(self, *args):
        return AssignmentVars(*args)

class AssignmentTracker(AssignmentTracker):
    def options(self, kwargs):
        self.track_return = kwargs.get('track_return', False)
        super().options(kwargs)

class AssignmentTracker(AssignmentTracker):
    def on_call(self, arg, cxt, my_vars):
        my_vars = cxt.parameters(my_vars)
        self.my_assignments.method_enter(cxt, self.fragments(my_vars))

    def on_line(self, arg, cxt, my_vars):
        self.my_assignments.method_statement(cxt, self.fragments(my_vars))

    def on_return(self, arg, cxt, my_vars):
        self.on_line(arg, cxt, my_vars)
        my_vars = {'<-%s' % cxt.method: arg} if self.track_return else {}
        self.my_assignments.method_exit(cxt, my_vars)

    def on_exception(self, arg, cxt, my_vara):
        return

    def track_event(self, event, arg, cxt, my_vars):
        self.current_event = event
        dispatch = {
            'call': self.on_call,
            'return': self.on_return,
            'line': self.on_line,
            'exception': self.on_exception
        }
        dispatch[event](arg, cxt, my_vars)

def C(cp_1):
    c_2 = cp_1
    c_3 = c_2
    return c_3


def B(bp_7):
    b_8 = bp_7
    return C(b_8)


def A(ap_12):
    a_13 = ap_12
    a_14 = B(a_13)
    a_14 = a_14
    a_13 = a_14
    a_14 = B(a_13)
    a_14 = B(a_14)[3:]

if __name__ == '__main__':
    with Tracer('---xxx') as tracer:
        A(tracer.my_input)
    tracker = AssignmentTracker(tracer.my_input, tracer.trace, log=True)
    for k, v in tracker.my_assignments.seq_vars().items():
        print(k, '=', repr(v))
    print()
    for k, v in tracker.my_assignments.defined_vars(formatted=True):
        print(k, '=', repr(v))

if __name__ == '__main__':
    traces = []
    for inputstr in URLS_X:
        clear_cache()
        with Tracer(inputstr, files=['urllib/parse.py']) as tracer:
            urlparse(tracer.my_input)
        traces.append((tracer.my_input, tracer.trace))

        tracker = AssignmentTracker(tracer.my_input, tracer.trace, log=True)
        for k, v in tracker.my_assignments.defined_vars():
            print(k, '=', repr(v))
        print()

### Recovering a Derivation Tree

if __name__ == '__main__':
    print('\n### Recovering a Derivation Tree')



class TreeMiner(TreeMiner):
    def get_derivation_tree(self):
        tree = (START_SYMBOL, [(self.my_input, [])])
        for var, value in self.my_assignments:
            self.log(0, "%s=%s" % (var, repr(value)))
            self.apply_new_definition(tree, var, value)
        return tree

#### Example 1: Recovering URL Derivation Tree

if __name__ == '__main__':
    print('\n#### Example 1: Recovering URL Derivation Tree')



##### URL 1 derivation tree

if __name__ == '__main__':
    print('\n##### URL 1 derivation tree')



if __name__ == '__main__':
    clear_cache()
    with Tracer(URLS_X[0], files=['urllib/parse.py']) as tracer:
        urlparse(tracer.my_input)
    sm = AssignmentTracker(tracer.my_input, tracer.trace)
    dt = TreeMiner(tracer.my_input, sm.my_assignments.defined_vars())
    display_tree(dt.tree)

##### URL 4 derivation tree

if __name__ == '__main__':
    print('\n##### URL 4 derivation tree')



if __name__ == '__main__':
    clear_cache()
    with Tracer(URLS_X[-1], files=['urllib/parse.py']) as tracer:
        urlparse(tracer.my_input)
    sm = AssignmentTracker(tracer.my_input, tracer.trace)
    dt = TreeMiner(tracer.my_input, sm.my_assignments.defined_vars())
    display_tree(dt.tree)

### Recover Grammar

if __name__ == '__main__':
    print('\n### Recover Grammar')



class GrammarMiner(GrammarMiner):
    def update_grammar(self, inputstr, trace):
        at = self.create_tracker(inputstr, trace)
        dt = self.create_tree_miner(inputstr, at.my_assignments.defined_vars())
        self.add_tree(dt)
        return self.grammar

    def create_tracker(self, *args):
        return AssignmentTracker(*args)

    def create_tree_miner(self, *args):
        return TreeMiner(*args)

if __name__ == '__main__':
    url_grammar = recover_grammar(url_parse, URLS_X, files=['urllib/parse.py'])

if __name__ == '__main__':
    syntax_diagram(url_grammar)

if __name__ == '__main__':
    f = GrammarFuzzer(url_grammar)
    for _ in range(10):
        print(f.fuzz())

#### Example 2: Recovering Inventory Grammar

if __name__ == '__main__':
    print('\n#### Example 2: Recovering Inventory Grammar')



if __name__ == '__main__':
    inventory_grammar = recover_grammar(process_vehicle, VEHICLES)

if __name__ == '__main__':
    syntax_diagram(inventory_grammar)

if __name__ == '__main__':
    f = GrammarFuzzer(inventory_grammar)
    for _ in range(10):
        print(f.fuzz())

### Problems with the Grammar Miner with Reassignment

if __name__ == '__main__':
    print('\n### Problems with the Grammar Miner with Reassignment')



if __name__ == '__main__':
    with Tracer(INVENTORY) as tracer:
        process_inventory(tracer.my_input)
    sm = AssignmentTracker(tracer.my_input, tracer.trace)
    dt = TreeMiner(tracer.my_input, sm.my_assignments.defined_vars())
    display_tree(dt.tree, graph_attr=lr_graph)

if __name__ == '__main__':
    dt = TreeMiner(tracer.my_input, sm.my_assignments.defined_vars(), log=True)

## A Grammar Miner with Scope
## --------------------------

if __name__ == '__main__':
    print('\n## A Grammar Miner with Scope')



### Input Stack

if __name__ == '__main__':
    print('\n### Input Stack')



class InputStack(CallStack):
    def __init__(self, i, fragment_len=FRAGMENT_LEN):
        self.inputs = [{START_SYMBOL: i}]
        self.fragment_len = fragment_len
        super().__init__()

class InputStack(InputStack):
    def in_current_record(self, val):
        return any(val in var for var in self.inputs[-1].values())

if __name__ == '__main__':
    my_istack = InputStack('hello my world')

if __name__ == '__main__':
    my_istack.in_current_record('hello')

if __name__ == '__main__':
    my_istack.in_current_record('bye')

if __name__ == '__main__':
    my_istack.inputs.append({'greeting': 'hello', 'location': 'world'})

if __name__ == '__main__':
    my_istack.in_current_record('hello')

if __name__ == '__main__':
    my_istack.in_current_record('my')

class InputStack(InputStack):
    def ignored(self, val):
        return not (isinstance(val, str) and len(val) >= self.fragment_len)

if __name__ == '__main__':
    my_istack = InputStack('hello world')
    my_istack.ignored(1)

if __name__ == '__main__':
    my_istack.ignored('a')

if __name__ == '__main__':
    my_istack.ignored('help')

class InputStack(InputStack):
    def in_scope(self, k, val):
        if self.ignored(val):
            return False
        return self.in_current_record(val)

class InputStack(InputStack):
    def enter(self, method, inputs):
        my_inputs = {k: v for k, v in inputs.items() if self.in_scope(k, v)}
        self.inputs.append(my_inputs)
        super().enter(method)

class InputStack(InputStack):
    def leave(self):
        self.inputs.pop()
        super().leave()

### ScopedVars

if __name__ == '__main__':
    print('\n### ScopedVars')



class ScopedVars(AssignmentVars):
    def method_init(self):
        self.call_stack = self.create_call_stack(self.my_input)
        self.event_locations = {self.call_stack.method_id: []}

    def create_call_stack(self, i):
        return InputStack(i)

class ScopedVars(ScopedVars):
    def method_enter(self, cxt, my_vars):
        self.current_event = 'call'
        self.call_stack.enter(cxt.method, my_vars)
        self.accessed_seq_var[self.call_stack.method_id] = {}
        self.event_locations[self.call_stack.method_id] = []
        self.register_event(cxt)
        self.update(my_vars)

class ScopedVars(ScopedVars):
    def update(self, v):
        if self.current_event == 'call':
            context = -2
        elif self.current_event == 'line':
            context = -1
        else:
            context = -1
        for k, v in v.items():
            self._set_kv(k, (v, self.call_stack.at(context)))
        self.var_location_register(self.new_vars)
        self.new_vars = set()

class ScopedVars(ScopedVars):
    def var_name(self, var):
        return (var, self.call_stack.method_id,
                self.accessed_seq_var[self.call_stack.method_id][var])

class ScopedVars(ScopedVars):
    def var_access(self, var):
        if var not in self.accessed_seq_var[self.call_stack.method_id]:
            self.accessed_seq_var[self.call_stack.method_id][var] = 0
        return self.var_name(var)

class ScopedVars(ScopedVars):
    def var_assign(self, var):
        self.accessed_seq_var[self.call_stack.method_id][var] += 1
        self.new_vars.add(self.var_name(var))
        return self.var_name(var)

class ScopedVars(ScopedVars):
    def defined_vars(self, formatted=True):
        def fmt(k):
            method, i = k[1]
            v = (method, i, k[0], self.var_def_lines[k])
            return "%s[%d]:%s@%s" % v if formatted else v

        return [(fmt(k), v) for k, v in self.defs.items()]

class ScopedVars(ScopedVars):
    def seq_vars(self, formatted=True):
        def fmt(k):
            method, i = k[1]
            v = (method, i, k[0], self.var_def_lines[k], k[2])
            return "%s[%d]:%s@%s:%s" % v if formatted else v

        return {fmt(k): v for k, v in self.defs.items()}

### Scope Tracker

if __name__ == '__main__':
    print('\n### Scope Tracker')



class ScopeTracker(AssignmentTracker):
    def __init__(self, my_input, trace, **kwargs):
        self.current_event = None
        super().__init__(my_input, trace, **kwargs)

    def create_assignments(self, *args):
        return ScopedVars(*args)

class ScopeTracker(ScopeTracker):
    def is_input_fragment(self, var, value):
        return self.my_assignments.call_stack.in_scope(var, value)

if __name__ == '__main__':
    vehicle_traces = []
    with Tracer(INVENTORY) as tracer:
        process_inventory(tracer.my_input)
    sm = ScopeTracker(tracer.my_input, tracer.trace)
    vehicle_traces.append((tracer.my_input, sm))
    for k, v in sm.my_assignments.seq_vars().items():
        print(k, '=', repr(v))

### Recovering a Derivation Tree

if __name__ == '__main__':
    print('\n### Recovering a Derivation Tree')



class ScopeTreeMiner(TreeMiner):
    def mseq(self, key):
        method, seq, var, lno = key
        return seq

class ScopeTreeMiner(ScopeTreeMiner):
    def nt_var(self, key):
        method, seq, var, lno = key
        return to_nonterminal("%s@%d:%s" % (method, lno, var))

class ScopeTreeMiner(ScopeTreeMiner):
    def partition(self, part, value):
        return value.partition(part)
    def partition_by_part(self, pair, value):
        (nt_var, nt_seq), (v, v_scope) = pair
        prefix_k_suffix = [
                    (nt_var, [(v, [], nt_seq)]) if i == 1 else (e, [])
                    for i, e in enumerate(self.partition(v, value))
                    if e]
        return prefix_k_suffix
    
    def insert_into_tree(self, my_tree, pair):
        var, values, my_scope = my_tree
        (nt_var, nt_seq), (v, v_scope) = pair
        applied = False
        for i, value_ in enumerate(values):
            key, arr, scope = value_
            self.log(2, "-> [%d] %s" % (i, repr(value_)))
            if is_nonterminal(key):
                applied = self.insert_into_tree(value_, pair)
                if applied:
                    break
            else:
                if v_scope != scope:
                    if nt_seq > scope:
                        continue
                if not v or not self.string_part_of_value(v, key):
                    continue
                prefix_k_suffix = [(k, children, scope) for k, children
                                   in self.partition_by_part(pair, key)]
                del values[i]
                for j, rep in enumerate(prefix_k_suffix):
                    values.insert(j + i, rep)

                applied = True
                self.log(2, " > %s" % (repr([i[0] for i in prefix_k_suffix])))
                break
        return applied

class ScopeTreeMiner(ScopeTreeMiner):
    def apply_new_definition(self, tree, var, value_):
        nt_var = self.nt_var(var)
        seq = self.mseq(var)
        val, (smethod, mseq) = value_
        return self.insert_into_tree(tree, ((nt_var, seq), (val, mseq)))

class ScopeTreeMiner(ScopeTreeMiner):
    def get_derivation_tree(self):
        tree = (START_SYMBOL, [(self.my_input, [], 0)], 0)
        for var, value in self.my_assignments:
            self.log(0, "%s=%s" % (var, repr(value)))
            self.apply_new_definition(tree, var, value)
        return tree

#### Example 1: Recovering URL Parse Tree

if __name__ == '__main__':
    print('\n#### Example 1: Recovering URL Parse Tree')



if __name__ == '__main__':
    url_dts = []
    for inputstr in URLS_X:
        clear_cache()
        with Tracer(inputstr, files=['urllib/parse.py']) as tracer:
            urlparse(tracer.my_input)
        sm = ScopeTracker(tracer.my_input, tracer.trace)
        for k, v in sm.my_assignments.defined_vars(formatted=False):
            print(k, '=', repr(v))
        dt = ScopeTreeMiner(
            tracer.my_input,
            sm.my_assignments.defined_vars(
                formatted=False))
        display_tree(dt.tree, graph_attr=lr_graph)
        url_dts.append(dt)

#### Example 2: Recovering Inventory Parse Tree

if __name__ == '__main__':
    print('\n#### Example 2: Recovering Inventory Parse Tree')



if __name__ == '__main__':
    with Tracer(INVENTORY) as tracer:
        process_inventory(tracer.my_input)

    sm = ScopeTracker(tracer.my_input, tracer.trace)
    for k, v in sm.my_assignments.defined_vars():
        print(k, '=', repr(v))
    inventory_dt = ScopeTreeMiner(
        tracer.my_input,
        sm.my_assignments.defined_vars(
            formatted=False))
    display_tree(inventory_dt.tree, graph_attr=lr_graph)

### Grammar Mining

if __name__ == '__main__':
    print('\n### Grammar Mining')



class ScopedGrammarMiner(GrammarMiner):
    def tree_to_grammar(self, tree):
        key, children, scope = tree
        one_alt = [ckey for ckey, gchildren, cscope in children if ckey != key]
        hsh = {key: [one_alt] if one_alt else []}
        for child in children:
            (ckey, _gc, _cscope) = child
            if not is_nonterminal(ckey):
                continue
            chsh = self.tree_to_grammar(child)
            for k in chsh:
                if k not in hsh:
                    hsh[k] = chsh[k]
                else:
                    hsh[k].extend(chsh[k])
        return hsh

if __name__ == '__main__':
    si = ScopedGrammarMiner()
    si.add_tree(inventory_dt)
    syntax_diagram(readable(si.grammar))

if __name__ == '__main__':
    su = ScopedGrammarMiner()
    for url_dt in url_dts:
        su.add_tree(url_dt)
    syntax_diagram(readable(su.grammar))

class ScopedGrammarMiner(ScopedGrammarMiner):
    def get_replacements(self, grammar):
        replacements = {}
        for k in grammar:
            if k == START_SYMBOL:
                continue
            alts = grammar[k]
            if len(set([str(i) for i in alts])) != 1:
                continue
            rule = alts[0]
            if len(rule) != 1:
                continue
            tok = rule[0]
            if not is_nonterminal(tok):
                continue
            replacements[k] = tok
        return replacements

class ScopedGrammarMiner(ScopedGrammarMiner):
    def clean_grammar(self):
        replacements = self.get_replacements(self.grammar)

        while True:
            changed = set()
            for k in self.grammar:
                if k in replacements:
                    continue
                new_alts = []
                for alt in self.grammar[k]:
                    new_alt = []
                    for t in alt:
                        if t in replacements:
                            new_alt.append(replacements[t])
                            changed.add(t)
                        else:
                            new_alt.append(t)
                    new_alts.append(new_alt)
                self.grammar[k] = new_alts
            if not changed:
                break
            for k in changed:
                self.grammar.pop(k, None)
        return readable(self.grammar)

if __name__ == '__main__':
    si = ScopedGrammarMiner()
    si.add_tree(inventory_dt)
    syntax_diagram(readable(si.clean_grammar()))

class ScopedGrammarMiner(ScopedGrammarMiner):
    def update_grammar(self, inputstr, trace):
        at = self.create_tracker(inputstr, trace)
        dt = self.create_tree_miner(
            inputstr, at.my_assignments.defined_vars(
                formatted=False))
        self.add_tree(dt)
        return self.grammar

    def create_tracker(self, *args):
        return ScopeTracker(*args)

    def create_tree_miner(self, *args):
        return ScopeTreeMiner(*args)

def recover_grammar(fn, inputs, **kwargs):
    miner = ScopedGrammarMiner()
    for inputstr in inputs:
        with Tracer(inputstr, **kwargs) as tracer:
            fn(tracer.my_input)
        miner.update_grammar(tracer.my_input, tracer.trace)
    return readable(miner.clean_grammar())

if __name__ == '__main__':
    url_grammar = recover_grammar(url_parse, URLS_X, files=['urllib/parse.py'])

if __name__ == '__main__':
    syntax_diagram(url_grammar)

if __name__ == '__main__':
    f = GrammarFuzzer(url_grammar)
    for _ in range(10):
        print(f.fuzz())

if __name__ == '__main__':
    inventory_grammar = recover_grammar(process_inventory, [INVENTORY])

if __name__ == '__main__':
    syntax_diagram(inventory_grammar)

if __name__ == '__main__':
    f = GrammarFuzzer(inventory_grammar)
    for _ in range(10):
        print(f.fuzz())

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    url_parse('https://www.fuzzingbook.org/')

if __name__ == '__main__':
    URLS

if __name__ == '__main__':
    grammar = recover_grammar(url_parse, URLS)
    grammar

from .GrammarCoverageFuzzer import GrammarCoverageFuzzer

if __name__ == '__main__':
    fuzzer = GrammarCoverageFuzzer(grammar)
    [fuzzer.fuzz() for i in range(5)]

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



### Exercise 1: Flattening complex objects

if __name__ == '__main__':
    print('\n### Exercise 1: Flattening complex objects')



class Vehicle:
    def __init__(self, vehicle):
        year, kind, company, model, *_ = vehicle.split(',')
        self.year, self.kind, self.company, self.model = year, kind, company, model

def process_inventory(inventory):
    res = []
    for vehicle in inventory.split('\n'):
        ret = process_vehicle(vehicle)
        res.extend(ret)
    return '\n'.join(res)

def process_vehicle(vehicle):
    v = Vehicle(vehicle)
    if v.kind == 'van':
        return process_van(v)

    elif v.kind == 'car':
        return process_car(v)

    else:
        raise Exception('Invalid entry')

def process_van(vehicle):
    res = [
        "We have a %s %s van from %s vintage." % (vehicle.company,
                                                  vehicle.model, vehicle.year)
    ]
    iyear = int(vehicle.year)
    if iyear > 2010:
        res.append("It is a recent model!")
    else:
        res.append("It is an old but reliable model!")
    return res

def process_car(vehicle):
    res = [
        "We have a %s %s car from %s vintage." % (vehicle.company,
                                                  vehicle.model, vehicle.year)
    ]
    iyear = int(vehicle.year)
    if iyear > 2016:
        res.append("It is a recent model!")
    else:
        res.append("It is an old but reliable model!")
    return res

if __name__ == '__main__':
    vehicle_grammar = recover_grammar(
        process_inventory,
        [INVENTORY],
        methods=INVENTORY_METHODS)

if __name__ == '__main__':
    syntax_diagram(vehicle_grammar)

if __name__ == '__main__':
    with Tracer(INVENTORY, methods=INVENTORY_METHODS, log=True) as tracer:
        process_inventory(tracer.my_input)
    print()
    print('Traced values:')
    for t in tracer.trace:
        print(t)

MAX_DEPTH = 10

def set_flatten_depth(depth):
    global MAX_DEPTH
    MAX_DEPTH = depth

def flatten(key, val, depth=MAX_DEPTH):
    tv = type(val)
    if depth <= 0:
        return [(key, val)]
    if isinstance(val, (int, float, complex, str, bytes, bytearray)):
        return [(key, val)]
    elif isinstance(val, (set, frozenset, list, tuple, range)):
        values = [(i, e) for i, elt in enumerate(val) for e in flatten(i, elt, depth-1)]
        return [("%s.%d" % (key, i), v) for i, v in values]
    elif isinstance(val, dict):
        values = [e for k, elt in val.items() for e in flatten(k, elt, depth-1)]
        return [("%s.%s" % (key, k), v) for k, v in values]
    elif isinstance(val, str):
        return [(key, val)]
    elif hasattr(val, '__dict__'):
        values = [e for k, elt in val.__dict__.items()
                  for e in flatten(k, elt, depth-1)]
        return [("%s.%s" % (key, k), v) for k, v in values]
    else:
        return [(key, val)]

class Context(Context):
    def extract_vars(self, frame):
        vals = inspect.getargvalues(frame).locals
        return {k1: v1 for k, v in vals.items() for k1, v1 in flatten(k, v)}

    def parameters(self, all_vars):
        def check_param(k):
            return any(k.startswith(p) for p in self.parameter_names)
        return {k: v for k, v in all_vars.items() if check_param(k)}

    def qualified(self, all_vars):
        return {"%s:%s" % (self.method, k): v for k, v in all_vars.items()}

if __name__ == '__main__':
    with Tracer(INVENTORY, methods=INVENTORY_METHODS, log=True) as tracer:
        process_inventory(tracer.my_input)
    print()
    print('Traced values:')
    for t in tracer.trace:
        print(t)

if __name__ == '__main__':
    vehicle_grammar = recover_grammar(
        process_inventory,
        [INVENTORY],
        methods=INVENTORY_METHODS)

if __name__ == '__main__':
    syntax_diagram(vehicle_grammar)

### Exercise 2: Incorporating Taints from InformationFlow

if __name__ == '__main__':
    print('\n### Exercise 2: Incorporating Taints from InformationFlow')



from .InformationFlow import ostr

def is_fragment(fragment, original):
    assert isinstance(original, ostr)
    if not isinstance(fragment, ostr):
        return False
    return set(fragment.origin) <= set(original.origin)

class TaintedInputStack(InputStack):
    def in_current_record(self, val):
        return any(is_fragment(val, var) for var in self.inputs[-1].values())

class TaintedInputStack(TaintedInputStack):
    def ignored(self, val):
        return not isinstance(val, ostr)

class TaintedScopedVars(ScopedVars):
    def create_call_stack(self, i):
        return TaintedInputStack(i)

class TaintedScopeTracker(ScopeTracker):
    def create_assignments(self, *args):
        return TaintedScopedVars(*args)

class TaintedScopeTreeMiner(ScopeTreeMiner):
    def string_part_of_value(self, part, value):
        return is_fragment(part, value)
    
    def partition(self, part, value):
        begin = value.origin.index(part.origin[0])
        end = value.origin.index(part.origin[-1])+1
        return value[:begin], value[begin:end], value[end:]

class TaintedScopedGrammarMiner(ScopedGrammarMiner):
    def create_tracker(self, *args):
        return TaintedScopeTracker(*args)

    def create_tree_miner(self, *args):
        return TaintedScopeTreeMiner(*args)

def recover_grammar_with_taints(fn, inputs, **kwargs):
    miner = TaintedScopedGrammarMiner()
    for inputstr in inputs:
        with Tracer(ostr(inputstr), **kwargs) as tracer:
            fn(tracer.my_input)
        miner.update_grammar(tracer.my_input, tracer.trace)
    return readable(miner.clean_grammar())

if __name__ == '__main__':
    inventory_grammar = recover_grammar_with_taints(
        process_inventory, [INVENTORY],
        methods=[
            'process_inventory', 'process_vehicle', 'process_car', 'process_van'
        ])

if __name__ == '__main__':
    syntax_diagram(inventory_grammar)

if __name__ == '__main__':
    url_grammar = recover_grammar_with_taints(
        url_parse, URLS_X + ['ftp://user4:pass1@host4/?key4=value3'],
        methods=['urlsplit', 'urlparse', '_splitnetloc'])

if __name__ == '__main__':
    syntax_diagram(url_grammar)
