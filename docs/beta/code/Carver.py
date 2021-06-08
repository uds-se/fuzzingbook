#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Carving Unit Tests" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/Carver.html
# Last change: 2021-06-04 15:28:25+02:00
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
The Fuzzing Book - Carving Unit Tests

This file can be _executed_ as a script, running all experiments:

    $ python Carver.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.Carver import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/Carver.html

This chapter provides means to _record and replay function calls_ during a system test.  Since individual function calls are much faster than a whole system run, such "carving" mechanisms have the potential to run tests much faster.

### Recording Calls

The `CallCarver` class records all calls occurring while it is active.  It is used in conjunction with a `with` clause:

>>> with CallCarver() as carver:
>>>     y = my_sqrt(2)
>>>     y = my_sqrt(4)

After execution, `called_functions()` lists the names of functions encountered:

>>> carver.called_functions()
['my_sqrt', '__exit__']

The `arguments()` method lists the arguments recorded for a function.  This is a mapping of the function name to a list of lists of arguments; each argument is a pair (parameter name, value).

>>> carver.arguments('my_sqrt')
[[('x', 2)], [('x', 4)]]

Complex arguments are properly serialized, such that they can be easily restored.

### Synthesizing Calls

While such recorded arguments already could be turned into arguments and calls, a much nicer alternative is to create a _grammar_ for recorded calls.  This allows to synthesize arbitrary _combinations_ of arguments, and also offers a base for further customization of calls.

The `CallGrammarMiner` class turns a list of carved executions into a grammar.

>>> my_sqrt_miner = CallGrammarMiner(carver)
>>> my_sqrt_grammar = my_sqrt_miner.mine_call_grammar()
>>> my_sqrt_grammar
{'': [''],
 '': [''],
 '': ['2', '4'],
 '': ['my_sqrt()']}

This grammar can be used to synthesize calls.

>>> fuzzer = GrammarCoverageFuzzer(my_sqrt_grammar)
>>> fuzzer.fuzz()
'my_sqrt(4)'

These calls can be executed in isolation, effectively extracting unit tests from system tests:

>>> eval(fuzzer.fuzz())
1.414213562373095


For more details, source, and documentation, see
"The Fuzzing Book - Carving Unit Tests"
at https://www.fuzzingbook.org/html/Carver.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Carving Unit Tests
# ==================

if __name__ == '__main__':
    print('# Carving Unit Tests')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from . import APIFuzzer

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## System Tests vs Unit Tests
## --------------------------

if __name__ == '__main__':
    print('\n## System Tests vs Unit Tests')



import urllib.parse

def webbrowser(url):
    """Download the http/https resource given by the URL"""
    import requests  # Only import if needed

    r = requests.get(url)
    return r.text

from .Timer import Timer

if __name__ == '__main__':
    with Timer() as webbrowser_timer:
        fuzzingbook_contents = webbrowser(
            "http://www.fuzzingbook.org/html/Fuzzer.html")

    print("Downloaded %d bytes in %.2f seconds" %
          (len(fuzzingbook_contents), webbrowser_timer.elapsed_time()))

if __name__ == '__main__':
    fuzzingbook_contents[:100]

from urllib.parse import urlparse

if __name__ == '__main__':
    urlparse('https://www.fuzzingbook.com/html/Carver.html')

if __name__ == '__main__':
    runs = 1000
    with Timer() as urlparse_timer:
        for i in range(runs):
            urlparse('https://www.fuzzingbook.com/html/Carver.html')

    avg_urlparse_time = urlparse_timer.elapsed_time() / 1000
    avg_urlparse_time

if __name__ == '__main__':
    webbrowser_timer.elapsed_time()

if __name__ == '__main__':
    webbrowser_timer.elapsed_time() / avg_urlparse_time

## Carving Unit Tests
## ------------------

if __name__ == '__main__':
    print('\n## Carving Unit Tests')



## Recording Calls
## ---------------

if __name__ == '__main__':
    print('\n## Recording Calls')



import sys

class Carver(object):
    def __init__(self, log=False):
        self._log = log
        self.reset()

    def reset(self):
        self._calls = {}

    # Start of `with` block
    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        sys.settrace(self.original_trace_function)

import inspect

def get_qualified_name(code):
    """Return the fully qualified name of the current function"""
    name = code.co_name
    module = inspect.getmodule(code)
    if module is not None:
        name = module.__name__ + "." + name
    return name

def get_arguments(frame):
    """Return call arguments in the given frame"""
    # When called, all arguments are local variables
    arguments = [(var, frame.f_locals[var]) for var in frame.f_locals]
    arguments.reverse()  # Want same order as call
    return arguments

