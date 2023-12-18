#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Fuzzing APIs" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/APIFuzzer.html
# Last change: 2023-11-12 13:48:13+01:00
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
The Fuzzing Book - Fuzzing APIs

This file can be _executed_ as a script, running all experiments:

    $ python APIFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.APIFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/APIFuzzer.html

This chapter provides *grammar constructors* that are useful for generating _function calls_.

The grammars are [probabilistic](ProbabilisticGrammarFuzzer.ipynb) and make use of [generators](GeneratorGrammarFuzzer.ipynb), so use `ProbabilisticGeneratorGrammarFuzzer` as a producer.

>>> from GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer

`INT_GRAMMAR`, `FLOAT_GRAMMAR`, `ASCII_STRING_GRAMMAR` produce integers, floats, and strings, respectively:

>>> fuzzer = ProbabilisticGeneratorGrammarFuzzer(INT_GRAMMAR)
>>> [fuzzer.fuzz() for i in range(10)]
['-51', '9', '0', '0', '0', '0', '32', '0', '0', '0']
>>> fuzzer = ProbabilisticGeneratorGrammarFuzzer(FLOAT_GRAMMAR)
>>> [fuzzer.fuzz() for i in range(10)]
['0e0',
 '-9.43e34',
 '-7.3282e0',
 '-9.5e-9',
 '0',
 '-30.840386e-5',
 '3',
 '-4.1e0',
 '-9.7',
 '413']
