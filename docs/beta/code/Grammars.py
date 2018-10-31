#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Grammars.html
# Last change: 2018-10-26 16:52:52+02:00
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


# # Fuzzing with Grammars

if __name__ == "__main__":
    print('# Fuzzing with Grammars')




# ## Input Languages

if __name__ == "__main__":
    print('\n## Input Languages')




# ## Grammars

if __name__ == "__main__":
    print('\n## Grammars')




# ### Rules and Expansions

if __name__ == "__main__":
    print('\n### Rules and Expansions')




# ### Arithmetic Expressions

if __name__ == "__main__":
    print('\n### Arithmetic Expressions')




# ## Representing Grammars in Python

if __name__ == "__main__":
    print('\n## Representing Grammars in Python')




import fuzzingbook_utils

DIGIT_GRAMMAR = {
    "<start>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

EXPR_GRAMMAR = {
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

if __name__ == "__main__":
    EXPR_GRAMMAR["<digit>"]


if __name__ == "__main__":
    "<identifier>" in EXPR_GRAMMAR


# ## Some Definitions

if __name__ == "__main__":
    print('\n## Some Definitions')




START_SYMBOL = "<start>"

import re

RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')

def nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_NONTERMINAL, expansion)

if __name__ == "__main__":
    assert nonterminals("<term> * <factor>") == ["<term>", "<factor>"]
    assert nonterminals("<digit><integer>") == ["<digit>", "<integer>"]
    assert nonterminals("1 < 3 > 2") == []
    assert nonterminals("1 <3> 2") == ["<3>"]
    assert nonterminals("1 + 2") == []
    assert nonterminals(("<1>", {'option': 'value'})) == ["<1>"]


def is_nonterminal(s):
    return re.match(RE_NONTERMINAL, s)

if __name__ == "__main__":
    assert is_nonterminal("<abc>")
    assert is_nonterminal("<symbol-1>")
    assert not is_nonterminal("+")


# ## A Simple Grammar Fuzzer

if __name__ == "__main__":
    print('\n## A Simple Grammar Fuzzer')




import random

class ExpansionError(Exception):
    pass

def simple_grammar_fuzzer(grammar, start_symbol=START_SYMBOL,
                          max_nonterminals=10, max_expansion_trials=100,
                          log=False):
    term = start_symbol
    expansion_trials = 0

    while len(nonterminals(term)) > 0:
        symbol_to_expand = random.choice(nonterminals(term))
        expansions = grammar[symbol_to_expand]
        expansion = random.choice(expansions)
        new_term = term.replace(symbol_to_expand, expansion, 1)

        if len(nonterminals(new_term)) < max_nonterminals:
            term = new_term
            if log:
                print("%-40s" % (symbol_to_expand + " -> " + expansion), term)
            expansion_trials = 0
        else:
            expansion_trials += 1
            if expansion_trials >= max_expansion_trials:
                raise ExpansionError("Cannot expand " + repr(term))

    return term

if __name__ == "__main__":
    simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=3, log=True)


if __name__ == "__main__":
    for i in range(10):
        print(simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=5))


# ## Some Grammars

if __name__ == "__main__":
    print('\n## Some Grammars')




# ### A CGI Grammar

if __name__ == "__main__":
    print('\n### A CGI Grammar')




CGI_GRAMMAR = {
    "<start>":
        ["<string>"],

    "<string>":
        ["<letter>", "<letter><string>"],

    "<letter>":
        ["<plus>", "<percent>", "<other>"],

    "<plus>":
        ["+"],

    "<percent>":
        ["%<hexdigit><hexdigit>"],

    "<hexdigit>":
        ["0", "1", "2", "3", "4", "5", "6", "7",
            "8", "9", "a", "b", "c", "d", "e", "f"],

    "<other>":  # Actually, could be _all_ letters
        ["0", "1", "2", "3", "4", "5", "a", "b", "c", "d", "e", "-", "_"],
}

if __name__ == "__main__":
    for i in range(10):
        print(simple_grammar_fuzzer(grammar=CGI_GRAMMAR, max_nonterminals=10))


# ### A URL Grammar

