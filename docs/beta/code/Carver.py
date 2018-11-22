#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Carver.html
# Last change: 2018-11-18 14:40:05+01:00
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


# # Carving Unit Tests

if __name__ == "__main__":
    print('# Carving Unit Tests')




# ## System Tests vs Unit Tests

if __name__ == "__main__":
    print('\n## System Tests vs Unit Tests')




import urllib.parse
import urllib.request

import fuzzingbook_utils

def webbrowser(url):
    """Download the http/https resource given by the URL"""
    response = urllib.request.urlopen(url)
    if response.getcode() == 200:
        contents = response.read()
    return contents.decode("utf8")

if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


if __name__ == "__main__":
    with Timer() as webbrowser_timer:
        fuzzingbook_contents = webbrowser(
            "http://www.fuzzingbook.org/html/Fuzzer.html")

    print("Downloaded %d bytes in %.2f seconds" %
          (len(fuzzingbook_contents), webbrowser_timer.elapsed_time()))


if __name__ == "__main__":
    fuzzingbook_contents[:100]


from urllib.parse import urlparse

if __name__ == "__main__":
    urlparse('https://www.fuzzingbook.com/html/Carver.html')


if __name__ == "__main__":
    runs = 1000
    with Timer() as urlparse_timer:
        for i in range(runs):
            urlparse('https://www.fuzzingbook.com/html/Carver.html')

    avg_urlparse_time = urlparse_timer.elapsed_time() / 1000
    avg_urlparse_time


if __name__ == "__main__":
    webbrowser_timer.elapsed_time()


if __name__ == "__main__":
    webbrowser_timer.elapsed_time() / avg_urlparse_time


# ## Carving Unit Tests

if __name__ == "__main__":
    print('\n## Carving Unit Tests')




# ## Recording Calls

if __name__ == "__main__":
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

# ### Recording my_sqrt()

if __name__ == "__main__":
    print('\n### Recording my_sqrt()')




if __package__ is None or __package__ == "":
    from Intro_Testing import my_sqrt
else:
    from .Intro_Testing import my_sqrt


if __name__ == "__main__":
    with CallCarver() as sqrt_carver:
        my_sqrt(2)
        my_sqrt(4)


if __name__ == "__main__":
    sqrt_carver.calls()


if __name__ == "__main__":
    sqrt_carver.called_functions()


if __name__ == "__main__":
    sqrt_carver.arguments("my_sqrt")


def simple_call_string(function_name, argument_list):
    """Return function_name(arg[0], arg[1], ...) as a string"""
    return function_name + "(" + \
        ", ".join([var + "=" + repr(value)
                   for (var, value) in argument_list]) + ")"

if __name__ == "__main__":
    for function_name in sqrt_carver.called_functions():
        for argument_list in sqrt_carver.arguments(function_name):
            print(simple_call_string(function_name, argument_list))


if __name__ == "__main__":
    eval("my_sqrt(x=2)")


# ### Carving urlparse()

if __name__ == "__main__":
    print('\n### Carving urlparse()')




if __name__ == "__main__":
    with CallCarver() as webbrowser_carver:
        webbrowser("http://www.example.com")


if __name__ == "__main__":
    print(webbrowser_carver.called_functions(qualified=True))


if __name__ == "__main__":
    urlparse_argument_list = webbrowser_carver.arguments("urllib.parse.urlparse")
    urlparse_argument_list


if __name__ == "__main__":
    urlparse_call = simple_call_string("urlparse", urlparse_argument_list[0])
    urlparse_call


if __name__ == "__main__":
    eval(urlparse_call)


# ## Replaying Calls

if __name__ == "__main__":
    print('\n## Replaying Calls')




if __name__ == "__main__":
    email_parse_argument_list = webbrowser_carver.arguments("email.parser.parse")


if __name__ == "__main__":
    email_parse_call = simple_call_string(
        "email.parser.parse",
        email_parse_argument_list[0])
    email_parse_call


# ### Serializing Objects

if __name__ == "__main__":
    print('\n### Serializing Objects')




import pickle    

if __name__ == "__main__":
    parser_object = email_parse_argument_list[0][0][1]
    parser_object


if __name__ == "__main__":
    pickled = pickle.dumps(parser_object)
    pickled


if __name__ == "__main__":
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

if __name__ == "__main__":
    call = call_string("email.parser.parse", email_parse_argument_list[0])
    print(call)


if __name__ == "__main__":
    eval(call)


# ### All Calls

if __name__ == "__main__":
    print('\n### All Calls')




import traceback

import enum
import socket

if __name__ == "__main__":
    all_functions = set(webbrowser_carver.called_functions(qualified=True))
    call_success = set()
    run_success = set()


if __name__ == "__main__":
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


if __name__ == "__main__":
    print("%d/%d calls (%.2f%%) successfully created and %d/%d calls (%.2f%%) successfully ran" % (
        len(call_success), len(all_functions), len(
            call_success) * 100 / len(all_functions),
        len(run_success), len(all_functions), len(run_success) * 100 / len(all_functions)))


if __name__ == "__main__":
    for i in range(10):
        print(list(exceptions_seen)[i])


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




class ResultCarver(CallCarver):
    def traceit(self, frame, event, arg):
        if event == "return":
            if self._log:
                print("Result:", arg)

        super().traceit(frame, event, arg)
        # Need to return traceit function such that it is invoked for return
        # events
        return self.traceit

if __name__ == "__main__":
    with ResultCarver(log=True) as result_carver:
        my_sqrt(2)


# #### Part 1: Store function results

if __name__ == "__main__":
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

if __name__ == "__main__":
    with ResultCarver(log=True) as result_carver:
        my_sqrt(2)
    result_carver._results


# #### Part 2: Access results

if __name__ == "__main__":
    print('\n#### Part 2: Access results')




class ResultCarver(ResultCarver):
    def result(self, function_name, argument):
        key = simple_call_string(function_name, arguments)
        return self._results[key]

# #### Part 3: Produce assertions

if __name__ == "__main__":
    print('\n#### Part 3: Produce assertions')




if __name__ == "__main__":
    with ResultCarver() as webbrowser_result_carver:
        webbrowser("http://www.example.com")


if __name__ == "__main__":
    for function_name in ["urllib.parse.urlparse", "urllib.parse.urlsplit"]:
        for arguments in webbrowser_result_carver.arguments(function_name):
            try:
                call = call_string(function_name, arguments)
                result = webbrowser_result_carver.result(function_name, arguments)
                print("assert", call, "==", call_value(result))
            except Exception:
                continue


from urllib.parse import SplitResult, ParseResult, urlparse, urlsplit

if __name__ == "__main__":
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

