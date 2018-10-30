#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Carver.html
# Last change: 2018-10-29 14:49:26+01:00
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




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


# ## System Tests vs Unit Tests

if __name__ == "__main__":
    print('\n## System Tests vs Unit Tests')




import urllib.parse, urllib.request

def webbrowser(url):
    """Download the http/https resource given by the URL"""
    response = urllib.request.urlopen(url)
    if response.getcode() == 200:
        contents = response.read()
    return contents

if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


if __name__ == "__main__":
    with Timer() as webbrowser_timer:
        fuzzingbook_contents = webbrowser("http://www.fuzzingbook.org/html/Fuzzer.html")

    print("Downloaded %d bytes in %.2f seconds" % (len(fuzzingbook_contents), webbrowser_timer.elapsed_time()))


if __name__ == "__main__":
    fuzzingbook_contents[:100]


from urllib.parse import urlparse

if __name__ == "__main__":
    urlparse('https://www.fuzzingbook.com/html/APIFuzzer.html')


if __name__ == "__main__":
    runs = 1000
    with Timer() as urlparse_timer:
        for i in range(runs):
            urlparse('https://www.fuzzingbook.com/html/APIFuzzer.html')

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
import inspect

class Carver(object):
    def __init__(self):
        self._calls = {}

    # Start of `with` block
    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        sys.settrace(self.original_trace_function)

def get_qualified_name(code):
    name = code.co_name
    module = inspect.getmodule(code)
    if module is not None:
        name = module.__name__ + "." + name
    return name

class Carver(Carver):
    def add_call(self, function_name, arguments):
        if function_name not in self._calls:
            self._calls[function_name] = []
        if arguments not in self._calls[function_name]:
            self._calls[function_name].append(arguments)
    
    # Tracking function: Record all calls and all args
    def traceit(self, frame, event, arg):
        if event != "call":
            return None
        
        code = frame.f_code
        function_name  = code.co_name
        qualified_name = get_qualified_name(code)

        # When called, all arguments are local variables
        arguments = [(var, frame.f_locals[var]) for var in frame.f_locals]
        arguments.reverse()  # Want same order as call

        self.add_call(function_name, arguments)
        if qualified_name != function_name:
            self.add_call(qualified_name, arguments)

        # Some tracking
        # print(simple_call_string(function_name, args))

        return None

class Carver(Carver):
    def calls(self):
        """Return a dictionary of all calls traced."""  
        return self._calls
    
    def arguments(self, function_name):
        """Return a list of all arguments of the given function
        as (VAR, VALUE) pairs.
        Raises an exception if the function was not traced."""
        return self._calls[function_name]
    
    def called_functions(self, qualified=True):
        """Return all functions called."""
        if qualified:
            return [function_name for function_name in self._calls.keys() if function_name.find('.') >= 0]
        else:
            return [function_name for function_name in self._calls.keys() if function_name.find('.') < 0]

# ### Recording my_sqrt()

if __name__ == "__main__":
    print('\n### Recording my_sqrt()')




if __package__ is None or __package__ == "":
    from Intro_Testing import my_sqrt
else:
    from .Intro_Testing import my_sqrt


if __name__ == "__main__":
    with Carver() as sqrt_carver:
        my_sqrt(2)
        my_sqrt(4)


if __name__ == "__main__":
    sqrt_carver.calls()


if __name__ == "__main__":
    sqrt_carver.arguments("my_sqrt")


def simple_call_string(function_name, argument_list):
    """Return function_name(arg[0], arg[1], ...) as a string"""
    return function_name + "(" + \
        ", ".join([var + "=" + repr(value) for (var, value) in argument_list]) + ")"

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
    with Carver() as webbrowser_carver:
        webbrowser("http://www.example.com")


if __name__ == "__main__":
    print(webbrowser_carver.called_functions())


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
    email_parse_call = simple_call_string("email.parser.parse", email_parse_argument_list[0])
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


def call_string(function_name, argument_list):
    """Return function_name(arg[0], arg[1], ...) as a string, pickling complex objects"""
    def call_value(value):
        value_as_string = repr(value)
        if value_as_string.find('<') >= 0:
            # Complex object
            value_as_string = "pickle.loads(" + repr(pickle.dumps(value)) + ")"
        return value_as_string
    
    if len(argument_list) > 0:
        (first_var, first_value) = argument_list[0]
        if first_var == "self":
            # Make this a method call
            method_name = function_name.split(".")[-1]
            function_name = call_value(first_value) + "." + method_name
            argument_list = argument_list[1:]
    
    return function_name + "(" + \
        ", ".join([var + "=" + call_value(value) for (var, value) in argument_list]) + ")"

if __name__ == "__main__":
    call = call_string("email.parser.parse", email_parse_argument_list[0])
    print(call)


if __name__ == "__main__":
    eval(call)


# ### All Calls

if __name__ == "__main__":
    print('\n### All Calls')




import traceback

import enum, socket

if __name__ == "__main__":
    all_functions = set(webbrowser_carver.called_functions())
    call_success = set()
    run_success = set()


if __name__ == "__main__":
    for function_name in webbrowser_carver.called_functions():
        for argument_list in webbrowser_carver.arguments(function_name):
            try:
                call = call_string(function_name, argument_list)
                call_success.add(function_name)

                result = eval(call)
                run_success.add(function_name)

            except:
                # print("->", call, file=sys.stderr)
                # traceback.print_exc()
                # print("", file=sys.stderr)
                continue


if __name__ == "__main__":
    print("%d/%d calls (%.2f%%) successfully created and %d/%d calls (%.2f%%) successfully ran" % (
        len(call_success), len(all_functions), len(call_success) * 100 / len(all_functions),
        len(run_success), len(all_functions), len(run_success) * 100 / len(all_functions)))


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




# ### Exercise 1: Carving Return Values

if __name__ == "__main__":
    print('\n### Exercise 1: Carving Return Values')



