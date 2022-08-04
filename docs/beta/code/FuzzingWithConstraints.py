#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Fuzzing with Constraints" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/FuzzingWithConstraints.html
# Last change: 2022-08-04 17:21:55+02:00
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

_For those only interested in using the code in this chapter (without wanting to know how it works), give an example.  This will be copied to the beginning of the chapter (before the first section) as text with rendered input and output._

/Users/zeller/Projects/fuzzingbook/notebooks/ClassDiagram.ipynb:367: UserWarning: ISLaSolver.solve() is listed as public, but has no docstring
  warnings.warn(f"{f.__qualname__}() is listed as public,"
/Users/zeller/Projects/fuzzingbook/notebooks/ClassDiagram.ipynb:440: UserWarning: Class ISLaSolver has no docstring
  warnings.warn(f"Class {cls.__name__} has no docstring")
* FIXME: Have docstrings for publicly available methods
* FIXME: Have a docstring for the `ISLaSolver` class
* FIXME: How do I check a given string whether it satisfies constraints? (Likely `isla.evaluator.evaluate(constraint, tree, grammar)`)


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

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Semantic Input Properties
## -------------------------

if __name__ == '__main__':
    print('\n## Semantic Input Properties')



from .Grammars import Grammar, is_valid_grammar

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

from .GrammarFuzzer import GrammarFuzzer

if __name__ == '__main__':
    fuzzer = GrammarFuzzer(CONFIG_GRAMMAR)

if __name__ == '__main__':
    for i in range(10):
        print(i)
        print(fuzzer.fuzz())

## Constraints to the Rescue
## -------------------------

if __name__ == '__main__':
    print('\n## Constraints to the Rescue')



import isla  # type: ignore

from isla.language import parse_isla  # type: ignore

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



## Quantifiers
## -----------

if __name__ == '__main__':
    print('\n## Quantifiers')



## Checking Inputs
## ---------------

if __name__ == '__main__':
    print('\n## Checking Inputs')



## A Simple Language
## -----------------

if __name__ == '__main__':
    print('\n## A Simple Language')



LANG_GRAMMAR: Grammar = {
    "<start>":
        ["<stmt>"],
    "<stmt>":
        ["<assgn>", "<assgn> ; <stmt>"],
    "<assgn>":
        ["<var> := <rhs>"],
    "<rhs>":
        ["<var>", "<digit>"],
    "<var>": list(string.ascii_lowercase),
    "<digit>": list(string.digits)
}

if __name__ == '__main__':
    assert is_valid_grammar(LANG_GRAMMAR)

## A Simple Fuzzer
## ---------------

if __name__ == '__main__':
    print('\n## A Simple Fuzzer')



if __name__ == '__main__':
    for i in range(10):
        print(fuzzer.fuzz())

## Beyond Syntax: Semantic Input Properties
## ----------------------------------------

if __name__ == '__main__':
    print('\n## Beyond Syntax: Semantic Input Properties')



from isla.isla_predicates import STANDARD_STRUCTURAL_PREDICATES  # type: ignore

if __name__ == '__main__':
    constraint = parse_isla("""
exists <assgn> assgn: 
  (before(assgn, <assgn>) and <assgn>.<rhs>.<var> = assgn.<var>)
""",
    grammar=LANG_GRAMMAR,
    structural_predicates=STANDARD_STRUCTURAL_PREDICATES)

if __name__ == '__main__':
    constraint = parse_isla("""
exists <digit> x:
  (str.to.int(x) >= 9)
""", grammar=LANG_GRAMMAR)

if __name__ == '__main__':
    constraint = parse_isla("""
exists <digit> x:
  (>= (str.to.int x) 9)
""", LANG_GRAMMAR)

if __name__ == '__main__':
    constraint = parse_isla("""
  (>= (str.to.int <digit>) 9)
""", LANG_GRAMMAR)

if __name__ == '__main__':
    solver = ISLaSolver(
        grammar=LANG_GRAMMAR,
        formula=constraint)

if __name__ == '__main__':
    solver = ISLaSolver(LANG_GRAMMAR, '(>= (str.to.int <digit>) 9)')

if __name__ == '__main__':
    for i in range(10):
        print(next(solver.solve()))

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



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



### Exercise 1: _Title_

if __name__ == '__main__':
    print('\n### Exercise 1: _Title_')



if __name__ == '__main__':
    pass

if __name__ == '__main__':
    2 + 2

### Exercise 2: _Title_

if __name__ == '__main__':
    print('\n### Exercise 2: _Title_')


