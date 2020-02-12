#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "The Fuzzing Book".
# Web site: https://www.fuzzingbook.org/html/APIFuzzer.html
# Last change: 2019-12-17 16:45:28+01:00
#
#!/
# Copyright (c) 2018-2020 CISPA, Saarland University, authors, and contributors
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


# # Fuzzing APIs

if __name__ == "__main__":
    print('# Fuzzing APIs')




# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




# ## Fuzzing a Function

if __name__ == "__main__":
    print('\n## Fuzzing a Function')




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


from urllib.parse import urlparse

if __name__ == "__main__":
    urlparse('https://www.fuzzingbook.com/html/APIFuzzer.html')


if __package__ is None or __package__ == "":
    from Grammars import URL_GRAMMAR, is_valid_grammar, START_SYMBOL, new_symbol, opts, extend_grammar
else:
    from .Grammars import URL_GRAMMAR, is_valid_grammar, START_SYMBOL, new_symbol, opts, extend_grammar

if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer, display_tree, all_terminals
else:
    from .GrammarFuzzer import GrammarFuzzer, display_tree, all_terminals


if __name__ == "__main__":
    url_fuzzer = GrammarFuzzer(URL_GRAMMAR)


if __name__ == "__main__":
    for i in range(10):
        url = url_fuzzer.fuzz()
        print(urlparse(url))


# ## Synthesizing Code

if __name__ == "__main__":
    print('\n## Synthesizing Code')




if __name__ == "__main__":
    call = "urlparse('http://www.example.com/')"


if __name__ == "__main__":
    eval(call)


URLPARSE_GRAMMAR = {
    "<call>":
        ['urlparse("<url>")']
}

# Import definitions from URL_GRAMMAR
URLPARSE_GRAMMAR.update(URL_GRAMMAR)
URLPARSE_GRAMMAR["<start>"] = ["<call>"]

assert is_valid_grammar(URLPARSE_GRAMMAR)

if __name__ == "__main__":
    URLPARSE_GRAMMAR


if __name__ == "__main__":
    urlparse_fuzzer = GrammarFuzzer(URLPARSE_GRAMMAR)
    urlparse_fuzzer.fuzz()


if __name__ == "__main__":
    # Call function_name(arg[0], arg[1], ...) as a string
    def do_call(call_string):
        print(call_string)
        result = eval(call_string)
        print("\t= " + repr(result))
        return result


if __name__ == "__main__":
    call = urlparse_fuzzer.fuzz()
    do_call(call)


URLPARSE_C_GRAMMAR = {
    "<cfile>": ["<cheader><cfunction>"],
    "<cheader>": ['#include "urlparse.h"\n\n'],
    "<cfunction>": ["void test() {\n<calls>}\n"],
    "<calls>": ["<call>", "<calls><call>"],
    "<call>": ['    urlparse("<url>");\n']
}

if __name__ == "__main__":
    URLPARSE_C_GRAMMAR.update(URL_GRAMMAR)


if __name__ == "__main__":
    URLPARSE_C_GRAMMAR["<start>"] = ["<cfile>"]


if __name__ == "__main__":
    assert is_valid_grammar(URLPARSE_C_GRAMMAR)


if __name__ == "__main__":
    urlparse_fuzzer = GrammarFuzzer(URLPARSE_C_GRAMMAR)
    print(urlparse_fuzzer.fuzz())


# ## Synthesizing Oracles

if __name__ == "__main__":
    print('\n## Synthesizing Oracles')




if __package__ is None or __package__ == "":
    from GeneratorGrammarFuzzer import GeneratorGrammarFuzzer, ProbabilisticGeneratorGrammarFuzzer
else:
    from .GeneratorGrammarFuzzer import GeneratorGrammarFuzzer, ProbabilisticGeneratorGrammarFuzzer


URLPARSE_ORACLE_GRAMMAR = extend_grammar(URLPARSE_GRAMMAR,
{
     "<call>": [("assert urlparse('<url>').geturl() == '<url>'",
                 opts(post=lambda url_1, url_2: [None, url_1]))]
})

if __name__ == "__main__":
    urlparse_oracle_fuzzer = GeneratorGrammarFuzzer(URLPARSE_ORACLE_GRAMMAR)
    test = urlparse_oracle_fuzzer.fuzz()
    print(test)


if __name__ == "__main__":
    exec(test)


