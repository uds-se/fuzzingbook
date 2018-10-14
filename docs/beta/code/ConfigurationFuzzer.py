#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/ConfigurationFuzzer.html
# Last change: 2018-10-14 23:12:59+02:00
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


# # Fuzzing Configurations

if __name__ == "__main__":
    print('# Fuzzing Configurations')




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


# ## A Grammar for Configurations

if __name__ == "__main__":
    print('\n## A Grammar for Configurations')




if __package__ is None or __package__ == "":
    from Grammars import crange, srange, convert_ebnf_grammar, is_valid_grammar, START_SYMBOL, new_symbol
else:
    from .Grammars import crange, srange, convert_ebnf_grammar, is_valid_grammar, START_SYMBOL, new_symbol


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


# ## Mining Configuration Options

if __name__ == "__main__":
    print('\n## Mining Configuration Options')




import sys

import string

class ParseInterrupt(Exception):
    pass

class ConfigurationGrammarMiner(object):
    def __init__(self, function, log=False):
        self.function = function    # FIXME: Should this be a runner?
        self.log = log

class ConfigurationGrammarMiner(ConfigurationGrammarMiner):
    OPTION_SYMBOL = "<option>"
    ARGUMENTS_SYMBOL = "<arguments>" 
    def mine_ebnf_grammar(self):
        self.grammar = { 
            START_SYMBOL: [ "(" + self.OPTION_SYMBOL + ")*" + self.ARGUMENTS_SYMBOL],
            self.OPTION_SYMBOL: [], 
            self.ARGUMENTS_SYMBOL: []
        }
        self.current_group = self.OPTION_SYMBOL

        old_trace = sys.settrace(self.traceit)
        try:
            self.function()
        except ParseInterrupt:
            pass
        sys.settrace(old_trace)
        
        return self.grammar
    
    def mine_grammar(self):
        return convert_ebnf_grammar(self.mine_ebnf_grammar())

class ConfigurationGrammarMiner(ConfigurationGrammarMiner):
    def traceit(self, frame, event, arg):
        if event != "call":
            return

        if "self" not in frame.f_locals:
            return
        self_var = frame.f_locals["self"]

        method_name = frame.f_code.co_name

        if method_name == "add_argument":
            in_group = repr(type(self_var)).find("Group") >= 0
            self.process_argument(frame.f_locals, in_group)
            
        if method_name == "add_mutually_exclusive_group":
            self.add_group(frame.f_locals, exclusive=True)

        if method_name == "add_argument_group":
            # self.add_group(frame.f_locals, exclusive=False)
            pass
    
        if method_name == "parse_args":
            raise ParseInterrupt

        return None

class ConfigurationGrammarMiner(ConfigurationGrammarMiner):
    def process_argument(self, locals, in_group):
        args = locals["args"]
        kwargs = locals["kwargs"]

        if self.log:
            print(args)
            print(kwargs)
            print()

        for arg in args:
            if arg.startswith('-'):
                if not in_group:
                    target = self.OPTION_SYMBOL
                else:
                    target = self.current_group
                metavar = None
                arg = " " + arg
            else:
                target = self.ARGUMENTS_SYMBOL
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
                if "type" in kwargs and isinstance(kwargs["type"], int):
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
                self.grammar[target].append(arg)
            else:
                self.grammar[target].append(arg)

class ConfigurationGrammarMiner(ConfigurationGrammarMiner):
    def add_group(self, locals, exclusive):
        kwargs = locals["kwargs"]
        if self.log:
            print(kwargs)

        required = kwargs.get("required", False)
        group = new_symbol(self.grammar, "<group>")

        if required and exclusive:
            group_expansion = group
        if required and not exclusive:
            group_expansion = group + "+"
        if not required and exclusive:
            group_expansion = group + "?"
        if not required and not exclusive:
            group_expansion = group + "*"

        self.grammar[START_SYMBOL][0] = group_expansion + self.grammar[START_SYMBOL][0]
        self.grammar[group] = []
        self.current_group = group

if __name__ == "__main__":
    miner = ConfigurationGrammarMiner(process_numbers, log=True)
    grammar_ebnf = miner.mine_ebnf_grammar()
    print(grammar_ebnf)


if __name__ == "__main__":
    assert is_valid_grammar(grammar_ebnf)


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


import os

def find_executable(name):
    for path in os.get_exec_path():
        qualified_name = os.path.join(path, name)
        if os.path.exists(qualified_name):
            return qualified_name
    return None

