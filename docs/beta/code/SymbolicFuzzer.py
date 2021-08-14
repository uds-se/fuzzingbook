#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Symbolic Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/SymbolicFuzzer.html
# Last change: 2021-06-08 13:13:28+02:00
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
The Fuzzing Book - Symbolic Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python SymbolicFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.SymbolicFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/SymbolicFuzzer.html

This chapter provides an implementation of a symbolic fuzzing engine `AdvancedSymbolicFuzzer`. The fuzzer uses symbolic execution to exhaustively explore paths in the program to a limited depth, and generate inputs that will reach these paths. Given a program to explore (`gcd` here), the fuzzer can be used as follows:

>>> gcd_fuzzer = AdvancedSymbolicFuzzer(gcd, max_tries=10, max_iter=10, max_depth=10)
>>> for i in range(10):
>>>     r = gcd_fuzzer.fuzz()
>>>     print(r)
{'a': 7, 'b': 5}
{'a': -1, 'b': 0}
{'a': 2, 'b': 7}
{'a': 10, 'b': 9}
{'a': 11, 'b': 21}
{'a': 11, 'b': -11}
{'a': 7, 'b': 6}
{'a': -2, 'b': 0}
{'a': 12, 'b': -12}
{'a': 9, 'b': 2}



For more details, source, and documentation, see
"The Fuzzing Book - Symbolic Fuzzing"
at https://www.fuzzingbook.org/html/SymbolicFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Symbolic Fuzzing
# ================

if __name__ == '__main__':
    print('# Symbolic Fuzzing')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Obtaining Path Conditions for Coverage
## --------------------------------------

if __name__ == '__main__':
    print('\n## Obtaining Path Conditions for Coverage')



def check_triangle(a: int, b: int, c: int) -> int:
    if a == b:
        if a == c:
            if b == c:
                return "Equilateral"
            else:
                return "Isosceles"
        else:
            return "Isosceles"
    else:
        if b != c:
            if a == c:
                return "Isosceles"
            else:
                return "Scalene"
        else:
            return "Isosceles"

### The Control Flow Graph

if __name__ == '__main__':
    print('\n### The Control Flow Graph')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .ControlFlow import PyCFG, CFGNode, to_graph, gen_cfg

import inspect

from graphviz import Source, Graph

def show_cfg(fn, **kwargs):
    return Source(to_graph(gen_cfg(inspect.getsource(fn)), **kwargs))

if __name__ == '__main__':
    show_cfg(check_triangle)

if __name__ == '__main__':
    paths = {
        '<path 1>': ([1, 2, 3, 4, 5], 'Equilateral'),
        '<path 2>': ([1, 2, 3, 4, 7], 'Isosceles'),
        '<path 3>': ([1, 2, 3, 9], 'Isosceles'),
        '<path 4>': ([1, 2, 11, 12, 13], 'Isosceles'),
        '<path 5>': ([1, 2, 11, 12, 15], 'Scalene'),
        '<path 6>': ([1, 2, 11, 17], 'Isosceles'),
    }

import z3

def get_annotations(fn):
    sig = inspect.signature(fn)
    return ([(i.name, i.annotation)
             for i in sig.parameters.values()], sig.return_annotation)

if __name__ == '__main__':
    params, ret = get_annotations(check_triangle)
    params, ret

SYM_VARS = {
    int: (
        z3.Int, z3.IntVal), float: (
            z3.Real, z3.RealVal), str: (
                z3.String, z3.StringVal)}

def get_symbolicparams(fn):
    params, ret = get_annotations(fn)
    return [SYM_VARS[typ][0](name)
            for name, typ in params], SYM_VARS[ret][0]('__return__')

if __name__ == '__main__':
    (a, b, c), r = get_symbolicparams(check_triangle)
    a, b, c, r

if __name__ == '__main__':
    z3.solve(a == b, a == c, b == c)

from .ConcolicFuzzer import ArcCoverage  # minor dependency

if __name__ == '__main__':
    with ArcCoverage() as cov:
        assert check_triangle(0, 0, 0) == 'Equilateral'
    cov._trace, cov.arcs()

### The CFG with Path Taken

if __name__ == '__main__':
    print('\n### The CFG with Path Taken')



if __name__ == '__main__':
    show_cfg(check_triangle, arcs=cov.arcs())

if __name__ == '__main__':
    z3.solve(a == b, a == c, z3.Not(b == c))

if __name__ == '__main__':
    z3.solve(a == b, z3.Not(a == c))

if __name__ == '__main__':
    with ArcCoverage() as cov:
        assert check_triangle(1, 1, 0) == 'Isosceles'
    [i for fn, i in cov._trace if fn == 'check_triangle']

if __name__ == '__main__':
    paths['<path 3>']

if __name__ == '__main__':
    z3.solve(z3.Not(a == b), b != c, a == c)

if __name__ == '__main__':
    pre_condition = z3.And(a > 0, b > 0, c > 0)

if __name__ == '__main__':
    z3.solve(pre_condition, z3.Not(a == b), b != c, a == c)

if __name__ == '__main__':
    with ArcCoverage() as cov:
        assert check_triangle(1, 2, 1) == 'Isosceles'
    [i for fn, i in cov._trace if fn == 'check_triangle']

if __name__ == '__main__':
    paths['<path 4>']

if __name__ == '__main__':
    z3.solve(pre_condition, z3.Not(a == b), b != c, z3.Not(a == c))

if __name__ == '__main__':
    with ArcCoverage() as cov:
        assert check_triangle(3, 1, 2) == 'Scalene'

if __name__ == '__main__':
    paths['<path 5>']

if __name__ == '__main__':
    z3.solve(pre_condition, z3.Not(a == b), z3.Not(b != c))

if __name__ == '__main__':
    with ArcCoverage() as cov:
        assert check_triangle(2, 1, 1) == 'Isosceles'
    [i for fn, i in cov._trace if fn == 'check_triangle']

