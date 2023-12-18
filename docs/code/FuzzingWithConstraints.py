#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Fuzzing with Constraints" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/FuzzingWithConstraints.html
# Last change: 2023-11-12 13:46:31+01:00
#
# Copyright (c) 2021-2023 CISPA Helmholtz Center for Information Security
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

This chapter introduces the [ISLa](https://rindphi.github.io/isla/) framework, consisting of 
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

With that, invoking `solver.solve()` returns a _solution_ for the constraints.

>>> str(solver.solve())
'(908)828-1795'

`solve()` returns a derivation tree, which typically is converted into a string using `str()` as above. The `print()` function does this implicitly.

Subsequent calls of `solve()` return more solutions:

>>> for _ in range(10):
>>>     print(solver.solve())
(908)434-2906
(908)244-7907
(908)911-7009
(908)757-9655
(908)524-3710
(908)610-9921
(908)381-6159
(908)560-2418
(908)826-1334
(906)339-8184


We see that the solver produces a number of inputs that all satisfy the constraint - the area code is always more than 900.

The `ISLaSolver()` constructor provides several additional parameters to configure the solver, as documented below.
Additional `ISLaSolver` methods allow checking inputs against constraints, and provide additional functionality.
The ISLa functionality is also available on the command line:

>>> !isla --help
usage: isla [-h] [-v]
            {solve,fuzz,check,find,parse,repair,mutate,create,config} ...

The ISLa command line interface.

options:
  -h, --help            show this help message and exit
  -v, --version         Print the ISLa version number

Commands:
  {solve,fuzz,check,find,parse,repair,mutate,create,config}
    solve               create solutions to ISLa constraints or check their
                        unsatisfiability
    fuzz                pass solutions to an ISLa constraint to a test subject
    check               check whether an input satisfies an ISLa constraint
    find                filter files satisfying syntactic & semantic
                        constraints
    parse               parse an input into a derivation tree if it satisfies
                        an ISLa constraint
    repair              try to repair an existing input such that it satisfies
                        an ISLa constraint
    mutate              mutate an input such that the result satisfies an ISLa
                        constraint
    create              create grammar and constraint stubs
    config              dumps the default configuration file



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
    YouTubeVideo("dgaGuwn-1OU")

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

if __name__ == '__main__':
    str(solver.solve())

if __name__ == '__main__':
    for _ in range(10):
        print(solver.solve())

### Excursion: Derivation Trees

if __name__ == '__main__':
    print('\n### Excursion: Derivation Trees')



if __name__ == '__main__':
    solution = solver.solve()
    solution

from .Parser import EarleyParser  # minor dependency
from .GrammarFuzzer import display_tree

if __name__ == '__main__':
    display_tree(solution)

if __name__ == '__main__':
    str(solution)

if __name__ == '__main__':
    print(solution)

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR,
                        'str.to.int(<pagesize>) >= 100000')

if __name__ == '__main__':
    print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                        '''
                    str.to.int(<pagesize>) >= 100 and 
                    str.to.int(<pagesize>) <= 200
                    ''')
    print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                        '''
                    str.to.int(<pagesize>) mod 7 = 0
                    ''')
    print(solver.solve())

from .bookutils import quiz

if __name__ == '__main__':
    quiz("Which of the following constraints expresses "
         "that the page size and the buffer size "
         "have to be equal? Try it out!",
         [
             "`<pagesize> is <bufsize>`",
             "`str.to.int(<pagesize>) = str.to.int(<bufsize>)`",
             "`<pagesize> = <bufsize>`",
             "`atoi(<pagesize>) == atoi(<bufsize>)`",
         ], "[4 ** 0.5, 9 ** 0.5]")

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                        '''
                    <pagesize> = <bufsize>
                    ''')
    print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                        '''
                    str.to.int(<pagesize>) > 1024 and
                    str.to.int(<bufsize>) = str.to.int(<pagesize>) + 1
                    ''')
    print(solver.solve())

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
    print(solver.solve())

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



## ISLa on the Command Line
## ------------------------

if __name__ == '__main__':
    print('\n## ISLa on the Command Line')



if __name__ == '__main__':
    with open('grammar.py', 'w') as f:
        f.write('grammar = ')
        f.write(str(CONFIG_GRAMMAR))

from .bookutils import print_file

if __name__ == '__main__':
    print_file('grammar.py')

if __name__ == '__main__':
    import os
    os.system(f'isla solve grammar.py')

if __name__ == '__main__':
    import os
    os.system(f"isla solve grammar.py --constraint '<pagesize> = <bufsize>'")

if __name__ == '__main__':
    import os
    os.system(f'isla solve grammar.py \\')
    os.system(f"    --constraint '<pagesize> = <bufsize> and str.to.int(<pagesize>) > 10000'")

if __name__ == '__main__':
    import os
    os.system(f'isla --help')

## Accessing Elements
## ------------------

