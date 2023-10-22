#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Testing Compilers" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/PythonFuzzer.html
# Last change: 2023-10-22 17:29:45+02:00
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
The Fuzzing Book - Testing Compilers

This file can be _executed_ as a script, running all experiments:

    $ python PythonFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.PythonFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/PythonFuzzer.html

This chapter provides a `PythonFuzzer` class that allows producing arbitrary Python code elements:

>>> fuzzer = PythonFuzzer()
>>> print(fuzzer.fuzz())
def Hw(): # type: 
    pass


By default, `PythonFuzzer` produces a _function definition_ – that is, a list of statements as above.
You can pass a `start_symbol` argument to state which Python element you'd like to have:

>>> fuzzer = PythonFuzzer('')
>>> print(fuzzer.fuzz())
while 
'' or {Z: *(set() ^ set())}:
    del 


Here is a list of all possible start symbols. Their names reflect the nonterminals from the [Python `ast` module documentation](https://docs.python.org/3/library/ast.html).

>>> sorted(list(PYTHON_AST_GRAMMAR.keys()))
['',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '',
 '']

If you'd like more control over Python code generation, here is what is happening behind the scenes.
The EBNF grammar `PYTHON_AST_GRAMMAR` can parse and produce _abstract syntax trees_ for Python.
To produce a Python module without `PythonFuzzer`, you would take these steps:

**Step 1:** Create a non-EBNF grammar suitable for `ISLaSolver` (or any other grammar fuzzer):

>>> python_ast_grammar = convert_ebnf_grammar(PYTHON_AST_GRAMMAR)

**Step 2:**  Feed the resulting grammar into a grammar fuzzer such as ISLa:

>>> solver = ISLaSolver(python_ast_grammar, start_symbol='')

**Step 3:**  Have the grammar fuzzer produce a string. This string represents an AST.

>>> ast_string = str(solver.solve())
>>> ast_string
'FunctionDef(name=\'t\', args=arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Break()], decorator_list=[], returns=Call(func=Name(id="set", ctx=Load()), args=[], keywords=[]), type_comment=\'\')'

**Step 4:**  Convert the AST into an actual Python AST data structure.

>>> from ast import *
>>> abstract_syntax_tree = eval(ast_string)

**Step 5:** Finally, convert the AST structure back into readable Python code:

>>> ast.fix_missing_locations(abstract_syntax_tree)
>>> print(ast.unparse(abstract_syntax_tree))
def t() -> set(): # type: 
    break


The chapter has many more applications, including parsing and mutating Python code, evolutionary fuzzing, and more.

Here are the details on the `PythonFuzzer` constructor:

PythonFuzzer(self, start_symbol: Optional[str] = None, *, grammar: Optional[Dict[str, List[Union[str, Tuple[str, Dict[str, Any]]]]]] = None, constraint: Optional[str] = None, **kw_params) -> None
Produce Python code. Parameters are:

start_symbol: The grammatical entity to be generated (default: <FunctionDef>)
grammar: The EBNF grammar to be used (default: PYTHON__AST_GRAMMAR); and
constraint an ISLa constraint (if any).

Additional keyword parameters are passed to the ISLaSolver superclass.

For more details, source, and documentation, see
"The Fuzzing Book - Testing Compilers"
at https://www.fuzzingbook.org/html/PythonFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Testing Compilers
# =================

if __name__ == '__main__':
    print('# Testing Compilers')



import sys

if __name__ == '__main__':
    if sys.version_info < (3, 10):
        print("This code requires Python 3.10 or later")
        sys.exit(0)

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## A Grammar for Concrete Code
## ---------------------------

if __name__ == '__main__':
    print('\n## A Grammar for Concrete Code')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .Grammars import Grammar
from .Grammars import is_valid_grammar, convert_ebnf_grammar, extend_grammar, trim_grammar

from typing import Optional

EXPR_GRAMMAR: Grammar = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<term> + <expr>", "<term> - <expr>", "<term>"],

    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>"],

    "<factor>":
        ["+<factor>",
         "-<factor>",
         "(<expr>)",
         "<integer>.<integer>",
         "<integer>"],

    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

if __name__ == '__main__':
    assert is_valid_grammar(EXPR_GRAMMAR)

from isla.solver import ISLaSolver  # type: ignore

if __name__ == '__main__':
    expr_solver = ISLaSolver(EXPR_GRAMMAR)
    for _ in range(10):
        print(expr_solver.solve())

if __name__ == '__main__':
    expr_solver.check('2 + 2')

if __name__ == '__main__':
    expr_solver.check('2 +  2')

if __name__ == '__main__':
    expr_solver.check('2+2')

if __name__ == '__main__':
    expr_solver.check('2 + 2    # should be 4')

if __name__ == '__main__':
    expr_solver.check('2 + \\\n2')  # An expression split over two lines

## Abstract Syntax Trees
## ---------------------

if __name__ == '__main__':
    print('\n## Abstract Syntax Trees')



def main():
    print("Hello, world!")  # A simple example

if __name__ == '__main__':
    main()

import inspect

if __name__ == '__main__':
    main_source = inspect.getsource(main)
    print(main_source)

import ast

if __name__ == '__main__':
    main_tree = ast.parse(main_source)

from .bookutils import show_ast

if __name__ == '__main__':
    show_ast(main_tree)

if __name__ == '__main__':
    print(ast.dump(main_tree, indent=4))

from ast import *

if __name__ == '__main__':
    my_main_tree = Module(
        body=[
            FunctionDef(
                name='main',
                args=arguments(
                    posonlyargs=[],
                    args=[],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]),
                body=[
                    Expr(
                        value=Call(
                            func=Name(id='print', ctx=Load()),
                            args=[
                                Constant(value='Hello, world!')],
                            keywords=[]))],
                decorator_list=[])],
        type_ignores=[])