if __name__ == '__main__':
    paths['<path 6>']

if __name__ == '__main__':
    seen = [z3.And(a == 2, b == 1, c == 1)]

if __name__ == '__main__':
    z3.solve(pre_condition, z3.Not(z3.Or(seen)), z3.Not(a == b), z3.Not(b != c))

if __name__ == '__main__':
    seen.append(z3.And(a == 1, b == 2, c == 2))

if __name__ == '__main__':
    z3.solve(pre_condition, z3.Not(z3.Or(seen)), z3.Not(a == b), z3.Not(b != c))

### Visualizing the Coverage

if __name__ == '__main__':
    print('\n### Visualizing the Coverage')



class ArcCoverage(ArcCoverage):
    def show_coverage(self, fn):
        src = fn if isinstance(fn, str) else inspect.getsource(fn)
        covered = set([lineno for method, lineno in self._trace])
        for i, s in enumerate(src.split('\n')):
            print('%s %2d: %s' % ('#' if i + 1 in covered else ' ', i + 1, s))

if __name__ == '__main__':
    with ArcCoverage() as cov:
        assert check_triangle(0, 0, 0) == 'Equilateral'
        assert check_triangle(1, 1, 0) == 'Isosceles'
        assert check_triangle(1, 2, 1) == 'Isosceles'
        assert check_triangle(3, 1, 2) == 'Scalene'
        assert check_triangle(2, 1, 1) == 'Isosceles'

if __name__ == '__main__':
    cov.show_coverage(check_triangle)

### Function Summaries

if __name__ == '__main__':
    print('\n### Function Summaries')



def abs_value(x: float) -> float:
    if x < 0:
        v: float = -x
    else:
        v: float = x
    return v

if __name__ == '__main__':
    show_cfg(abs_value)

if __name__ == '__main__':
    (x,), r = get_symbolicparams(abs_value)

if __name__ == '__main__':
    l2_F = x < 0
    l2_T = z3.Not(x < 0)

if __name__ == '__main__':
    v_0 = z3.Real('v_0')
    l3 = z3.And(l2_F, v_0 == -x)

if __name__ == '__main__':
    v_1 = z3.Real('v_1')
    l5 = z3.And(l2_T, v_1 == x)

if __name__ == '__main__':
    v = z3.Real('v')
    for s in [z3.And(l3, v == v_0), z3.And(l5, v == v_1)]:
        z3.solve(x != 0, s)

if __name__ == '__main__':
    v = z3.Real('v')
    l6 = z3.Or(z3.And(l3, v == v_0), z3.And(l5, v == v_1))
    z3.solve(l6)

if __name__ == '__main__':
    s = z3.Solver()
    s.add(l6)
    for i in range(5):
        if s.check() == z3.sat:
            m = s.model()
            x_val = m[x]
            print(m)
        else:
            print('no solution')
            break
        s.add(z3.Not(x == x_val))
    s

if __name__ == '__main__':
    s.add(x < 0)
    for i in range(5):
        if s.check() == z3.sat:
            m = s.model()
            x_val = m[x]
            print(m)
        else:
            print('no solution')
            break
        s.add(z3.Not(x == x_val))

    s

if __name__ == '__main__':
    abs_value_summary = l6
    abs_value_summary

if __name__ == '__main__':
    z3.simplify(l6)

import ast
import astor

def prefix_vars(astnode, prefix):
    if isinstance(astnode, ast.BoolOp):
        return ast.BoolOp(astnode.op,
                          [prefix_vars(i, prefix) for i in astnode.values], [])
    elif isinstance(astnode, ast.BinOp):
        return ast.BinOp(
            prefix_vars(astnode.left, prefix), astnode.op,
            prefix_vars(astnode.right, prefix))
    elif isinstance(astnode, ast.UnaryOp):
        return ast.UnaryOp(astnode.op, prefix_vars(astnode.operand, prefix))
    elif isinstance(astnode, ast.Call):
        return ast.Call(prefix_vars(astnode.func, prefix),
                        [prefix_vars(i, prefix) for i in astnode.args],
                        astnode.keywords)
    elif isinstance(astnode, ast.Compare):
        return ast.Compare(
            prefix_vars(astnode.left, prefix), astnode.ops,
            [prefix_vars(i, prefix) for i in astnode.comparators])
    elif isinstance(astnode, ast.Name):
        if astnode.id in {'And', 'Or', 'Not'}:
            return ast.Name('z3.%s' % (astnode.id), astnode.ctx)
        else:
            return ast.Name('%s%s' % (prefix, astnode.id), astnode.ctx)
    elif isinstance(astnode, ast.Return):
        return ast.Return(prefix_vars(astnode.value, env))
    else:
        return astnode

if __name__ == '__main__':
    ast.parse('x+y')

def get_expression(src):
    return ast.parse(src).body[0].value

if __name__ == '__main__':
    e = get_expression('x+y')
    e

def to_src(astnode):
    return astor.to_source(astnode).strip()

if __name__ == '__main__':
    to_src(e)

if __name__ == '__main__':
    abs_value_summary_ast = get_expression(str(abs_value_summary))
    print(to_src(prefix_vars(abs_value_summary_ast, 'x1_')))

#### Get Names and Types of Variables Used

if __name__ == '__main__':
    print('\n#### Get Names and Types of Variables Used')



def z3_names_and_types(z3_ast):
    hm = {}
    children = z3_ast.children()
    if children:
        for c in children:
            hm.update(z3_names_and_types(c))
    else:
        # HACK.. How else to distinguish literals and vars?
        if (str(z3_ast.decl()) != str(z3_ast.sort())):
            hm["%s" % str(z3_ast.decl())] = 'z3.%s' % str(z3_ast.sort())
        else:
            pass
    return hm

