#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/APIFuzzer.html
# Last change: 2018-10-30 13:41:25+01:00
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




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


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
    from Grammars import URL_GRAMMAR, is_valid_grammar
else:
    from .Grammars import URL_GRAMMAR, is_valid_grammar

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


# ## Carving Function Calls

if __name__ == "__main__":
    print('\n## Carving Function Calls')




from urllib.parse import *

if __name__ == "__main__":
    # return function_name(arg[0], arg[1], ...) as a string
    def call_with_args(function_name, args):
        return function_name + "(" + \
            ", ".join([var + "=" + repr(value) for (var, value) in args]) + ")"


if __name__ == "__main__":
    call_with_args("urlparse", [("url", "http://example.com")])


if __name__ == "__main__":
    # This is where we store all calls and arguments
    the_args = {}


if __name__ == "__main__":
    # Tracking function: Record all calls and all args
    def traceit(frame, event, arg):
        if event == "call":
            code = frame.f_code
            function_name = code.co_name

            if function_name.startswith('_'):
                return None # Internal function

            # When called, all arguments are local variables
            variables = frame.f_locals.keys()
            args = [(var, frame.f_locals[var]) for var in variables]

            if function_name not in the_args:
                the_args[function_name] = []
            if args not in the_args[function_name]:
                the_args[function_name].append(args)

            # Some tracking
            # print(call_with_args(function_name, args))

        # If we return None, this will only be called for functions (more efficient)
        return None


import math
import sys

if __name__ == "__main__":
    # Record all function calls during an execution
    def power(x, y):
        return math.pow(x, y)

    def powerpair(pair):
        return power(pair[0], pair[1])

    def record_calls():
        global the_args
        the_args = {}

        urls = [
            "https://andreas:zeller@cispa.saarland:8080/faculty/q?=zeller",
            "http://fuzzingbook.com/fuzzing",
            "http://google.com/query",
            "http://microsoft.com/windows",
            "https://mark:zuckerberg@facebook.com:666/friends"
        ]

        sys.settrace(traceit)

        for n in range(0, 10):
            x = power(n, n)
            x = powerpair((n, n))

        for url in urls:
            parts = urlparse(url)
            url = urlunparse(parts)

        sys.settrace(None)


if __name__ == "__main__":
    record_calls()


if __name__ == "__main__":
    the_args


if __name__ == "__main__":
    # Re-run all calls seen, invoking functions directly
    def run_calls():
        for function_name in the_args.keys():
            if function_name.startswith("_") or function_name.startswith("<"):
                continue        # Internal call

            for args in the_args[function_name]:
                call_string = call_with_args(function_name, args)
                do_call(call_string)


if __name__ == "__main__":
    run_calls()


# ## Mining a Grammar

if __name__ == "__main__":
    print('\n## Mining a Grammar')




if __name__ == "__main__":
    # Convert a variable name into a grammar nonterminal
    def nonterminal(var):
        return "<" + var.lower() + ">"


def mine_grammar_from_calls():
    all_calls = "<call>"
    grammar = {
        "<start>": [all_calls],
    }
    
    function_nonterminals = []
    for function_name in the_args.keys():
        if function_name.startswith("_") or function_name.startswith("<"):
            # Internal function
            continue
        
        nonterminal_name = nonterminal(function_name)
        function_nonterminals.append(nonterminal_name)
        
        # Add a rule for the function
        expansion = function_name + "("
        first_arg = True
        for (var, _) in the_args[function_name][0]:
            arg_name = nonterminal(function_name + "_" + var)
            if not first_arg:
                expansion += ", "
            first_arg = False
            expansion += var + "=" + arg_name
        expansion += ")"
        # TODO: Handle polymorphic functions
        grammar[nonterminal_name] = [expansion]

        # Add rules for the arguments
        values = {}
        for args in the_args[function_name]:
            for (var, value) in args:
                if var not in values:
                    values[var] = []
                if value not in values[var]:
                    values[var].append(value)
        g = value_rules(values, function_name)
        grammrs = merge_grammars(grammar, g)
        
    # Add a rule for all calls
    grammar[all_calls] = function_nonterminals
            
    return grammar

if __name__ == "__main__":
    # Merge two grammars G1 and G2
    def merge_grammars(g1, g2):
        merged_grammar = g1
        for key2 in g2.keys():
            repl2 = g2[key2]
            key_found = False
            for key1 in g1.keys():
                repl1 = g1[key1]
                for repl in repl2:
                    if key1 == key2:
                        key_found = True
                        if repl not in repl1:
                            # Extend existing rule
                            merged_grammar[key1] = repl1 + [repl]

            if not key_found:
                # Add new rule
                merged_grammar[key2] = repl2
        return merged_grammar