class CallCarver(Carver):
    def add_call(self, function_name, arguments):
        """Add given call to list of calls"""
        if function_name not in self._calls:
            self._calls[function_name] = []
        self._calls[function_name].append(arguments)

    # Tracking function: Record all calls and all args
    def traceit(self, frame, event, arg):
        if event != "call":
            return None

        code = frame.f_code
        function_name = code.co_name
        qualified_name = get_qualified_name(code)
        arguments = get_arguments(frame)

        self.add_call(function_name, arguments)
        if qualified_name != function_name:
            self.add_call(qualified_name, arguments)

        if self._log:
            print(simple_call_string(function_name, arguments))

        return None

class CallCarver(CallCarver):
    def calls(self):
        """Return a dictionary of all calls traced."""
        return self._calls

    def arguments(self, function_name):
        """Return a list of all arguments of the given function
        as (VAR, VALUE) pairs.
        Raises an exception if the function was not traced."""
        return self._calls[function_name]

    def called_functions(self, qualified=False):
        """Return all functions called."""
        if qualified:
            return [function_name for function_name in self._calls.keys()
                    if function_name.find('.') >= 0]
        else:
            return [function_name for function_name in self._calls.keys()
                    if function_name.find('.') < 0]

### Recording my_sqrt()

if __name__ == '__main__':
    print('\n### Recording my_sqrt()')



from .Intro_Testing import my_sqrt

if __name__ == '__main__':
    with CallCarver() as sqrt_carver:
        my_sqrt(2)
        my_sqrt(4)

if __name__ == '__main__':
    sqrt_carver.calls()

if __name__ == '__main__':
    sqrt_carver.called_functions()

if __name__ == '__main__':
    sqrt_carver.arguments("my_sqrt")

def simple_call_string(function_name, argument_list):
    """Return function_name(arg[0], arg[1], ...) as a string"""
    return function_name + "(" + \
        ", ".join([var + "=" + repr(value)
                   for (var, value) in argument_list]) + ")"

if __name__ == '__main__':
    for function_name in sqrt_carver.called_functions():
        for argument_list in sqrt_carver.arguments(function_name):
            print(simple_call_string(function_name, argument_list))

if __name__ == '__main__':
    eval("my_sqrt(x=2)")

### Carving urlparse()

if __name__ == '__main__':
    print('\n### Carving urlparse()')



if __name__ == '__main__':
    with CallCarver() as webbrowser_carver:
        webbrowser("http://www.example.com")

if __name__ == '__main__':
    function_list = webbrowser_carver.called_functions(qualified=True)
    len(function_list)

if __name__ == '__main__':
    print(function_list[:50])

if __name__ == '__main__':
    urlparse_argument_list = webbrowser_carver.arguments("urllib.parse.urlparse")
    urlparse_argument_list

if __name__ == '__main__':
    urlparse_call = simple_call_string("urlparse", urlparse_argument_list[0])
    urlparse_call

if __name__ == '__main__':
    eval(urlparse_call)

## Replaying Calls
## ---------------

if __name__ == '__main__':
    print('\n## Replaying Calls')



if __name__ == '__main__':
    email_parse_argument_list = webbrowser_carver.arguments("email.parser.parse")

if __name__ == '__main__':
    email_parse_call = simple_call_string(
        "email.parser.parse",
        email_parse_argument_list[0])
    email_parse_call

### Serializing Objects

if __name__ == '__main__':
    print('\n### Serializing Objects')



import pickle    

if __name__ == '__main__':
    parser_object = email_parse_argument_list[0][0][1]
    parser_object

if __name__ == '__main__':
    pickled = pickle.dumps(parser_object)
    pickled

if __name__ == '__main__':
    unpickled_parser_object = pickle.loads(pickled)
    unpickled_parser_object

def call_value(value):
    value_as_string = repr(value)
    if value_as_string.find('<') >= 0:
        # Complex object
        value_as_string = "pickle.loads(" + repr(pickle.dumps(value)) + ")"
    return value_as_string

def call_string(function_name, argument_list):
    """Return function_name(arg[0], arg[1], ...) as a string, pickling complex objects"""
    if len(argument_list) > 0:
        (first_var, first_value) = argument_list[0]
        if first_var == "self":
            # Make this a method call
            method_name = function_name.split(".")[-1]
            function_name = call_value(first_value) + "." + method_name
            argument_list = argument_list[1:]

    return function_name + "(" + \
        ", ".join([var + "=" + call_value(value)
                   for (var, value) in argument_list]) + ")"

if __name__ == '__main__':
    call = call_string("email.parser.parse", email_parse_argument_list[0])
    print(call)

if __name__ == '__main__':
    eval(call)

### All Calls

if __name__ == '__main__':
    print('\n### All Calls')



import traceback

import enum
import socket

if __name__ == '__main__':
    all_functions = set(webbrowser_carver.called_functions(qualified=True))
    call_success = set()
    run_success = set()

