#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/GrammarMiner.html
# Last change: 2018-10-23 12:27:39+02:00
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


# # Mining Input Grammars

if __name__ == "__main__":
    print('# Mining Input Grammars')




# ## A Simple Grammar Miner

if __name__ == "__main__":
    print('\n## A Simple Grammar Miner')




# ### Function Under Test

if __name__ == "__main__":
    print('\n### Function Under Test')




from urllib.parse import urlparse

FUNCTION = urlparse
INPUTS = [
    'http://user:pass@www.google.com:80/?q=path#ref',
    'https://www.cispa.saarland:80/',
    'http://www.fuzzingbook.org/#News',
]

# ## Tracing Variable Values

if __name__ == "__main__":
    print('\n## Tracing Variable Values')




import sys

if __name__ == "__main__":
    # We store individual variable/value pairs here
    global the_values
    the_values = {}

    # The current input string
    global the_input
    the_input = None


if __name__ == "__main__":
    # We record all string variables and values occurring during execution
    def traceit(frame, event, arg):
        global the_values
        variables = frame.f_locals.keys()

        for var in variables:
            value = frame.f_locals[var]
            # print(var, value)

            # Save all non-trivial string values that also occur in the input
            if type(value) == type('') and len(value) >= 2 and value in the_input:
                the_values[var] = value

        return traceit


if __name__ == "__main__":
    # Trace function
    def trace_function(function, input):
        # We obtain a mapping of variables to values
        global the_input
        the_input = input

        global the_values
        the_values = {}

        sys.settrace(traceit)
        o = function(the_input)
        sys.settrace(None)

        return the_values


if __name__ == "__main__":
    values = trace_function(FUNCTION, INPUTS[0])
    for var in values.keys():
        print(var + " = " + repr(values[var]))
    print('')


# ### Extracting a Grammar

if __name__ == "__main__":
    print('\n### Extracting a Grammar')




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    from fuzzingbook_utils import set_fixed_seed
    set_fixed_seed.set_fixed_seed()



if __package__ is None or __package__ == "":
    from Grammars import START_SYMBOL
else:
    from .Grammars import START_SYMBOL


if __name__ == "__main__":
    # Convert a variable name into a grammar nonterminal
    def nonterminal(var):
        return "<" + var.lower() + ">"


if __name__ == "__main__":
    # Obtain a grammar for a specific input
    def get_grammar(function, input):
        # Here's our initial grammar
        grammar = {START_SYMBOL: [input]}

        # Trace execution
        values = trace_function(function, input)

        # Replace as listed above
        while True:
            new_rules = []
            for var in values:
                value = values[var]
                for key in grammar:
                    repl_alternatives = grammar[key]
                    for j in range(0, len(repl_alternatives)):
                        repl = repl_alternatives[j]
                        if value in repl:                    
                            # Replace value by nonterminal name
                            alt_key = nonterminal(var)
                            repl_alternatives[j] = repl.replace(value, alt_key)
                            new_rules = new_rules + [(var, alt_key, value)]

            if len(new_rules) == 0:
                break # Nothing to expand anymore

            for (var, alt_key, value) in new_rules:
                # Add new rule to grammar
                grammar[alt_key] = [value]

                # Do not expand this again
                del values[var]

        return grammar


if __name__ == "__main__":
    grammar = get_grammar(FUNCTION, INPUTS[0])
    grammar


if __name__ == "__main__":
    grammar = get_grammar(FUNCTION, INPUTS[1])
    grammar


if __name__ == "__main__":
    grammar = get_grammar(FUNCTION, INPUTS[2])
    grammar


# ### Merging Grammars

if __name__ == "__main__":
    print('\n### Merging Grammars')




def merge_grammars(g1, g2):
    merged_grammar = g1
    for key2 in g2:
        repl2 = g2[key2]
        key_found = False
        for key1 in g1:
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

def get_merged_grammar(function, inputs):
    merged_grammar = None
    for input in inputs:
        grammar = get_grammar(function, input)
        # print(repr(input) + " ->\n" + grammar_to_string(grammar))
        if merged_grammar is None:
            merged_grammar = grammar
        else:
            merged_grammar = merge_grammars(merged_grammar, grammar)

    return merged_grammar

if __name__ == "__main__":
    grammar = get_merged_grammar(FUNCTION, INPUTS)
    grammar


# ### Fuzzing

if __name__ == "__main__":
    print('\n### Fuzzing')




if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer
else:
    from .GrammarFuzzer import GrammarFuzzer


if __name__ == "__main__":
    f = GrammarFuzzer(grammar)
    for i in range(10):
        print(f.fuzz())


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




# ### Exercise 1: _Title_

if __name__ == "__main__":
    print('\n### Exercise 1: _Title_')




if __name__ == "__main__":
    # Some code that is part of the exercise
    pass


if __name__ == "__main__":
    # Some code for the solution
    2 + 2


# ### Exercise 2: _Title_

if __name__ == "__main__":
    print('\n### Exercise 2: _Title_')