if __name__ == '__main__':
    abs_value_declarations = z3_names_and_types(abs_value_summary)
    abs_value_declarations

def used_identifiers(src):
    def names(astnode):
        lst = []
        if isinstance(astnode, ast.BoolOp):
            for i in astnode.values:
                lst.extend(names(i))
        elif isinstance(astnode, ast.BinOp):
            lst.extend(names(astnode.left))
            lst.extend(names(astnode.right))
        elif isinstance(astnode, ast.UnaryOp):
            lst.extend(names(astnode.operand))
        elif isinstance(astnode, ast.Call):
            for i in astnode.args:
                lst.extend(names(i))
        elif isinstance(astnode, ast.Compare):
            lst.extend(names(astnode.left))
            for i in astnode.comparators:
                lst.extend(names(i))
        elif isinstance(astnode, ast.Name):
            lst.append(astnode.id)
        elif isinstance(astnode, ast.Expr):
            lst.extend(names(astnode.value))
        elif isinstance(astnode, (ast.Num, ast.Str, ast.Tuple, ast.NameConstant)):
            pass
        elif isinstance(astnode, ast.Assign):
            for t in astnode.targets:
                lst.extend(names(t))
            lst.extend(names(astnode.value))
        elif isinstance(astnode, ast.Module):
            for b in astnode.body:
                lst.extend(names(b))
        else:
            raise Exception(str(astnode))
        return list(set(lst))
    return names(ast.parse(src))

if __name__ == '__main__':
    used_identifiers(str(abs_value_summary))

if __name__ == '__main__':
    function_summaries = {}
    function_summaries['abs_value'] = {
        'predicate': str(abs_value_summary),
        'vars': abs_value_declarations}

SYM_VARS_STR = {
    k.__name__: ("z3.%s" % v1.__name__, "z3.%s" % v2.__name__)
    for k, (v1, v2) in SYM_VARS.items()
}
SYM_VARS_STR

def translate_to_z3_name(v):
    return SYM_VARS_STR[v][0]

def declarations(astnode, hm=None):
    if hm is None:
        hm = {}
    if isinstance(astnode, ast.Module):
        for b in astnode.body:
            declarations(b, hm)
    elif isinstance(astnode, ast.FunctionDef):
        #hm[astnode.name + '__return__'] = translate_to_z3_name(astnode.returns.id)
        for a in astnode.args.args:
            hm[a.arg] = translate_to_z3_name(a.annotation.id)
        for b in astnode.body:
            declarations(b, hm)
    elif isinstance(astnode, ast.Call):
        # get declarations from the function summary.
        n = astnode.function
        assert isinstance(n, ast.Name)  # for now.
        name = n.id
        hm.update(dict(function_summaries[name]['vars']))
    elif isinstance(astnode, ast.AnnAssign):
        assert isinstance(astnode.target, ast.Name)
        hm[astnode.target.id] = translate_to_z3_name(astnode.annotation.id)
    elif isinstance(astnode, ast.Assign):
        # verify it is already defined
        for t in astnode.targets:
            assert isinstance(t, ast.Name)
            assert t.id in hm
    elif isinstance(astnode, ast.AugAssign):
        assert isinstance(astnode.target, ast.Name)
        assert astnode.target.id in hm
    elif isinstance(astnode, (ast.If, ast.For, ast.While)):
        for b in astnode.body:
            declarations(b, hm)
        for b in astnode.orelse:
            declarations(b, hm)
    elif isinstance(astnode, ast.Return):
        pass
    else:
        raise Exception(str(astnode))
    return hm

if __name__ == '__main__':
    declarations(ast.parse('s: int = 3\np: float = 4.0\ns += 1'))

def used_vars(fn):
    return declarations(ast.parse(inspect.getsource(fn)))

if __name__ == '__main__':
    used_vars(check_triangle)

if __name__ == '__main__':
    used_vars(abs_value)

def define_symbolic_vars(fn_vars, prefix):
    sym_var_dec = ', '.join([prefix + n for n in fn_vars])
    sym_var_def = ', '.join(["%s('%s%s')" % (t, prefix, n)
                             for n, t in fn_vars.items()])
    return "%s = %s" % (sym_var_dec, sym_var_def)

if __name__ == '__main__':
    define_symbolic_vars(abs_value_declarations, '')

def gen_fn_summary(prefix, fn):
    summary = function_summaries[fn.__name__]['predicate']
    fn_vars = function_summaries[fn.__name__]['vars']
    decl = define_symbolic_vars(fn_vars, prefix)
    summary_ast = get_expression(summary)
    return decl, to_src(prefix_vars(summary_ast, prefix))

if __name__ == '__main__':
    gen_fn_summary('a_', abs_value)

if __name__ == '__main__':
    gen_fn_summary('b_', abs_value)

def abs_max(a: float, b: float):
    a1: float = abs_value(a)
    b1: float = abs_value(b)
    if a1 > b1:
        c: float = a1
    else:
        c: float = b1
    return c

if __name__ == '__main__':
    a = z3.Real('a')
    b = z3.Real('b')

if __name__ == '__main__':
    a1 = z3.Real('a1')

if __name__ == '__main__':
    d, v = gen_fn_summary('abs1_', abs_value)
    d, v

if __name__ == '__main__':
    l2_src = "l2 = z3.And(a == abs1_x, a1 == abs1_v, %s)" % v
    l2_src

if __name__ == '__main__':
    exec(d)
    exec(l2_src)

if __name__ == '__main__':
    l2

if __name__ == '__main__':
    b1 = z3.Real('b1')
    d, v = gen_fn_summary('abs2_', abs_value)
    l3_src = "l3_ = z3.And(b == abs2_x, b1 == abs2_v, %s)" % v
    exec(d)
    exec(l3_src)

if __name__ == '__main__':
    l3_