if __name__ == '__main__':
    my_main_tree = fix_missing_locations(my_main_tree)  # required for trees built from constructors
    my_main_code = compile(my_main_tree, filename='<unknown>', mode='exec')

if __name__ == '__main__':
    del main  # This deletes the definition of main()

if __name__ == '__main__':
    exec(my_main_code)  # This defines main() again from `code`

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    print(ast.unparse(my_main_tree))

## A Grammar for ASTs
## ------------------

if __name__ == '__main__':
    print('\n## A Grammar for ASTs')



### Constants

if __name__ == '__main__':
    print('\n### Constants')



import string

ANYTHING_BUT_DOUBLE_QUOTES_AND_BACKSLASH = (string.digits + string.ascii_letters + string.punctuation + ' ').replace('"', '').replace('\\', '')
ANYTHING_BUT_SINGLE_QUOTES_AND_BACKSLASH = (string.digits + string.ascii_letters + string.punctuation + ' ').replace("'", '').replace('\\', '')

if __name__ == '__main__':
    ANYTHING_BUT_DOUBLE_QUOTES_AND_BACKSLASH

if __name__ == '__main__':
    ANYTHING_BUT_SINGLE_QUOTES_AND_BACKSLASH

PYTHON_AST_CONSTANTS_GRAMMAR: Grammar = {
    '<start>': [ '<expr>' ],

    # Expressions
    '<expr>': [ '<Constant>', '<Expr>' ],
    '<Expr>': [ 'Expr(value=<expr>)' ],

    # Constants
    '<Constant>': [ 'Constant(value=<literal>)' ],
    '<literal>': [ '<string>', '<integer>', '<float>', '<bool>', '<none>' ],

    # Strings
    '<string>': [ '"<not_double_quotes>*"', "'<not_single_quotes>*'" ],
    '<not_double_quotes>': list(ANYTHING_BUT_DOUBLE_QUOTES_AND_BACKSLASH),
    '<not_single_quotes>': list(ANYTHING_BUT_SINGLE_QUOTES_AND_BACKSLASH),
    # FIXME: The actual rules for Python strings are also more complex:
    # https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals

    # Numbers
    '<integer>': [ '<digit>', '<nonzerodigit><digits>' ],
    '<float>': [ '<integer>.<integer>' ],
    '<nonzerodigit>': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
    '<digits>': [ '<digit><digits>', '<digit>' ],
    '<digit>': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    # FIXME: There are _many_ more ways to express numbers in Python; see
    # https://docs.python.org/3/reference/lexical_analysis.html#numeric-literals

    # More
    '<bool>': [ 'True', 'False' ],
    '<none>': [ 'None' ],

    # FIXME: Not supported: bytes, format strings, regex strings...
}

if __name__ == '__main__':
    assert is_valid_grammar(PYTHON_AST_CONSTANTS_GRAMMAR)

if __name__ == '__main__':
    constants_grammar = convert_ebnf_grammar(PYTHON_AST_CONSTANTS_GRAMMAR)
    constants_solver = ISLaSolver(constants_grammar)
    constants_tree_str = str(constants_solver.solve())
    print(constants_tree_str)

if __name__ == '__main__':
    constants_tree = eval(constants_tree_str)
    ast.unparse(constants_tree)

def test_samples(grammar: Grammar, iterations: int = 10, start_symbol = None, log: bool = True):
    g = convert_ebnf_grammar(grammar)
    solver = ISLaSolver(g, start_symbol=start_symbol, max_number_free_instantiations=iterations)
    for i in range(iterations):
        tree_str = str(solver.solve())
        tree = eval(tree_str)
        ast.fix_missing_locations(tree)
        if log:
            code = ast.unparse(tree)
            print(f'{code:40} # {tree_str}')

if __name__ == '__main__':
    test_samples(PYTHON_AST_CONSTANTS_GRAMMAR)

if __name__ == '__main__':
    sample_constant_code = "4711"
    sample_constant_ast = ast.parse(sample_constant_code).body[0]  # get the `Expr` node
    sample_constant_ast_str = ast.dump(sample_constant_ast)
    print(sample_constant_ast_str)

if __name__ == '__main__':
    constant_solver = ISLaSolver(constants_grammar)
    constant_solver.check(sample_constant_ast_str)

if __name__ == '__main__':
    ast.unparse(Constant(value=-1))

from .bookutils import quiz

if __name__ == '__main__':
    quiz("If we parse a negative number, do we obtain ",
        [
            "a `Constant()` with a negative value, or",
            "a unary `-` operator applied to a positive value?"
        ], 1 ** 0 + 1 ** 1)

if __name__ == '__main__':
    print(ast.dump(ast.parse('-1')))

if __name__ == '__main__':
    sample_constant_code = "-1"
    sample_constant_ast = ast.parse(sample_constant_code).body[0]  # get the `Expr` node
    sample_constant_ast_str = ast.dump(sample_constant_ast)
    constant_solver = ISLaSolver(constants_grammar)
    constant_solver.check(sample_constant_ast_str)

### Excursion: Composites

if __name__ == '__main__':
    print('\n### Excursion: Composites')



if __name__ == '__main__':
    print(ast.dump(ast.parse("{ 'a': set() }"), indent=4))