if __name__ == "__main__":
    print('\n### A URL Grammar')




URL_GRAMMAR = {
    "<start>":
        ["<url>"],
    "<url>":
        ["<scheme>://<authority><path><query>"],
    "<scheme>":
        ["http", "https", "ftp", "ftps"],
    "<authority>":
        ["<host>", "<host>:<port>", "<userinfo>@<host>", "<userinfo>@<host>:<port>"],
    "<host>":  # Just a few
        ["cispa.saarland", "www.google.com", "fuzzingbook.com"],
    "<port>":
        ["80", "8080", "<nat>"],
    "<nat>":
        ["<digit>", "<digit><digit>"],
    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "<userinfo>":  # Just one
        ["user:password"],
    "<path>":  # Just a few
        ["", "/", "/<id>"],
    "<id>":  # Just a few
        ["abc", "def", "x<digit><digit>"],
    "<query>":
        ["", "?<params>"],
    "<params>":
        ["<param>", "<param>&<params>"],
    "<param>":  # Just a few
        ["<id>=<id>", "<id>=<nat>"],
}

if __name__ == "__main__":
    for i in range(10):
        print(simple_grammar_fuzzer(grammar=URL_GRAMMAR, max_nonterminals=10))


# ## Grammars as Mutation Seeds

if __name__ == "__main__":
    print('\n## Grammars as Mutation Seeds')




if __package__ is None or __package__ == "":
    from MutationFuzzer import MutationFuzzer
else:
    from .MutationFuzzer import MutationFuzzer


if __name__ == "__main__":
    number_of_seeds = 10
    seeds = [
        simple_grammar_fuzzer(
            grammar=URL_GRAMMAR,
            max_nonterminals=10) for i in range(number_of_seeds)]
    seeds


if __name__ == "__main__":
    m = MutationFuzzer(seeds)


if __name__ == "__main__":
    for i in range(20):
        print(m.fuzz())


# ## Grammar Shortcuts

if __name__ == "__main__":
    print('\n## Grammar Shortcuts')




# ### Escapes

if __name__ == "__main__":
    print('\n### Escapes')




if __name__ == "__main__":
    nonterminal_grammar = {
        "<start>": ["<nonterminal>"],
        "<nonterminal>": ["<left-angle><identifier><right-angle>"],
        "<left-angle>": ["<"],
        "<right-angle>": [">"]
    }


# ### Character Classes

if __name__ == "__main__":
    print('\n### Character Classes')




import string

if __name__ == "__main__":
    string.ascii_letters


def srange(characters):
    """Construct a list with all characters in the string }`characters`"""
    return [c for c in characters]

if __name__ == "__main__":
    srange(string.ascii_letters)[:10]


if __name__ == "__main__":
    nonterminal_grammar["<identifier>"] = ["<idchar>", "<idchar><identifier>"]
    nonterminal_grammar["<idchar>"] = srange(
        string.ascii_letters) + srange(string.digits) + srange("-_")


if __name__ == "__main__":
    [simple_grammar_fuzzer(nonterminal_grammar, "<identifier>") for i in range(10)]


def crange(character_start, character_end):
    return [chr(i)
            for i in range(ord(character_start), ord(character_end) + 1)]

if __name__ == "__main__":
    crange('0', '9')


if __name__ == "__main__":
    assert crange('a', 'z') == srange(string.ascii_lowercase)


# ### Grammar Shortcuts

if __name__ == "__main__":
    print('\n### Grammar Shortcuts')




if __name__ == "__main__":
    nonterminal_grammar["<identifier>"]


from copy import deepcopy

if __name__ == "__main__":
    nonterminal_ebnf_grammar = deepcopy(nonterminal_grammar)
    nonterminal_ebnf_grammar["<identifier>"] = "<idchar>+"


EXPR_EBNF_GRAMMAR = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<term> + <expr>", "<term> - <expr>", "<term>"],

    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>"],

    "<factor>":
        ["<sign>?<factor>", "(<expr>)", "<integer>(.<integer>)?"],

    "<sign>":
        ["+", "-"],

    "<integer>":
        ["<digit>+"],

    "<digit>":
        srange(string.digits)
}