if __name__ == '__main__':
    print('\n## Accessing Elements')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                    '''
                <pagesize>.<int> = <bufsize>.<int>
                ''')
    print(solver.solve())

from .ExpectError import ExpectError

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            <config>..<digit> = "7" and <config>..<leaddigit> = "7"
            ''')
    print(solver.solve())

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
    for i in range(5):
        print(i)
        print(fuzzer.fuzz())

if __name__ == '__main__':
    solver = ISLaSolver(LINES_OF_THREE_AS_OR_BS_GRAMMAR, 
                '''
            <A>.<B>[2] = "b"
            ''')

    for i in range(5):
        print(i)
        print(solver.solve())

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

    for _ in range(10):
        print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            exists <int> in <start>:
                str.to.int(<int>) > 1000
            ''')

    print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            forall <int> in <start>:
                str.to.int(<int>) > 1000
            ''')

    for _ in range(10):
        print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            str.to.int(<int>) > 1000
            ''')

    for _ in range(10):
        print(solver.solve())

## Picking Expansions
## ------------------

if __name__ == '__main__':
    print('\n## Picking Expansions')



if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            forall <int>="<leaddigit><digits>" in <start>:
                (<leaddigit> = "7")
            ''')

if __name__ == '__main__':
    str(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            forall <int> in <start>:
                (str.to.int(<int>) > 100)
            ''')

    str(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            str.to.int(<int>) > 100
            ''')

    str(solver.solve())

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
    for _ in range(10):
        print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            forall <int>="<leaddigit><digits>" in <start>:
                (<leaddigit> = "9")
            ''')
    print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            <int>.<leaddigit> = "9"
            ''')
    print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(CONFIG_GRAMMAR, 
                '''
            <leaddigit> = "9"
            ''')
    print(solver.solve())

## Checking Strings
## ----------------

if __name__ == '__main__':
    print('\n## Checking Strings')



if __name__ == '__main__':
    constraint = '<pagesize> = <bufsize>'
    solver = ISLaSolver(CONFIG_GRAMMAR, constraint)

if __name__ == '__main__':
    solver.check('pagesize=12\nbufsize=34')

if __name__ == '__main__':
    solver.check('pagesize=27\nbufsize=27')

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

    for _ in range(3):
        print(solver.solve())

### Excursion: Solver Configuration Parameters

if __name__ == '__main__':
    print('\n### Excursion: Solver Configuration Parameters')



if __name__ == '__main__':
    solver = ISLaSolver(XML_GRAMMAR, 
                '''
            <xml-tree>.<open-tag>.<id> = <xml-tree>.<close-tag>.<id>
            ''', max_number_smt_instantiations=10)

    for _ in range(3):
        print(solver.solve())

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

    for _ in range(3):
        print(solver.solve())

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
            ''',
                max_number_smt_instantiations=1,
                max_number_free_instantiations=1)

if __name__ == '__main__':
    for _ in range(10):
        print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(LANG_GRAMMAR, 
                '''
            forall <rhs> in <assgn>:
                exists <assgn> declaration:
                    (before(declaration, <assgn>) and
                     <rhs>.<var> = declaration.<lhs>.<var>)
            ''',
                max_number_free_instantiations=1,
                max_number_smt_instantiations=1)

if __name__ == '__main__':
    for _ in range(10):
        print(solver.solve())

if __name__ == '__main__':
    solver = ISLaSolver(LANG_GRAMMAR, 
                '''
            forall <rhs> in <assgn>:
                exists <assgn> declaration:
                    (before(declaration, <assgn>) and
                     <rhs>.<var> = declaration.<lhs>.<var>)
            and
            count(start, "<assgn>", "5")
            ''', 
                max_number_smt_instantiations=1,
                max_number_free_instantiations=1)

if __name__ == '__main__':
    for _ in range(10):
        print(solver.solve())

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
    str(solver.solve())

if __name__ == '__main__':
    for _ in range(10):
        print(solver.solve())

from .ClassDiagram import display_class_hierarchy

if __name__ == '__main__':
    display_class_hierarchy([ISLaSolver],
                             public_methods=[
                                ISLaSolver.__init__,
                                ISLaSolver.solve,
                                ISLaSolver.check,
                                ISLaSolver.parse,
                            ])

if __name__ == '__main__':
    import os
    os.system(f'isla --help')

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
    for _ in range(10):
        # Get the solution
        solution = solver.solve()
        print(f'Solution: {repr(str(solution))}', end=' ')

        # Print statistics
        low_byte = solution.filter(lambda n: n.value == "<length>")[0][1]
        chars = solution.filter(lambda n: n.value == "<chars>")[0][1]
        print(f'(<length> = {ord(str(low_byte))}, len(<chars>) = {len(str(chars))})')
        print()

import os

with ExpectError(FileNotFoundError, mute=True):
    os.remove('grammar.py')
