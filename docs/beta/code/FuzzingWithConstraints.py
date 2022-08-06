#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Fuzzing with Constraints" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/FuzzingWithConstraints.html
# Last change: 2022-08-06 18:16:43+02:00
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
The Fuzzing Book - Fuzzing with Constraints

This file can be _executed_ as a script, running all experiments:

    $ python FuzzingWithConstraints.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.FuzzingWithConstraints import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/FuzzingWithConstraints.html

This chapter introduces the _ISLa framework_, consisting of 
* the _ISLa specification language_, allowing to add _constraints_ to a grammar
* the _ISLa solver_, solving these constraints to produce semantically (and syntactically) valid inputs
* the _ISLa checker_, checking given inputs for whether they satisfy these constraints.

A typical usage of the ISLa solver is as follows.
First, install ISLa, using 
shell
$ pip install isla-solver

Then, you can import the solver as

>>> from isla.solver import ISLaSolver  # type: ignore

The ISLa solver needs two things. First, a _grammar_ - say, US phone numbers.

>>> from Grammars import US_PHONE_GRAMMAR

Second, you need )constraints – a string expressing a condition over one or more grammar elements.
Common functions include
* `str.len()`, returning the length of a string
* `str.to.int()`, converting a string to an integer

Here, we instantiate the ISLa solver with a constraint stating that the area code should be above 900:

>>> solver = ISLaSolver(US_PHONE_GRAMMAR, 
>>>             """
>>>             str.to.int() > 900
>>>             """)

With that, invoking `solver.solve()` produces an iterator over multiple solutions.

>>> for _ in range(10):
>>>     print(next(solver.solve()))
(906)465-8279
(901)695-2708
(902)382-9074
(904)632-6458
(992)839-0278
(920)458-0439
(908)847-3098
(910)589-0372
(914)992-6350
(984)431-0475


We see that the solver produces a number of inputs that all satisfy the constraint.

The `solve()` method provides several additional parameters to configure the solver, as documented below
Additional `ISLaSolver` methods allow to check inputs against constraints, and provide additional functionality.

/Users/zeller/Projects/fuzzingbook/notebooks/ClassDiagram.ipynb:367: UserWarning: ISLaSolver.solve() is listed as public, but has no docstring
  warnings.warn(f"{f.__qualname__}() is listed as public,"
/Users/zeller/Projects/fuzzingbook/notebooks/ClassDiagram.ipynb:440: UserWarning: Class ISLaSolver has no docstring
  warnings.warn(f"Class {cls.__name__} has no docstring")
* FIXME: Have docstrings for publicly available methods
* FIXME: Have a docstring for the `ISLaSolver` class
* FIXME: Have a public interface for checking inputs against constraints (preferably in `ISLaSolver`, as it already has the grammar and the constraints).


For more details, source, and documentation, see
"The Fuzzing Book - Fuzzing with Constraints"
at https://www.fuzzingbook.org/html/FuzzingWithConstraints.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Fuzzing with Constraints
# ========================

if __name__ == '__main__':
    print('# Fuzzing with Constraints')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo("w4u5gCgPlmg")

if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

import sys

if __name__ == '__main__':
    if sys.version_info < (3, 10):
        print("This code requires Python 3.10 or later")
        sys.exit(0)

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Semantic Input Properties
## -------------------------

if __name__ == '__main__':
    print('\n## Semantic Input Properties')



from .Grammars import Grammar, is_valid_grammar, syntax_diagram, crange

import string

CONFIG_GRAMMAR: Grammar = {
    "<start>": ["<config>"],
    "<config>": [
        "pagesize=<pagesize>\n"
        "bufsize=<bufsize>"
    ],
    "<pagesize>": ["<int>"],
    "<bufsize>": ["<int>"],
    "<int>": ["<digit>", "<leaddigit><int>"],
    "<digit>": list("0123456789"),
    "<leaddigit>": list("123456789")
}

if __name__ == '__main__':
    assert is_valid_grammar(CONFIG_GRAMMAR)

if __name__ == '__main__':
    syntax_diagram(CONFIG_GRAMMAR)

from .GrammarFuzzer import GrammarFuzzer, DerivationTree

if __name__ == '__main__':
    fuzzer = GrammarFuzzer(CONFIG_GRAMMAR)

if __name__ == '__main__':
    for i in range(10):
        print(i)
        print(fuzzer.fuzz())

## Specifying Constraints
## ----------------------

if __name__ == '__main__':
    print('\n## Specifying Constraints')



import isla  # type: ignore

from isla.solver import ISLaSolver  # type: ignore

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 'str.len(<pagesize>) >= 6')