PYTHON_AST_COMPOSITES_GRAMMAR: Grammar = extend_grammar(
    PYTHON_AST_CONSTANTS_GRAMMAR, {
    '<expr>': PYTHON_AST_CONSTANTS_GRAMMAR['<expr>'] + [
        '<Dict>', '<Set>', '<List>', '<Tuple>'
    ],

    '<Dict>': [ 'Dict(keys=<expr_list>, values=<expr_list>)' ],
    '<Set>': [ 'Set(elts=<nonempty_expr_list>)', '<EmptySet>' ],
    '<EmptySet>': [ 'Call(func=Name(id="set", ctx=Load()), args=[], keywords=[])' ],
    '<List>': [
        'List(elts=<expr_list>, ctx=Load())',
        'List(elts=<expr_list>, ctx=Del())',
    ],
    '<Tuple>': [
        'Tuple(elts=<expr_list>, ctx=Load())',
        'Tuple(elts=<expr_list>, ctx=Del())',
    ],

    # Lists of expressions
    '<expr_list>': [ '[<exprs>?]' ],
    '<nonempty_expr_list>': [ '[<exprs>]' ],
    '<exprs>': [ '<expr>', '<exprs>, <expr>' ],
})

if __name__ == '__main__':
    assert is_valid_grammar(PYTHON_AST_COMPOSITES_GRAMMAR)

if __name__ == '__main__':
    for elt in [ '<Constant>', '<Dict>', '<Set>', '<List>', '<Tuple>' ]:
        print(elt)
        test_samples(PYTHON_AST_COMPOSITES_GRAMMAR, start_symbol=elt)
        print()

if __name__ == '__main__':
    print(ast.unparse(Set(elts=[])))

if __name__ == '__main__':
    {*()}

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



### Excursion: Expressions

if __name__ == '__main__':
    print('\n### Excursion: Expressions')



if __name__ == '__main__':
    print(ast.dump(ast.parse("2 + 2 is not False"), indent=4))

PYTHON_AST_EXPRS_GRAMMAR: Grammar = extend_grammar(PYTHON_AST_COMPOSITES_GRAMMAR, {
    '<expr>': PYTHON_AST_COMPOSITES_GRAMMAR['<expr>'] + [
        '<BoolOp>', '<BinOp>', '<UnaryOp>', '<Compare>',
    ],

    # Booleans: and or
    '<BoolOp>': [ 'BoolOp(op=<boolop>, values=<expr_list>)' ],
    '<boolop>': [ 'And()', 'Or()' ],

    # Binary operators: + - * ...
    '<BinOp>': [ 'BinOp(left=<expr>, op=<operator>, right=<expr>)' ],
    '<operator>': [ 'Add()', 'Sub()', 'Mult()', 'MatMult()',
                   'Div()', 'Mod()', 'Pow()',
                   'LShift()', 'RShift()', 'BitOr()', 'BitXor()', 'BitAnd()',
                   'FloorDiv()' ],

    # Unary operators: not + - ...
    '<UnaryOp>': [ 'UnaryOp(op=<unaryop>, operand=<expr>)'],
    '<unaryop>': [ 'Invert()', 'Not()', 'UAdd()', 'USub()' ],

    # Comparisons: == != < <= > >= is in ...
    '<Compare>': [ 'Compare(left=<expr>, ops=<cmpop_list>, comparators=<expr_list>)'],
    '<cmpop_list>': [ '[<cmpops>?]' ],
    '<cmpops>': [ '<cmpop>', '<cmpop>, <cmpops>' ],
    '<cmpop>': [ 'Eq()', 'NotEq()', 'Lt()', 'LtE()', 'Gt()', 'GtE()',
                 'Is()', 'IsNot()', 'In()', 'NotIn()' ],

    # FIXME: There's a few more expressions: GeneratorExp, Await, YieldFrom, ...
})

if __name__ == '__main__':
    assert is_valid_grammar(PYTHON_AST_EXPRS_GRAMMAR)

if __name__ == '__main__':
    for elt in [ '<BoolOp>', '<BinOp>', '<UnaryOp>', '<Compare>' ]:
        print(elt)
        test_samples(PYTHON_AST_EXPRS_GRAMMAR, start_symbol=elt)
        print()

if __name__ == '__main__':
    expr_iterations = 20
    bad_syntax = 0
    bad_type = 0
    ast_exprs_grammar = convert_ebnf_grammar(PYTHON_AST_EXPRS_GRAMMAR)
    expr_solver = ISLaSolver(ast_exprs_grammar, max_number_free_instantiations=expr_iterations)
    for i in range(expr_iterations):
        expr_tree = eval(str(expr_solver.solve()))
        expr_tree = fix_missing_locations(expr_tree)
        expr_str = ast.unparse(expr_tree)
        print(i, expr_str)
        try:
            ...  # insert parsing code here
        except SyntaxError:
            bad_syntax += 1
        except TypeError:
            bad_type += 1

        try:
            ...  # <-- insert evaluation code here
        except TypeError:
            bad_type += 1
        except SyntaxError:
            bad_syntax += 1

    print(f"Bad syntax: {bad_syntax}/{expr_iterations}")
    print(f"Bad type: {bad_type}/{expr_iterations}")

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



### Excursion: Names and Function Calls

if __name__ == '__main__':
    print('\n### Excursion: Names and Function Calls')



ID_START = string.ascii_letters + '_'
ID_CONTINUE = ID_START + string.digits

if __name__ == '__main__':
    ID_CONTINUE

if __name__ == '__main__':
    print(ast.dump(ast.parse("xyzzy(a, b=c)"), indent=4))

PYTHON_AST_IDS_GRAMMAR: Grammar = extend_grammar(PYTHON_AST_EXPRS_GRAMMAR, {
    '<expr>': PYTHON_AST_EXPRS_GRAMMAR['<expr>'] + [
        '<Name>', '<Call>'
    ],

    # Identifiers
    '<Name>': [
        'Name(id=<identifier>, ctx=Load())',
        'Name(id=<identifier>, ctx=Del())'
    ],
    '<identifier>': [ "'<id>'" ],
    '<id>': [ '<id_start><id_continue>*' ],
    '<id_start>': list(ID_START),
    '<id_continue>': list(ID_CONTINUE),
    # FIXME: Actual rules are a bit more complex; see
    # https://docs.python.org/3/reference/lexical_analysis.html#identifiers

    # Function Calls
   '<Call>': [ 'Call(func=<func>, args=<expr_list>, keywords=<keyword_list>)' ],
   '<func>': [ '<expr>' ],  # Actually <Expr>, but this is more readable and parses 90%
    '<keyword_list>': [ '[<keywords>?]' ],
    '<keywords>': [ '<keyword>', '<keyword>, <keywords>' ],
    '<keyword>': [ 'keyword(arg=<identifier>, value=<expr>)' ]
})

