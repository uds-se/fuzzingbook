#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Prototyping with Python" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/PrototypingWithPython.html
# Last change: 2021-06-02 17:56:07+02:00
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
The Fuzzing Book - Prototyping with Python

This file can be _executed_ as a script, running all experiments:

    $ python PrototypingWithPython.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.PrototypingWithPython import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/PrototypingWithPython.html


For more details, source, and documentation, see
"The Fuzzing Book - Prototyping with Python"
at https://www.fuzzingbook.org/html/PrototypingWithPython.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Prototyping with Python
# =======================

if __name__ == '__main__':
    print('# Prototyping with Python')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo("IAreRIID9lM")

## Python is Easy
## --------------

if __name__ == '__main__':
    print('\n## Python is Easy')



def triangle(a, b, c):
    if a == b:
        if b == c:
            return 'equilateral'
        else:
            return 'isosceles #1'
    else:
        if b == c:
            return 'isosceles #2'
        else:
            if a == c:
                return 'isosceles #3'
            else:
                return 'scalene'

if __name__ == '__main__':
    triangle(2, 3, 4)

## Fuzzing is as Easy as Always
## ----------------------------

if __name__ == '__main__':
    print('\n## Fuzzing is as Easy as Always')



from random import randrange

if __name__ == '__main__':
    for i in range(10):
        a = randrange(1, 10)
        b = randrange(1, 10)
        c = randrange(1, 10)

        t = triangle(a, b, c)
        print(f"triangle({a}, {b}, {c}) = {repr(t)}")

## Dynamic Analysis in Python: So Easy it Hurts
## --------------------------------------------

if __name__ == '__main__':
    print('\n## Dynamic Analysis in Python: So Easy it Hurts')



import sys
import inspect

def traceit(frame, event, arg):
    function_code = frame.f_code
    function_name = function_code.co_name
    lineno = frame.f_lineno
    vars = frame.f_locals

    source_lines, starting_line_no = inspect.getsourcelines(frame.f_code)
    loc = f"{function_name}:{lineno} {source_lines[lineno - starting_line_no].rstrip()}"
    vars = ", ".join(f"{name} = {vars[name]}" for name in vars)

    print(f"{loc:50} ({vars})")

    return traceit

def triangle_traced():
    sys.settrace(traceit)
    triangle(2, 2, 1)
    sys.settrace(None)

if __name__ == '__main__':
    triangle_traced()

## Static Analysis in Python: Still Easy
## -------------------------------------

if __name__ == '__main__':
    print('\n## Static Analysis in Python: Still Easy')



from .bookutils import rich_output

import ast
import astor

if __name__ == '__main__':
    if rich_output():
        # Normally, this will do
        from showast import show_ast
    else:
        def show_ast(tree):
            ast.dump(tree)

if __name__ == '__main__':
    triangle_source = inspect.getsource(triangle)
    triangle_ast = ast.parse(triangle_source)
    show_ast(triangle_ast)

def collect_conditions(tree):
    conditions = []

    def traverse(node):
        if isinstance(node, ast.If):
            cond = astor.to_source(node.test).strip()
            conditions.append(cond)

        for child in ast.iter_child_nodes(node):
            traverse(child)

    traverse(tree)
    return conditions

if __name__ == '__main__':
    collect_conditions(triangle_ast)

## Symbolic Reasoning in Python: There's a Package for That
## --------------------------------------------------------

if __name__ == '__main__':
    print("\n## Symbolic Reasoning in Python: There's a Package for That")



import z3

if __name__ == '__main__':
    a = z3.Int('a')
    b = z3.Int('b')
    c = z3.Int('c')

if __name__ == '__main__':
    s = z3.Solver()
    s.add(z3.And(a > 0, b > 0, c > 0))  # Triangle edges are positive
    s.add(z3.And(a != b, b != c, a != c))  # Our condition
    s.check()

if __name__ == '__main__':
    m = s.model()
    m

if __name__ == '__main__':
    triangle(m[a].as_long(), m[b].as_long(), m[c].as_long())

## A Symbolic Test Generator
## -------------------------

if __name__ == '__main__':
    print('\n## A Symbolic Test Generator')



def collect_path_conditions(tree):
    paths = []

    def traverse_if_children(children, context, cond):
        old_paths = len(paths)
        for child in children:
            traverse(child, context + [cond])
        if len(paths) == old_paths:
            paths.append(context + [cond])

    def traverse(node, context):
        if isinstance(node, ast.If):
            cond = astor.to_source(node.test).strip()
            not_cond = "z3.Not" + cond

            traverse_if_children(node.body, context, cond)
            traverse_if_children(node.orelse, context, not_cond)

        else:
            for child in ast.iter_child_nodes(node):
                traverse(child, context)

    traverse(tree, [])
    
    return ["z3.And(" + ", ".join(path) + ")" for path in paths]

if __name__ == '__main__':
    path_conditions = collect_path_conditions(triangle_ast)
    path_conditions

if __name__ == '__main__':
    for path_condition in path_conditions:
        s = z3.Solver()
        s.add(a > 0, b > 0, c > 0)
        eval(f"s.check({path_condition})")
        m = s.model()
        print(m, triangle(m[a].as_long(), m[b].as_long(), m[c].as_long()))

## Things that will not work
## -------------------------

if __name__ == '__main__':
    print('\n## Things that will not work')



### (No) Type Checking

if __name__ == '__main__':
    print('\n### (No) Type Checking')



def typed_triangle(a: int, b: int, c: int) -> str:
    return triangle(a, b, c)

### (No) Program Proofs

if __name__ == '__main__':
    print('\n### (No) Program Proofs')



if __name__ == '__main__':
    x = 42
    x = "a string"

if __name__ == '__main__':
    p1, p2 = True, False

    if p1:
        x = 42
    if p2:
        del x

    # Does x exist at this point?

## The Virtues of Prototyping
## --------------------------

if __name__ == '__main__':
    print('\n## The Virtues of Prototyping')



## Try it out!
## -----------

if __name__ == '__main__':
    print('\n## Try it out!')



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



### Exercise 1: Features! Features!

if __name__ == '__main__':
    print('\n### Exercise 1: Features! Features!')


