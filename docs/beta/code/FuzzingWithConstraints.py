#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Fuzzing with Constraints" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/FuzzingWithConstraints.html
# Last change: 2022-08-09 11:02:46+02:00
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

Second, you need _constraints_ – a string expressing a condition over one or more grammar elements.
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
(960)451-2706
(910)831-0847
(904)468-5290
(940)348-3721
(914)771-6402
(909)281-2704
(920)528-9146
(908)643-6982
(980)638-7014
(901)896-7204


We see that the solver produces a number of inputs that all satisfy the constraint - the area code is always more than 900.

The `solve()` method provides several additional parameters to configure the solver, as documented below
Additional `ISLaSolver` methods allow to check inputs against constraints, and provide additional functionality.

>>> from ClassDiagram import display_class_hierarchy
>>> hierarchy = display_class_hierarchy([ISLaSolver],
>>>                        public_methods=[
>>>                             ISLaSolver.__init__,
>>>                             ISLaSolver.solve,
>>>                             ISLaSolver.evaluate,
>>>                         ])
>>> hierarchy

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
    YouTubeVideo("FADrEcA0wos")

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
    "<int>": ["<leaddigit><digits>"],
    "<digits>": ["", "<digit><digits>"],
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

### Excursion: Unrestricted Grammars

if __name__ == '__main__':
    print('\n### Excursion: Unrestricted Grammars')



### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



## Specifying Constraints
## ----------------------

if __name__ == '__main__':
    print('\n## Specifying Constraints')



import isla  # type: ignore

from isla.solver import ISLaSolver  # type: ignore

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 'str.len(<pagesize>) >= 6')

import itertools

if __name__ == '__main__':
    solutions = itertools.islice(solver.solve(), 10)
    for i, solution in enumerate(solutions):
        print(i)
        print(solution)   

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR,
                        'str.to.int(<pagesize>) >= 100000')
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
                    str.to.int(<pagesize>) mod 7 = 0
                    ''')
    print(next(solver.solve()))

from .bookutils import quiz

if __name__ == '__main__':
    quiz("Which of the following constraints expresses "
         "that the page size and the buffer size "
         "have to be equal? Try it out!",
         [
             "`<pagesize> is <bufsize>`",
             "`str.to.int(<pagesize>) = str.to.int(<bufsize>)`",
             "`<pagesize>) = <bufsize>`",
             "`atoi(<pagesize>) == atoi(<bufsize>)`",
         ], "[4 ** 0.5, 9 ** 0.5]")

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

if __name__ == '__main__':
    quiz("Which constraints are necessary to "
         "ensure that all digits are between 1 and 3?",
         [
             "`str.to.int(<digit>) >= 1`",
             "`str.to.int(<digit>) <= 3`",
             "`str.to.int(<leaddigit>) >= 1`",
             "`str.to.int(<leaddigit>) <= 3`",
         ], "[1 ** 0, 4 ** 0.5, 16 ** 0.5]")

### Excursion: Using SMT-LIB Syntax

if __name__ == '__main__':
    print('\n### Excursion: Using SMT-LIB Syntax')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                    '''
                (and
                  (> (str.to.int <pagesize>) 1024)
                  (= (str.to.int <bufsize>)
                     (+ (str.to.int <pagesize>) 1)))
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

from .Parser import EarleyParser  # minor dependency
from .GrammarFuzzer import display_tree

if __name__ == '__main__':
    inp = 'pagesize=12\nbufsize=34'
    parser = EarleyParser(CONFIG_GRAMMAR)
    tree = next(parser.parse(inp))
    display_tree(tree)

LINES_OF_THREE_AS_OR_BS_GRAMMAR: Grammar = {
    '<start>': ['<A>'],
    '<A>': ['<B><B><B>', '<B><B><B>\n<A>'],
    '<B>': ['a', 'b']
}

if __name__ == '__main__':
    fuzzer = GrammarFuzzer(LINES_OF_THREE_AS_OR_BS_GRAMMAR)
    for _ in range(5):
        print(fuzzer.fuzz())
        print()

if __name__ == '__main__':
    solver = ISLaSolver(LINES_OF_THREE_AS_OR_BS_GRAMMAR, 
                '''
            <A>.<B>[2] = "b"
            ''')

    for solution in itertools.islice(solver.solve(), 5):
        print(solution)
        print()

## Quantifiers
## -----------

if __name__ == '__main__':
    print('\n## Quantifiers')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            exists <int> i in <start>:
                str.to.int(i) > 1000
            ''')

    for i, solution in enumerate(itertools.islice(solver.solve(), 10)):
        print(i)
        print(solution)

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            forall <int> i in <start>:
                str.to.int(i) > 1000
            ''')

    for i, solution in enumerate(itertools.islice(solver.solve(), 10)):
        print(i)
        print(solution)

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            str.to.int(<int>) > 1000
            ''')

    for i, solution in enumerate(itertools.islice(solver.solve(), 10)):
        print(i)
        print(solution)

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
            forall <int> i="{<leaddigit> lead}<digits>" in <start>:
                (lead = "9")
            ''')