if __name__ == '__main__':
    assert is_valid_grammar(PYTHON_AST_IDS_GRAMMAR)

if __name__ == '__main__':
    for elt in [ '<Name>', '<Call>' ]:
        print(elt)
        test_samples(PYTHON_AST_IDS_GRAMMAR, start_symbol=elt)
        print()

if __name__ == '__main__':
    ast_ids_grammar = convert_ebnf_grammar(PYTHON_AST_IDS_GRAMMAR)

if __name__ == '__main__':
    id_solver = ISLaSolver(ast_ids_grammar, start_symbol='<id>')
    assert id_solver.check('open')

if __name__ == '__main__':
    name_solver = ISLaSolver(ast_ids_grammar)
    assert name_solver.check("Name(id='open', ctx=Load())")

if __name__ == '__main__':
    call_solver = ISLaSolver(ast_ids_grammar, start_symbol='<keyword_list>')
    assert call_solver.check('[]')

if __name__ == '__main__':
    call_str = ast.dump(ast.parse('open()').body[0].value)  # type: ignore
    call_solver = ISLaSolver(ast_ids_grammar)
    assert call_solver.check(call_str)

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



### Excursion: Attributes and Subscripts

if __name__ == '__main__':
    print('\n### Excursion: Attributes and Subscripts')



if __name__ == '__main__':
    print(ast.dump(ast.parse("a[b].c"), indent=4))

PYTHON_AST_ATTRS_GRAMMAR: Grammar = extend_grammar(PYTHON_AST_IDS_GRAMMAR, {
    '<expr>': PYTHON_AST_IDS_GRAMMAR['<expr>'] + [
        '<Attribute>', '<Subscript>', '<Starred>',
    ],

    # Attributes
    '<Attribute>': [
        'Attribute(value=<expr>, attr=<identifier>, ctx=Load())',
        'Attribute(value=<expr>, attr=<identifier>, ctx=Del())',
    ],

    # Subscripts
    '<Subscript>': [
        'Subscript(value=<expr>, slice=<Slice>, ctx=Load())',
        'Subscript(value=<expr>, slice=<Slice>, ctx=Del())',
    ],
    '<Slice>': [
        'Slice()',
        'Slice(<expr>)',
        'Slice(<expr>, <expr>)',
        'Slice(<expr>, <expr>, <expr>)',
    ],

    # Starred
    '<Starred>': [
        'Starred(value=<expr>, ctx=Load())',
        'Starred(value=<expr>, ctx=Del())',
    ],

    # We're extending the set of callers a bit
    '<func>': [ '<Name>', '<Attribute>', '<Subscript>' ],
})

if __name__ == '__main__':
    assert is_valid_grammar(PYTHON_AST_ATTRS_GRAMMAR)

if __name__ == '__main__':
    for elt in [ '<Attribute>', '<Subscript>', '<Starred>' ]:
        print(elt)
        test_samples(PYTHON_AST_ATTRS_GRAMMAR, start_symbol=elt)
        print()

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



### Excursion: Variable Assignments

if __name__ == '__main__':
    print('\n### Excursion: Variable Assignments')



PYTHON_AST_ASSIGNMENTS_GRAMMAR: Grammar = extend_grammar(PYTHON_AST_ATTRS_GRAMMAR, {
    '<start>': [ '<stmt>' ],

    '<stmt>': [
        '<Assign>', '<AugAssign>',
        '<Expr>'
    ],

    # Assignments
    '<Assign>': [
        'Assign(targets=<nonempty_lhs_expr_list>, value=<expr><type_comment>?)',
    ],
    '<type_comment>': [ ', type_comment=<string>' ],
    '<AugAssign>': [
        'AugAssign(target=<lhs_expr>, op=<operator>, value=<expr>)',
    ],

    # Lists of left-hand side expressions
    # '<lhs_expr_list>': [ '[<lhs_exprs>?]' ],
    '<nonempty_lhs_expr_list>': [ '[<lhs_exprs>]' ],
    '<lhs_exprs>': [ '<lhs_expr>', '<lhs_exprs>, <lhs_expr>' ],

    # On the left-hand side of assignments, we allow a number of structures
    '<lhs_expr>': [
        '<lhs_Name>',  # Most common
        '<lhs_List>', '<lhs_Tuple>',
        '<lhs_Attribute>',
        '<lhs_Subscript>',
        '<lhs_Starred>',
    ],

    '<lhs_Name>': [ 'Name(id=<identifier>, ctx=Store())', ],

    '<lhs_List>': [
        'List(elts=<nonempty_lhs_expr_list>, ctx=Store())',
    ],
    '<lhs_Tuple>': [
        'Tuple(elts=<nonempty_lhs_expr_list>, ctx=Store())',
    ],
    '<lhs_Attribute>': [
        'Attribute(value=<lhs_expr>, attr=<identifier>, ctx=Store())',
    ],
    '<lhs_Subscript>': [
        'Subscript(value=<lhs_expr>, slice=<Slice>, ctx=Store())',
    ],
    '<lhs_Starred>': [
        'Starred(value=<lhs_expr>, ctx=Store())',
    ],
})

if __name__ == '__main__':
    assert is_valid_grammar(PYTHON_AST_ASSIGNMENTS_GRAMMAR)