if __name__ == '__main__':
    l3 = z3.And(l2, l3_)

if __name__ == '__main__':
    l3

if __name__ == '__main__':
    z3.simplify(l3)

if __name__ == '__main__':
    l4_cond = a1 > b1
    l4 = z3.And(l3, l4_cond)

if __name__ == '__main__':
    c_0 = z3.Real('c_0')
    l5 = z3.And(l4, c_0 == a1)

if __name__ == '__main__':
    l6 = z3.And(l3, z3.Not(l4_cond))

if __name__ == '__main__':
    c_1 = z3.Real('c_1')
    l7 = z3.And(l6, c_1 == b1)

if __name__ == '__main__':
    s1 = z3.Solver()
    s1.add(l5)
    s1.check()

if __name__ == '__main__':
    m1 = s1.model()
    sorted([(d, m1[d]) for d in m1.decls() if not d.name(
    ).startswith('abs')], key=lambda x: x[0].name())

if __name__ == '__main__':
    s2 = z3.Solver()
    s2.add(l7)
    s2.check()

if __name__ == '__main__':
    m2 = s2.model()
    sorted([(d, m2[d]) for d in m2.decls() if not d.name(
    ).startswith('abs')], key=lambda x: x[0].name())

## SimpleSymbolicFuzzer
## --------------------

if __name__ == '__main__':
    print('\n## SimpleSymbolicFuzzer')



from .Fuzzer import Fuzzer

class SimpleSymbolicFuzzer(Fuzzer):
    def __init__(self, fn, **kwargs):
        self.fn_name = fn.__name__
        py_cfg = PyCFG()
        py_cfg.gen_cfg(inspect.getsource(fn))
        self.fnenter, self.fnexit = py_cfg.functions[self.fn_name]
        self.used_variables = used_vars(fn)
        self.fn_args = list(inspect.signature(fn).parameters)
        self.z3 = z3.Solver()

        self.paths = None
        self.last_path = None

        self.options(kwargs)
        self.process()

    def process(self):
        pass

MAX_DEPTH = 100

MAX_TRIES = 100

MAX_ITER = 100

class SimpleSymbolicFuzzer(SimpleSymbolicFuzzer):
    def options(self, kwargs):
        self.max_depth = kwargs.get('max_depth', MAX_DEPTH)
        self.max_tries = kwargs.get('max_tries', MAX_TRIES)
        self.max_iter = kwargs.get('max_iter', MAX_ITER)
        self._options = kwargs

if __name__ == '__main__':
    symfz_ct = SimpleSymbolicFuzzer(check_triangle)

if __name__ == '__main__':
    symfz_ct.fnenter, symfz_ct.fnexit

### Generating All Possible Paths

if __name__ == '__main__':
    print('\n### Generating All Possible Paths')



class SimpleSymbolicFuzzer(SimpleSymbolicFuzzer):
    def get_all_paths(self, fenter, depth=0):
        if depth > self.max_depth:
            raise Exception('Maximum depth exceeded')
        if not fenter.children:
            return [[(0, fenter)]]

        fnpaths = []
        for idx, child in enumerate(fenter.children):
            child_paths = self.get_all_paths(child, depth + 1)
            for path in child_paths:
                # In a conditional branch, idx is 0 for IF, and 1 for Else
                fnpaths.append([(idx, fenter)] + path)
        return fnpaths

if __name__ == '__main__':
    symfz_ct = SimpleSymbolicFuzzer(check_triangle)
    paths = symfz_ct.get_all_paths(symfz_ct.fnenter)
    print(len(paths))
    paths[1]

class SimpleSymbolicFuzzer(SimpleSymbolicFuzzer):
    def process(self):
        self.paths = self.get_all_paths(self.fnenter)
        self.last_path = len(self.paths)

### Extracting All Constraints

if __name__ == '__main__':
    print('\n### Extracting All Constraints')



class SimpleSymbolicFuzzer(SimpleSymbolicFuzzer):
    def extract_constraints(self, path):
        predicates = []
        for (idx, elt) in path:
            if isinstance(elt.ast_node, ast.AnnAssign):
                if elt.ast_node.target.id in {'_if', '_while'}:
                    s = to_src(elt.ast_node.annotation)
                    predicates.append(("%s" if idx == 0 else "z3.Not%s") % s)
                elif isinstance(elt.ast_node.annotation, ast.Call):
                    assert elt.ast_node.annotation.func.id == self.fn_name
                else:
                    node = elt.ast_node
                    t = ast.Compare(node.target, [ast.Eq()], [node.value])
                    predicates.append(to_src(t))
            elif isinstance(elt.ast_node, ast.Assign):
                node = elt.ast_node
                t = ast.Compare(node.targets[0], [ast.Eq()], [node.value])
                predicates.append(to_src(t))
            else:
                pass
        return predicates

if __name__ == '__main__':
    symfz_ct = SimpleSymbolicFuzzer(check_triangle)
    paths = symfz_ct.get_all_paths(symfz_ct.fnenter)
    symfz_ct.extract_constraints(paths[0])

if __name__ == '__main__':
    constraints = symfz_ct.extract_constraints(paths[1])
    constraints

### Fuzzing with Simple Symbolic Fuzzer

if __name__ == '__main__':
    print('\n### Fuzzing with Simple Symbolic Fuzzer')



from contextlib import contextmanager

@contextmanager
def checkpoint(z3solver):
    z3solver.push()
    yield z3solver
    z3solver.pop()