URLPARSE_ORACLE_GRAMMAR = extend_grammar(URLPARSE_GRAMMAR,
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

if __name__ == "__main__":
    urlparse_oracle_fuzzer = GeneratorGrammarFuzzer(URLPARSE_ORACLE_GRAMMAR)
    test = urlparse_oracle_fuzzer.fuzz()
    print(test)


if __name__ == "__main__":
    exec(test)


def fuzzed_url_element(symbol):
    return GrammarFuzzer(URLPARSE_GRAMMAR, start_symbol=symbol).fuzz()

if __name__ == "__main__":
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


# ## Synthesizing Data

if __name__ == "__main__":
    print('\n## Synthesizing Data')




# ### Integers

if __name__ == "__main__":
    print('\n### Integers')




if __package__ is None or __package__ == "":
    from Grammars import convert_ebnf_grammar, crange
else:
    from .Grammars import convert_ebnf_grammar, crange


if __package__ is None or __package__ == "":
    from ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer
else:
    from .ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer


INT_EBNF_GRAMMAR = {
    "<start>": ["<int>"],
    "<int>": ["<_int>"],
    "<_int>": ["(-)?<leaddigit><digit>*", "0"],
    "<leaddigit>": crange('1', '9'),
    "<digit>": crange('0', '9')
}

assert is_valid_grammar(INT_EBNF_GRAMMAR)

INT_GRAMMAR = convert_ebnf_grammar(INT_EBNF_GRAMMAR)
INT_GRAMMAR

if __name__ == "__main__":
    int_fuzzer = GrammarFuzzer(INT_GRAMMAR)
    print([int_fuzzer.fuzz() for i in range(10)])


if __package__ is None or __package__ == "":
    from Grammars import set_opts
else:
    from .Grammars import set_opts


import random

def int_grammar_with_range(start, end):
    int_grammar = extend_grammar(INT_GRAMMAR)
    set_opts(int_grammar, "<int>", "<_int>",
        opts(pre=lambda: random.randint(start, end)))
    return int_grammar

if __name__ == "__main__":
    int_fuzzer = GeneratorGrammarFuzzer(int_grammar_with_range(900, 1000))
    [int_fuzzer.fuzz() for i in range(10)]


# ### Floats

if __name__ == "__main__":
    print('\n### Floats')




FLOAT_EBNF_GRAMMAR = {
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

if __name__ == "__main__":
    float_fuzzer = ProbabilisticGrammarFuzzer(FLOAT_GRAMMAR)
    print([float_fuzzer.fuzz() for i in range(10)])


def float_grammar_with_range(start, end):
    float_grammar = extend_grammar(FLOAT_GRAMMAR)
    set_opts(float_grammar, "<float>", "<_float>", opts(
        pre=lambda: start + random.random() * (end - start)))
    return float_grammar

if __name__ == "__main__":
    float_fuzzer = ProbabilisticGeneratorGrammarFuzzer(
        float_grammar_with_range(900.0, 900.9))
    [float_fuzzer.fuzz() for i in range(10)]


# ### Strings

if __name__ == "__main__":
    print('\n### Strings')




ASCII_STRING_EBNF_GRAMMAR = {
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

if __name__ == "__main__":
    string_fuzzer = ProbabilisticGrammarFuzzer(ASCII_STRING_GRAMMAR)
    print([string_fuzzer.fuzz() for i in range(10)])


# ## Synthesizing Composite Data

if __name__ == "__main__":
    print('\n## Synthesizing Composite Data')




# ### Lists

if __name__ == "__main__":
    print('\n### Lists')




LIST_EBNF_GRAMMAR = {
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

if __name__ == "__main__":
    int_list_fuzzer = ProbabilisticGrammarFuzzer(list_grammar(INT_GRAMMAR))
    [int_list_fuzzer.fuzz() for i in range(10)]


if __name__ == "__main__":
    string_list_fuzzer = ProbabilisticGrammarFuzzer(
        list_grammar(ASCII_STRING_GRAMMAR))
    [string_list_fuzzer.fuzz() for i in range(10)]


if __name__ == "__main__":
    float_list_fuzzer = ProbabilisticGeneratorGrammarFuzzer(list_grammar(
        float_grammar_with_range(900.0, 900.9)))
    [float_list_fuzzer.fuzz() for i in range(10)]


# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




if __package__ is None or __package__ == "":
    from GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer
else:
    from .GeneratorGrammarFuzzer import ProbabilisticGeneratorGrammarFuzzer


if __name__ == "__main__":
    int_grammar = int_grammar_with_range(100, 200)
    fuzzer = ProbabilisticGeneratorGrammarFuzzer(int_grammar)
    [fuzzer.fuzz() for i in range(10)]


from math import sqrt

if __name__ == "__main__":
    eval("sqrt(" + fuzzer.fuzz() + ")")


if __name__ == "__main__":
    int_list_grammar = list_grammar(int_grammar)
    fuzzer = ProbabilisticGeneratorGrammarFuzzer(int_list_grammar)
    [fuzzer.fuzz() for i in range(5)]


if __name__ == "__main__":
    eval("len(" + fuzzer.fuzz() + ")")


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




# ### Exercise 1: Deep Arguments

if __name__ == "__main__":
    print('\n### Exercise 1: Deep Arguments')




# ### Exercise 2: Covering Argument Combinations

if __name__ == "__main__":
    print('\n### Exercise 2: Covering Argument Combinations')




# ### Exercise 3: Mutating Arguments

if __name__ == "__main__":
    print('\n### Exercise 3: Mutating Arguments')