if __name__ == '__main__':
    for elt in ['<Assign>', '<AugAssign>']:
        print(elt)
        test_samples(PYTHON_AST_ASSIGNMENTS_GRAMMAR, start_symbol=elt)
        print()

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



### Excursion: Statements

if __name__ == '__main__':
    print('\n### Excursion: Statements')



PYTHON_AST_STMTS_GRAMMAR: Grammar = extend_grammar(PYTHON_AST_ASSIGNMENTS_GRAMMAR, {
    '<start>': [ '<stmt>' ],

    '<stmt>': PYTHON_AST_ASSIGNMENTS_GRAMMAR['<stmt>'] + [
        '<For>', '<While>', '<If>',
        '<Return>', '<Delete>', '<Assert>',
        '<Pass>', '<Break>', '<Continue>',
        '<With>'
    ],

    # Control structures
    '<For>': [
        'For(target=<lhs_expr>, iter=<expr>, body=<nonempty_stmt_list>, orelse=<stmt_list><type_comment>)'
    ],
    '<stmt_list>': [ '[<stmts>?]' ],
    '<nonempty_stmt_list>': [ '[<stmts>]' ],
    '<stmts>': [ '<stmt>', '<stmt>, <stmts>' ],

    '<While>': [
        'While(test=<expr>, body=<nonempty_stmt_list>, orelse=<stmt_list>)'
    ],

    '<If>': [
        'If(test=<expr>, body=<nonempty_stmt_list>, orelse=<stmt_list>)'
    ],

    '<With>': [
        'With(items=<withitem_list>, body=<nonempty_stmt_list><type_comment>?)'
    ],
    '<withitem_list>': [ '[<withitems>?]' ],
    '<withitems>': [ '<withitem>', '<withitems>, <withitem>' ],
    '<withitem>': [
        'withitem(context_expr=<expr>)',
        'withitem(context_expr=<expr>, optional_vars=<lhs_expr>)',
    ],

    # Other statements
    '<Return>': [
        'Return()',
        'Return(value=<expr>)'
    ],
    '<Delete>': [
        'Delete(targets=<expr_list>)'
    ],
    '<Assert>': [
        'Assert(test=<expr>)',
        'Assert(test=<expr>, msg=<expr>)'
    ],
    '<Pass>': [ 'Pass()'],
    '<Break>': [ 'Break()' ],
    '<Continue>': [ 'Continue()']

    # FIXME: A few more: AsyncFor, AsyncWith, Match, Try, TryStar, With
    # Import, ImportFrom, Global, Nonlocal...
})

if __name__ == '__main__':
    assert is_valid_grammar(PYTHON_AST_STMTS_GRAMMAR)

if __name__ == '__main__':
    for elt in PYTHON_AST_STMTS_GRAMMAR['<stmt>']:
        print(elt)
        test_samples(PYTHON_AST_STMTS_GRAMMAR, start_symbol=elt)
        print()

if __name__ == '__main__':
    with_tree = ast.parse("""
with open('foo.txt') as myfile:
    content = myfile.readlines()
    if content is not None:
        print(content)
""")

if __name__ == '__main__':
    python_ast_stmts_grammar = convert_ebnf_grammar(PYTHON_AST_STMTS_GRAMMAR)
    with_tree_str = ast.dump(with_tree.body[0])  # get the `With(...)` subtree
    with_solver = ISLaSolver(python_ast_stmts_grammar)
    assert with_solver.check(with_tree_str)

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



### Excursion: Function Definitions

if __name__ == '__main__':
    print('\n### Excursion: Function Definitions')



if __name__ == '__main__':
    print(ast.dump(ast.parse("""
def f(a, b=1):
    pass
"""
    ), indent=4))

PYTHON_AST_DEFS_GRAMMAR: Grammar = extend_grammar(PYTHON_AST_STMTS_GRAMMAR, {
    '<stmt>': PYTHON_AST_STMTS_GRAMMAR['<stmt>'] + [ '<FunctionDef>' ],

    '<FunctionDef>': [
        'FunctionDef(name=<identifier>, args=<arguments>, body=<nonempty_stmt_list>, decorator_list=<expr_list><returns>?<type_comment>?)'
    ],
    '<arguments>': [
        'arguments(posonlyargs=<arg_list>, args=<arg_list><vararg>?, kwonlyargs=<arg_list>, kw_defaults=<expr_list><kwarg>?, defaults=<expr_list>)'
    ],

    '<arg_list>': [ '[<args>?]' ],
    '<args>': [ '<arg>', '<arg>, <arg>' ],
    '<arg>': [ 'arg(arg=<identifier>)' ],

    '<vararg>': [ ', vararg=<arg>' ],
    '<kwarg>': [ ', kwarg=<arg>' ],
    '<returns>': [ ', returns=<expr>' ],

    # FIXME: Not handled: AsyncFunctionDef, ClassDef
})

import sys

if sys.version_info >= (3, 12):
    PYTHON_AST_DEFS_GRAMMAR: Grammar = extend_grammar(PYTHON_AST_DEFS_GRAMMAR, {
    '<FunctionDef>': [
        'FunctionDef(name=<identifier>, args=<arguments>, body=<nonempty_stmt_list>, decorator_list=<expr_list><returns>?<type_comment>?<type_params>?)'
    ],
    '<type_params>': [
        ', type_params=<type_param_list>',
    ],
    '<type_param_list>': [ '[<type_param>?]' ],
    '<type_param>': [ '<TypeVar>', '<ParamSpec>', '<TypeVarTuple>' ],
    '<TypeVar>': [
        'TypeVar(name=<identifier>(, bound=<expr>)?)'
    ],
    '<ParamSpec>': [
        'ParamSpec(name=<identifier>)'
    ],
    '<TypeVarTuple>': [
        'TypeVarTuple(name=<identifier>)'
    ]
    })

