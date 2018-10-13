#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/OptionFuzzer.html
# Last change: 2018-10-12 10:00:49+02:00
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


# # Combinatorial Fuzzing

if __name__ == "__main__":
    print('# Combinatorial Fuzzing')




# ## Configuration Options

if __name__ == "__main__":
    print('\n## Configuration Options')




# import fuzzingbook_utils

import argparse

def process_numbers(args=[]):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum,
                        help='sum the integers')
    group.add_argument('--min', dest='accumulate', action='store_const',
                        const=min,
                        help='compute the minimum')
    group.add_argument('--max', dest='accumulate', action='store_const',
                        const=max,
                        help='compute the maximum')

    args = parser.parse_args(args)
    print(args.accumulate(args.integers))

if __name__ == "__main__":
    process_numbers(["--min", "100", "200", "300"])


if __name__ == "__main__":
    process_numbers(["--sum", '1', '2', '3'])


if __package__ is None or __package__ == "":
    from Grammars import crange, srange, convert_ebnf_grammar, is_valid_grammar, START_SYMBOL
else:
    from .Grammars import crange, srange, convert_ebnf_grammar, is_valid_grammar, START_SYMBOL


PROCESS_NUMBERS_GRAMMAR_EBNF = {
    "<start>": ["<operator> <integers>"],
    "<operator>": ["--sum", "--min", "--max"],
    "<integers>": ["<integer>", "<integers> <integer>"],
    "<integer>": ["<digit>+"],
    "<digit>": crange('0', '9')
}

assert is_valid_grammar(PROCESS_NUMBERS_GRAMMAR_EBNF)

PROCESS_NUMBERS_GRAMMAR = convert_ebnf_grammar(PROCESS_NUMBERS_GRAMMAR_EBNF)

if __package__ is None or __package__ == "":
    from GrammarCoverageFuzzer import GrammarCoverageFuzzer
else:
    from .GrammarCoverageFuzzer import GrammarCoverageFuzzer


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(PROCESS_NUMBERS_GRAMMAR, min_nonterminals=10)
    for i in range(3):
        print(f.fuzz())


# ## Mining Options

if __name__ == "__main__":
    print('\n## Mining Options')




import sys

import string

class ParseInterrupt(Exception):
    pass

class OptionGrammarMiner(object):
    def __init__(self, function, log=False):
        self.function = function    # FIXME: Should this be a runner?
        self.log = log

class OptionGrammarMiner(OptionGrammarMiner):
    OPTION_SYMBOL   = "<options>" 
    ARGUMENT_SYMBOL = "<arguments>" 
    def mine_ebnf(self):
        self.grammar = { 
            START_SYMBOL: [self.OPTION_SYMBOL + self.ARGUMENT_SYMBOL],
            self.OPTION_SYMBOL: [""], 
            self.ARGUMENT_SYMBOL: [""]
        }
        assert is_valid_grammar(self.grammar)
        
        old_trace = sys.settrace(self.traceit)
        try:
            self.function()
        except ParseInterrupt:
            pass
        sys.settrace(old_trace)
        
        return self.grammar
    
    def mine(self):
        return convert_ebnf_grammar(self.mine_ebnf())

class OptionGrammarMiner(OptionGrammarMiner):
    def traceit(self, frame, event, arg):
        if event != "call":
            return

        if "self" not in frame.f_locals:
            return
        self_var = frame.f_locals["self"]

        method_name = frame.f_code.co_name
        if method_name == "add_argument":
            self.process_argument(frame.f_locals)

        if method_name == "parse_args":
            raise ParseInterrupt

        return None

class OptionGrammarMiner(OptionGrammarMiner):
    def process_argument(self, locals):
        args = locals["args"]
        kwargs = locals["kwargs"]

        if self.log:
            print(args)
            print(kwargs)
            print()

        for arg in args:
            if arg.startswith('-'):
                target = self.OPTION_SYMBOL
                metavar = None
                arg = " " + arg
            else:
                target = self.ARGUMENT_SYMBOL
                metavar = arg
                arg = ""

            if "nargs" in kwargs:
                nargs = kwargs["nargs"]
            else:
                nargs = 1
            
            if "action" in kwargs:
                # No argument
                param = ""
                nargs = 0
            else:
                if "type" in kwargs and issubclass(kwargs["type"], int):
                    type_ = "int"
                else:
                    type_ = "str"

                if metavar is None and "metavar" in kwargs:
                    metavar = kwargs["metavar"]
                    
                if metavar is not None:
                    self.grammar["<" + metavar + ">"] = ["<" + type_ + ">"]
                else:
                    metavar = type_
                    
                if type_ == "int":
                    self.grammar["<int>"] = ["(-)?<digit>+"]
                    self.grammar["<digit>"] = crange('0', '9')
                    param = " <" + metavar + ">"
                else:
                    self.grammar["<str>"] = ["<char>+"]
                    self.grammar["<char>"] = srange(string.digits + string.ascii_letters + string.punctuation)
                    param = " <" + metavar + ">"

            if isinstance(nargs, int):
                for i in range(nargs):
                    arg += param
            else:
                assert nargs in "?+*"
                arg += '(' + param + ')' + nargs
                    
            if target == self.OPTION_SYMBOL:
                self.grammar[target][0] += '(' + arg + ')?'
            else:
                self.grammar[target][0] += arg

if __name__ == "__main__":
    om = OptionGrammarMiner(process_numbers, log=True)
    grammar_ebnf = om.mine_ebnf()
    assert is_valid_grammar(grammar_ebnf)
    grammar_ebnf


if __name__ == "__main__":
    grammar = convert_ebnf_grammar(grammar_ebnf)
    assert is_valid_grammar(grammar)


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(grammar)
    for i in range(10):
        print(f.fuzz())


# ## Complex Args

if __name__ == "__main__":
    print('\n## Complex Args')




if __name__ == "__main__":
    import os
    os.system(r'autopep8 --help')


import autopep8

if __name__ == "__main__":
    om = OptionGrammarMiner(autopep8.main, log=True)
    grammar_ebnf = om.mine_ebnf()
    grammar_ebnf


if __name__ == "__main__":
    grammar = convert_ebnf_grammar(grammar_ebnf)
    assert is_valid_grammar(grammar)


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(grammar, max_nonterminals=40)
    for i in range(10):
        print(f.fuzz())


# ## _Section 2_

if __name__ == "__main__":
    print('\n## _Section 2_')




# ## _Section 3_

if __name__ == "__main__":
    print('\n## _Section 3_')




# import fuzzingbook_utils

if __name__ == "__main__":
    # More code
    pass


if __name__ == "__main__":
    # Even more code
    pass


# ## _Section 4_

if __name__ == "__main__":
    print('\n## _Section 4_')




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