if __name__ == '__main__':
    for i, solution in enumerate(itertools.islice(solver.solve(), 10)):
        print(i)
        print(solution)

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            <int>.<leaddigit> = "9"
            ''')

if __name__ == '__main__':
    for i, solution in enumerate(itertools.islice(solver.solve(), 10)):
        print(i)
        print(solution)

## Checking Inputs
## ---------------

if __name__ == '__main__':
    print('\n## Checking Inputs')



if __name__ == '__main__':
    constraint = '<pagesize> = <bufsize>'
    solver = ISLaSolver(CONFIG_GRAMMAR, constraint)

if __name__ == '__main__':
    solver.evaluate('pagesize=12\nbufsize=34')

if __name__ == '__main__':
    solver.evaluate('pagesize=27\nbufsize=27')

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
            ''', max_number_smt_instantiations=1)

    for solution in itertools.islice(solver.solve(), 3):
        print(solution)

### Excursion: Solver Configuration Parameters

if __name__ == '__main__':
    print('\n### Excursion: Solver Configuration Parameters')



if __name__ == '__main__':
    solver = ISLaSolver(XML_GRAMMAR, 
                '''
            <xml-tree>.<open-tag>.<id> = <xml-tree>.<close-tag>.<id>
            ''', max_number_smt_instantiations=10)

    for solution in itertools.islice(solver.solve(), 3):
        print(solution)

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



if __name__ == '__main__':
    solver = ISLaSolver(XML_GRAMMAR, 
                '''
            <xml-tree>.<open-tag>.<id> = <xml-tree>.<close-tag>.<id>
            and
            str.len(<id>) > 10
            ''', max_number_smt_instantiations=1)

    for solution in itertools.islice(solver.solve(), 3):
        print(solution)

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
            forall <rhs> in <assgn>:
                exists <assgn> declaration:
                    <rhs>.<var> = declaration.<lhs>.<var>
            ''', max_number_smt_instantiations=1, max_number_free_instantiations=1)

if __name__ == '__main__':
    for solution in itertools.islice(solver.solve(), 10):
        print(solution)

if __name__ == '__main__':
    solver = ISLaSolver(LANG_GRAMMAR, 
                '''
            forall <rhs> in <assgn>:
                exists <assgn> declaration:
                    (before(declaration, <assgn>) and
                     <rhs>.<var> = declaration.<lhs>.<var>)
            ''', max_number_free_instantiations=1, max_number_smt_instantiations=1)

if __name__ == '__main__':
    for solution in itertools.islice(solver.solve(), 10):
        print(solution)

if __name__ == '__main__':
    solver = ISLaSolver(LANG_GRAMMAR, 
                '''
            forall <rhs> in <assgn>:
                exists <assgn> declaration:
                    (before(declaration, <assgn>) and
                     <rhs>.<var> = declaration.<lhs>.<var>)
            and
            count(start, "<assgn>", "5")
            ''', max_number_smt_instantiations=1, max_number_free_instantiations=1)

if __name__ == '__main__':
    for solution in itertools.islice(solver.solve(), 10):
        print(solution)

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

from .ClassDiagram import display_class_hierarchy
hierarchy = display_class_hierarchy([ISLaSolver],
                       public_methods=[
                            ISLaSolver.__init__,
                            ISLaSolver.solve,
                            ISLaSolver.evaluate,
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



### Exercise 1: String Encodings

if __name__ == '__main__':
    print('\n### Exercise 1: String Encodings')



#### Part 1: Syntax

if __name__ == '__main__':
    print('\n#### Part 1: Syntax')



import string

PASCAL_STRING_GRAMMAR: Grammar = {
    "<start>": ["<string>"],
    "<string>": ["<length><chars>"],
    "<length>": ["<byte>"],
    "<byte>": crange('\x00', '\xff'),
    "<chars>": ["", "<char><chars>"],
    "<char>": list(string.printable),
}

if __name__ == '__main__':
    assert is_valid_grammar(PASCAL_STRING_GRAMMAR)

if __name__ == '__main__':
    fuzzer = GrammarFuzzer(PASCAL_STRING_GRAMMAR)

if __name__ == '__main__':
    for _ in range(10):
        print(repr(fuzzer.fuzz()))

#### Part 2: Semantics

if __name__ == '__main__':
    print('\n#### Part 2: Semantics')



if __name__ == '__main__':
    solver = ISLaSolver(PASCAL_STRING_GRAMMAR, 
                '''
            str.to_code(<string>.<length>.<byte>) =
            str.len(<string>.<chars>)
            ''')

if __name__ == '__main__':
    for solution in itertools.islice(solver.solve(), 10):
        low_byte = solution.filter(lambda n: n.value == "<length>")[0][1]
        chars = solution.filter(lambda n: n.value == "<chars>")[0][1]

        print(f'Solution: "{solution}"', end=' ')
        print(f'(length: {ord(str(low_byte))}, len(chars): {len(str(chars))})')
        print()