if __name__ == '__main__':
    exceptions_seen = set()

    for function_name in webbrowser_carver.called_functions(qualified=True):
        for argument_list in webbrowser_carver.arguments(function_name):
            try:
                call = call_string(function_name, argument_list)
                call_success.add(function_name)

                result = eval(call)
                run_success.add(function_name)

            except Exception as exc:
                exceptions_seen.add(repr(exc))
                # print("->", call, file=sys.stderr)
                # traceback.print_exc()
                # print("", file=sys.stderr)
                continue

if __name__ == '__main__':
    print("%d/%d calls (%.2f%%) successfully created and %d/%d calls (%.2f%%) successfully ran" % (
        len(call_success), len(all_functions), len(
            call_success) * 100 / len(all_functions),
        len(run_success), len(all_functions), len(run_success) * 100 / len(all_functions)))

if __name__ == '__main__':
    for i in range(10):
        print(list(exceptions_seen)[i])

## Mining API Grammars from Carved Calls
## -------------------------------------

if __name__ == '__main__':
    print('\n## Mining API Grammars from Carved Calls')



### From Calls to Grammars

if __name__ == '__main__':
    print('\n### From Calls to Grammars')



import math

def power(x, y):
    return math.pow(x, y)

if __name__ == '__main__':
    with CallCarver() as power_carver:
        z = power(1, 2)
        z = power(3, 4)

if __name__ == '__main__':
    power_carver.arguments("power")

from .Grammars import START_SYMBOL, is_valid_grammar, new_symbol, extend_grammar

POWER_GRAMMAR = {
    "<start>": ["power(<x>, <y>)"],
    "<x>": ["1", "3"],
    "<y>": ["2", "4"]
}

assert is_valid_grammar(POWER_GRAMMAR)

from .GrammarCoverageFuzzer import GrammarCoverageFuzzer

if __name__ == '__main__':
    power_fuzzer = GrammarCoverageFuzzer(POWER_GRAMMAR)
    [power_fuzzer.fuzz() for i in range(5)]

### A Grammar Miner for Calls

if __name__ == '__main__':
    print('\n### A Grammar Miner for Calls')



class CallGrammarMiner(object):
    def __init__(self, carver, log=False):
        self.carver = carver
        self.log = log

#### Initial Grammar

if __name__ == '__main__':
    print('\n#### Initial Grammar')



import copy 

class CallGrammarMiner(CallGrammarMiner):
    CALL_SYMBOL = "<call>"

    def initial_grammar(self):
        return extend_grammar(
            {START_SYMBOL: [self.CALL_SYMBOL],
                self.CALL_SYMBOL: []
             })

if __name__ == '__main__':
    m = CallGrammarMiner(power_carver)
    initial_grammar = m.initial_grammar()
    initial_grammar

#### A Grammar from Arguments

if __name__ == '__main__':
    print('\n#### A Grammar from Arguments')



if __name__ == '__main__':
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

if __name__ == '__main__':
    m = CallGrammarMiner(power_carver)
    var_grammar, var_symbols = m.mine_arguments_grammar(
        "power", arguments, initial_grammar)

if __name__ == '__main__':
    var_grammar

if __name__ == '__main__':
    var_symbols

#### A Grammar from Calls

if __name__ == '__main__':
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

if __name__ == '__main__':
    m = CallGrammarMiner(power_carver)
    function_grammar, function_symbol = m.mine_function_grammar(
        "power", initial_grammar)
    function_grammar

if __name__ == '__main__':
    function_symbol

#### A Grammar from all Calls

if __name__ == '__main__':
    print('\n#### A Grammar from all Calls')



if __name__ == '__main__':
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

if __name__ == '__main__':
    m = CallGrammarMiner(power_carver)
    power_grammar = m.mine_call_grammar()
    power_grammar

if __name__ == '__main__':
    power_fuzzer = GrammarCoverageFuzzer(power_grammar)
    [power_fuzzer.fuzz() for i in range(5)]

## Fuzzing Web Functions
## ---------------------

if __name__ == '__main__':
    print('\n## Fuzzing Web Functions')



if __name__ == '__main__':
    with CallCarver() as webbrowser_carver:
        webbrowser("https://www.fuzzingbook.org")
        webbrowser("http://www.example.com")

if __name__ == '__main__':
    m = CallGrammarMiner(webbrowser_carver)
    webbrowser_grammar = m.mine_call_grammar()

if __name__ == '__main__':
    call_list = webbrowser_grammar['<call>']
    len(call_list)

if __name__ == '__main__':
    print(call_list[:20])

if __name__ == '__main__':
    webbrowser_grammar["<urlsplit>"]

if __name__ == '__main__':
    webbrowser_grammar["<urlsplit-url>"]

if __name__ == '__main__':
    webbrowser_grammar["<urlsplit-scheme>"]

