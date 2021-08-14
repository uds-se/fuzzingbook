#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Mutation Analysis" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/MutationAnalysis.html
# Last change: 2021-06-04 14:41:13+02:00
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
The Fuzzing Book - Mutation Analysis

This file can be _executed_ as a script, running all experiments:

    $ python MutationAnalysis.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.MutationAnalysis import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/MutationAnalysis.html

This chapter introduces two methods of running *mutation analysis* on subject programs. The first class `MuFunctionAnalyzer` targets individual functions. Given a function `gcd` and two test cases evaluate, one can run mutation analysis on the test cases as follows:

>>> for mutant in MuFunctionAnalyzer(gcd, log=True):
>>>     with mutant:
>>>         assert gcd(1, 0) == 1, "Minimal"
>>>         assert gcd(0, 1) == 1, "Mirror"
>>> mutant.pm.score()
->	gcd_1
	gcd_2
	gcd_3
	gcd_4
 Minimal


0.25

The second class `MuProgramAnalyzer` targets standalone programs with test suites. Given a program `gcd` whose source code is provided in `gcd_src` and the test suite is provided by `TestGCD`, one can evaluate the mutation score of `TestGCD` as follows:

>>> class TestGCD(unittest.TestCase):
>>>     def test_simple(self):
>>>         assert cfg.gcd(1, 0) == 1
>>> 
>>>     def test_mirror(self):
>>>         assert cfg.gcd(0, 1) == 1
>>> for mutant in MuProgramAnalyzer('gcd', gcd_src):
>>>     mutant[test_module].runTest('TestGCD')
>>> mutant.pm.score()
======================================================================
FAIL: test_simple (__main__.TestGCD)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "", line 3, in test_simple
    assert cfg.gcd(1, 0) == 1
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
======================================================================
FAIL: test_simple (__main__.TestGCD)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "", line 3, in test_simple
    assert cfg.gcd(1, 0) == 1
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
======================================================================
FAIL: test_simple (__main__.TestGCD)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "", line 3, in test_simple
    assert cfg.gcd(1, 0) == 1
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
======================================================================
FAIL: test_simple (__main__.TestGCD)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "", line 3, in test_simple
    assert cfg.gcd(1, 0) == 1
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
======================================================================
FAIL: test_simple (__main__.TestGCD)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "", line 3, in test_simple
    assert cfg.gcd(1, 0) == 1
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
======================================================================
FAIL: test_simple (__main__.TestGCD)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "", line 3, in test_simple
    assert cfg.gcd(1, 0) == 1
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
======================================================================
FAIL: test_simple (__main__.TestGCD)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "", line 3, in test_simple
    assert cfg.gcd(1, 0) == 1
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)

1.0

The mutation score thus obtained is a better indicator of the quality of a given test suite than pure coverage.


For more details, source, and documentation, see
"The Fuzzing Book - Mutation Analysis"
at https://www.fuzzingbook.org/html/MutationAnalysis.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Mutation Analysis
# =================

if __name__ == '__main__':
    print('# Mutation Analysis')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Why Structural Coverage is Not Enough
## -------------------------------------

if __name__ == '__main__':
    print('\n## Why Structural Coverage is Not Enough')



def ineffective_test():
    execute_the_program_as_a_whole()
    assert True

def ineffective_test():
    try:
        execute_the_program_as_a_whole()
    except:
        pass
    assert True

## Seeding Artificial Faults with Mutation Analysis
## ------------------------------------------------

if __name__ == '__main__':
    print('\n## Seeding Artificial Faults with Mutation Analysis')



## Structural Coverage Adequacy by Example
## ---------------------------------------

if __name__ == '__main__':
    print('\n## Structural Coverage Adequacy by Example')



def triangle(a, b, c):
    if a == b:
        if b == c:
            return 'Equilateral'
        else:
            return 'Isosceles'
    else:
        if b == c:
            return "Isosceles"
        else:
            if a == c:
                return "Isosceles"
            else:
                return "Scalene"

