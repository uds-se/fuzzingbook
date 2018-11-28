#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/APIFuzzer.html
# Last change: 2018-11-26 01:08:49-08:00
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


# # Fuzzing APIs

if __name__ == "__main__":
    print('# Fuzzing APIs')




# ## Fuzzing a Function

if __name__ == "__main__":
    print('\n## Fuzzing a Function')




# ### Testing a URL Parser

if __name__ == "__main__":
    print('\n### Testing a URL Parser')




import fuzzingbook_utils

from urllib.parse import urlparse

if __name__ == "__main__":
    urlparse('https://www.fuzzingbook.com/html/APIFuzzer.html')


if __package__ is None or __package__ == "":
    from Grammars import URL_GRAMMAR, is_valid_grammar, START_SYMBOL, new_symbol
else:
    from .Grammars import URL_GRAMMAR, is_valid_grammar, START_SYMBOL, new_symbol

from GrammarFuzzer import GrammarFuzzer, display_tree, all_terminals

if __name__ == "__main__":
    url_fuzzer = GrammarFuzzer(URL_GRAMMAR)


if __name__ == "__main__":
    for i in range(10):
        url = url_fuzzer.fuzz()
        print(urlparse(url))


# ### Synthesizing Code

if __name__ == "__main__":
    print('\n### Synthesizing Code')




if __name__ == "__main__":
    call = "urlparse('http://www.example.com/')"


if __name__ == "__main__":
    eval(call)


URLPARSE_GRAMMAR = {
    "<call>":
        ['urlparse("<url>")']
}

if __name__ == "__main__":
    URLPARSE_GRAMMAR.update(URL_GRAMMAR)


if __name__ == "__main__":
    URLPARSE_GRAMMAR["<start>"] = ["<call>"]


if __name__ == "__main__":
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


# ## Mining API Grammars

if __name__ == "__main__":
    print('\n## Mining API Grammars')




# ### From Calls to Grammars

if __name__ == "__main__":
    print('\n### From Calls to Grammars')




import math

def power(x, y):
    return math.pow(x, y)

if __package__ is None or __package__ == "":
    from Carver import CallCarver, call_value, call_string
else:
    from .Carver import CallCarver, call_value, call_string


if __name__ == "__main__":
    with CallCarver() as power_carver:
        z = power(1, 2)
        z = power(3, 4)


if __name__ == "__main__":
    power_carver.arguments("power")


POWER_GRAMMAR = {
    "<start>": ["power(<x>, <y>)"],
    "<x>": ["1", "3"],
    "<y>": ["2", "4"]
}

if __name__ == "__main__":
    assert is_valid_grammar(POWER_GRAMMAR)


if __package__ is None or __package__ == "":
    from GrammarCoverageFuzzer import GrammarCoverageFuzzer
else:
    from .GrammarCoverageFuzzer import GrammarCoverageFuzzer


if __name__ == "__main__":
    power_fuzzer = GrammarCoverageFuzzer(POWER_GRAMMAR)
    [power_fuzzer.fuzz() for i in range(5)]


# ### A Grammar Miner for Calls

if __name__ == "__main__":
    print('\n### A Grammar Miner for Calls')




class CallGrammarMiner(object):
    def __init__(self, carver, log=False):
        self.carver = carver
        self.log = log

# #### Initial Grammar

if __name__ == "__main__":
    print('\n#### Initial Grammar')




import copy 

class CallGrammarMiner(CallGrammarMiner):
    CALL_SYMBOL = "<call>"

    def initial_grammar(self):
        return copy.deepcopy(
            {START_SYMBOL: [self.CALL_SYMBOL],
                self.CALL_SYMBOL: []
             })

if __name__ == "__main__":
    m = CallGrammarMiner(power_carver)
    initial_grammar = m.initial_grammar()
    initial_grammar


# #### A Grammar from Arguments

if __name__ == "__main__":
    print('\n#### A Grammar from Arguments')




if __name__ == "__main__":
    arguments = power_carver.arguments("power")
    arguments


class CallGrammarMiner(CallGrammarMiner):
    def var_symbol(self, function_name, var, grammar):
        return new_symbol(grammar, "<" + function_name + "-" + var + ">")

    def mine_arguments_grammar(self, function_name, arguments, grammar):
        var_grammar = {}

        variables = {}
        for argument_list in arguments:
            for (var, value) in argument_list:
                value_string = call_value(value)
                if self.log:
                    print(var, "=", value_string)

                if value_string.find("<") >= 0:
                    var_grammar["<langle>"] = ["<"]
                    value_string = value_string.replace("<", "<langle>")

                if var not in variables:
                    variables[var] = set()
                variables[var].add(value_string)

        var_symbols = []
        for var in variables:
            var_symbol = self.var_symbol(function_name, var, grammar)
            var_symbols.append(var_symbol)
            var_grammar[var_symbol] = list(variables[var])

        return var_grammar, var_symbols