# #### Creating New Symbols

if __name__ == "__main__":
    print('\n#### Creating New Symbols')




def new_symbol(grammar, symbol_name="<symbol>"):
    """Return a new symbol for `grammar` based on `symbol_name`"""
    count = 1
    while True:
        tentative_symbol_name = symbol_name[:-1] + "-" + repr(count) + ">"
        if tentative_symbol_name not in grammar:
            return tentative_symbol_name
        count += 1

if __name__ == "__main__":
    assert new_symbol(EXPR_EBNF_GRAMMAR, '<expr>') == '<expr-1>'


# #### Expanding Parenthesized Expressions

if __name__ == "__main__":
    print('\n#### Expanding Parenthesized Expressions')




RE_PARENTHESIZED_EXPR = re.compile(r'\([^())]*\)[?+*]')

def parenthesized_expressions(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_PARENTHESIZED_EXPR, expansion)

if __name__ == "__main__":
    assert parenthesized_expressions("(<foo>)* (<foo><bar>)+ (+<foo>)? <integer>(.<integer>)?") == [
        '(<foo>)*', '(<foo><bar>)+', '(+<foo>)?', '(.<integer>)?']


def convert_ebnf_parentheses(ebnf_grammar):
    """Convert a grammar in extended BNF to BNF"""
    grammar = deepcopy(ebnf_grammar)
    for nonterminal in ebnf_grammar:
        expansions = ebnf_grammar[nonterminal]

        for i in range(len(expansions)):
            expansion = expansions[i]

            while True:
                parenthesized_exprs = parenthesized_expressions(expansion)
                if len(parenthesized_exprs) == 0:
                    break

                for expr in parenthesized_exprs:
                    operator = expr[-1:]
                    contents = expr[1:-2]

                    new_sym = new_symbol(grammar)
                    expansion = grammar[nonterminal][i].replace(
                        expr, new_sym + operator, 1)
                    grammar[nonterminal][i] = expansion
                    grammar[new_sym] = [contents]

    return grammar

if __name__ == "__main__":
    convert_ebnf_parentheses({"<number>": ["<integer>(.<integer>)?"]})


if __name__ == "__main__":
    convert_ebnf_parentheses({"<foo>": ["((<foo>)?)+"]})


# #### Expanding Operators

if __name__ == "__main__":
    print('\n#### Expanding Operators')




RE_EXTENDED_NONTERMINAL = re.compile(r'(<[^<> ]*>[?+*])')

def extended_nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_EXTENDED_NONTERMINAL, expansion)

if __name__ == "__main__":
    assert extended_nonterminals(
        "<foo>* <bar>+ <elem>? <none>") == ['<foo>*', '<bar>+', '<elem>?']


def convert_ebnf_operators(ebnf_grammar):
    """Convert a grammar in extended BNF to BNF"""
    grammar = deepcopy(ebnf_grammar)
    for nonterminal in ebnf_grammar:
        expansions = ebnf_grammar[nonterminal]

        for i in range(len(expansions)):
            expansion = expansions[i]
            extended_symbols = extended_nonterminals(expansion)

            for extended_symbol in extended_symbols:
                operator = extended_symbol[-1:]
                original_symbol = extended_symbol[:-1]

                new_sym = new_symbol(grammar, original_symbol)
                grammar[nonterminal][i] = grammar[nonterminal][i].replace(
                    extended_symbol, new_sym, 1)

                if operator == '?':
                    grammar[new_sym] = ["", original_symbol]
                elif operator == '*':
                    grammar[new_sym] = ["", original_symbol + new_sym]
                elif operator == '+':
                    grammar[new_sym] = [
                        original_symbol, original_symbol + new_sym]

    return grammar

if __name__ == "__main__":
    convert_ebnf_operators({"<integer>": ["<digit>+"]})


# #### All Together

if __name__ == "__main__":
    print('\n#### All Together')




def convert_ebnf_grammar(ebnf_grammar):
    return convert_ebnf_operators(convert_ebnf_parentheses(ebnf_grammar))

if __name__ == "__main__":
    convert_ebnf_grammar({"<authority>": ["(<userinfo>@)?<host>(:<port>)?"]})