def strong_oracle(fn):
    assert fn(1, 1, 1) == 'Equilateral'

    assert fn(1, 2, 1) == 'Isosceles'
    assert fn(2, 2, 1) == 'Isosceles'
    assert fn(1, 2, 2) == 'Isosceles'

    assert fn(1, 2, 3) == 'Scalene'

if __name__ == '__main__':
    strong_oracle(triangle)

if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .Coverage import Coverage

import inspect

class Coverage(Coverage):
    def show_coverage(self, fn):
        src = inspect.getsource(fn)
        name = fn.__name__
        covered = set([lineno for method,
                       lineno in self._trace if method == name])
        for i, s in enumerate(src.split('\n')):
            print('%s %2d: %s' % ('#' if i + 1 in covered else ' ', i + 1, s))

if __name__ == '__main__':
    with Coverage() as cov:
        strong_oracle(triangle)

if __name__ == '__main__':
    cov.show_coverage(triangle)

def weak_oracle(fn):
    assert fn(1, 1, 1) == 'Equilateral'

    assert fn(1, 2, 1) != 'Equilateral'
    assert fn(2, 2, 1) != 'Equilateral'
    assert fn(1, 2, 2) != 'Equilateral'

    assert fn(1, 2, 3) != 'Equilateral'

if __name__ == '__main__':
    with Coverage() as cov:
        weak_oracle(triangle)

if __name__ == '__main__':
    cov.show_coverage(triangle)

## Injecting Artificial Faults
## ---------------------------

if __name__ == '__main__':
    print('\n## Injecting Artificial Faults')



def triangle_m1(a, b, c):
    if a == b:
        if b == c:
            return 'Equilateral'
        else:
            # return 'Isosceles'
            return None  # <-- injected fault
    else:
        if b == c:
            return "Isosceles"
        else:
            if a == c:
                return "Isosceles"
            else:
                return "Scalene"

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        weak_oracle(triangle_m1)

if __name__ == '__main__':
    with ExpectError():
        strong_oracle(triangle_m1)

## Mutating Python Code
## --------------------

if __name__ == '__main__':
    print('\n## Mutating Python Code')



import ast
import astor
import inspect

if __name__ == '__main__':
    triangle_source = inspect.getsource(triangle)
    triangle_source

from .bookutils import print_content

if __name__ == '__main__':
    print_content(triangle_source, '.py')

if __name__ == '__main__':
    triangle_ast = ast.parse(triangle_source)

if __name__ == '__main__':
    print(astor.dump_tree(triangle_ast))

from .bookutils import rich_output

if __name__ == '__main__':
    if rich_output():
        import showast
        showast.show_ast(triangle_ast)

if __name__ == '__main__':
    print_content(astor.to_source(triangle_ast), '.py')

## A Simple Mutator for Functions
## ------------------------------

if __name__ == '__main__':
    print('\n## A Simple Mutator for Functions')



class MuFunctionAnalyzer:
    def __init__(self, fn, log=False):
        self.fn = fn
        self.name = fn.__name__
        src = inspect.getsource(fn)
        self.ast = ast.parse(src)
        self.src = astor.to_source(self.ast)  # normalize
        self.mutator = self.mutator_object()
        self.nmutations = self.get_mutation_count()
        self.un_detected = set()
        self.mutants = []
        self.log = log

    def mutator_object(self, locations=None):
        return StmtDeletionMutator(locations)

    def register(self, m):
        self.mutants.append(m)

    def finish(self):
        pass

class MuFunctionAnalyzer(MuFunctionAnalyzer):
    def get_mutation_count(self):
        self.mutator.visit(self.ast)
        return self.mutator.count

class Mutator(ast.NodeTransformer):
    def __init__(self, mutate_location=-1):
        self.count = 0
        self.mutate_location = mutate_location

    def mutable_visit(self, node):
        self.count += 1  # statements start at line no 1
        if self.count == self.mutate_location:
            return self.mutation_visit(node)
        return self.generic_visit(node)