if __name__ == '__main__':
    assert is_valid_grammar(PYTHON_AST_DEFS_GRAMMAR)

if __name__ == '__main__':
    for elt in [ '<arguments>', '<FunctionDef>' ]:
        print(elt)
        test_samples(PYTHON_AST_DEFS_GRAMMAR, start_symbol=elt)
        print()

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



### Excursion: Modules

if __name__ == '__main__':
    print('\n### Excursion: Modules')



PYTHON_AST_MODULE_GRAMMAR: Grammar = extend_grammar(PYTHON_AST_DEFS_GRAMMAR, {
    '<start>': [ '<mod>' ],
    '<mod>': [ '<Module>' ],
    '<Module>': [ 'Module(body=<nonempty_stmt_list>, type_ignores=<type_ignore_list>)'],

    '<type_ignore_list>': [ '[<type_ignores>?]' ],
    '<type_ignores>': [ '<type_ignore>', '<type_ignore>, <type_ignore>' ],
    '<type_ignore>': [ 'TypeIgnore(lineno=<integer>, tag=<string>)' ],
})

if __name__ == '__main__':
    assert is_valid_grammar(PYTHON_AST_MODULE_GRAMMAR)

if __name__ == '__main__':
    for elt in [ '<Module>' ]:
        print(elt)
        test_samples(PYTHON_AST_MODULE_GRAMMAR, start_symbol=elt)
        print()

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



PYTHON_AST_GRAMMAR = PYTHON_AST_MODULE_GRAMMAR
python_ast_grammar = convert_ebnf_grammar(PYTHON_AST_GRAMMAR)

if __name__ == '__main__':
    for elt in [ '<FunctionDef>' ]:
        print(elt)
        test_samples(PYTHON_AST_GRAMMAR, start_symbol=elt)
        print()

## A Class for Fuzzing Python
## --------------------------

if __name__ == '__main__':
    print('\n## A Class for Fuzzing Python')



class PythonFuzzer(ISLaSolver):
    """Produce Python code."""

    def __init__(self,
                 start_symbol: Optional[str] = None, *,
                 grammar: Optional[Grammar] = None,
                 constraint: Optional[str] =None,
                 **kw_params) -> None:
        """Produce Python code. Parameters are:

        * `start_symbol`: The grammatical entity to be generated (default: `<FunctionDef>`)
        * `grammar`: The EBNF grammar to be used (default: `PYTHON__AST_GRAMMAR`); and
        * `constraint` an ISLa constraint (if any).

        Additional keyword parameters are passed to the `ISLaSolver` superclass.
        """
        if start_symbol is None:
            start_symbol = '<FunctionDef>'
        if grammar is None:
            grammar = PYTHON_AST_GRAMMAR
        assert start_symbol in grammar

        g = convert_ebnf_grammar(grammar)
        if constraint is None:
            super().__init__(g, start_symbol=start_symbol, **kw_params)
        else:
            super().__init__(g, constraint, start_symbol=start_symbol, **kw_params)

    def fuzz(self) -> str:
        """Produce a Python code string."""
        abstract_syntax_tree = eval(str(self.solve()))
        ast.fix_missing_locations(abstract_syntax_tree)
        return ast.unparse(abstract_syntax_tree)

if __name__ == '__main__':
    fuzzer = PythonFuzzer()
    print(fuzzer.fuzz())

if __name__ == '__main__':
    fuzzer = PythonFuzzer('<While>')
    print(fuzzer.fuzz())

if __name__ == '__main__':
    sorted(list(PYTHON_AST_GRAMMAR.keys()))

## Customizing the Python Fuzzer
## -----------------------------

if __name__ == '__main__':
    print('\n## Customizing the Python Fuzzer')



### Adjusting the Grammar

if __name__ == '__main__':
    print('\n### Adjusting the Grammar')



if __name__ == '__main__':
    PYTHON_AST_GRAMMAR['<FunctionDef>']

if __name__ == '__main__':
    python_ast_grammar_without_decorators: Grammar = extend_grammar(PYTHON_AST_GRAMMAR,
    {
        '<FunctionDef>' :
            ['FunctionDef(name=<identifier>, args=<arguments>, body=<nonempty_stmt_list>, decorator_list=[])']
    })

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        assert is_valid_grammar(python_ast_grammar_without_decorators)

if __name__ == '__main__':
    python_ast_grammar_without_decorators = trim_grammar(python_ast_grammar_without_decorators)

if __name__ == '__main__':
    assert is_valid_grammar(python_ast_grammar_without_decorators)

if __name__ == '__main__':
    fuzzer = PythonFuzzer(grammar=python_ast_grammar_without_decorators)
    print(fuzzer.fuzz())

### Using Constraints for Customizing

if __name__ == '__main__':
    print('\n### Using Constraints for Customizing')



if __name__ == '__main__':
    fuzzer = PythonFuzzer(constraint='str.len(<id>) = 10')
    print(fuzzer.fuzz())

if __name__ == '__main__':
    fuzzer = PythonFuzzer(constraint='<FunctionDef>.<identifier> = "\'my_favorite_function\'"')
    print(fuzzer.fuzz())

if __name__ == '__main__':
    fuzzer = PythonFuzzer(constraint=
    """
    exists <integer> x:
        (inside(x, <nonempty_stmt_list>) and str.to.int(x) > 1000)
""")
    print(fuzzer.fuzz())

if __name__ == '__main__':
    fuzzer = PythonFuzzer(constraint="""
    forall <FunctionDef> def: count(def, "<stmt>", "3")
""")
    print(fuzzer.fuzz())