if __name__ == "__main__":
    expr_grammar = convert_ebnf_grammar(EXPR_EBNF_GRAMMAR)
    expr_grammar


# ## Checking Grammars

if __name__ == "__main__":
    print('\n## Checking Grammars')




import sys

def def_used_nonterminals(grammar, start_symbol=START_SYMBOL):
    defined_nonterminals = set()
    used_nonterminals = set([start_symbol])

    for defined_nonterminal in grammar:
        defined_nonterminals.add(defined_nonterminal)
        expansions = grammar[defined_nonterminal]
        if not isinstance(expansions, list):
            print(repr(defined_nonterminal) + ": expansion is not a list",
                  file=sys.stderr)
            return None, None

        if len(expansions) == 0:
            print(repr(defined_nonterminal) + ": expansion list empty",
                  file=sys.stderr)
            return None, None

        for expansion in expansions:
            if isinstance(expansion, tuple):
                expansion = expansion[0]
            if not isinstance(expansion, str):
                print(repr(defined_nonterminal) + ": "
                      + repr(expansion) + ": not a string",
                      file=sys.stderr)
                return None, None

            for used_nonterminal in nonterminals(expansion):
                used_nonterminals.add(used_nonterminal)

    return defined_nonterminals, used_nonterminals

def is_valid_grammar(grammar, start_symbol=START_SYMBOL):
    defined_nonterminals, used_nonterminals = def_used_nonterminals(
        grammar, start_symbol)
    if defined_nonterminals is None or used_nonterminals is None:
        return False

    for unused_nonterminal in defined_nonterminals - used_nonterminals:
        print(repr(unused_nonterminal) + ": defined, but not used",
              file=sys.stderr)
    for undefined_nonterminal in used_nonterminals - defined_nonterminals:
        print(repr(undefined_nonterminal) + ": used, but not defined",
              file=sys.stderr)

    return used_nonterminals == defined_nonterminals

if __name__ == "__main__":
    assert is_valid_grammar(EXPR_GRAMMAR)
    assert is_valid_grammar(CGI_GRAMMAR)
    assert is_valid_grammar(URL_GRAMMAR)


if __name__ == "__main__":
    assert is_valid_grammar(EXPR_EBNF_GRAMMAR)


if __name__ == "__main__":
    assert not is_valid_grammar({"<start>": ["<x>"], "<y>": ["1"]})


if __name__ == "__main__":
    assert not is_valid_grammar({"<start>": "123"})


if __name__ == "__main__":
    assert not is_valid_grammar({"<start>": []})


if __name__ == "__main__":
    assert not is_valid_grammar({"<start>": [1, 2, 3]})


# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Background

if __name__ == "__main__":
    print('\n## Background')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1: A JSON Grammar

if __name__ == "__main__":
    print('\n### Exercise 1: A JSON Grammar')




CHARACTERS_WITHOUT_QUOTE = (string.digits
                            + string.ascii_letters
                            + string.punctuation.replace('"', '').replace('\\', '')
                            + ' ')

JSON_EBNF_GRAMMAR = {
    "<start>": ["<json>"],

    "<json>": ["<element>"],

    "<element>": ["<ws><value><ws>"],

    "<value>": ["<object>", "<array>", "<string>", "<number>", "true", "false", "null"],

    "<object>": ["{<ws>}", "{<members>}"],

    "<members>": ["<member>(,<members>)*"],

    "<member>": ["<ws><string><ws>:<element>"],

    "<array>": ["{<ws>}", "{<elements>}"],

    "<elements>": ["<element>(,<elements>)*"],

    "<element>": ["<ws><value><ws>"],

    "<string>": ['"' + "<characters>" + '"'],

    "<characters>": srange(CHARACTERS_WITHOUT_QUOTE),

    "<number>": ["<int><frac><exp>"],

    "<int>": ["<digit>", "<onenine><digits>", "-<digits>", "-<onenine><digits>"],

    "<digits>": ["<digit>+"],

    "<digit>": ['0', "<onenine>"],

    "<onenine>": crange('1', '9'),

    "<frac>": ["", ".<digits>"],

    "<exp>": ["", "E<sign><digits>", "e<sign><digits>"],

    "<sign>": ["", '+', '-'],

    # "<ws>": srange(string.whitespace)

    "<ws>": [" "]
}