class StmtDeletionMutator(Mutator):
    def visit_Return(self, node): return self.mutable_visit(node)
    def visit_Delete(self, node): return self.mutable_visit(node)

    def visit_Assign(self, node): return self.mutable_visit(node)
    def visit_AnnAssign(self, node): return self.mutable_visit(node)
    def visit_AugAssign(self, node): return self.mutable_visit(node)

    def visit_Raise(self, node): return self.mutable_visit(node)
    def visit_Assert(self, node): return self.mutable_visit(node)

    def visit_Global(self, node): return self.mutable_visit(node)
    def visit_Nonlocal(self, node): return self.mutable_visit(node)

    def visit_Expr(self, node): return self.mutable_visit(node)

    def visit_Pass(self, node): return self.mutable_visit(node)
    def visit_Break(self, node): return self.mutable_visit(node)
    def visit_Continue(self, node): return self.mutable_visit(node)

class StmtDeletionMutator(StmtDeletionMutator):
    def mutation_visit(self, node): return ast.Pass()    

if __name__ == '__main__':
    MuFunctionAnalyzer(triangle).nmutations

class MuFunctionAnalyzer(MuFunctionAnalyzer):
    def __iter__(self):
        return PMIterator(self)

class PMIterator:
    def __init__(self, pm):
        self.pm = pm
        self.idx = 0

class PMIterator(PMIterator):
    def __next__(self):
        i = self.idx
        if i >= self.pm.nmutations:
            self.pm.finish()
            raise StopIteration()
        self.idx += 1
        mutant = Mutant(self.pm, self.idx, log=self.pm.log)
        self.pm.register(mutant)
        return mutant

class Mutant:
    def __init__(self, pm, location, log=False):
        self.pm = pm
        self.i = location
        self.name = "%s_%s" % (self.pm.name, self.i)
        self._src = None
        self.tests = []
        self.detected = False
        self.log = log

if __name__ == '__main__':
    for m in MuFunctionAnalyzer(triangle):
        print(m.name)

class Mutant(Mutant):
    def generate_mutant(self, location):
        mutant_ast = self.pm.mutator_object(
            location).visit(ast.parse(self.pm.src))  # copy
        return astor.to_source(mutant_ast)

class Mutant(Mutant):
    def src(self):
        if self._src is None:
            self._src = self.generate_mutant(self.i)
        return self._src

import difflib

if __name__ == '__main__':
    for mutant in MuFunctionAnalyzer(triangle):
        shape_src = mutant.pm.src
        for line in difflib.unified_diff(mutant.pm.src.split('\n'),
                                         mutant.src().split('\n'),
                                         fromfile=mutant.pm.name,
                                         tofile=mutant.name, n=3):
            print(line)

class Mutant(Mutant):
    def diff(self):
        return '\n'.join(difflib.unified_diff(self.pm.src.split('\n'),
                                              self.src().split('\n'),
                                              fromfile='original',
                                              tofile='mutant',
                                              n=3))

## Evaluating Mutations
## --------------------

if __name__ == '__main__':
    print('\n## Evaluating Mutations')



class Mutant(Mutant):
    def __enter__(self):
        if self.log:
            print('->\t%s' % self.name)
        c = compile(self.src(), '<mutant>', 'exec')
        eval(c, globals())

class Mutant(Mutant):
    def __exit__(self, exc_type, exc_value, traceback):
        if self.log:
            print('<-\t%s' % self.name)
        if exc_type is not None:
            self.detected = True
            if self.log:
                print("Detected %s" % self.name, exc_type, exc_value)
        globals()[self.pm.name] = self.pm.fn
        if self.log:
            print()
        return True

from .ExpectError import ExpectTimeout

class MuFunctionAnalyzer(MuFunctionAnalyzer):
    def finish(self):
        self.un_detected = {
            mutant for mutant in self.mutants if not mutant.detected}

class MuFunctionAnalyzer(MuFunctionAnalyzer):
    def score(self):
        return (self.nmutations - len(self.un_detected)) / self.nmutations

import sys