if __name__ == '__main__':
    fuzzer = PythonFuzzer(constraint='<FunctionDef>..<expr_list> = "[]"')
    print(fuzzer.fuzz())

## Mutating Code
## -------------

if __name__ == '__main__':
    print('\n## Mutating Code')



### Parsing Inputs

if __name__ == '__main__':
    print('\n### Parsing Inputs')



def sum(a, b):    # A simple example
    the_sum = a + b
    return the_sum

if __name__ == '__main__':
    sum_source = inspect.getsource(sum)
    sum_tree = ast.parse(sum_source)
    print(ast.unparse(sum_tree))

if __name__ == '__main__':
    sum_str = ast.dump(sum_tree)
    sum_str

if __name__ == '__main__':
    solver = ISLaSolver(python_ast_grammar)
    solver.check(sum_str)

if __name__ == '__main__':
    sum_tree = solver.parse(sum_str)

if __name__ == '__main__':
    len(repr(sum_tree))

if __name__ == '__main__':
    repr(sum_tree)[:200]

from .GrammarFuzzer import display_tree

if __name__ == '__main__':
    display_tree(sum_tree)

if __name__ == '__main__':
    python_ast_grammar['<start>']

if __name__ == '__main__':
    python_ast_grammar['<mod>']

if __name__ == '__main__':
    python_ast_grammar['<Module>']

if __name__ == '__main__':
    str(sum_tree)

if __name__ == '__main__':
    sum_ast = ast.fix_missing_locations(eval(str(sum_tree)))
    print(ast.unparse(sum_ast))

### Mutating Inputs

if __name__ == '__main__':
    print('\n### Mutating Inputs')



if __name__ == '__main__':
    sum_mutated_tree = solver.mutate(sum_str, min_mutations=1, max_mutations=1)

if __name__ == '__main__':
    sum_mutated_ast = ast.fix_missing_locations(eval(str(sum_mutated_tree)))
    print(ast.unparse(sum_mutated_ast))

if __name__ == '__main__':
    sum_mutated_tree = solver.mutate(sum_str, min_mutations=10, max_mutations=20)

if __name__ == '__main__':
    sum_mutated_ast = ast.fix_missing_locations(eval(str(sum_mutated_tree)))
    print(ast.unparse(sum_mutated_ast))

### How Effective is Mutation?

if __name__ == '__main__':
    print('\n### How Effective is Mutation?')



def has_distributive_law(tree) -> bool:
    for node in walk(tree):  # iterate over all nodes in `tree`
        # print(node)
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Mult):
                if isinstance(node.right, ast.BinOp):
                    if isinstance(node.right.op, ast.Add):
                        return True

                if isinstance(node.left, ast.BinOp):
                    if isinstance(node.left.op, ast.Add):
                        return True

    return False

if __name__ == '__main__':
    show_ast(ast.parse("1 + (2 * 3)"))

if __name__ == '__main__':
    has_distributive_law(ast.parse("1 * (2 + 3)"))

if __name__ == '__main__':
    has_distributive_law(ast.parse("(1 + 2) * 3"))

if __name__ == '__main__':
    has_distributive_law(ast.parse("1 + (2 * 3)"))

if __name__ == '__main__':
    has_distributive_law(ast.parse("def f(a, b):\n    return a * (b + 10)"))

def how_many_mutations(code: str) -> int:
    solver = ISLaSolver(python_ast_grammar)

    code_ast = ast.parse(code)
    code_ast = ast.fix_missing_locations(code_ast)
    code_ast_str = ast.dump(code_ast)
    code_derivation_tree = solver.parse(code_ast_str)
    mutations = 0
    mutated_code_ast = code_ast

    while not has_distributive_law(mutated_code_ast):
        mutations += 1
        if mutations % 100 == 0:
            print(f'{mutations}...', end='')

        mutated_code_str = str(solver.mutate(code_derivation_tree))
        mutated_code_ast = eval(mutated_code_str)
        # mutated_code_ast = ast.fix_missing_locations(mutated_code_ast)
        # print(ast.dump(mutated_code_ast))
        # print(ast.unparse(mutated_code_ast))

    return mutations

if __name__ == '__main__':
    assert how_many_mutations('1 * (2 + 3)') == 0

if __name__ == '__main__':
    how_many_mutations('2 + 2')    # <-- Note: this can take a minute

if __name__ == '__main__':
    how_many_mutations('2')  # <-- Note: this can take several minutes

## Evolutionary Fuzzing
## --------------------

if __name__ == '__main__':
    print('\n## Evolutionary Fuzzing')



### Getting Coverage

if __name__ == '__main__':
    print('\n### Getting Coverage')



from .Coverage import Coverage

if __name__ == '__main__':
    mult_ast = ast.parse("1 * 2")
    with Coverage() as cov:
        has_distributive_law(mult_ast)

if __name__ == '__main__':
    cov.coverage()

def show_coverage(cov, fun):
    fun_lines, fun_start = inspect.getsourcelines(fun)
    fun_name = fun.__name__
    coverage = cov.coverage()
    for line in range(len(fun_lines)):
        if (fun_name, line + fun_start) in coverage:
            print('# ', end='')  # covered lines
        else:
            print('  ', end='')  # uncovered lines
        print(line + fun_start, fun_lines[line], end='')

if __name__ == '__main__':
    show_coverage(cov, has_distributive_law)

### Fitness

if __name__ == '__main__':
    print('\n### Fitness')



def ast_fitness(code_ast) -> int:
    with Coverage() as cov:
        has_distributive_law(code_ast)
    lines = set()
    for (name, line) in cov.coverage():
        if name == has_distributive_law.__name__:
            lines.add(line)
    return len(lines)

if __name__ == '__main__':
    ast_fitness(ast.parse("1"))

if __name__ == '__main__':
    ast_fitness(ast.parse("1 + 1"))