>>> fuzzer = ProbabilisticGeneratorGrammarFuzzer(ASCII_STRING_GRAMMAR)
>>> [fuzzer.fuzz() for i in range(10)]
['"#vYV*t@I%KNTT[q~}&-v+[zAzj[X-z|RzC$(g$Br]1tC\':5!5>> int_grammar = int_grammar_with_range(100, 200)
>>> fuzzer = ProbabilisticGeneratorGrammarFuzzer(int_grammar)
>>> [fuzzer.fuzz() for i in range(10)]
['154', '149', '185', '117', '182', '154', '131', '194', '147', '192']

`float_grammar_with_range(start, end)` produces a floating-number grammar with values `N` such that `start >> float_grammar = float_grammar_with_range(100, 200)
>>> fuzzer = ProbabilisticGeneratorGrammarFuzzer(float_grammar)
>>> [fuzzer.fuzz() for i in range(10)]
['121.8092479227325',
 '187.18037169119634',
 '127.9576486784452',
 '125.47768739781723',
 '151.8091820472274',
 '117.864410860742',
 '187.50918008379483',
 '119.29335112884749',
 '149.2637029583114',
 '126.61818995939146']

All such values can be immediately used for testing function calls:

>>> from math import sqrt
>>> fuzzer = ProbabilisticGeneratorGrammarFuzzer(int_grammar)
>>> call = "sqrt(" + fuzzer.fuzz() + ")"
>>> call
'sqrt(143)'
>>> eval(call)
11.958260743101398

These grammars can also be composed to form more complex grammars. `list_grammar(object_grammar)` returns a grammar that produces lists of objects as defined by `object_grammar`.

>>> int_list_grammar = list_grammar(int_grammar)
>>> fuzzer = ProbabilisticGeneratorGrammarFuzzer(int_list_grammar)
>>> [fuzzer.fuzz() for i in range(5)]
['[118, 111, 188, 137, 129]',
 '[170, 172]',
 '[171, 161, 117, 191, 175, 183, 164]',
 '[189]',
 '[129, 110, 178]']
>>> some_list = eval(fuzzer.fuzz())
>>> some_list
[172, 120, 106, 192, 124, 191, 161, 100, 117]
>>> len(some_list)
9

In a similar vein, we can construct arbitrary further data types for testing individual functions programmatically.


For more details, source, and documentation, see
"The Fuzzing Book - Fuzzing APIs"
at https://www.fuzzingbook.org/html/APIFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Fuzzing APIs
# ============

if __name__ == '__main__':
    print('# Fuzzing APIs')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo('CC1VvOGkzm8')

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Fuzzing a Function
## ------------------

if __name__ == '__main__':
    print('\n## Fuzzing a Function')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from urllib.parse import urlparse

if __name__ == '__main__':
    urlparse('https://www.fuzzingbook.com/html/APIFuzzer.html')

from .Grammars import URL_GRAMMAR, is_valid_grammar, START_SYMBOL
from .Grammars import opts, extend_grammar, Grammar
from .GrammarFuzzer import GrammarFuzzer

if __name__ == '__main__':
    url_fuzzer = GrammarFuzzer(URL_GRAMMAR)

if __name__ == '__main__':
    for i in range(10):
        url = url_fuzzer.fuzz()
        print(urlparse(url))

## Synthesizing Code
## -----------------

if __name__ == '__main__':
    print('\n## Synthesizing Code')



if __name__ == '__main__':
    call = "urlparse('http://www.cispa.de/')"

if __name__ == '__main__':
    eval(call)

URLPARSE_GRAMMAR: Grammar = {
    "<call>":
        ['urlparse("<url>")']
}

# Import definitions from URL_GRAMMAR
URLPARSE_GRAMMAR.update(URL_GRAMMAR)
URLPARSE_GRAMMAR["<start>"] = ["<call>"]

assert is_valid_grammar(URLPARSE_GRAMMAR)

if __name__ == '__main__':
    URLPARSE_GRAMMAR

if __name__ == '__main__':
    urlparse_fuzzer = GrammarFuzzer(URLPARSE_GRAMMAR)
    urlparse_fuzzer.fuzz()

def do_call(call_string):
    print(call_string)
    result = eval(call_string)
    print("\t= " + repr(result))
    return result

if __name__ == '__main__':
    call = urlparse_fuzzer.fuzz()
    do_call(call)

URLPARSE_C_GRAMMAR: Grammar = {
    "<cfile>": ["<cheader><cfunction>"],
    "<cheader>": ['#include "urlparse.h"\n\n'],
    "<cfunction>": ["void test() {\n<calls>}\n"],
    "<calls>": ["<call>", "<calls><call>"],
    "<call>": ['    urlparse("<url>");\n']
}

URLPARSE_C_GRAMMAR.update(URL_GRAMMAR)

if __name__ == '__main__':
    URLPARSE_C_GRAMMAR["<start>"] = ["<cfile>"]

if __name__ == '__main__':
    assert is_valid_grammar(URLPARSE_C_GRAMMAR)

if __name__ == '__main__':
    urlparse_fuzzer = GrammarFuzzer(URLPARSE_C_GRAMMAR)
    print(urlparse_fuzzer.fuzz())

## Synthesizing Oracles
## --------------------

if __name__ == '__main__':
    print('\n## Synthesizing Oracles')



from .GeneratorGrammarFuzzer import GeneratorGrammarFuzzer, ProbabilisticGeneratorGrammarFuzzer

URLPARSE_ORACLE_GRAMMAR: Grammar = extend_grammar(URLPARSE_GRAMMAR,
{
     "<call>": [("assert urlparse('<url>').geturl() == '<url>'",
                 opts(post=lambda url_1, url_2: [None, url_1]))]
})

if __name__ == '__main__':
    urlparse_oracle_fuzzer = GeneratorGrammarFuzzer(URLPARSE_ORACLE_GRAMMAR)
    test = urlparse_oracle_fuzzer.fuzz()
    print(test)

if __name__ == '__main__':
    exec(test)

URLPARSE_ORACLE_GRAMMAR: Grammar = extend_grammar(URLPARSE_GRAMMAR,
{
     "<call>": [("result = urlparse('<scheme>://<host><path>?<params>')\n"
                 # + "print(result)\n"
                 + "assert result.scheme == '<scheme>'\n"
                 + "assert result.netloc == '<host>'\n"
                 + "assert result.path == '<path>'\n"
                 + "assert result.query == '<params>'",
                 opts(post=lambda scheme_1, authority_1, path_1, params_1,
                      scheme_2, authority_2, path_2, params_2:
                      [None, None, None, None,
                       scheme_1, authority_1, path_1, params_1]))]
})

# Get rid of unused symbols
del URLPARSE_ORACLE_GRAMMAR["<url>"]
del URLPARSE_ORACLE_GRAMMAR["<query>"]
del URLPARSE_ORACLE_GRAMMAR["<authority>"]
del URLPARSE_ORACLE_GRAMMAR["<userinfo>"]
del URLPARSE_ORACLE_GRAMMAR["<port>"]

if __name__ == '__main__':
    urlparse_oracle_fuzzer = GeneratorGrammarFuzzer(URLPARSE_ORACLE_GRAMMAR)
    test = urlparse_oracle_fuzzer.fuzz()
    print(test)

if __name__ == '__main__':
    exec(test)

def fuzzed_url_element(symbol):
    return GrammarFuzzer(URLPARSE_GRAMMAR, start_symbol=symbol).fuzz()

if __name__ == '__main__':
    scheme = fuzzed_url_element("<scheme>")
    authority = fuzzed_url_element("<authority>")
    path = fuzzed_url_element("<path>")
    query = fuzzed_url_element("<params>")
    url = "%s://%s%s?%s" % (scheme, authority, path, query)
    result = urlparse(url)
    # print(result)
    assert result.geturl() == url
    assert result.scheme == scheme
    assert result.path == path
    assert result.query == query

## Synthesizing Data
## -----------------

if __name__ == '__main__':
    print('\n## Synthesizing Data')



### Integers

if __name__ == '__main__':
    print('\n### Integers')



from .Grammars import convert_ebnf_grammar, crange

from .ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer

INT_EBNF_GRAMMAR: Grammar = {
    "<start>": ["<int>"],
    "<int>": ["<_int>"],
    "<_int>": ["(-)?<leaddigit><digit>*", "0"],
    "<leaddigit>": crange('1', '9'),
    "<digit>": crange('0', '9')
}

assert is_valid_grammar(INT_EBNF_GRAMMAR)

INT_GRAMMAR = convert_ebnf_grammar(INT_EBNF_GRAMMAR)
INT_GRAMMAR

if __name__ == '__main__':
    int_fuzzer = GrammarFuzzer(INT_GRAMMAR)
    print([int_fuzzer.fuzz() for i in range(10)])

from .Grammars import set_opts

import random

def int_grammar_with_range(start, end):
    int_grammar = extend_grammar(INT_GRAMMAR)
    set_opts(int_grammar, "<int>", "<_int>",
        opts(pre=lambda: random.randint(start, end)))
    return int_grammar

if __name__ == '__main__':
    int_fuzzer = GeneratorGrammarFuzzer(int_grammar_with_range(900, 1000))
    [int_fuzzer.fuzz() for i in range(10)]

### Floats

if __name__ == '__main__':
    print('\n### Floats')



FLOAT_EBNF_GRAMMAR: Grammar = {
    "<start>": ["<float>"],
    "<float>": [("<_float>", opts(prob=0.9)), "inf", "NaN"],
    "<_float>": ["<int>(.<digit>+)?<exp>?"],
    "<exp>": ["e<int>"]
}
FLOAT_EBNF_GRAMMAR.update(INT_EBNF_GRAMMAR)
FLOAT_EBNF_GRAMMAR["<start>"] = ["<float>"]

assert is_valid_grammar(FLOAT_EBNF_GRAMMAR)

FLOAT_GRAMMAR = convert_ebnf_grammar(FLOAT_EBNF_GRAMMAR)
FLOAT_GRAMMAR

if __name__ == '__main__':
    float_fuzzer = ProbabilisticGrammarFuzzer(FLOAT_GRAMMAR)
    print([float_fuzzer.fuzz() for i in range(10)])

def float_grammar_with_range(start, end):
    float_grammar = extend_grammar(FLOAT_GRAMMAR)
    set_opts(float_grammar, "<float>", "<_float>", opts(
        pre=lambda: start + random.random() * (end - start)))
    return float_grammar

if __name__ == '__main__':
    float_fuzzer = ProbabilisticGeneratorGrammarFuzzer(
        float_grammar_with_range(900.0, 900.9))
    [float_fuzzer.fuzz() for i in range(10)]

### Strings

if __name__ == '__main__':
    print('\n### Strings')



ASCII_STRING_EBNF_GRAMMAR: Grammar = {
    "<start>": ["<ascii-string>"],
    "<ascii-string>": ['"<ascii-chars>"'],
    "<ascii-chars>": [
        ("", opts(prob=0.05)),
        "<ascii-chars><ascii-char>"
    ],
    "<ascii-char>": crange(" ", "!") + [r'\"'] + crange("#", "~")
}

assert is_valid_grammar(ASCII_STRING_EBNF_GRAMMAR)

ASCII_STRING_GRAMMAR = convert_ebnf_grammar(ASCII_STRING_EBNF_GRAMMAR)

if __name__ == '__main__':
    string_fuzzer = ProbabilisticGrammarFuzzer(ASCII_STRING_GRAMMAR)
    print([string_fuzzer.fuzz() for i in range(10)])

## Synthesizing Composite Data
## ---------------------------

if __name__ == '__main__':
    print('\n## Synthesizing Composite Data')



### Lists

if __name__ == '__main__':
    print('\n### Lists')



LIST_EBNF_GRAMMAR: Grammar = {
    "<start>": ["<list>"],
    "<list>": [
        ("[]", opts(prob=0.05)),
        "[<list-objects>]"
    ],
    "<list-objects>": [
        ("<list-object>", opts(prob=0.2)),
        "<list-object>, <list-objects>"
    ],
    "<list-object>": ["0"],
}

assert is_valid_grammar(LIST_EBNF_GRAMMAR)

LIST_GRAMMAR = convert_ebnf_grammar(LIST_EBNF_GRAMMAR)

def list_grammar(object_grammar, list_object_symbol=None):
    obj_list_grammar = extend_grammar(LIST_GRAMMAR)
    if list_object_symbol is None:
        # Default: Use the first expansion of <start> as list symbol
        list_object_symbol = object_grammar[START_SYMBOL][0]

    obj_list_grammar.update(object_grammar)
    obj_list_grammar[START_SYMBOL] = ["<list>"]
    obj_list_grammar["<list-object>"] = [list_object_symbol]

    assert is_valid_grammar(obj_list_grammar)

    return obj_list_grammar

if __name__ == '__main__':
    int_list_fuzzer = ProbabilisticGrammarFuzzer(list_grammar(INT_GRAMMAR))
    [int_list_fuzzer.fuzz() for i in range(10)]

if __name__ == '__main__':
    string_list_fuzzer = ProbabilisticGrammarFuzzer(
        list_grammar(ASCII_STRING_GRAMMAR))
    [string_list_fuzzer.fuzz() for i in range(10)]

if __name__ == '__main__':
    float_list_fuzzer = ProbabilisticGeneratorGrammarFuzzer(list_grammar(
        float_grammar_with_range(900.0, 900.9)))
    [float_list_fuzzer.fuzz() for i in range(10)]

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



from .GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer

if __name__ == '__main__':
    fuzzer = ProbabilisticGeneratorGrammarFuzzer(INT_GRAMMAR)
    [fuzzer.fuzz() for i in range(10)]

if __name__ == '__main__':
    fuzzer = ProbabilisticGeneratorGrammarFuzzer(FLOAT_GRAMMAR)
    [fuzzer.fuzz() for i in range(10)]

if __name__ == '__main__':
    fuzzer = ProbabilisticGeneratorGrammarFuzzer(ASCII_STRING_GRAMMAR)
    [fuzzer.fuzz() for i in range(10)]

if __name__ == '__main__':
    int_grammar = int_grammar_with_range(100, 200)
    fuzzer = ProbabilisticGeneratorGrammarFuzzer(int_grammar)
    [fuzzer.fuzz() for i in range(10)]

if __name__ == '__main__':
    float_grammar = float_grammar_with_range(100, 200)
    fuzzer = ProbabilisticGeneratorGrammarFuzzer(float_grammar)
    [fuzzer.fuzz() for i in range(10)]

from math import sqrt

if __name__ == '__main__':
    fuzzer = ProbabilisticGeneratorGrammarFuzzer(int_grammar)
    call = "sqrt(" + fuzzer.fuzz() + ")"
    call

if __name__ == '__main__':
    eval(call)

if __name__ == '__main__':
    int_list_grammar = list_grammar(int_grammar)
    fuzzer = ProbabilisticGeneratorGrammarFuzzer(int_list_grammar)
    [fuzzer.fuzz() for i in range(5)]

if __name__ == '__main__':
    some_list = eval(fuzzer.fuzz())

if __name__ == '__main__':
    some_list

if __name__ == '__main__':
    len(some_list)

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



### Exercise 1: Deep Arguments

if __name__ == '__main__':
    print('\n### Exercise 1: Deep Arguments')



### Exercise 2: Covering Argument Combinations

if __name__ == '__main__':
    print('\n### Exercise 2: Covering Argument Combinations')



### Exercise 3: Mutating Arguments

if __name__ == '__main__':
    print('\n### Exercise 3: Mutating Arguments')