if __name__ == '__main__':
    for mutant in MuFunctionAnalyzer(triangle, log=True):
        with mutant:
            assert triangle(1, 1, 1) == 'Equilateral', "Equal Check1"
            assert triangle(1, 0, 1) != 'Equilateral', "Equal Check2"
            assert triangle(1, 0, 2) != 'Equilateral', "Equal Check3"
    mutant.pm.score()

if __name__ == '__main__':
    for mutant in MuFunctionAnalyzer(triangle):
        with mutant:
            weak_oracle(triangle)
    mutant.pm.score()

def oracle():
    strong_oracle(triangle)

if __name__ == '__main__':
    for mutant in MuFunctionAnalyzer(triangle, log=True):
        with mutant:
            oracle()
    mutant.pm.score()

def gcd(a, b):
    if a < b:
        c = a
        a = b
        b = c

    while b != 0:
        c = a
        a = b
        b = c % b
    return a

if __name__ == '__main__':
    for mutant in MuFunctionAnalyzer(gcd, log=True):
        with mutant:
            assert gcd(1, 0) == 1, "Minimal"
            assert gcd(0, 1) == 1, "Mirror"
    mutant.pm.score()

## Mutator for Modules and Test Suites
## -----------------------------------

if __name__ == '__main__':
    print('\n## Mutator for Modules and Test Suites')



import types

def import_code(code, name):
    module = types.ModuleType(name)
    exec(code, module.__dict__)
    return module

if __name__ == '__main__':
    shape = import_code(shape_src, 'shape')

if __name__ == '__main__':
    shape.triangle(1, 1, 1)

import unittest

class StrongShapeTest(unittest.TestCase):

    def test_equilateral(self):
        assert shape.triangle(1, 1, 1) == 'Equilateral'

    def test_isosceles(self):
        assert shape.triangle(1, 2, 1) == 'Isosceles'
        assert shape.triangle(2, 2, 1) == 'Isosceles'
        assert shape.triangle(1, 2, 2) == 'Isosceles'

    def test_scalene(self):
        assert shape.triangle(1, 2, 3) == 'Scalene'

def suite(test_class):
    suite = unittest.TestSuite()
    for f in test_class.__dict__:
        if f.startswith('test_'):
            suite.addTest(test_class(f))
    return suite

if __name__ == '__main__':
    suite(StrongShapeTest).run(unittest.TestResult())

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=0, failfast=True)
    runner.run(suite(StrongShapeTest))

if __name__ == '__main__':
    with Coverage() as cov:
        suite(StrongShapeTest).run(unittest.TestResult())

if __name__ == '__main__':
    cov.show_coverage(triangle)

class WeakShapeTest(unittest.TestCase):
    def test_equilateral(self):
        assert shape.triangle(1, 1, 1) == 'Equilateral'

    def test_isosceles(self):
        assert shape.triangle(1, 2, 1) != 'Equilateral'
        assert shape.triangle(2, 2, 1) != 'Equilateral'
        assert shape.triangle(1, 2, 2) != 'Equilateral'

    def test_scalene(self):
        assert shape.triangle(1, 2, 3) != 'Equilateral'

if __name__ == '__main__':
    with Coverage() as cov:
        suite(WeakShapeTest).run(unittest.TestResult())

if __name__ == '__main__':
    cov.show_coverage(triangle)

class MuProgramAnalyzer(MuFunctionAnalyzer):
    def __init__(self, name, src):
        self.name = name
        self.ast = ast.parse(src)
        self.src = astor.to_source(self.ast)
        self.changes = []
        self.mutator = self.mutator_object()
        self.nmutations = self.get_mutation_count()
        self.un_detected = set()

    def mutator_object(self, locations=None):
        return AdvStmtDeletionMutator(self, locations)

class AdvMutator(Mutator):
    def __init__(self, analyzer, mutate_locations=None):
        self.count = 0
        self.mutate_locations = [] if mutate_locations is None else mutate_locations
        self.pm = analyzer

    def mutable_visit(self, node):
        self.count += 1  # statements start at line no 1
        return self.mutation_visit(node)