assert is_valid_grammar(JSON_EBNF_GRAMMAR)

JSON_GRAMMAR = convert_ebnf_grammar(JSON_EBNF_GRAMMAR)

if __package__ is None or __package__ == "":
    from ExpectError import ExpectError
else:
    from .ExpectError import ExpectError


if __name__ == "__main__":
    for i in range(10):
        with ExpectError():
            print(simple_grammar_fuzzer(JSON_GRAMMAR, '<object>'))


# ### Exercise 2: Finding Bugs

if __name__ == "__main__":
    print('\n### Exercise 2: Finding Bugs')




if __package__ is None or __package__ == "":
    from ExpectError import ExpectError, ExpectTimeout
else:
    from .ExpectError import ExpectError, ExpectTimeout


if __name__ == "__main__":
    with ExpectError():
        simple_grammar_fuzzer(nonterminal_grammar, log=True)


if __name__ == "__main__":
    with ExpectTimeout(1):
        for i in range(10):
            print(simple_grammar_fuzzer(expr_grammar))


# ### Exercise 3: Grammars with Regular Expressions

if __name__ == "__main__":
    print('\n### Exercise 3: Grammars with Regular Expressions')




# #### Part 1: Convert regular expressions

if __name__ == "__main__":
    print('\n#### Part 1: Convert regular expressions')




# #### Part 2: Identify and expand regular expressions

if __name__ == "__main__":
    print('\n#### Part 2: Identify and expand regular expressions')




# ### Exercise 4: Defining Grammars as Functions (Advanced)

if __name__ == "__main__":
    print('\n### Exercise 4: Defining Grammars as Functions (Advanced)')




def expression_grammar_fn():
    start = "<expr>"
    expr = "<term> + <expr>" | "<term> - <expr>"
    term = "<factor> * <term>" | "<factor> / <term>" | "<factor>"
    factor = "+<factor>" | "-<factor>" | "(<expr>)" | "<integer>.<integer>" | "<integer>"
    integer = "<digit><integer>" | "<digit>"
    digit = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

if __name__ == "__main__":
    with ExpectError():
        alt_expression_grammar()


import ast
import inspect

if __name__ == "__main__":
    source = inspect.getsource(expression_grammar_fn)
    source


if __name__ == "__main__":
    tree = ast.parse(source)


def get_alternatives(op, to_expr=lambda o: o.s):
    if isinstance(op, ast.BinOp) and isinstance(op.op, ast.BitOr):
        return get_alternatives(op.left, to_expr) + [to_expr(op.right)]
    return [to_expr(op)]

def funct_parser(tree, to_expr=lambda o: o.s):
    return {assign.targets[0].id: get_alternatives(assign.value, to_expr)
            for assign in tree.body[0].body}

if __name__ == "__main__":
    grammar = funct_parser(tree)
    for symbol in grammar:
        print(symbol, "::=", grammar[symbol])


# #### Part 1 (a): One Single Function

if __name__ == "__main__":
    print('\n#### Part 1 (a): One Single Function')




def define_grammar(fn, to_expr=lambda o: o.s):
    source = inspect.getsource(fn)
    tree = ast.parse(source)
    grammar = funct_parser(tree, to_expr)
    return grammar

if __name__ == "__main__":
    define_grammar(expression_grammar_fn)


# #### Part 1 (b): Alternative representations

if __name__ == "__main__":
    print('\n#### Part 1 (b): Alternative representations')




def define_name(o): return o.id if isinstance(o, ast.Name) else o.s

def define_expr(op):
    if isinstance(op, ast.BinOp) and isinstance(op.op, ast.Add):
        return (*define_expr(op.left), define_name(op.right))
    return (define_name(op),)

def define_ex_grammar(fn):
    return define_grammar(fn, define_expr)

# #### Part 2: Extended Grammars

if __name__ == "__main__":
    print('\n#### Part 2: Extended Grammars')




def identifier_grammar_fn():
    identifier = idchar * (1,)