if __name__ == "__main__":
    find_executable("autopep8")


def autopep8():
    executable = find_executable("autopep8")
    first_line = open(executable).readline()
    assert first_line.find("python") >= 0
    contents = open(executable).read()
    exec(contents)

if __name__ == "__main__":
    miner = ConfigurationGrammarMiner(autopep8, log=True)


if __name__ == "__main__":
    grammar = miner.mine_ebnf_grammar()
    print(grammar["<option>"])


if __name__ == "__main__":
    grammar = convert_ebnf_grammar(grammar_ebnf)
    assert is_valid_grammar(grammar)
    print(grammar["<option>"])


if __name__ == "__main__":
    grammar["<arguments>"] = [" foo.py"]
    f = GrammarCoverageFuzzer(grammar, max_nonterminals=3)
    for i in range(20):
        print(f.fuzz())


def create_foo_py():
    open("foo.py", "w").write("""
def twice(x):
    return x+x
""")

if __name__ == "__main__":
    create_foo_py()


if __name__ == "__main__":
    print(open("foo.py").read())


if __package__ is None or __package__ == "":
    from Fuzzer import ProgramRunner
else:
    from .Fuzzer import ProgramRunner


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(grammar, max_nonterminals=5)
    for i in range(20):
        invocation = "autopep8" + f.fuzz()
        print("$ " + invocation)
        args = invocation.split()
        autopep8 = ProgramRunner(args)
        result, outcome = autopep8.run()
        if result.stderr != "":
            print(result.stderr, end="")


import os

if __name__ == "__main__":
    os.remove("foo.py")


# ## Putting it all Together

if __name__ == "__main__":
    print('\n## Putting it all Together')




class ConfigurationRunner(ProgramRunner):
    def __init__(self, program, arguments=None):
        if isinstance(program, str):
            self.base_executable = program
        else:
            self.base_executable = program[0]

        self.find_contents()
        self.find_grammar()
        if arguments is not None:
            self.set_arguments(arguments)
        super().__init__(program)

    def find_contents(self):
        self._executable = find_executable(self.base_executable)
        first_line = open(self._executable).readline()
        assert first_line.find("python") >= 0
        self.contents = open(self._executable).read()

    def invoker(self):
        exec(self.contents)
    
    def find_grammar(self):
        miner = ConfigurationGrammarMiner(self.invoker)
        self._grammar = miner.mine_grammar()

    def grammar(self):
        return self._grammar

    def executable(self):
        return self._executable

    def set_arguments(self, args):
        self._grammar["<arguments>"] = [" " + args]
        
    def set_invocation(self, program):
        self.program = program

if __name__ == "__main__":
    conf_runner = ConfigurationRunner("autopep8", "foo.py")


if __name__ == "__main__":
    conf_runner.grammar()["<option>"]


class ConfigurationFuzzer(GrammarCoverageFuzzer):
    def __init__(self, runner, *args, **kwargs):
        self.runner = runner
        grammar = runner.grammar()
        super().__init__(grammar, *args, **kwargs)

    def run(self, runner=None, inp=""):
        if runner is None:
            runner = self.runner
        invocation = runner.executable() + " " + self.fuzz()
        runner.set_invocation(invocation.split())
        return runner.run(inp)

if __name__ == "__main__":
    conf_fuzzer = ConfigurationFuzzer(conf_runner, max_nonterminals=5)


if __name__ == "__main__":
    conf_fuzzer.fuzz()


if __name__ == "__main__":
    conf_fuzzer.run(conf_runner)


# ## MyPy

if __name__ == "__main__":
    print('\n## MyPy')




if __name__ == "__main__":
    mypy = ConfigurationRunner("mypy", "foo.py")
    print(mypy.grammar()["<option>"])


if __name__ == "__main__":
    mypy_fuzzer = ConfigurationFuzzer(mypy, max_nonterminals=3)
    for i in range(10):
        print(mypy_fuzzer.fuzz())


if __name__ == "__main__":
    notedown = ConfigurationRunner("notedown")
    print(notedown.grammar()["<option>"])


if __name__ == "__main__":
    notedown_fuzzer = ConfigurationFuzzer(notedown, max_nonterminals=3)
    for i in range(10):
        print(notedown_fuzzer.fuzz())


# ## Combinatorial Testing

if __name__ == "__main__":
    print('\n## Combinatorial Testing')




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