if __name__ == '__main__':
    ast_fitness(ast.parse("1 * 2"))

if __name__ == '__main__':
    ast_fitness(ast.parse("1 * (2 + 3)"))

def tree_fitness(tree) -> float:
    code_str = str(tree)
    code_ast = ast.fix_missing_locations(eval(code_str))
    fitness = ast_fitness(code_ast)
    # print(ast.unparse(code_ast), f"\n=> Fitness = {fitness}\n")
    return fitness + 1 / len(code_str)

if __name__ == '__main__':
    tree_fitness(sum_tree)

### Evolving Inputs

if __name__ == '__main__':
    print('\n### Evolving Inputs')



def initial_population(tree):
    return [ (tree, tree_fitness(tree)) ]

if __name__ == '__main__':
    sum_population = initial_population(sum_tree)

if __name__ == '__main__':
    len(sum_population)

OFFSPRING = 2

def evolve(population, min_fitness=-1):
    solver = ISLaSolver(python_ast_grammar)

    for (candidate, _) in list(population):
        for i in range(OFFSPRING):
            child = solver.mutate(candidate, min_mutations=1, max_mutations=1)
            child_fitness = tree_fitness(child)
            if child_fitness > min_fitness:
                population.append((child, child_fitness))
    return population

if __name__ == '__main__':
    sum_population = evolve(sum_population)
    len(sum_population)

if __name__ == '__main__':
    sum_population = evolve(sum_population)
    len(sum_population)

if __name__ == '__main__':
    sum_population = evolve(sum_population)
    len(sum_population)

if __name__ == '__main__':
    sum_population = evolve(sum_population)
    len(sum_population)

if __name__ == '__main__':
    sum_population = evolve(sum_population)
    len(sum_population)

### Survival of the Fittest

if __name__ == '__main__':
    print('\n### Survival of the Fittest')



POPULATION_SIZE = 100

def get_fitness(elem):
    (candidate, fitness) = elem
    return fitness

def select(population):
    population = sorted(population, key=get_fitness, reverse=True)
    population = population[:POPULATION_SIZE]
    return population

if __name__ == '__main__':
    sum_population = select(sum_population)
    len(sum_population)

### Evolution

if __name__ == '__main__':
    print('\n### Evolution')



GENERATIONS = 100  # Upper bound

if __name__ == '__main__':
    trial = 1
    found = False

    while not found:
        sum_population = initial_population(sum_tree)
        prev_best_fitness = -1

        for generation in range(GENERATIONS):
            sum_population = evolve(sum_population, min_fitness=prev_best_fitness)
            sum_population = select(sum_population)
            best_candidate, best_fitness = sum_population[0]
            if best_fitness > prev_best_fitness:
                print(f"Generation {generation}: found new best candidate (fitness={best_fitness}):")
                best_ast = ast.fix_missing_locations(eval(str(best_candidate)))
                print(ast.unparse(best_ast))
                prev_best_fitness = best_fitness

                if has_distributive_law(best_ast):
                    print("Done!")
                    found = True
                    break

        trial = trial + 1
        print(f"\n\nRestarting; trial #{trial}")

if __name__ == '__main__':
    print(ast.unparse(best_ast))

if __name__ == '__main__':
    assert has_distributive_law(best_ast)

### Chances of Evolutionary Fuzzing

if __name__ == '__main__':
    print('\n### Chances of Evolutionary Fuzzing')



if __name__ == '__main__':
    assert '<BinOp>' in python_ast_grammar['<expr>']

if __name__ == '__main__':
    len(python_ast_grammar['<expr>'])

if __name__ == '__main__':
    assert 'Add()' in python_ast_grammar['<operator>']
    assert 'Mult()' in python_ast_grammar['<operator>']

if __name__ == '__main__':
    len(python_ast_grammar['<operator>'])

if __name__ == '__main__':
    (len(python_ast_grammar['<expr>'])       # chances of choosing a `BinOp`
    * len(python_ast_grammar['<operator>'])  # chances of choosing a `*`
    * len(python_ast_grammar['<expr>'])      # chances of choosing a `BinOp` as a child
    * len(python_ast_grammar['<operator>'])  # chances of choosing a `+`
    / 2)   # two chances - one for the left child, one for the right

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    fuzzer = PythonFuzzer()
    print(fuzzer.fuzz())

if __name__ == '__main__':
    fuzzer = PythonFuzzer('<While>')
    print(fuzzer.fuzz())

if __name__ == '__main__':
    sorted(list(PYTHON_AST_GRAMMAR.keys()))

if __name__ == '__main__':
    python_ast_grammar = convert_ebnf_grammar(PYTHON_AST_GRAMMAR)

if __name__ == '__main__':
    solver = ISLaSolver(python_ast_grammar, start_symbol='<FunctionDef>')

if __name__ == '__main__':
    ast_string = str(solver.solve())
    ast_string

from ast import *

if __name__ == '__main__':
    abstract_syntax_tree = eval(ast_string)

if __name__ == '__main__':
    ast.fix_missing_locations(abstract_syntax_tree)
    print(ast.unparse(abstract_syntax_tree))

import inspect
import markdown
from .bookutils import HTML

if __name__ == '__main__':
    sig = inspect.signature(PythonFuzzer.__init__)
    sig_str = str(sig) if sig else ""
    doc = inspect.getdoc(PythonFuzzer.__init__) or ""
    HTML(markdown.markdown('`PythonFuzzer' + sig_str + '`\n\n' + doc))

from .ClassDiagram import display_class_hierarchy

if __name__ == '__main__':
    display_class_hierarchy([PythonFuzzer],
                            public_methods=[
                                PythonFuzzer.__init__,
                                PythonFuzzer.fuzz,
                                ISLaSolver.__init__
                            ],
                            project='fuzzingbook')

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')