class SimpleSymbolicFuzzer(SimpleSymbolicFuzzer):
    def solve_path_constraint(self, path):
        # re-initializing does not seem problematic.
        # a = z3.Int('a').get_id() remains the same.
        constraints = self.extract_constraints(path)
        decl = define_symbolic_vars(self.used_variables, '')
        exec(decl)

        solutions = {}
        with checkpoint(self.z3):
            st = 'self.z3.add(%s)' % ', '.join(constraints)
            eval(st)
            if self.z3.check() != z3.sat:
                return {}
            m = self.z3.model()
            solutions = {d.name(): m[d] for d in m.decls()}
            my_args = {k: solutions.get(k, None) for k in self.fn_args}
        predicate = 'z3.And(%s)' % ','.join(
            ["%s == %s" % (k, v) for k, v in my_args.items()])
        eval('self.z3.add(z3.Not(%s))' % predicate)
        return my_args

class SimpleSymbolicFuzzer(SimpleSymbolicFuzzer):
    def get_next_path(self):
        self.last_path -= 1
        if self.last_path == -1:
            self.last_path = len(self.paths) - 1
        return self.paths[self.last_path]

class SimpleSymbolicFuzzer(SimpleSymbolicFuzzer):
    def fuzz(self):
        for i in range(self.max_tries):
            res = self.solve_path_constraint(self.get_next_path())
            if res:
                return res
        return {}

if __name__ == '__main__':
    a, b, c = None, None, None
    symfz_ct = SimpleSymbolicFuzzer(check_triangle)
    for i in range(1, 10):
        r = symfz_ct.fuzz()
        v = check_triangle(r['a'].as_long(), r['b'].as_long(), r['c'].as_long())
        print(r, "result:", v)

if __name__ == '__main__':
    symfz_av = SimpleSymbolicFuzzer(abs_value)
    for i in range(1, 10):
        r = symfz_av.fuzz()
        v = abs_value(r['x'].numerator_as_long() / r['x'].denominator_as_long())
        print(r, "result:", v)

### Problems with the Simple Fuzzer

if __name__ == '__main__':
    print('\n### Problems with the Simple Fuzzer')



def gcd(a: int, b: int) -> int:
    if a < b:
        c: int = a
        a = b
        b = c

    while b != 0:
        c: int = a
        a = b
        b = c % b
    return a

if __name__ == '__main__':
    show_cfg(gcd)

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        symfz_gcd = SimpleSymbolicFuzzer(gcd, max_depth=1000, max_iter=10)
        for i in range(1, 100):
            r = symfz_gcd.fuzz()
            v = gcd(r['a'].as_long(), r['b'].as_long())
            print(r, v)

## Advanced Symbolic Fuzzer
## ------------------------

if __name__ == '__main__':
    print('\n## Advanced Symbolic Fuzzer')



class AdvancedSymbolicFuzzer(SimpleSymbolicFuzzer):
    def options(self, kwargs):
        super().options(kwargs)

### Dealing with Reassingments

if __name__ == '__main__':
    print('\n### Dealing with Reassingments')



def rename_variables(astnode, env):
    if isinstance(astnode, ast.BoolOp):
        fn = 'z3.And' if isinstance(astnode.op, ast.And) else 'z3.Or'
        return ast.Call(
            ast.Name(fn, None),
            [rename_variables(i, env) for i in astnode.values], [])
    elif isinstance(astnode, ast.BinOp):
        return ast.BinOp(
            rename_variables(astnode.left, env), astnode.op,
            rename_variables(astnode.right, env))
    elif isinstance(astnode, ast.UnaryOp):
        if isinstance(astnode.op, ast.Not):
            return ast.Call(
                ast.Name('z3.Not', None),
                [rename_variables(astnode.operand, env)], [])
        else:
            return ast.UnaryOp(astnode.op,
                               rename_variables(astnode.operand, env))
    elif isinstance(astnode, ast.Call):
        return ast.Call(astnode.func,
                        [rename_variables(i, env) for i in astnode.args],
                        astnode.keywords)
    elif isinstance(astnode, ast.Compare):
        return ast.Compare(
            rename_variables(astnode.left, env), astnode.ops,
            [rename_variables(i, env) for i in astnode.comparators])
    elif isinstance(astnode, ast.Name):
        if astnode.id not in env:
            env[astnode.id] = 0
        num = env[astnode.id]
        return ast.Name('_%s_%d' % (astnode.id, num), astnode.ctx)
    elif isinstance(astnode, ast.Return):
        return ast.Return(rename_variables(astnode.value, env))
    else:
        return astnode

if __name__ == '__main__':
    env = {'x': 1}

if __name__ == '__main__':
    ba = get_expression('x == 1 and y == 2')
    type(ba)

if __name__ == '__main__':
    assert to_src(rename_variables(ba, env)) == 'z3.And(_x_1 == 1, _y_0 == 2)'

if __name__ == '__main__':
    bo = get_expression('x == 1 or y == 2')
    type(bo.op)

if __name__ == '__main__':
    assert to_src(rename_variables(bo, env)) == 'z3.Or(_x_1 == 1, _y_0 == 2)'

if __name__ == '__main__':
    b = get_expression('x + y')
    type(b)

if __name__ == '__main__':
    assert to_src(rename_variables(b, env)) == '(_x_1 + _y_0)'

if __name__ == '__main__':
    u = get_expression('-y')
    type(u)

if __name__ == '__main__':
    assert to_src(rename_variables(u, env)) == '(-_y_0)'

if __name__ == '__main__':
    un = get_expression('not y')
    type(un.op)

if __name__ == '__main__':
    assert to_src(rename_variables(un, env)) == 'z3.Not(_y_0)'

if __name__ == '__main__':
    c = get_expression('x == y')
    type(c)

if __name__ == '__main__':
    assert to_src(rename_variables(c, env)) == '(_x_1 == _y_0)'

if __name__ == '__main__':
    f = get_expression('fn(x,y)')
    type(f)

if __name__ == '__main__':
    assert to_src(rename_variables(f, env)) == 'fn(_x_1, _y_0)'

if __name__ == '__main__':
    env

### Tracking Assignments

if __name__ == '__main__':
    print('\n### Tracking Assignments')