DEEP_VALUES = False

if __name__ == "__main__":
    # Return a grammar only for the values in VALUES
    def value_rules(values, prefix):
        grammar = {}
        for var in values.keys():
            arg_name = nonterminal(prefix + "_" + var)
            if DEEP_VALUES:
                for value in values[var]:
                    g = deep_value_expansions(arg_name, value)
                    grammar = merge_grammars(grammar, g)
            else:
                expansions = [repr(value) for value in values[var]]
                grammar[arg_name] = expansions

        return grammar


if __name__ == "__main__":
    api_grammar = mine_grammar_from_calls()


if __name__ == "__main__":
    api_grammar


if __name__ == "__main__":
    urlunsplit_fuzzer = GrammarFuzzer(api_grammar, start_symbol='<urlunsplit>')


if __name__ == "__main__":
    for i in range(10):
        do_call(urlunsplit_fuzzer.fuzz())


if __name__ == "__main__":
    urlunparse_fuzzer = GrammarFuzzer(api_grammar, start_symbol='<urlunparse>')


if __name__ == "__main__":
    for i in range(10):
        do_call(urlunparse_fuzzer.fuzz())


# ## Deep Values

if __name__ == "__main__":
    print('\n## Deep Values')




if __name__ == "__main__":
    # Expand a structured value into individual grammar rules       
    def deep_value_expansions(prefix, value):
        # print("Expanding", prefix, "=", repr(value))

        grammar = {}

        attributes = value_attributes(value)
        if attributes is not None:
            # A class or named tuple
            attr_names = []
            for attribute in attributes:
                if attribute.startswith("_"):
                    # Internal attribute
                    continue
                attr_name = prefix + "_" + attribute.upper()
                attr_names.append((attribute, attr_name))
                g = deep_value_expansions(attr_name, getattr(value, attribute))
                grammar = merge_grammars(grammar, g)

            expansion = value.__class__.__name__ + "("
            first_attribute = True
            for (attribute, attr_name) in attr_names:
                if not first_attribute:
                    expansion += ", "
                first_attribute = False
                expansion += attribute + " = " + attr_name
            expansion += ")"
            grammar[prefix] = [expansion]

        elif isinstance(value, type(())):
            # A tuple
            field_names = []
            for index in range(0, len(value)):
                field_name = prefix + "_" + repr(index)
                field_names.append(field_name)
                g = deep_value_expansions(field_name, value[index])
                grammar = merge_grammars(grammar, g)

            grammar[prefix] = ["(" + ", ".join(field_names) + ")"]

        else:
            # Can only expand to value
            grammar[prefix] = [repr(value)]

        # print("Expanded:", grammar_to_string(grammar))
        return grammar



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




# ### Exercise 1: Synthesizing Oracles

if __name__ == "__main__":
    print('\n### Exercise 1: Synthesizing Oracles')




if __name__ == "__main__":
    result = urlparse("https://www.fuzzingbook.org")
    assert result.scheme == "https"
    assert result.netloc == "www.fuzzingbook.org"


if __name__ == "__main__":
    urlparse_fuzzer = GrammarFuzzer(URLPARSE_GRAMMAR)
    call = urlparse_fuzzer.fuzz()
    call


if __name__ == "__main__":
    call_tree = urlparse_fuzzer.derivation_tree
    display_tree(call_tree)


def get_element(tree, name):
    """Return definition of `name` in `tree` as a string"""
    (symbol, children) = tree
    if symbol == name:
        return all_terminals(tree)
    for c in children:
        result = get_element(c, name)
        if result is not None:
            return result
    return None # Not Found

if __name__ == "__main__":
    get_element(call_tree, "<scheme>")


if __name__ == "__main__":
    get_element(call_tree, "<host>")


if __name__ == "__main__":
    test = ""
    for i in range(10):
        call = urlparse_fuzzer.fuzz()
        tree = urlparse_fuzzer.derivation_tree
        test += "result = " + call + "\n"
        test += "assert result.scheme == " + repr(get_element(tree, "<scheme>")) + "\n"
    print(test)


if __name__ == "__main__":
    exec(test)


# ### Exercise 2: _Title_

if __name__ == "__main__":
    print('\n### Exercise 2: _Title_')