if __name__ == '__main__':
    for i in range(10):
        print(i)
        print(next(solver.solve()))   

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 'str.to.int(<pagesize>) >= 100000')
    print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                        '''
                    str.to.int(<pagesize>) >= 100 and 
                    str.to.int(<pagesize>) <= 200
                    ''')
    print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                        '''
                    (= (mod (str.to.int <pagesize>) 7) 0)
                    ''')
    print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                        '''
                    <pagesize> = <bufsize>
                    ''')
    print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                        '''
                    str.to.int(<pagesize>) > 1024 and
                    str.to.int(<bufsize>) = str.to.int(<pagesize>) + 1
                    ''')
    print(next(solver.solve()))

### Excursion: Using SMT-LIB Syntax

if __name__ == '__main__':
    print('\n### Excursion: Using SMT-LIB Syntax')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                    '''
                (> (str.to.int <pagesize>) 1024)
                and
                (= (str.to.int <bufsize>) (+ (str.to.int <pagesize>) 1))
                ''')
    print(next(solver.solve()))

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



## Accessing Elements
## ------------------

if __name__ == '__main__':
    print('\n## Accessing Elements')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                    '''
                <pagesize>.<int> = <bufsize>.<int>
                ''')
    print(next(solver.solve()))

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        solver = ISLaSolver(CONFIG_GRAMMAR, 
                    '''
                <config>..<digit> = "7"
                ''')
        print(next(solver.solve()))

from .Parser import EarleyParser
from .GrammarFuzzer import display_tree

if __name__ == '__main__':
    inp = 'pagesize=12\nbufsize=34'
    parser = EarleyParser(CONFIG_GRAMMAR)
    tree = next(parser.parse(inp))
    display_tree(tree)

if __name__ == '__main__':
    with ExpectError():
        solver = ISLaSolver(CONFIG_GRAMMAR, 
                    '''
                <int>.<digit>[2] = "7"
                ''')
        print(next(solver.solve()))

## Quantifiers
## -----------

if __name__ == '__main__':
    print('\n## Quantifiers')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            exists <int> i in <start>:
                (str.to.int(i) > 1000)
            ''')
    for i in range(10):
        print(i)
        print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            forall <int> i in <start>:
                (str.to.int(i) > 1000)
            ''')
    print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            str.to.int(<int>) > 1000
            ''')
    print(next(solver.solve()))

## Picking Expansions
## ------------------

if __name__ == '__main__':
    print('\n## Picking Expansions')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            forall <int> i="<digit>" in <start>:
                (i = "7")
            ''')

if __name__ == '__main__':
    print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            forall <int> i="<leaddigit><int>" in <start>:
                (str.to.int(i) > 100)
            ''')

if __name__ == '__main__':
    print(next(solver.solve()))

## Matching Expansion Elements
## ---------------------------

if __name__ == '__main__':
    print('\n## Matching Expansion Elements')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            forall <int> i="{<leaddigit> lead}{<int> remainder}" in <start>:
                (lead = "9")
            ''')

if __name__ == '__main__':
    print(next(solver.solve()))