class PNode:
    def __init__(self, idx, cfgnode, parent=None, order=0, seen=None):
        self.seen = {} if seen is None else seen
        self.max_iter = MAX_ITER
        self.idx, self.cfgnode, self.parent, self.order = idx, cfgnode, parent, order

    def __repr__(self):
        return "PNode:%d[%s order:%d]" % (self.idx, str(self.cfgnode),
                                          self.order)

if __name__ == '__main__':
    cfg = PyCFG()
    cfg.gen_cfg(inspect.getsource(gcd))
    gcd_fnenter, _ = cfg.functions['gcd']

if __name__ == '__main__':
    PNode(0, gcd_fnenter)

class PNode(PNode):
    def copy(self, order):
        p = PNode(self.idx, self.cfgnode, self.parent, order, self.seen)
        assert p.order == order
        return p

if __name__ == '__main__':
    PNode(0, gcd_fnenter).copy(1)

#### Stepwise Exploration of Paths

if __name__ == '__main__':
    print('\n#### Stepwise Exploration of Paths')



class PNode(PNode):
    def explore(self):
        ret = []
        for (i, n) in enumerate(self.cfgnode.children):
            key = "[%d]%s" % (self.idx + 1, n)
            ccount = self.seen.get(key, 0)
            if ccount > self.max_iter:
                continue  # drop this child
            self.seen[key] = ccount + 1
            pn = PNode(self.idx + 1, n, self.copy(i), seen=self.seen)
            ret.append(pn)
        return ret

if __name__ == '__main__':
    PNode(0, gcd_fnenter).explore()

if __name__ == '__main__':
    PNode(0, gcd_fnenter).explore()[0].explore()

class PNode(PNode):
    def get_path_to_root(self):
        path = []
        n = self
        while n:
            path.append(n)
            n = n.parent
        return list(reversed(path))

if __name__ == '__main__':
    p = PNode(0, gcd_fnenter)
    [s.get_path_to_root() for s in p.explore()[0].explore()[0].explore()[0].explore()]

class PNode(PNode):
    def __str__(self):
        path = self.get_path_to_root()
        ssa_path = to_single_assignment_predicates(path)
        return ', '.join([to_src(p) for p in ssa_path])

#### Renaming Used Variables

if __name__ == '__main__':
    print('\n#### Renaming Used Variables')



def to_single_assignment_predicates(path):
    env = {}
    new_path = []
    for i, node in enumerate(path):
        ast_node = node.cfgnode.ast_node
        new_node = None
        if isinstance(ast_node, ast.AnnAssign) and ast_node.target.id in {
                'exit'}:
            new_node = None
        elif isinstance(ast_node, ast.AnnAssign) and ast_node.target.id in {'enter'}:
            args = [
                ast.parse(
                    "%s == _%s_0" %
                    (a.id, a.id)).body[0].value for a in ast_node.annotation.args]
            new_node = ast.Call(ast.Name('z3.And', None), args, [])
        elif isinstance(ast_node, ast.AnnAssign) and ast_node.target.id in {'_if', '_while'}:
            new_node = rename_variables(ast_node.annotation, env)
            if node.order != 0:
                assert node.order == 1
                new_node = ast.Call(ast.Name('z3.Not', None), [new_node], [])
        elif isinstance(ast_node, ast.AnnAssign):
            assigned = ast_node.target.id
            val = [rename_variables(ast_node.value, env)]
            env[assigned] = 0 if assigned not in env else env[assigned] + 1
            target = ast.Name('_%s_%d' %
                              (ast_node.target.id, env[assigned]), None)
            new_node = ast.Expr(ast.Compare(target, [ast.Eq()], val))
        elif isinstance(ast_node, ast.Assign):
            assigned = ast_node.targets[0].id
            val = [rename_variables(ast_node.value, env)]
            env[assigned] = 0 if assigned not in env else env[assigned] + 1
            target = ast.Name('_%s_%d' %
                              (ast_node.targets[0].id, env[assigned]), None)
            new_node = ast.Expr(ast.Compare(target, [ast.Eq()], val))
        elif isinstance(ast_node, (ast.Return, ast.Pass)):
            new_node = None
        else:
            s = "NI %s %s" % (type(ast_node), ast_node.target.id)
            raise Exception(s)
        new_path.append(new_node)
    return new_path

if __name__ == '__main__':
    p = PNode(0, gcd_fnenter)
    path = p.explore()[0].explore()[0].explore()[0].get_path_to_root()
    spath = to_single_assignment_predicates(path)

if __name__ == '__main__':
    [to_src(s) for s in spath]

#### Check Before You Loop

if __name__ == '__main__':
    print('\n#### Check Before You Loop')



def identifiers_with_types(identifiers, defined):
    with_types = dict(defined)
    for i in identifiers:
        if i[0] == '_':
            nxt = i[1:].find('_', 1)
            name = i[1:nxt + 1]
            assert name in defined
            typ = defined[name]
            with_types[i] = typ
    return with_types

class AdvancedSymbolicFuzzer(AdvancedSymbolicFuzzer):
    def extract_constraints(self, path):
        return [to_src(p) for p in to_single_assignment_predicates(path) if p]

### Solving Path Constraints

if __name__ == '__main__':
    print('\n### Solving Path Constraints')



class AdvancedSymbolicFuzzer(AdvancedSymbolicFuzzer):
    def solve_path_constraint(self, path):
        # re-initializing does not seem problematic.
        # a = z3.Int('a').get_id() remains the same.
        constraints = self.extract_constraints(path)
        identifiers = [
            c for i in constraints for c in used_identifiers(i)]  # <- changes
        with_types = identifiers_with_types(
            identifiers, self.used_variables)  # <- changes
        decl = define_symbolic_vars(with_types, '')
        exec(decl)

        solutions = {}
        with checkpoint(self.z3):
            st = 'self.z3.add(%s)' % ', '.join(constraints)
            eval(st)
            if self.z3.check() != z3.sat:
                return {}
            m = self.z3.model()
            solutions = {d.name(): m[d] for d in m.decls()}
            my_args = {k: solutions.get(k, None) for k in self.fn_args}
        predicate = 'z3.And(%s)' % ','.join(
            ["%s == %s" % (k, v) for k, v in my_args.items()])
        eval('self.z3.add(z3.Not(%s))' % predicate)
        return my_args