class AdvStmtDeletionMutator(AdvMutator, StmtDeletionMutator):
    def __init__(self, analyzer, mutate_locations=None):
        AdvMutator.__init__(self, analyzer, mutate_locations)

    def mutation_visit(self, node):
        index = 0  # there is only one way to delete a statement -- replace it by pass
        if not self.mutate_locations:  # counting pass
            self.pm.changes.append((self.count, index))
            return self.generic_visit(node)
        else:
            # get matching changes for this pass
            mutating_lines = set((count, idx)
                                 for (count, idx) in self.mutate_locations)
            if (self.count, index) in mutating_lines:
                return ast.Pass()
            else:
                return self.generic_visit(node)

if __name__ == '__main__':
    MuProgramAnalyzer('shape', shape_src).nmutations

class MuProgramAnalyzer(MuProgramAnalyzer):
    def __iter__(self):
        return AdvPMIterator(self)

class AdvPMIterator:
    def __init__(self, pm):
        self.pm = pm
        self.idx = 0

class AdvPMIterator(AdvPMIterator):
    def __next__(self):
        i = self.idx
        if i >= len(self.pm.changes):
            raise StopIteration()
        self.idx += 1
        # there could be multiple changes in one mutant
        return AdvMutant(self.pm, [self.pm.changes[i]])

class AdvMutant(Mutant):
    def __init__(self, pm, locations):
        self.pm = pm
        self.i = locations
        self.name = "%s_%s" % (self.pm.name,
                               '_'.join([str(i) for i in self.i]))
        self._src = None

if __name__ == '__main__':
    shape_src = inspect.getsource(triangle)

if __name__ == '__main__':
    for m in MuProgramAnalyzer('shape', shape_src):
        print(m.name)

class AdvMutant(AdvMutant):
    def generate_mutant(self, locations):
        mutant_ast = self.pm.mutator_object(
            locations).visit(ast.parse(self.pm.src))  # copy
        return astor.to_source(mutant_ast)

class AdvMutant(AdvMutant):
    def src(self):
        if self._src is None:
            self._src = self.generate_mutant(self.i)
        return self._src

import difflib

class AdvMutant(AdvMutant):
    def diff(self):
        return '\n'.join(difflib.unified_diff(self.pm.src.split('\n'),
                                              self.src().split('\n'),
                                              fromfile='original',
                                              tofile='mutant',
                                              n=3))

if __name__ == '__main__':
    for mutant in MuProgramAnalyzer('shape', shape_src):
        print(mutant.name)
        print(mutant.diff())
        break

class AdvMutant(AdvMutant):
    def __getitem__(self, test_module):
        test_module.__dict__[
            self.pm.name] = import_code(
            self.src(), self.pm.name)
        return MutantTestRunner(self, test_module)

from .ExpectError import ExpectTimeout

class MutantTestRunner:
    def __init__(self, mutant, test_module):
        self.mutant = mutant
        self.tm = test_module

    def runTest(self, tc):
        suite = unittest.TestSuite()
        test_class = self.tm.__dict__[tc]
        for f in test_class.__dict__:
            if f.startswith('test_'):
                suite.addTest(test_class(f))
        runner = unittest.TextTestRunner(verbosity=0, failfast=True)
        try:
            with ExpectTimeout(1):
                res = runner.run(suite)
                if res.wasSuccessful():
                    self.mutant.pm.un_detected.add(self)
                return res
        except SyntaxError:
            print('Syntax Error (%s)' % self.mutant.name)
            return None
        raise Exception('Unhandled exception during test execution')

class MuProgramAnalyzer(MuProgramAnalyzer):
    def score(self):
        return (self.nmutations - len(self.un_detected)) / self.nmutations

import sys

if __name__ == '__main__':
    test_module = sys.modules[__name__]
    for mutant in MuProgramAnalyzer('shape', shape_src):
        mutant[test_module].runTest('WeakShapeTest')
    mutant.pm.score()