if __name__ == "__main__":
    m = CallGrammarMiner(power_carver)
    var_grammar, var_symbols = m.mine_arguments_grammar(
        "power", arguments, initial_grammar)


if __name__ == "__main__":
    var_grammar


if __name__ == "__main__":
    var_symbols


# #### A Grammar from Calls

if __name__ == "__main__":
    print('\n#### A Grammar from Calls')




class CallGrammarMiner(CallGrammarMiner):
    def function_symbol(self, function_name, grammar):
        return new_symbol(grammar, "<" + function_name + ">")

    def mine_function_grammar(self, function_name, grammar):
        arguments = self.carver.arguments(function_name)

        if self.log:
            print(function_name, arguments)

        var_grammar, var_symbols = self.mine_arguments_grammar(
            function_name, arguments, grammar)

        function_grammar = var_grammar
        function_symbol = self.function_symbol(function_name, grammar)

        if len(var_symbols) > 0 and var_symbols[0].find("-self") >= 0:
            # Method call
            function_grammar[function_symbol] = [
                var_symbols[0] + "." + function_name + "(" + ", ".join(var_symbols[1:]) + ")"]
        else:
            function_grammar[function_symbol] = [
                function_name + "(" + ", ".join(var_symbols) + ")"]

        if self.log:
            print(function_symbol, "::=", function_grammar[function_symbol])

        return function_grammar, function_symbol

if __name__ == "__main__":
    m = CallGrammarMiner(power_carver)
    function_grammar, function_symbol = m.mine_function_grammar(
        "power", initial_grammar)
    function_grammar


if __name__ == "__main__":
    function_symbol


# #### A Grammar from all Calls

if __name__ == "__main__":
    print('\n#### A Grammar from all Calls')




if __name__ == "__main__":
    power_carver.called_functions()


class CallGrammarMiner(CallGrammarMiner):
    def mine_call_grammar(self, function_list=None, qualified=False):
        grammar = self.initial_grammar()
        fn_list = function_list
        if function_list is None:
            fn_list = self.carver.called_functions(qualified=qualified)

        for function_name in fn_list:
            if function_list is None and (function_name.startswith("_") or function_name.startswith("<")):
                continue  # Internal function

            # Ignore errors with mined functions
            try:
                function_grammar, function_symbol = self.mine_function_grammar(
                    function_name, grammar)
            except:
                if function_list is not None:
                    raise

            if function_symbol not in grammar[self.CALL_SYMBOL]:
                grammar[self.CALL_SYMBOL].append(function_symbol)
            grammar.update(function_grammar)

        assert is_valid_grammar(grammar)
        return grammar

if __name__ == "__main__":
    m = CallGrammarMiner(power_carver)
    power_grammar = m.mine_call_grammar()
    power_grammar


if __name__ == "__main__":
    power_fuzzer = GrammarCoverageFuzzer(power_grammar)
    [power_fuzzer.fuzz() for i in range(5)]


# ## Fuzzing Web Functions

if __name__ == "__main__":
    print('\n## Fuzzing Web Functions')




if __package__ is None or __package__ == "":
    from Carver import webbrowser
else:
    from .Carver import webbrowser


if __name__ == "__main__":
    with CallCarver() as webbrowser_carver:
        webbrowser("http://www.fuzzingbook.org")
        webbrowser("https://www.example.com")


if __name__ == "__main__":
    m = CallGrammarMiner(webbrowser_carver)
    webbrowser_grammar = m.mine_call_grammar()


if __name__ == "__main__":
    print(webbrowser_grammar['<call>'])


if __name__ == "__main__":
    webbrowser_grammar["<urlsplit>"]


if __name__ == "__main__":
    webbrowser_grammar["<urlsplit-url>"]


if __name__ == "__main__":
    webbrowser_grammar["<urlsplit-scheme>"]


if __name__ == "__main__":
    urlsplit_fuzzer = GrammarCoverageFuzzer(
        webbrowser_grammar, start_symbol="<urlsplit>")
    for i in range(5):
        print(urlsplit_fuzzer.fuzz())


from urllib.parse import urlsplit

if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


if __name__ == "__main__":
    with Timer() as urlsplit_timer:
        urlsplit('http://www.fuzzingbook.org/', 'http', True)
    urlsplit_timer.elapsed_time()


if __name__ == "__main__":
    with Timer() as webbrowser_timer:
        webbrowser("http://www.fuzzingbook.org")
    webbrowser_timer.elapsed_time()


if __name__ == "__main__":
    webbrowser_timer.elapsed_time() / urlsplit_timer.elapsed_time()


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




# ### Exercise 1: Covering Argument Combinations

if __name__ == "__main__":
    print('\n### Exercise 1: Covering Argument Combinations')




# ### Exercise 2: Mutating Arguments

if __name__ == "__main__":
    print('\n### Exercise 2: Mutating Arguments')




# ### Exercise 3: Abstracting Arguments

if __name__ == "__main__":
    print('\n### Exercise 3: Abstracting Arguments')