### Generating All Paths

if __name__ == '__main__':
    print('\n### Generating All Paths')



class AdvancedSymbolicFuzzer(AdvancedSymbolicFuzzer):
    def get_all_paths(self, fenter):
        path_lst = [PNode(0, fenter)]
        completed = []
        for i in range(self.max_iter):
            new_paths = [PNode(0, fenter)]
            for path in path_lst:
                # explore each path once
                if path.cfgnode.children:
                    np = path.explore()
                    for p in np:
                        if path.idx > self.max_depth:
                            break
                        new_paths.append(p)
                else:
                    completed.append(path)
            path_lst = new_paths
        return completed + path_lst

if __name__ == '__main__':
    asymfz_gcd = AdvancedSymbolicFuzzer(
        gcd, max_iter=10, max_tries=10, max_depth=10)
    paths = asymfz_gcd.get_all_paths(asymfz_gcd.fnenter)
    print(len(paths))
    paths[37].get_path_to_root()

if __name__ == '__main__':
    for s in to_single_assignment_predicates(paths[37].get_path_to_root()):
        if s is not None:
            print(to_src(s))

if __name__ == '__main__':
    constraints = asymfz_gcd.extract_constraints(paths[37].get_path_to_root())

if __name__ == '__main__':
    constraints

class AdvancedSymbolicFuzzer(AdvancedSymbolicFuzzer):
    def get_next_path(self):
        self.last_path -= 1
        if self.last_path == -1:
            self.last_path = len(self.paths) - 1
        return self.paths[self.last_path].get_path_to_root()

### Fuzzing with Advanced Symbolic Fuzzer

if __name__ == '__main__':
    print('\n### Fuzzing with Advanced Symbolic Fuzzer')



if __name__ == '__main__':
    asymfz_gcd = AdvancedSymbolicFuzzer(
        gcd, max_tries=10, max_iter=10, max_depth=10)
    data = []
    for i in range(10):
        r = asymfz_gcd.fuzz()
        data.append((r['a'].as_long(), r['b'].as_long()))
        v = gcd(*data[-1])
        print(r, "result:", repr(v))

if __name__ == '__main__':
    with ArcCoverage() as cov:
        for a, b in data:
            gcd(a, b)

if __name__ == '__main__':
    cov.show_coverage(gcd)

if __name__ == '__main__':
    show_cfg(gcd, arcs=cov.arcs())

#### Example: Roots of a Quadratic Equation

if __name__ == '__main__':
    print('\n#### Example: Roots of a Quadratic Equation')



from typing import Tuple

def roots(a: float, b: float, c: float) -> Tuple[float, float]:
    d: float = b * b - 4 * a * c
    ax: float = 0.5 * d
    bx: float = 0
    while (ax - bx) > 0.1:
        bx = 0.5 * (ax + d / ax)
        ax = bx
    s: float = bx

    a2: float = 2 * a
    ba2: float = b / a2
    return -ba2 + s / a2, -ba2 - s / a2

def sym_to_float(v):
    if v is None:
        return math.inf
    elif isinstance(v, z3.IntNumRef):
        return v.as_long()
    return v.numerator_as_long() / v.denominator_as_long()

if __name__ == '__main__':
    asymfz_roots = AdvancedSymbolicFuzzer(
        roots,
        max_tries=10,
        max_iter=10,
        max_depth=10)
    with ExpectError():
        for i in range(100):
            r = asymfz_roots.fuzz()
            print(r)
            d = [sym_to_float(r[i]) for i in ['a', 'b', 'c']]
            v = roots(*d)
            print(d, v)

#####  Roots - Check Before Divide

if __name__ == '__main__':
    print('\n#####  Roots - Check Before Divide')



def roots2(a: float, b: float, c: float) -> Tuple[float, float]:
    d: float = b * b - 4 * a * c

    xa: float = 0.5 * d
    xb: float = 0
    while (xa - xb) > 0.1:
        xb = 0.5 * (xa + d / xa)
        xa = xb
    s: float = xb

    if a == 0:
        return -c / b

    a2: float = 2 * a
    ba2: float = b / a2
    return -ba2 + s / a2, -ba2 - s / a2

if __name__ == '__main__':
    asymfz_roots = AdvancedSymbolicFuzzer(
        roots2,
        max_tries=10,
        max_iter=10,
        max_depth=10)
    with ExpectError():
        for i in range(1000):
            r = asymfz_roots.fuzz()
            d = [sym_to_float(r[i]) for i in ['a', 'b', 'c']]
            v = roots2(*d)
            #print(d, v)

#####  Roots - Eliminating the Zero Division Error

if __name__ == '__main__':
    print('\n#####  Roots - Eliminating the Zero Division Error')



import math

def roots3(a: float, b: float, c: float) -> Tuple[float, float]:
    d: float = b * b - 4 * a * c

    xa: float = 0.5 * d
    xb: float = 0
    while (xa - xb) > 0.1:
        xb = 0.5 * (xa + d / xa)
        xa = xb
    s: float = xb

    if a == 0:
        if b == 0:
            return math.inf
        return -c / b

    a2: float = 2 * a
    ba2: float = b / a2
    return -ba2 + s / a2, -ba2 - s / a2