if __name__ == '__main__':
    urlsplit_fuzzer = GrammarCoverageFuzzer(
        webbrowser_grammar, start_symbol="<urlsplit>")
    for i in range(5):
        print(urlsplit_fuzzer.fuzz())

from urllib.parse import urlsplit

from .Timer import Timer

if __name__ == '__main__':
    with Timer() as urlsplit_timer:
        urlsplit('http://www.fuzzingbook.org/', 'http', True)
    urlsplit_timer.elapsed_time()

if __name__ == '__main__':
    with Timer() as webbrowser_timer:
        webbrowser("http://www.fuzzingbook.org")
    webbrowser_timer.elapsed_time()

if __name__ == '__main__':
    webbrowser_timer.elapsed_time() / urlsplit_timer.elapsed_time()

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



### Recording Calls

if __name__ == '__main__':
    print('\n### Recording Calls')



if __name__ == '__main__':
    with CallCarver() as carver:
        y = my_sqrt(2)
        y = my_sqrt(4)

if __name__ == '__main__':
    carver.called_functions()

if __name__ == '__main__':
    carver.arguments('my_sqrt')

### Synthesizing Calls

if __name__ == '__main__':
    print('\n### Synthesizing Calls')



if __name__ == '__main__':
    my_sqrt_miner = CallGrammarMiner(carver)
    my_sqrt_grammar = my_sqrt_miner.mine_call_grammar()
    my_sqrt_grammar

if __name__ == '__main__':
    fuzzer = GrammarCoverageFuzzer(my_sqrt_grammar)
    fuzzer.fuzz()

if __name__ == '__main__':
    eval(fuzzer.fuzz())

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



class ResultCarver(CallCarver):
    def traceit(self, frame, event, arg):
        if event == "return":
            if self._log:
                print("Result:", arg)

        super().traceit(frame, event, arg)
        # Need to return traceit function such that it is invoked for return
        # events
        return self.traceit

if __name__ == '__main__':
    with ResultCarver(log=True) as result_carver:
        my_sqrt(2)

#### Part 1: Store function results

if __name__ == '__main__':
    print('\n#### Part 1: Store function results')



class ResultCarver(CallCarver):
    def reset(self):
        super().reset()
        self._call_stack = []
        self._results = {}

    def add_result(self, function_name, arguments, result):
        key = simple_call_string(function_name, arguments)
        self._results[key] = result

    def traceit(self, frame, event, arg):
        if event == "call":
            code = frame.f_code
            function_name = code.co_name
            qualified_name = get_qualified_name(code)
            self._call_stack.append(
                (function_name, qualified_name, get_arguments(frame)))

        if event == "return":
            result = arg
            (function_name, qualified_name, arguments) = self._call_stack.pop()
            self.add_result(function_name, arguments, result)
            if function_name != qualified_name:
                self.add_result(qualified_name, arguments, result)
            if self._log:
                print(
                    simple_call_string(
                        function_name,
                        arguments),
                    "=",
                    result)

        # Keep on processing current calls
        super().traceit(frame, event, arg)

        # Need to return traceit function such that it is invoked for return
        # events
        return self.traceit

if __name__ == '__main__':
    with ResultCarver(log=True) as result_carver:
        my_sqrt(2)
    result_carver._results

#### Part 2: Access results

if __name__ == '__main__':
    print('\n#### Part 2: Access results')



class ResultCarver(ResultCarver):
    def result(self, function_name, argument):
        key = simple_call_string(function_name, arguments)
        return self._results[key]

#### Part 3: Produce assertions

if __name__ == '__main__':
    print('\n#### Part 3: Produce assertions')



if __name__ == '__main__':
    with ResultCarver() as webbrowser_result_carver:
        webbrowser("http://www.example.com")

if __name__ == '__main__':
    for function_name in ["urllib.parse.urlparse", "urllib.parse.urlsplit"]:
        for arguments in webbrowser_result_carver.arguments(function_name):
            try:
                call = call_string(function_name, arguments)
                result = webbrowser_result_carver.result(function_name, arguments)
                print("assert", call, "==", call_value(result))
            except Exception:
                continue

from urllib.parse import SplitResult, ParseResult, urlparse, urlsplit

if __name__ == '__main__':
    assert urlparse(
        url='http://www.example.com',
        scheme='',
        allow_fragments=True) == ParseResult(
            scheme='http',
            netloc='www.example.com',
            path='',
            params='',
            query='',
        fragment='')
    assert urlsplit(
        url='http://www.example.com',
        scheme='',
        allow_fragments=True) == SplitResult(
            scheme='http',
            netloc='www.example.com',
            path='',
            query='',
        fragment='')

### Exercise 2: Abstracting Arguments

if __name__ == '__main__':
    print('\n### Exercise 2: Abstracting Arguments')