if __name__ == '__main__':
    for mutant in MuProgramAnalyzer('shape', shape_src):
        mutant[test_module].runTest('StrongShapeTest')
    mutant.pm.score()

if __name__ == '__main__':
    gcd_src = inspect.getsource(gcd)

class TestGCD(unittest.TestCase):
    def test_simple(self):
        assert cfg.gcd(1, 0) == 1

    def test_mirror(self):
        assert cfg.gcd(0, 1) == 1

if __name__ == '__main__':
    for mutant in MuProgramAnalyzer('cfg', gcd_src):
        mutant[test_module].runTest('TestGCD')
    mutant.pm.score()

## The Problem of  Equivalent Mutants
## ----------------------------------

if __name__ == '__main__':
    print('\n## The Problem of  Equivalent Mutants')



def new_gcd(a, b):
    if a < b:
        a, b = b, a
    else:
        a, b = a, b

    while b != 0:
        a, b = b, a % b
    return a

def gcd(a, b):
    if a < b:
        a, b = b, a
    else:
        pass

    while b != 0:
        a, b = b, a % b
    return a

if __name__ == '__main__':
    for i, mutant in enumerate(MuFunctionAnalyzer(new_gcd)):
        print(i,mutant.src())

### Statistical Estimation of Number of Equivalent Mutants

if __name__ == '__main__':
    print('\n### Statistical Estimation of Number of Equivalent Mutants')



### Statistical Estimation of the Number of Immortals by Chao's Estimator

if __name__ == '__main__':
    print("\n### Statistical Estimation of the Number of Immortals by Chao's Estimator")



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    for mutant in MuFunctionAnalyzer(gcd, log=True):
        with mutant:
            assert gcd(1, 0) == 1, "Minimal"
            assert gcd(0, 1) == 1, "Mirror"
    mutant.pm.score()

class TestGCD(unittest.TestCase):
    def test_simple(self):
        assert cfg.gcd(1, 0) == 1

    def test_mirror(self):
        assert cfg.gcd(0, 1) == 1

if __name__ == '__main__':
    for mutant in MuProgramAnalyzer('gcd', gcd_src):
        mutant[test_module].runTest('TestGCD')
    mutant.pm.score()

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



### Exercise 1:  Arithmetic Expression Mutators

if __name__ == '__main__':
    print('\n### Exercise 1:  Arithmetic Expression Mutators')



if __name__ == '__main__':
    print(astor.dump_tree(ast.parse("1 + 2 - 3 * 4 / 5")))

if __name__ == '__main__':
    print(astor.dump_tree(ast.parse("1 + 2 - 3 * 4 / 5")))

class BinOpMutator(Mutator):
    def visit_BinOp(self, node): return self.mutable_visit(node)

class BinOpMutator(BinOpMutator):
    def mutation_visit(self, node):
        replacement = {
            type(ast.Add()): ast.Sub(),
            type(ast.Sub()): ast.Add(),
            type(ast.Mult()): ast.Div(),
            type(ast.Div()): ast.Mult()
        }
        
        try:
            node.op = replacement[type(node.op)]
        except KeyError:
            pass  # All other binary operators (and, mod, etc.)

        return node

class MuBinOpAnalyzer(MuFunctionAnalyzer):
    def mutator_object(self, locations=None):
        return BinOpMutator(locations)

def arith_expr():
    return 1 + 2 - 3 * 4 / 5

if __name__ == '__main__':
    for mutant in MuBinOpAnalyzer(arith_expr, log=True):
        print(mutant.diff())

### Exercise 2: Optimizing Mutation Analysis

if __name__ == '__main__':
    print('\n### Exercise 2: Optimizing Mutation Analysis')



### Exercise 3: Byte Code Mutator

if __name__ == '__main__':
    print('\n### Exercise 3: Byte Code Mutator')



### Exercise 4: Estimating Residual Defect Density

if __name__ == '__main__':
    print('\n### Exercise 4: Estimating Residual Defect Density')