if __name__ == '__main__':
    asymfz_roots = AdvancedSymbolicFuzzer(
        roots3,
        max_tries=10,
        max_iter=10,
        max_depth=10)
    for i in range(10):
        r = asymfz_roots.fuzz()
        print(r)
        d = [sym_to_float(r[i]) for i in ['a', 'b', 'c']]
        v = roots3(*d)
        print(d, v)

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    gcd_fuzzer = AdvancedSymbolicFuzzer(gcd, max_tries=10, max_iter=10, max_depth=10)
    for i in range(10):
        r = gcd_fuzzer.fuzz()
        print(r)

## Limitations
## -----------

if __name__ == '__main__':
    print('\n## Limitations')



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



### Exercise 1: _Extending Symbolic Fuzzer to use function summaries_

if __name__ == '__main__':
    print('\n### Exercise 1: _Extending Symbolic Fuzzer to use function summaries_')



### Exercise 2: _Statically checking if a loop should be unrolled further_

if __name__ == '__main__':
    print('\n### Exercise 2: _Statically checking if a loop should be unrolled further_')



if __name__ == '__main__':
    i = 0
    while i < 10:
        i += 1

class AdvancedSymbolicFuzzer(AdvancedSymbolicFuzzer):
    def get_all_paths(self, fenter):
        path_lst = [PNode(0, fenter)]
        completed = []
        for i in range(self.max_iter):
            new_paths = [PNode(0, fenter)]
            for path in path_lst:
                # explore each path once
                if path.cfgnode.children:
                    np = path.explore()
                    for p in np:
                        if path.idx > self.max_depth:
                            break
                        if self.can_be_satisfied(p):
                            new_paths.append(p)
                        else:
                            break
                else:
                    completed.append(path)
            path_lst = new_paths
        return completed + path_lst

class AdvancedSymbolicFuzzer(AdvancedSymbolicFuzzer):
    def can_be_satisfied(self, p):
        s2 = self.extract_constraints(p.get_path_to_root())
        s = z3.Solver()
        identifiers = [c for i in s2 for c in used_identifiers(i)]
        with_types = identifiers_with_types(identifiers, self.used_variables)
        decl = define_symbolic_vars(with_types, '')
        exec(decl)
        exec("s.add(z3.And(%s))" % ','.join(s2), globals(), locals())
        return s.check() == z3.sat

### Exercise 3: _Implementing a Concolic Fuzzer_

if __name__ == '__main__':
    print('\n### Exercise 3: _Implementing a Concolic Fuzzer_')



class ArcCoverage(ArcCoverage):
    def offsets_from_entry(self, fn):
        zero = self._trace[0][1] - 1
        return [l - zero for (f, l) in self._trace if f == fn]

if __name__ == '__main__':
    with ArcCoverage() as cov:
        roots3(1, 1, 1)

if __name__ == '__main__':
    cov.offsets_from_entry('roots3')

class ConcolicTracer(AdvancedSymbolicFuzzer):
    def __init__(self, fn, fnargs, **kwargs):
        with ArcCoverage() as cov:
            fn(*fnargs)
        self.lines = cov.offsets_from_entry(fn.__name__)
        self.current_line = 0
        super().__init__(fn, **kwargs)

class ConcolicTracer(ConcolicTracer):
    def get_all_paths(self, fenter):
        assert fenter.ast_node.lineno == self.lines[self.current_line]
        self.current_line += 1
        last_node = PNode(0, fenter)
        while last_node and self.current_line < len(self.lines):
            if last_node.cfgnode.children:
                np = last_node.explore()
                for p in np:
                    if self.lines[self.current_line] == p.cfgnode.ast_node.lineno:
                        self.current_line += 1
                        last_node = p
                        break
                else:
                    last_node = None
                    break
            else:
                break
        assert len(self.lines) == self.current_line
        return [last_node]

#### Tracing the Execution Concolicaly

if __name__ == '__main__':
    print('\n#### Tracing the Execution Concolicaly')



if __name__ == '__main__':
    acfz_roots = ConcolicTracer(
        roots3,
        fnargs=[1, 1, 1],
        max_tries=10,
        max_iter=10,
        max_depth=10)

if __name__ == '__main__':
    acfz_roots.paths[0].get_path_to_root()

if __name__ == '__main__':
    print(cov.offsets_from_entry('roots3'))
    print([i.cfgnode.ast_node.lineno for i in acfz_roots.paths[0].get_path_to_root()])
    print(acfz_roots.lines)

if __name__ == '__main__':
    constraints = acfz_roots.extract_constraints(
        acfz_roots.paths[0].get_path_to_root())

if __name__ == '__main__':
    constraints

if __name__ == '__main__':
    identifiers = [c for i in constraints for c in used_identifiers(i)]
    with_types = identifiers_with_types(identifiers, acfz_roots.used_variables)
    decl = define_symbolic_vars(with_types, '')
    exec(decl)

if __name__ == '__main__':
    eval('z3.solve(%s)' % ','.join(constraints))

if __name__ == '__main__':
    acfz_roots.fuzz()

if __name__ == '__main__':
    with ArcCoverage() as cov:
        roots(1, 1, 1)
    show_cfg(roots, arcs=cov.arcs())

if __name__ == '__main__':
    with ArcCoverage() as cov:
        roots(-1, 0, 0)
    show_cfg(roots, arcs=cov.arcs())

#### Exploring Nearby Paths

if __name__ == '__main__':
    print('\n#### Exploring Nearby Paths')



if __name__ == '__main__':
    constraints

if __name__ == '__main__':
    new_constraints = constraints[0:4] + ['z3.Not(%s)' % constraints[4]]

if __name__ == '__main__':
    new_constraints

if __name__ == '__main__':
    eval('z3.solve(%s)' % ','.join(new_constraints))

if __name__ == '__main__':
    with ArcCoverage() as cov:
        roots3(1, 0, -11 / 20)
    show_cfg(roots3, arcs=cov.arcs())