if __name__ == '__main__':
    for i in range(1, 10):
        print(i)
        print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            <int>.<leaddigit> = "9"
            ''')

if __name__ == '__main__':
    for i in range(10):
        print(i)
        print(next(solver.solve()))

## Checking Inputs
## ---------------

if __name__ == '__main__':
    print('\n## Checking Inputs')



if __name__ == '__main__':
    constraint = '<pagesize> = <bufsize>'
    solver = ISLaSolver(CONFIG_GRAMMAR, constraint)

if __name__ == '__main__':
    tree = solver.parse('<config>', 'pagesize=12\nbufsize=34')

from isla.evaluator import evaluate  # type: ignore

if __name__ == '__main__':
    evaluate(constraint, tree, CONFIG_GRAMMAR)

if __name__ == '__main__':
    tree = solver.parse('<config>', 'pagesize=27\nbufsize=27')

if __name__ == '__main__':
    evaluate(constraint, tree, CONFIG_GRAMMAR)

## Case Studies
## ------------

if __name__ == '__main__':
    print('\n## Case Studies')



### Matching Identifiers in XML

if __name__ == '__main__':
    print('\n### Matching Identifiers in XML')



XML_GRAMMAR: Grammar = {
    "<start>": ["<xml-tree>"],
    "<xml-tree>": ["<open-tag><xml-content><close-tag>"],
    "<open-tag>": ["<<id>>"],
    "<close-tag>": ["</<id>>"],
    "<xml-content>": ["Text", "<xml-tree>"],
    "<id>": ["<letter>", "<id><letter>"],
    "<letter>": crange('a', 'z')
}

if __name__ == '__main__':
    assert is_valid_grammar(XML_GRAMMAR)

if __name__ == '__main__':
    syntax_diagram(XML_GRAMMAR)

if __name__ == '__main__':
    fuzzer = GrammarFuzzer(XML_GRAMMAR)
    fuzzer.fuzz()

if __name__ == '__main__':
    solver = ISLaSolver(XML_GRAMMAR, 
                '''
            <xml-tree>.<open-tag>.<id> = <xml-tree>.<close-tag>.<id>
            ''')
    for _ in range(3):
        print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(XML_GRAMMAR, 
                '''
            <xml-tree>.<open-tag>.<id> = <xml-tree>.<close-tag>.<id>
            and
            str.len(<id>) > 10
            ''')
    for _ in range(3):
        print(next(solver.solve()))

### Definitions and Usages in Programming Languages

if __name__ == '__main__':
    print('\n### Definitions and Usages in Programming Languages')



LANG_GRAMMAR: Grammar = {
    "<start>":
        ["<stmt>"],
    "<stmt>":
        ["<assgn>", "<assgn>; <stmt>"],
    "<assgn>":
        ["<lhs> := <rhs>"],
    "<lhs>":
        ["<var>"],
    "<rhs>":
        ["<var>", "<digit>"],
    "<var>": list(string.ascii_lowercase),
    "<digit>": list(string.digits)
}

if __name__ == '__main__':
    assert is_valid_grammar(LANG_GRAMMAR)

if __name__ == '__main__':
    syntax_diagram(LANG_GRAMMAR)

if __name__ == '__main__':
    fuzzer = GrammarFuzzer(LANG_GRAMMAR)

if __name__ == '__main__':
    for _ in range(10):
        print(fuzzer.fuzz())

if __name__ == '__main__':
    solver = ISLaSolver(LANG_GRAMMAR, 
                '''
            forall <rhs> in <stmt>:
                exists <lhs> in <stmt>:
                    <rhs>.<var> = <lhs>.<var>
            ''')

if __name__ == '__main__':
    for _ in range(10):
        print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(LANG_GRAMMAR, 
                '''
            forall <rhs> in <stmt>:
                exists <lhs> in <stmt>:
                    (before(<lhs>, <rhs>) and
                     <rhs>.<var> = <lhs>.<var>)
            ''')

if __name__ == '__main__':
    for _ in range(10):
        print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(LANG_GRAMMAR, 
                '''
            forall <rhs> in <stmt>:
                exists <lhs> in <stmt>:
                    (before(<lhs>, <rhs>) and
                     <rhs>.<var> = <lhs>.<var>)
            and
            count(<start>, "<assgn>", 5)
            ''')

if __name__ == '__main__':
    with ExpectError():
        for _ in range(10):
            print(next(solver.solve()))

if __name__ == '__main__':
    solver = ISLaSolver(LANG_GRAMMAR, 
                '''
            str.len(<stmt>) > 20
            ''')

if __name__ == '__main__':
    with ExpectError():
        for _ in range(10):
            print(next(solver.solve()))

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



from isla.solver import ISLaSolver  # type: ignore

from .Grammars import US_PHONE_GRAMMAR

if __name__ == '__main__':
    solver = ISLaSolver(US_PHONE_GRAMMAR, 
                """
            str.to.int(<area>) > 900
            """)

if __name__ == '__main__':
    for _ in range(10):
        print(next(solver.solve()))

import warnings

if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("default")

        from ClassDiagram import display_class_hierarchy
        hierarchy = display_class_hierarchy([ISLaSolver],
                               public_methods=[
                                    ISLaSolver.__init__,
                                    ISLaSolver.solve,
                                ])
    hierarchy

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


