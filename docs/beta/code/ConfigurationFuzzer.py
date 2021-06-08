#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Testing Configurations" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/ConfigurationFuzzer.html
# Last change: 2021-06-04 14:57:19+02:00
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
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
The Fuzzing Book - Testing Configurations

This file can be _executed_ as a script, running all experiments:

    $ python ConfigurationFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.ConfigurationFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/ConfigurationFuzzer.html

This chapter provides two classes:

* `OptionRunner` automatically extract command-line options from a Python program;
* `OptionFuzzer` uses these to automatically test a Python program with a large variety of options.

`OptionRunner` runs a program up to the point where it parses its arguments, and then extracts a grammar that describes its invocations:

>>> autopep8_runner = OptionRunner("autopep8", "foo.py")

The grammar can be extracted via the method `ebnf_grammar()`:

>>> option_ebnf_grammar = autopep8_runner.ebnf_grammar()
>>> print(option_ebnf_grammar)
{'': ['()*'], '': [' -h', ' --help', ' --version', ' -v', ' --verbose', ' -d', ' --diff', ' -i', ' --in-place', ' --global-config ', ' --ignore-local-config', ' -r', ' --recursive', ' -j ', ' --jobs ', ' -p ', ' --pep8-passes ', ' -a', ' --aggressive', ' --experimental', ' --exclude ', ' --list-fixes', ' --ignore ', ' --select ', ' --max-line-length ', ' --line-range  ', ' --range  ', ' --indent-size ', ' --hang-closing', ' --exit-code'], '': [' foo.py'], '': ['+'], '': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'], '': [''], '': ['(-)?+'], '': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], '': [''], '': [''], '': [''], '': ['']}


The grammar can be immediately used for fuzzing. A `GrammarCoverageFuzzer` will ensure all options are covered:

>>> from Grammars import convert_ebnf_grammar
>>> fuzzer = GrammarCoverageFuzzer(convert_ebnf_grammar(option_ebnf_grammar))
>>> [fuzzer.fuzz() for i in range(3)]
[' --pep8-passes 62 foo.py',
 ' --exit-code -j -95 --in-place -d --line-range 87 1 --list-fixes --range 3 0 --hang-closing --aggressive --experimental foo.py',
 ' --indent-size 4 --ignore 7_ -p -3 --jobs 9 --diff -i -a --ignore-local-config -h --select y -r --exclude Ig8> --max-line-length -43 --help --verbose --global-config AR --recursive --version -v --ignore m --select ~a|h< --global-config vx --exclude `q --ignore l --select J --select pLNOV --ignore Y{ --global-config ; --exclude f --select Hr --exclude - --select * --exclude )W --select c9+4 --select 0]s --ignore b6 --ignore k$? --select G --select BM --global-config \\1[ --exclude Z --exclude d --exclude #\' --global-config DU --select u --global-config QSz --ignore e!,t2F --global-config w. --exclude i --select n --exclude ETCj --exclude P: --ignore (& --exclude K3@ --select =/ --select Xo --exclude %" --select } --exclude 5 --ignore )^ --global-config 6 --exclude O!& --global-config B foo.py']

The `OptionFuzzer` class summarizes these steps.  Its constructor takes an `OptionRunner` to automatically extract the grammar; it does the necessary steps to extract the grammar and fuzz with it.

>>> autopep8_runner = OptionRunner("autopep8", "foo.py")
>>> autopep8_fuzzer = OptionFuzzer(autopep8_runner)
>>> [autopep8_fuzzer.fuzz() for i in range(3)]
[' --indent-size 9 foo.py',
 ' -v --global-config F --range -0 -715382 --help --ignore-local-config -j -4 -a --exit-code -r --list-fixes --hang-closing --diff --version --select hZ --jobs 5 --pep8-passes -6 --line-range -9 5 --exclude k% --recursive -h -i --max-line-length 703 --aggressive -d --verbose --experimental --in-place -p -9 --ignore G --ignore 8U --global-config mKa --global-config 45[ --ignore & --global-config Yp --global-config .i) --select |7 --select `*l^SIy> --exclude C --global-config = --ignore xD --global-config bQ --select Tsq --select \\ --select cd~t --exclude ?V --global-config 1O:R --global-config g --global-config E$W --exclude MN --global-config ;v --select !2B#X --select / --global-config L9J_w3 --ignore \' --select uz( --exclude P@ --global-config ero --exclude H --global-config 0,fj --ignore }
For more details, source, and documentation, see
"The Fuzzing Book - Testing Configurations"
at https://www.fuzzingbook.org/html/ConfigurationFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Testing Configurations
# ======================

if __name__ == '__main__':
    print('# Testing Configurations')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Configuration Options
## ---------------------

if __name__ == '__main__':
    print('\n## Configuration Options')



if __name__ == '__main__':
    import os
    os.system(f'grep --help')

## Options in Python
## -----------------

if __name__ == '__main__':
    print('\n## Options in Python')



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

if __name__ == '__main__':
    process_numbers(["--min", "100", "200", "300"])

if __name__ == '__main__':
    process_numbers(["--sum", "1", "2", "3"])

if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError(print_traceback=False):
        process_numbers(["--sum", "--max", "1", "2", "3"])

## A Grammar for Configurations
## ----------------------------

if __name__ == '__main__':
    print('\n## A Grammar for Configurations')



from .Grammars import crange, srange, convert_ebnf_grammar, extend_grammar, is_valid_grammar
from .Grammars import START_SYMBOL, new_symbol

PROCESS_NUMBERS_EBNF_GRAMMAR = {
    "<start>": ["<operator> <integers>"],
    "<operator>": ["--sum", "--min", "--max"],
    "<integers>": ["<integer>", "<integers> <integer>"],
    "<integer>": ["<digit>+"],
    "<digit>": crange('0', '9')
}

assert is_valid_grammar(PROCESS_NUMBERS_EBNF_GRAMMAR)

PROCESS_NUMBERS_GRAMMAR = convert_ebnf_grammar(PROCESS_NUMBERS_EBNF_GRAMMAR)

from .GrammarCoverageFuzzer import GrammarCoverageFuzzer

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(PROCESS_NUMBERS_GRAMMAR, min_nonterminals=10)
    for i in range(3):
        print(f.fuzz())

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(PROCESS_NUMBERS_GRAMMAR, min_nonterminals=10)
    for i in range(3):
        args = f.fuzz().split()
        print(args)
        process_numbers(args)

## Mining Configuration Options
## ----------------------------

if __name__ == '__main__':
    print('\n## Mining Configuration Options')



### Tracking Arguments

if __name__ == '__main__':
    print('\n### Tracking Arguments')



import sys

import string

def traceit(frame, event, arg):
    if event != "call":
        return
    method_name = frame.f_code.co_name
    if method_name != "add_argument":
        return
    locals = frame.f_locals
    print(method_name, locals)

if __name__ == '__main__':
    sys.settrace(traceit)
    process_numbers(["--sum", "1", "2", "3"])
    sys.settrace(None)

def traceit(frame, event, arg):
    if event != "call":
        return
    method_name = frame.f_code.co_name
    if method_name != "add_argument":
        return
    locals = frame.f_locals
    print(locals['args'])

if __name__ == '__main__':
    sys.settrace(traceit)
    process_numbers(["--sum", "1", "2", "3"])
    sys.settrace(None)

### A Grammar Miner for Options and Arguments

if __name__ == '__main__':
    print('\n### A Grammar Miner for Options and Arguments')



class ParseInterrupt(Exception):
    pass

class OptionGrammarMiner(object):
    def __init__(self, function, log=False):
        self.function = function
        self.log = log

class OptionGrammarMiner(OptionGrammarMiner):
    OPTION_SYMBOL = "<option>"
    ARGUMENTS_SYMBOL = "<arguments>"

    def mine_ebnf_grammar(self):
        self.grammar = {
            START_SYMBOL: ["(" + self.OPTION_SYMBOL + ")*" + self.ARGUMENTS_SYMBOL],
            self.OPTION_SYMBOL: [],
            self.ARGUMENTS_SYMBOL: []
        }
        self.current_group = self.OPTION_SYMBOL

        old_trace = sys.gettrace()
        sys.settrace(self.traceit)
        try:
            self.function()
        except ParseInterrupt:
            pass
        sys.settrace(old_trace)

        return self.grammar

    def mine_grammar(self):
        return convert_ebnf_grammar(self.mine_ebnf_grammar())

class OptionGrammarMiner(OptionGrammarMiner):
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
        elif method_name == "add_mutually_exclusive_group":
            self.add_group(frame.f_locals, exclusive=True)
        elif method_name == "add_argument_group":
            # self.add_group(frame.f_locals, exclusive=False)
            pass
        elif method_name == "parse_args":
            raise ParseInterrupt

        return None

class OptionGrammarMiner(OptionGrammarMiner):
    def process_argument(self, locals, in_group):
        args = locals["args"]
        kwargs = locals["kwargs"]

        if self.log:
            print(args)
            print(kwargs)
            print()

        for arg in args:
            self.process_arg(arg, in_group, kwargs)

class OptionGrammarMiner(OptionGrammarMiner):
    def process_arg(self, arg, in_group, kwargs):
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

        param = self.add_parameter(kwargs, metavar)
        if param == "":
            nargs = 0

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

import inspect

class OptionGrammarMiner(OptionGrammarMiner):
    def add_parameter(self, kwargs, metavar):
        if "action" in kwargs:
            # No parameter
            return ""

        type_ = "str"
        if "type" in kwargs:
            given_type = kwargs["type"]
            # int types come as '<class int>'
            if inspect.isclass(given_type) and issubclass(given_type, int):
                type_ = "int"

        if metavar is None:
            if "metavar" in kwargs:
                metavar = kwargs["metavar"]
            else:
                metavar = type_

        self.add_type_rule(type_)
        if metavar != type_:
            self.add_metavar_rule(metavar, type_)

        param = " <" + metavar + ">"

        return param

class OptionGrammarMiner(OptionGrammarMiner):
    def add_type_rule(self, type_):
        if type_ == "int":
            self.add_int_rule()
        else:
            self.add_str_rule()

    def add_int_rule(self):
        self.grammar["<int>"] = ["(-)?<digit>+"]
        self.grammar["<digit>"] = crange('0', '9')

    def add_str_rule(self):
        self.grammar["<str>"] = ["<char>+"]
        self.grammar["<char>"] = srange(
            string.digits
            + string.ascii_letters
            + string.punctuation)

    def add_metavar_rule(self, metavar, type_):
        self.grammar["<" + metavar + ">"] = ["<" + type_ + ">"]

class OptionGrammarMiner(OptionGrammarMiner):
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

        self.grammar[START_SYMBOL][0] = group_expansion + \
            self.grammar[START_SYMBOL][0]
        self.grammar[group] = []
        self.current_group = group

if __name__ == '__main__':
    miner = OptionGrammarMiner(process_numbers, log=True)
    process_numbers_grammar = miner.mine_ebnf_grammar()

if __name__ == '__main__':
    process_numbers_grammar

if __name__ == '__main__':
    process_numbers_grammar["<start>"]

if __name__ == '__main__':
    process_numbers_grammar["<group>"]

if __name__ == '__main__':
    process_numbers_grammar["<option>"]

if __name__ == '__main__':
    process_numbers_grammar["<arguments>"]

if __name__ == '__main__':
    process_numbers_grammar["<integers>"]

if __name__ == '__main__':
    process_numbers_grammar["<int>"]

if __name__ == '__main__':
    assert is_valid_grammar(process_numbers_grammar)

if __name__ == '__main__':
    grammar = convert_ebnf_grammar(process_numbers_grammar)
    assert is_valid_grammar(grammar)

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(grammar)
    for i in range(10):
        print(f.fuzz())

## Testing Autopep8
## ----------------

if __name__ == '__main__':
    print('\n## Testing Autopep8')



if __name__ == '__main__':
    import os
    os.system(f'autopep8 --help')

### Autopep8 Setup

if __name__ == '__main__':
    print('\n### Autopep8 Setup')



import os

def find_executable(name):
    for path in os.get_exec_path():
        qualified_name = os.path.join(path, name)
        if os.path.exists(qualified_name):
            return qualified_name
    return None

if __name__ == '__main__':
    autopep8_executable = find_executable("autopep8")
    assert autopep8_executable is not None
    autopep8_executable

def autopep8():
    executable = find_executable("autopep8")

    # First line has to contain "/usr/bin/env python" or like
    first_line = open(executable).readline()
    assert first_line.find("python") >= 0

    contents = open(executable).read()
    exec(contents)

### Mining an Autopep8 Grammar

if __name__ == '__main__':
    print('\n### Mining an Autopep8 Grammar')



if __name__ == '__main__':
    autopep8_miner = OptionGrammarMiner(autopep8)

if __name__ == '__main__':
    autopep8_ebnf_grammar = autopep8_miner.mine_ebnf_grammar()

if __name__ == '__main__':
    print(autopep8_ebnf_grammar["<option>"])

if __name__ == '__main__':
    autopep8_ebnf_grammar["<line>"]

if __name__ == '__main__':
    autopep8_ebnf_grammar["<arguments>"]

if __name__ == '__main__':
    autopep8_ebnf_grammar["<files>"]

if __name__ == '__main__':
    autopep8_ebnf_grammar["<arguments>"] = [" <files>"]
    autopep8_ebnf_grammar["<files>"] = ["foo.py"]
    assert is_valid_grammar(autopep8_ebnf_grammar)

### Creating Autopep8 Options

if __name__ == '__main__':
    print('\n### Creating Autopep8 Options')



if __name__ == '__main__':
    autopep8_grammar = convert_ebnf_grammar(autopep8_ebnf_grammar)
    assert is_valid_grammar(autopep8_grammar)

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(autopep8_grammar, max_nonterminals=4)
    for i in range(20):
        print(f.fuzz())

def create_foo_py():
    open("foo.py", "w").write("""
def twice(x = 2):
    return  x  +  x
""")

if __name__ == '__main__':
    create_foo_py()

if __name__ == '__main__':
    print(open("foo.py").read(), end="")

if __name__ == '__main__':
    import os
    os.system(f'autopep8 foo.py')

from .Fuzzer import ProgramRunner

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(autopep8_grammar, max_nonterminals=5)
    for i in range(20):
        invocation = "autopep8" + f.fuzz()
        print("$ " + invocation)
        args = invocation.split()
        autopep8 = ProgramRunner(args)
        result, outcome = autopep8.run()
        if result.stderr != "":
            print(result.stderr, end="")

if __name__ == '__main__':
    print(open("foo.py").read(), end="")

import os

if __name__ == '__main__':
    os.remove("foo.py")

## Classes for Fuzzing Configuration Options
## -----------------------------------------

if __name__ == '__main__':
    print('\n## Classes for Fuzzing Configuration Options')



class OptionRunner(ProgramRunner):
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

class OptionRunner(OptionRunner):
    def find_contents(self):
        self._executable = find_executable(self.base_executable)
        first_line = open(self._executable).readline()
        assert first_line.find("python") >= 0
        self.contents = open(self._executable).read()

    def invoker(self):
        exec(self.contents)

    def executable(self):
        return self._executable

class OptionRunner(OptionRunner):
    def find_grammar(self):
        miner = OptionGrammarMiner(self.invoker)
        self._ebnf_grammar = miner.mine_ebnf_grammar()

    def ebnf_grammar(self):
        return self._ebnf_grammar

    def grammar(self):
        return convert_ebnf_grammar(self._ebnf_grammar)

from .Grammars import unreachable_nonterminals

class OptionRunner(OptionRunner):
    def set_arguments(self, args):
        self._ebnf_grammar["<arguments>"] = [" " + args]
        # Delete rules for previous arguments
        for nonterminal in unreachable_nonterminals(self._ebnf_grammar):
            del self._ebnf_grammar[nonterminal]

    def set_invocation(self, program):
        self.program = program

if __name__ == '__main__':
    autopep8_runner = OptionRunner("autopep8", "foo.py")

if __name__ == '__main__':
    print(autopep8_runner.ebnf_grammar()["<option>"])

class OptionFuzzer(GrammarCoverageFuzzer):
    def __init__(self, runner, *args, **kwargs):
        assert issubclass(type(runner), OptionRunner)
        self.runner = runner
        grammar = runner.grammar()
        super().__init__(grammar, *args, **kwargs)

class OptionFuzzer(OptionFuzzer):
    def run(self, runner=None, inp=""):
        if runner is None:
            runner = self.runner
        assert issubclass(type(runner), OptionRunner)
        invocation = runner.executable() + " " + self.fuzz()
        runner.set_invocation(invocation.split())
        return runner.run(inp)

### Example: Autopep8

if __name__ == '__main__':
    print('\n### Example: Autopep8')



if __name__ == '__main__':
    autopep8_fuzzer = OptionFuzzer(autopep8_runner, max_nonterminals=5)

if __name__ == '__main__':
    for i in range(3):
        print(autopep8_fuzzer.fuzz())

if __name__ == '__main__':
    autopep8_fuzzer.run(autopep8_runner)

### Example: MyPy

if __name__ == '__main__':
    print('\n### Example: MyPy')



if __name__ == '__main__':
    assert find_executable("mypy") is not None

if __name__ == '__main__':
    mypy_runner = OptionRunner("mypy", "foo.py")
    print(mypy_runner.ebnf_grammar()["<option>"])

if __name__ == '__main__':
    mypy_fuzzer = OptionFuzzer(mypy_runner, max_nonterminals=5)
    for i in range(10):
        print(mypy_fuzzer.fuzz())

### Example: Notedown

if __name__ == '__main__':
    print('\n### Example: Notedown')



if __name__ == '__main__':
    assert find_executable("notedown") is not None

if __name__ == '__main__':
    notedown_runner = OptionRunner("notedown")

if __name__ == '__main__':
    print(notedown_runner.ebnf_grammar()["<option>"])

if __name__ == '__main__':
    notedown_fuzzer = OptionFuzzer(notedown_runner, max_nonterminals=5)
    for i in range(10):
        print(notedown_fuzzer.fuzz())

## Combinatorial Testing
## ---------------------

if __name__ == '__main__':
    print('\n## Combinatorial Testing')



from itertools import combinations

if __name__ == '__main__':
    option_list = notedown_runner.ebnf_grammar()["<option>"]
    pairs = list(combinations(option_list, 2))

if __name__ == '__main__':
    len(pairs)

if __name__ == '__main__':
    print(pairs[:20])

def pairwise(option_list):
    return [option_1 + option_2
            for (option_1, option_2) in combinations(option_list, 2)]

if __name__ == '__main__':
    print(pairwise(option_list)[:20])

if __name__ == '__main__':
    notedown_grammar = notedown_runner.grammar()
    pairwise_notedown_grammar = extend_grammar(notedown_grammar)
    pairwise_notedown_grammar["<option>"] = pairwise(notedown_grammar["<option>"])
    assert is_valid_grammar(pairwise_notedown_grammar)

if __name__ == '__main__':
    notedown_fuzzer = GrammarCoverageFuzzer(
        pairwise_notedown_grammar, max_nonterminals=4)

if __name__ == '__main__':
    for i in range(10):
        print(notedown_fuzzer.fuzz())

if __name__ == '__main__':
    for combination_length in range(1, 20):
        tuples = list(combinations(option_list, combination_length))
        print(combination_length, len(tuples))

if __name__ == '__main__':
    len(autopep8_runner.ebnf_grammar()["<option>"])

if __name__ == '__main__':
    len(autopep8_runner.ebnf_grammar()["<option>"]) * \
        (len(autopep8_runner.ebnf_grammar()["<option>"]) - 1)

if __name__ == '__main__':
    len(mypy_runner.ebnf_grammar()["<option>"])

if __name__ == '__main__':
    len(mypy_runner.ebnf_grammar()["<option>"]) * \
        (len(mypy_runner.ebnf_grammar()["<option>"]) - 1)

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    autopep8_runner = OptionRunner("autopep8", "foo.py")

if __name__ == '__main__':
    option_ebnf_grammar = autopep8_runner.ebnf_grammar()
    print(option_ebnf_grammar)

from .Grammars import convert_ebnf_grammar

if __name__ == '__main__':
    fuzzer = GrammarCoverageFuzzer(convert_ebnf_grammar(option_ebnf_grammar))
    [fuzzer.fuzz() for i in range(3)]

if __name__ == '__main__':
    autopep8_runner = OptionRunner("autopep8", "foo.py")
    autopep8_fuzzer = OptionFuzzer(autopep8_runner)

if __name__ == '__main__':
    [autopep8_fuzzer.fuzz() for i in range(3)]

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



### Exercise 1: #ifdef Configuration Fuzzing

if __name__ == '__main__':
    print('\n### Exercise 1: #ifdef Configuration Fuzzing')



#### Part 1: Extract Preprocessor Variables

if __name__ == '__main__':
    print('\n#### Part 1: Extract Preprocessor Variables')



if __name__ == '__main__':
    filename = "xmlparse.c"

    open(filename, "w").write(
        """
#if defined(_WIN32) && !defined(LOAD_LIBRARY_SEARCH_SYSTEM32)
# define LOAD_LIBRARY_SEARCH_SYSTEM32  0x00000800
#endif

#if !defined(HAVE_GETRANDOM) && !defined(HAVE_SYSCALL_GETRANDOM) \
    && !defined(HAVE_ARC4RANDOM_BUF) && !defined(HAVE_ARC4RANDOM) \
    && !defined(XML_DEV_URANDOM) \
    && !defined(_WIN32) \
    && !defined(XML_POOR_ENTROPY)
# error
#endif

#if !defined(TIOCSWINSZ) || defined(__SCO__) || defined(__UNIXWARE__)
#define USE_SYSV_ENVVARS	/* COLUMNS/LINES vs. TERMCAP */
#endif

#ifdef XML_UNICODE_WCHAR_T
#define XML_T(x) (const wchar_t)x
#define XML_L(x) L ## x
#else
#define XML_T(x) (const unsigned short)x
#define XML_L(x) x
#endif

int fun(int x) { return XML_T(x); }
""");

import re

if __name__ == '__main__':
    re_cpp_if_directive = re.compile(r"\s*#\s*(el)?if")
    re_cpp_identifier = re.compile(r"[a-zA-Z_$]+")

def cpp_identifiers(lines):
    identifiers = set()
    for line in lines:
        if re_cpp_if_directive.match(line):
            identifiers |= set(re_cpp_identifier.findall(line))

    # These are preprocessor keywords
    identifiers -= {"if", "ifdef", "ifndef", "defined"}
    return identifiers

if __name__ == '__main__':
    cpp_ids = cpp_identifiers(open("xmlparse.c").readlines())
    cpp_ids

#### Part 2: Derive an Option Grammar

if __name__ == '__main__':
    print('\n#### Part 2: Derive an Option Grammar')



from .Grammars import new_symbol

if __name__ == '__main__':
    cpp_grammar = {
        "<start>": ["cc -c<options> " + filename],
        "<options>": ["<option>", "<options><option>"],
        "<option>": []
    }
    for id in cpp_ids:
        s = new_symbol(cpp_grammar, "<" + id + ">")
        cpp_grammar["<option>"].append(s)
        cpp_grammar[s] = [" -D" + id]

    cpp_grammar

if __name__ == '__main__':
    assert is_valid_grammar(cpp_grammar)

#### Part 3: C Preprocessor Configuration Fuzzing

if __name__ == '__main__':
    print('\n#### Part 3: C Preprocessor Configuration Fuzzing')



if __name__ == '__main__':
    g = GrammarCoverageFuzzer(cpp_grammar)
    g.fuzz()

from .Fuzzer import ProgramRunner

if __name__ == '__main__':
    for i in range(10):
        invocation = g.fuzz()
        print("$", invocation)
        # subprocess.call(invocation, shell=True)
        cc_runner = ProgramRunner(invocation.split(' '))
        (result, outcome) = cc_runner.run()
        print(result.stderr, end="")

if __name__ == '__main__':
    pairwise_cpp_grammar = extend_grammar(cpp_grammar)
    pairwise_cpp_grammar["<option>"] = pairwise(cpp_grammar["<option>"])
    pairwise_cpp_grammar["<option>"][:10]

if __name__ == '__main__':
    for i in range(10):
        invocation = g.fuzz()
        print("$", invocation)
        # subprocess.call(invocation, shell=True)
        cc_runner = ProgramRunner(invocation.split(' '))
        (result, outcome) = cc_runner.run()
        print(result.stderr, end="")

if __name__ == '__main__':
    os.remove("xmlparse.c")

if __name__ == '__main__':
    if os.path.exists("xmlparse.o"):
        os.remove("xmlparse.o")

### Exercise 2: .ini Configuration Fuzzing

if __name__ == '__main__':
    print('\n### Exercise 2: .ini Configuration Fuzzing')



import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'ServerAliveInterval': '45',
                         'Compression': 'yes',
                         'CompressionLevel': '9'}
    config['bitbucket.org'] = {}
    config['bitbucket.org']['User'] = 'hg'
    config['topsecret.server.com'] = {}
    topsecret = config['topsecret.server.com']
    topsecret['Port'] = '50022'     # mutates the parser
    topsecret['ForwardX11'] = 'no'  # same here
    config['DEFAULT']['ForwardX11'] = 'yes'
    with open('example.ini', 'w') as configfile:
        config.write(configfile)

    with open('example.ini') as configfile:
        print(configfile.read(), end="")

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('example.ini')
    topsecret = config['topsecret.server.com']
    topsecret['Port']

#### Part 1: Read Configuration

if __name__ == '__main__':
    print('\n#### Part 1: Read Configuration')



#### Part 2: Create a Configuration Grammar

if __name__ == '__main__':
    print('\n#### Part 2: Create a Configuration Grammar')



#### Part 3: Mine a Configuration Grammar

if __name__ == '__main__':
    print('\n#### Part 3: Mine a Configuration Grammar')



class TrackingConfigParser(configparser.ConfigParser):
    def __getitem__(self, key):
        print("Accessing", repr(key))
        return super().__getitem__(key)

if __name__ == '__main__':
    tracking_config_parser = TrackingConfigParser()
    tracking_config_parser.read('example.ini')
    section = tracking_config_parser['topsecret.server.com']

import os

if __name__ == '__main__':
    os.remove("example.ini")

### Exercise 3: Extracting and Fuzzing C Command-Line Options

if __name__ == '__main__':
    print('\n### Exercise 3: Extracting and Fuzzing C Command-Line Options')



#### Part 1: Getopt Fuzzing

if __name__ == '__main__':
    print('\n#### Part 1: Getopt Fuzzing')



#### Part 2: Fuzzing Long Options in C

if __name__ == '__main__':
    print('\n#### Part 2: Fuzzing Long Options in C')



### Exercise 4: Expansions in Context

if __name__ == '__main__':
    print('\n### Exercise 4: Expansions in Context')



if __name__ == '__main__':
    autopep8_runner.ebnf_grammar()["<line>"]

if __name__ == '__main__':
    autopep8_runner.ebnf_grammar()["<int>"]

if __name__ == '__main__':
    autopep8_runner.ebnf_grammar()["<digit>"]
