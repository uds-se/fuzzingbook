#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Mining Function Specifications" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/DynamicInvariants.html
# Last change: 2021-06-02 17:50:08+02:00
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
The Fuzzing Book - Mining Function Specifications

This file can be _executed_ as a script, running all experiments:

    $ python DynamicInvariants.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.DynamicInvariants import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/DynamicInvariants.html

This chapter provides two classes that automatically extract specifications from a function and a set of inputs:

* `TypeAnnotator` for _types_, and
* `InvariantAnnotator` for _pre-_ and _postconditions_.

Both work by _observing_ a function and its invocations within a `with` clause.  Here is an example for the type annotator:

>>> def sum2(a, b):
>>>     return a + b
>>> with TypeAnnotator() as type_annotator:
>>>     sum2(1, 2)
>>>     sum2(-4, -5)
>>>     sum2(0, 0)

The `typed_functions()` method will return a representation of `sum2()` annotated with types observed during execution.

>>> print(type_annotator.typed_functions())
def sum2(a: int, b: int) ->int:
    return a + b



The invariant annotator works in a similar fashion:

>>> with InvariantAnnotator() as inv_annotator:
>>>     sum2(1, 2)
>>>     sum2(-4, -5)
>>>     sum2(0, 0)

The `functions_with_invariants()` method will return a representation of `sum2()` annotated with inferred pre- and postconditions that all hold for the observed values.

>>> print(inv_annotator.functions_with_invariants())
@precondition(lambda a, b: isinstance(a, int))
@precondition(lambda a, b: isinstance(b, int))
@postcondition(lambda return_value, a, b: a == return_value - b)
@postcondition(lambda return_value, a, b: b == return_value - a)
@postcondition(lambda return_value, a, b: isinstance(return_value, int))
@postcondition(lambda return_value, a, b: return_value == a + b)
@postcondition(lambda return_value, a, b: return_value == b + a)
def sum2(a, b):
    return a + b



Such type specifications and invariants can be helpful as _oracles_ (to detect deviations from a given set of runs) as well as for all kinds of _symbolic code analyses_.  The chapter gives details on how to customize the properties checked for.


For more details, source, and documentation, see
"The Fuzzing Book - Mining Function Specifications"
at https://www.fuzzingbook.org/html/DynamicInvariants.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Mining Function Specifications
# ==============================

if __name__ == '__main__':
    print('# Mining Function Specifications')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from . import Coverage
from . import Intro_Testing

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Specifications and Assertions
## -----------------------------

if __name__ == '__main__':
    print('\n## Specifications and Assertions')



def my_sqrt(x):
    assert x >= 0  # Precondition
    
    ...
    
    assert result * result == x  # Postcondition
    return result

## Why Generic Error Checking is Not Enough
## ----------------------------------------

if __name__ == '__main__':
    print('\n## Why Generic Error Checking is Not Enough')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

def my_sqrt(x):
    """Computes the square root of x, using the Newton-Raphson method"""
    approx = None
    guess = x / 2
    while approx != guess:
        approx = guess
        guess = (approx + x / approx) / 2
    return approx

from .ExpectError import ExpectError, ExpectTimeout

if __name__ == '__main__':
    with ExpectError():
        my_sqrt("foo")

if __name__ == '__main__':
    with ExpectError():
        x = my_sqrt(0.0)

if __name__ == '__main__':
    with ExpectTimeout(1):
        x = my_sqrt(-1.0)

## Specifying and Checking Data Types
## ----------------------------------

if __name__ == '__main__':
    print('\n## Specifying and Checking Data Types')



def my_sqrt_with_type_annotations(x: float) -> float:
    """Computes the square root of x, using the Newton-Raphson method"""
    return my_sqrt(x)

### Runtime Type Checking

if __name__ == '__main__':
    print('\n### Runtime Type Checking')



import enforce

@enforce.runtime_validation
def my_sqrt_with_checked_type_annotations(x: float) -> float:
    """Computes the square root of x, using the Newton-Raphson method"""
    return my_sqrt(x)

if __name__ == '__main__':
    with ExpectError():
        my_sqrt_with_checked_type_annotations(True)

if __name__ == '__main__':
    my_sqrt(True)

### Static Type Checking

if __name__ == '__main__':
    print('\n### Static Type Checking')



import inspect
import tempfile

if __name__ == '__main__':
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.py')
    f.name

if __name__ == '__main__':
    f.write(inspect.getsource(my_sqrt))
    f.write('\n')
    f.write(inspect.getsource(my_sqrt_with_type_annotations))
    f.write('\n')
    f.write("print(my_sqrt_with_type_annotations('123'))\n")
    f.flush()

from .bookutils import print_file

if __name__ == '__main__':
    print_file(f.name)

import subprocess

if __name__ == '__main__':
    result = subprocess.run(["mypy", "--strict", f.name], universal_newlines=True, stdout=subprocess.PIPE)
    del f  # Delete temporary file

if __name__ == '__main__':
    print(result.stdout)

## Mining Type Specifications
## --------------------------

if __name__ == '__main__':
    print('\n## Mining Type Specifications')



if __name__ == '__main__':
    y = my_sqrt(25.0)
    y

if __name__ == '__main__':
    y = my_sqrt(2.0)
    y

### Tracking Calls

if __name__ == '__main__':
    print('\n### Tracking Calls')



import sys

class Tracker(object):
    def __init__(self, log=False):
        self._log = log
        self.reset()

    def reset(self):
        self._calls = {}
        self._stack = []

    def traceit(self):
        """Placeholder to be overloaded in subclasses"""
        pass

    # Start of `with` block
    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        sys.settrace(self.original_trace_function)

class CallTracker(Tracker):
    def traceit(self, frame, event, arg):
        """Tracking function: Record all calls and all args"""
        if event == "call":
            self.trace_call(frame, event, arg)
        elif event == "return":
            self.trace_return(frame, event, arg)
            
        return self.traceit

class CallTracker(CallTracker):
    def trace_call(self, frame, event, arg):
        """Save current function name and args on the stack"""
        code = frame.f_code
        function_name = code.co_name
        arguments = get_arguments(frame)
        self._stack.append((function_name, arguments))

        if self._log:
            print(simple_call_string(function_name, arguments))

def get_arguments(frame):
    """Return call arguments in the given frame"""
    # When called, all arguments are local variables
    arguments = [(var, frame.f_locals[var]) for var in frame.f_locals]
    arguments.reverse()  # Want same order as call
    return arguments

class CallTracker(CallTracker):
    def trace_return(self, frame, event, arg):
        """Get return value and store complete call with arguments and return value"""
        code = frame.f_code
        function_name = code.co_name
        return_value = arg
        # TODO: Could call get_arguments() here to also retrieve _final_ values of argument variables
        
        called_function_name, called_arguments = self._stack.pop()
        assert function_name == called_function_name
        
        if self._log:
            print(simple_call_string(function_name, called_arguments), "returns", return_value)
            
        self.add_call(function_name, called_arguments, return_value)

def simple_call_string(function_name, argument_list, return_value=None):
    """Return function_name(arg[0], arg[1], ...) as a string"""
    call = function_name + "(" + \
        ", ".join([var + "=" + repr(value)
                   for (var, value) in argument_list]) + ")"

    if return_value is not None:
        call += " = " + repr(return_value)
        
    return call

class CallTracker(CallTracker):
    def add_call(self, function_name, arguments, return_value=None):
        """Add given call to list of calls"""
        if function_name not in self._calls:
            self._calls[function_name] = []
        self._calls[function_name].append((arguments, return_value))

class CallTracker(CallTracker):
    def calls(self, function_name=None):
        """Return list of calls for function_name, 
        or a mapping function_name -> calls for all functions tracked"""
        if function_name is None:
            return self._calls

        return self._calls[function_name]

if __name__ == '__main__':
    with CallTracker(log=True) as tracker:
        y = my_sqrt(25)
        y = my_sqrt(2.0)

if __name__ == '__main__':
    calls = tracker.calls('my_sqrt')
    calls

if __name__ == '__main__':
    my_sqrt_argument_list, my_sqrt_return_value = calls[0]
    simple_call_string('my_sqrt', my_sqrt_argument_list, my_sqrt_return_value)

def hello(name):
    print("Hello,", name)

if __name__ == '__main__':
    with CallTracker() as tracker:
        hello("world")

if __name__ == '__main__':
    hello_calls = tracker.calls('hello')
    hello_calls

if __name__ == '__main__':
    hello_argument_list, hello_return_value = hello_calls[0]
    simple_call_string('hello', hello_argument_list, hello_return_value)

### Getting Types

if __name__ == '__main__':
    print('\n### Getting Types')



if __name__ == '__main__':
    type(4)

if __name__ == '__main__':
    type(2.0)

if __name__ == '__main__':
    type([4])

if __name__ == '__main__':
    parameter, value = my_sqrt_argument_list[0]
    parameter, type(value)

if __name__ == '__main__':
    type(my_sqrt_return_value)

def my_sqrt_annotated(x: int) -> float:
    return my_sqrt(x)

if __name__ == '__main__':
    my_sqrt_annotated.__annotations__

### Accessing Function Structure

if __name__ == '__main__':
    print('\n### Accessing Function Structure')



import ast
import inspect
import astor

if __name__ == '__main__':
    my_sqrt_source = inspect.getsource(my_sqrt)
    my_sqrt_source

from .bookutils import print_content

if __name__ == '__main__':
    print_content(my_sqrt_source, '.py')

if __name__ == '__main__':
    my_sqrt_ast = ast.parse(my_sqrt_source)

if __name__ == '__main__':
    print(astor.dump_tree(my_sqrt_ast))

from .bookutils import rich_output

if __name__ == '__main__':
    if rich_output():
        import showast
        showast.show_ast(my_sqrt_ast)

if __name__ == '__main__':
    print_content(astor.to_source(my_sqrt_ast), '.py')

### Annotating Functions with Given Types

if __name__ == '__main__':
    print('\n### Annotating Functions with Given Types')



def parse_type(name):
    class ValueVisitor(ast.NodeVisitor):
        def visit_Expr(self, node):
            self.value_node = node.value
        
    tree = ast.parse(name)
    name_visitor = ValueVisitor()
    name_visitor.visit(tree)
    return name_visitor.value_node

if __name__ == '__main__':
    print(astor.dump_tree(parse_type('int')))

if __name__ == '__main__':
    print(astor.dump_tree(parse_type('[object]')))

class TypeTransformer(ast.NodeTransformer):
    def __init__(self, argument_types, return_type=None):
        self.argument_types = argument_types
        self.return_type = return_type
        super().__init__()

class TypeTransformer(TypeTransformer):
    def visit_FunctionDef(self, node):
        """Add annotation to function"""
        # Set argument types
        new_args = []
        for arg in node.args.args:
            new_args.append(self.annotate_arg(arg))

        new_arguments = ast.arguments(
            new_args,
            node.args.vararg,
            node.args.kwonlyargs,
            node.args.kw_defaults,
            node.args.kwarg,
            node.args.defaults
        )

        # Set return type
        if self.return_type is not None:
            node.returns = parse_type(self.return_type)
        
        return ast.copy_location(ast.FunctionDef(node.name, new_arguments, 
                                                 node.body, node.decorator_list,
                                                 node.returns), node)

class TypeTransformer(TypeTransformer):
    def annotate_arg(self, arg):
        """Add annotation to single function argument"""
        arg_name = arg.arg
        if arg_name in self.argument_types:
            arg.annotation = parse_type(self.argument_types[arg_name])
        return arg

if __name__ == '__main__':
    new_ast = TypeTransformer({'x': 'int'}, 'float').visit(my_sqrt_ast)

if __name__ == '__main__':
    print_content(astor.to_source(new_ast), '.py')

if __name__ == '__main__':
    hello_source = inspect.getsource(hello)

if __name__ == '__main__':
    hello_ast = ast.parse(hello_source)

if __name__ == '__main__':
    new_ast = TypeTransformer({'name': 'str'}, 'None').visit(hello_ast)

if __name__ == '__main__':
    print_content(astor.to_source(new_ast), '.py')

### Annotating Functions with Mined Types

if __name__ == '__main__':
    print('\n### Annotating Functions with Mined Types')



def type_string(value):
    return type(value).__name__

if __name__ == '__main__':
    type_string(4)

if __name__ == '__main__':
    type_string([])

if __name__ == '__main__':
    type_string([3])

if __name__ == '__main__':
    with CallTracker() as tracker:
        y = my_sqrt(25.0)
        y = my_sqrt(2.0)

if __name__ == '__main__':
    tracker.calls()

def annotate_types(calls):
    annotated_functions = {}
    
    for function_name in calls:
        try:
            annotated_functions[function_name] = annotate_function_with_types(function_name, calls[function_name])
        except KeyError:
            continue

    return annotated_functions

def annotate_function_with_types(function_name, function_calls):
    function = globals()[function_name]  # May raise KeyError for internal functions
    function_code = inspect.getsource(function)
    function_ast = ast.parse(function_code)
    return annotate_function_ast_with_types(function_ast, function_calls)

from typing import Any

def annotate_function_ast_with_types(function_ast, function_calls):
    parameter_types = {}
    return_type = None

    for calls_seen in function_calls:
        args, return_value = calls_seen
        if return_value is not None:
            if return_type is not None and return_type != type_string(return_value):
                return_type = 'Any'
            else:
                return_type = type_string(return_value)
            
            
        for parameter, value in args:
            try:
                different_type = parameter_types[parameter] != type_string(value)
            except KeyError:
                different_type = False
                
            if different_type:
                parameter_types[parameter] = 'Any'
            else:
                parameter_types[parameter] = type_string(value)
        
    annotated_function_ast = TypeTransformer(parameter_types, return_type).visit(function_ast)
    return annotated_function_ast

if __name__ == '__main__':
    print_content(astor.to_source(annotate_types(tracker.calls())['my_sqrt']), '.py')

### All-in-one Annotation

if __name__ == '__main__':
    print('\n### All-in-one Annotation')



class TypeTracker(CallTracker):
    pass

class TypeAnnotator(TypeTracker):
    def typed_functions_ast(self, function_name=None):
        if function_name is None:
            return annotate_types(self.calls())
        
        return annotate_function_with_types(function_name, self.calls(function_name))
    
    def typed_functions(self, function_name=None):
        if function_name is None:
            functions = ''
            for f_name in self.calls():
                try:
                    f_text = astor.to_source(self.typed_functions_ast(f_name))
                except KeyError:
                    f_text = ''
                functions += f_text
            return functions

        return astor.to_source(self.typed_functions_ast(function_name))

if __name__ == '__main__':
    with TypeAnnotator() as annotator:
        y = my_sqrt(25.0)
        y = my_sqrt(2.0)

if __name__ == '__main__':
    print_content(annotator.typed_functions(), '.py')

if __name__ == '__main__':
    with TypeAnnotator() as annotator:
        hello('type annotations')
        y = my_sqrt(1.0)

if __name__ == '__main__':
    print_content(annotator.typed_functions(), '.py')

### Multiple Types

if __name__ == '__main__':
    print('\n### Multiple Types')



if __name__ == '__main__':
    with CallTracker() as tracker:
        y = my_sqrt(25.0)
        y = my_sqrt(4)

if __name__ == '__main__':
    print_content(astor.to_source(annotate_types(tracker.calls())['my_sqrt']), '.py')

def sum3(a, b, c):
    return a + b + c

if __name__ == '__main__':
    with TypeAnnotator() as annotator:
        y = sum3(1.0, 2.0, 3.0)
    y

if __name__ == '__main__':
    print_content(annotator.typed_functions(), '.py')

if __name__ == '__main__':
    with TypeAnnotator() as annotator:
        y = sum3(1, 2, 3)
    y

if __name__ == '__main__':
    print_content(annotator.typed_functions(), '.py')

if __name__ == '__main__':
    with TypeAnnotator() as annotator:
        y = sum3("one", "two", "three")
    y

if __name__ == '__main__':
    print_content(annotator.typed_functions(), '.py')

if __name__ == '__main__':
    with TypeAnnotator() as annotator:
        y = sum3(1, 2, 3)
        y = sum3("one", "two", "three")

if __name__ == '__main__':
    typed_sum3_def = annotator.typed_functions('sum3')

if __name__ == '__main__':
    print_content(typed_sum3_def, '.py')

## Specifying and Checking Invariants
## ----------------------------------

if __name__ == '__main__':
    print('\n## Specifying and Checking Invariants')



### Annotating Functions with Pre- and Postconditions

if __name__ == '__main__':
    print('\n### Annotating Functions with Pre- and Postconditions')



def my_sqrt_with_invariants(x):
    assert x >= 0  # Precondition
    
    ...
    
    assert result * result == x  # Postcondition
    return result

import functools

def condition(precondition=None, postcondition=None):
    def decorator(func):
        @functools.wraps(func) # preserves name, docstring, etc
        def wrapper(*args, **kwargs):
            if precondition is not None:
               assert precondition(*args, **kwargs), "Precondition violated"

            retval = func(*args, **kwargs) # call original function or method
            if postcondition is not None:
               assert postcondition(retval, *args, **kwargs), "Postcondition violated"

            return retval
        return wrapper
    return decorator

def precondition(check):
    return condition(precondition=check)

def postcondition(check):
    return condition(postcondition=check)

@precondition(lambda x: x > 0)
def my_sqrt_with_precondition(x):
    return my_sqrt(x)

if __name__ == '__main__':
    with ExpectError():
        my_sqrt_with_precondition(-1.0)

EPSILON = 1e-5

@postcondition(lambda ret, x: ret * ret - x < EPSILON)
def my_sqrt_with_postcondition(x):
    return my_sqrt(x)

if __name__ == '__main__':
    y = my_sqrt_with_postcondition(2.0)
    y

@postcondition(lambda ret, x: ret * ret - x < EPSILON)
def buggy_my_sqrt_with_postcondition(x):
    return my_sqrt(x) + 0.1

if __name__ == '__main__':
    with ExpectError():
        y = buggy_my_sqrt_with_postcondition(2.0)

## Mining Invariants
## -----------------

if __name__ == '__main__':
    print('\n## Mining Invariants')



### Defining Properties

if __name__ == '__main__':
    print('\n### Defining Properties')



INVARIANT_PROPERTIES = [
    "X < 0",
    "X <= 0",
    "X > 0",
    "X >= 0",
    "X == 0",
    "X != 0",
]

INVARIANT_PROPERTIES += [
    "X == Y",
    "X > Y",
    "X < Y",
    "X >= Y",
    "X <= Y",
]

INVARIANT_PROPERTIES += [
    "isinstance(X, bool)",
    "isinstance(X, int)",
    "isinstance(X, float)",
    "isinstance(X, list)",
    "isinstance(X, dict)",
]

INVARIANT_PROPERTIES += [
    "X == Y + Z",
    "X == Y * Z",
    "X == Y - Z",
    "X == Y / Z",
]

INVARIANT_PROPERTIES += [
    "X < Y < Z",
    "X <= Y <= Z",
    "X > Y > Z",
    "X >= Y >= Z",
]

INVARIANT_PROPERTIES += [
    "X == len(Y)",
    "X == sum(Y)",
    "X.startswith(Y)",
]

### Extracting Meta-Variables

if __name__ == '__main__':
    print('\n### Extracting Meta-Variables')



def metavars(prop):
    metavar_list = []
    
    class ArgVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            if node.id.isupper():
                metavar_list.append(node.id)

    ArgVisitor().visit(ast.parse(prop))
    return metavar_list

if __name__ == '__main__':
    assert metavars("X < 0") == ['X']

if __name__ == '__main__':
    assert metavars("X.startswith(Y)") == ['X', 'Y']

if __name__ == '__main__':
    assert metavars("isinstance(X, str)") == ['X']

### Instantiating Properties

if __name__ == '__main__':
    print('\n### Instantiating Properties')



def instantiate_prop_ast(prop, var_names):
    class NameTransformer(ast.NodeTransformer):
        def visit_Name(self, node):
            if node.id not in mapping:
                return node
            return ast.Name(id=mapping[node.id], ctx=ast.Load())
    
    meta_variables = metavars(prop)
    assert len(meta_variables) == len(var_names)

    mapping = {}
    for i in range(0, len(meta_variables)):
        mapping[meta_variables[i]] = var_names[i]

    prop_ast = ast.parse(prop, mode='eval')
    new_ast = NameTransformer().visit(prop_ast)

    return new_ast

def instantiate_prop(prop, var_names):
    prop_ast = instantiate_prop_ast(prop, var_names)
    prop_text = astor.to_source(prop_ast).strip()
    while prop_text.startswith('(') and prop_text.endswith(')'):
        prop_text = prop_text[1:-1]
    return prop_text

if __name__ == '__main__':
    assert instantiate_prop("X > Y", ['a', 'b']) == 'a > b'

if __name__ == '__main__':
    assert instantiate_prop("X.startswith(Y)", ['x', 'y']) == 'x.startswith(y)'

### Evaluating Properties

if __name__ == '__main__':
    print('\n### Evaluating Properties')



def prop_function_text(prop):
    return "lambda " + ", ".join(metavars(prop)) + ": " + prop

def prop_function(prop):
    return eval(prop_function_text(prop))

if __name__ == '__main__':
    prop_function_text("X > Y")

if __name__ == '__main__':
    p = prop_function("X > Y")
    p(100, 1)

if __name__ == '__main__':
    p(1, 100)

### Checking Invariants

if __name__ == '__main__':
    print('\n### Checking Invariants')



import itertools

if __name__ == '__main__':
    for combination in itertools.permutations([1.0, 2.0, 3.0], 2):
        print(combination)

def true_property_instantiations(prop, vars_and_values, log=False):
    instantiations = set()
    p = prop_function(prop)

    len_metavars = len(metavars(prop))
    for combination in itertools.permutations(vars_and_values, len_metavars):
        args = [value for var_name, value in combination]
        var_names = [var_name for var_name, value in combination]
        
        try:
            result = p(*args)
        except:
            result = None

        if log:
            print(prop, combination, result)
        if result:
            instantiations.add((prop, tuple(var_names)))
            
    return instantiations

if __name__ == '__main__':
    invs = true_property_instantiations("X < Y", [('x', -1), ('y', 1)], log=True)
    invs

if __name__ == '__main__':
    for prop, var_names in invs:
        print(instantiate_prop(prop, var_names))

if __name__ == '__main__':
    invs = true_property_instantiations("X < 0", [('x', -1), ('y', 1)], log=True)

if __name__ == '__main__':
    for prop, var_names in invs:
        print(instantiate_prop(prop, var_names))

### Extracting Invariants

if __name__ == '__main__':
    print('\n### Extracting Invariants')



class InvariantTracker(CallTracker):
    def __init__(self, props=None, **kwargs):
        if props is None:
            props = INVARIANT_PROPERTIES

        self.props = props
        super().__init__(**kwargs)

RETURN_VALUE = 'return_value'

class InvariantTracker(InvariantTracker):
    def invariants(self, function_name=None):
        if function_name is None:
            return {function_name: self.invariants(function_name) for function_name in self.calls()}
        
        invariants = None
        for variables, return_value in self.calls(function_name):
            vars_and_values = variables + [(RETURN_VALUE, return_value)]
            
            s = set()
            for prop in self.props:
                s |= true_property_instantiations(prop, vars_and_values, self._log)
            if invariants is None:
                invariants = s
            else:
                invariants &= s

        return invariants

if __name__ == '__main__':
    with InvariantTracker() as tracker:
        y = my_sqrt(25.0)
        y = my_sqrt(10.0)

    tracker.calls()

if __name__ == '__main__':
    invs = tracker.invariants('my_sqrt')
    invs

def pretty_invariants(invariants):
    props = []
    for (prop, var_names) in invariants:
        props.append(instantiate_prop(prop, var_names))
    return sorted(props)

if __name__ == '__main__':
    pretty_invariants(invs)

if __name__ == '__main__':
    my_sqrt(0.01)

if __name__ == '__main__':
    with InvariantTracker() as tracker:
        y = my_sqrt(25.0)
        y = my_sqrt(10.0)
        y = my_sqrt(0.01)

    pretty_invariants(tracker.invariants('my_sqrt'))

if __name__ == '__main__':
    with InvariantTracker() as tracker:
        y = sum3(1, 2, 3)
        y = sum3(-4, -5, -6)

    pretty_invariants(tracker.invariants('sum3'))

if __name__ == '__main__':
    with InvariantTracker() as tracker:
        y = sum3('a', 'b', 'c')
        y = sum3('f', 'e', 'd')

    pretty_invariants(tracker.invariants('sum3'))

if __name__ == '__main__':
    with InvariantTracker() as tracker:
        y = sum3('a', 'b', 'c')
        y = sum3('c', 'b', 'a')
        y = sum3(-4, -5, -6)
        y = sum3(0, 0, 0)

    pretty_invariants(tracker.invariants('sum3'))

### Converting Mined Invariants to Annotations

if __name__ == '__main__':
    print('\n### Converting Mined Invariants to Annotations')



class InvariantAnnotator(InvariantTracker):
    def params(self, function_name):
        arguments, return_value = self.calls(function_name)[0]
        return ", ".join(arg_name for (arg_name, arg_value) in arguments)

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        y = my_sqrt(25.0)
        y = sum3(1, 2, 3)

if __name__ == '__main__':
    annotator.params('my_sqrt')

if __name__ == '__main__':
    annotator.params('sum3')

class InvariantAnnotator(InvariantAnnotator):
    def preconditions(self, function_name):
        conditions = []

        for inv in pretty_invariants(self.invariants(function_name)):
            if inv.find(RETURN_VALUE) >= 0:
                continue  # Postcondition

            cond = "@precondition(lambda " + self.params(function_name) + ": " + inv + ")"
            conditions.append(cond)

        return conditions

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        y = my_sqrt(25.0)
        y = my_sqrt(0.01)
        y = sum3(1, 2, 3)

if __name__ == '__main__':
    annotator.preconditions('my_sqrt')

class InvariantAnnotator(InvariantAnnotator):
    def postconditions(self, function_name):
        conditions = []

        for inv in pretty_invariants(self.invariants(function_name)):
            if inv.find(RETURN_VALUE) < 0:
                continue  # Precondition

            cond = ("@postcondition(lambda " + 
                RETURN_VALUE + ", " + self.params(function_name) + ": " + inv + ")")
            conditions.append(cond)

        return conditions

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        y = my_sqrt(25.0)
        y = my_sqrt(0.01)
        y = sum3(1, 2, 3)

if __name__ == '__main__':
    annotator.postconditions('my_sqrt')

class InvariantAnnotator(InvariantAnnotator):
    def functions_with_invariants(self):
        functions = ""
        for function_name in self.invariants():
            try:
                function = self.function_with_invariants(function_name)
            except KeyError:
                continue
            functions += function
        return functions

    def function_with_invariants(self, function_name):
        function = globals()[function_name]  # Can throw KeyError
        source = inspect.getsource(function)
        return "\n".join(self.preconditions(function_name) + 
                         self.postconditions(function_name)) + '\n' + source

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        y = my_sqrt(25.0)
        y = my_sqrt(0.01)
        y = sum3(1, 2, 3)

if __name__ == '__main__':
    print_content(annotator.function_with_invariants('my_sqrt'), '.py')

### Some Examples

if __name__ == '__main__':
    print('\n### Some Examples')



def list_length(L):
    if L == []:
        length = 0
    else:
        length = 1 + list_length(L[1:])
    return length

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        length = list_length([1, 2, 3])

    print_content(annotator.functions_with_invariants(), '.py')

def sum2(a, b):
    return a + b

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        sum2(31, 45)
        sum2(0, 0)
        sum2(-1, -5)

if __name__ == '__main__':
    print_content(annotator.functions_with_invariants(), '.py')

def print_sum(a, b):
    print(a + b)

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        print_sum(31, 45)
        print_sum(0, 0)
        print_sum(-1, -5)

if __name__ == '__main__':
    print_content(annotator.functions_with_invariants(), '.py')

### Checking Specifications

if __name__ == '__main__':
    print('\n### Checking Specifications')



if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        y = my_sqrt(25.0)
        y = my_sqrt(0.01)

if __name__ == '__main__':
    my_sqrt_def = annotator.functions_with_invariants()
    my_sqrt_def = my_sqrt_def.replace('my_sqrt', 'my_sqrt_annotated')

if __name__ == '__main__':
    print_content(my_sqrt_def, '.py')

if __name__ == '__main__':
    exec(my_sqrt_def)

if __name__ == '__main__':
    with ExpectError():
        my_sqrt_annotated(-1.0)

if __name__ == '__main__':
    with ExpectTimeout(1):
        my_sqrt(-1.0)

if __name__ == '__main__':
    my_sqrt_def = my_sqrt_def.replace('my_sqrt_annotated', 'my_sqrt_negative')
    my_sqrt_def = my_sqrt_def.replace('return approx', 'return -approx')

if __name__ == '__main__':
    print_content(my_sqrt_def, '.py')

if __name__ == '__main__':
    exec(my_sqrt_def)

if __name__ == '__main__':
    with ExpectError():
        my_sqrt_negative(2.0)

## Mining Specifications from Generated Tests
## ------------------------------------------

if __name__ == '__main__':
    print('\n## Mining Specifications from Generated Tests')



def sum2(a, b):
    return a + b

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        y = sum2(2, 2)
    print_content(annotator.functions_with_invariants(), '.py')

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        length = sum2(1, 2)
        length = sum2(-1, -2)
        length = sum2(0, 0)

    print_content(annotator.functions_with_invariants(), '.py')

from .GrammarFuzzer import GrammarFuzzer  # minor dependency
from .Grammars import is_valid_grammar, crange, convert_ebnf_grammar  # minor dependency

SUM2_EBNF_GRAMMAR = {
    "<start>": ["<sum2>"],
    "<sum2>": ["sum2(<int>, <int>)"],
    "<int>": ["<_int>"],
    "<_int>": ["(-)?<leaddigit><digit>*", "0"],
    "<leaddigit>": crange('1', '9'),
    "<digit>": crange('0', '9')
}

assert is_valid_grammar(SUM2_EBNF_GRAMMAR)

if __name__ == '__main__':
    sum2_grammar =  convert_ebnf_grammar(SUM2_EBNF_GRAMMAR)

if __name__ == '__main__':
    sum2_fuzzer = GrammarFuzzer(sum2_grammar)
    [sum2_fuzzer.fuzz() for i in range(10)]

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        for i in range(10):
            eval(sum2_fuzzer.fuzz())

    print_content(annotator.function_with_invariants('sum2'), '.py')

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



def sum2(a, b):
    return a + b

if __name__ == '__main__':
    with TypeAnnotator() as type_annotator:
        sum2(1, 2)
        sum2(-4, -5)
        sum2(0, 0)

if __name__ == '__main__':
    print(type_annotator.typed_functions())

if __name__ == '__main__':
    with InvariantAnnotator() as inv_annotator:
        sum2(1, 2)
        sum2(-4, -5)
        sum2(0, 0)

if __name__ == '__main__':
    print(inv_annotator.functions_with_invariants())

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



### Exercise 1: Union Types

if __name__ == '__main__':
    print('\n### Exercise 1: Union Types')



from typing import Union, Optional

def my_sqrt_with_union_type(x: Union[int, float]) -> float:
    ...

### Exercise 2: Types for Local Variables

if __name__ == '__main__':
    print('\n### Exercise 2: Types for Local Variables')



def my_sqrt_with_local_types(x: Union[int, float]) -> float:
    """Computes the square root of x, using the Newton-Raphson method"""
    approx: Optional[float] = None
    guess: float = x / 2
    while approx != guess:
        approx: float = guess
        guess: float = (approx + x / approx) / 2
    return approx

### Exercise 3: Verbose Invariant Checkers

if __name__ == '__main__':
    print('\n### Exercise 3: Verbose Invariant Checkers')



@precondition(lambda s: len(s) > 0)
def remove_first_char(s):
    return s[1:]

if __name__ == '__main__':
    with ExpectError():
        remove_first_char('')

def condition(precondition=None, postcondition=None, doc='Unknown'):
   def decorator(func):
       @functools.wraps(func) # preserves name, docstring, etc
       def wrapper(*args, **kwargs):
           if precondition is not None:
               assert precondition(*args, **kwargs), "Precondition violated: " + doc

           retval = func(*args, **kwargs) # call original function or method
           if postcondition is not None:
               assert postcondition(retval, *args, **kwargs), "Postcondition violated: " + doc

           return retval
       return wrapper
   return decorator

def precondition(check, **kwargs):
   return condition(precondition=check, doc=kwargs.get('doc', 'Unknown'))

def postcondition(check, **kwargs):
   return condition(postcondition=check, doc=kwargs.get('doc', 'Unknown'))

@precondition(lambda s: len(s) > 0, doc="len(s) > 0")
def remove_first_char(s):
    return s[1:]

remove_first_char('abc')

if __name__ == '__main__':
    with ExpectError():
        remove_first_char('')

class InvariantAnnotator(InvariantAnnotator):
   def preconditions(self, function_name):
       conditions = []

       for inv in pretty_invariants(self.invariants(function_name)):
           if inv.find(RETURN_VALUE) >= 0:
               continue  # Postcondition

           cond = "@precondition(lambda " + self.params(function_name) + ": " + inv + ', doc=' + repr(inv) + ")"
           conditions.append(cond)

       return conditions

class InvariantAnnotator(InvariantAnnotator):
   def postconditions(self, function_name):
       conditions = []

       for inv in pretty_invariants(self.invariants(function_name)):
           if inv.find(RETURN_VALUE) < 0:
               continue  # Precondition

           cond = ("@postcondition(lambda " + 
               RETURN_VALUE + ", " + self.params(function_name) + ": " + inv + ', doc=' + repr(inv) + ")")
           conditions.append(cond)

       return conditions

if __name__ == '__main__':
    with InvariantAnnotator() as annotator:
        y = sum2(2, 2)
    print_content(annotator.functions_with_invariants(), '.py')

### Exercise 4: Save Initial Values

if __name__ == '__main__':
    print('\n### Exercise 4: Save Initial Values')



### Exercise 5: Implications

if __name__ == '__main__':
    print('\n### Exercise 5: Implications')



### Exercise 6: Local Variables

if __name__ == '__main__':
    print('\n### Exercise 6: Local Variables')



### Exercise 7: Exploring Invariant Alternatives

if __name__ == '__main__':
    print('\n### Exercise 7: Exploring Invariant Alternatives')



### Exercise 8: Grammar-Generated Properties

if __name__ == '__main__':
    print('\n### Exercise 8: Grammar-Generated Properties')



### Exercise 9: Embedding Invariants as Assertions

if __name__ == '__main__':
    print('\n### Exercise 9: Embedding Invariants as Assertions')



class EmbeddedInvariantAnnotator(InvariantTracker):
    def functions_with_invariants_ast(self, function_name=None):
        if function_name is None:
            return annotate_functions_with_invariants(self.invariants())
        
        return annotate_function_with_invariants(function_name, self.invariants(function_name))
    
    def functions_with_invariants(self, function_name=None):
        if function_name is None:
            functions = ''
            for f_name in self.invariants():
                try:
                    f_text = astor.to_source(self.functions_with_invariants_ast(f_name))
                except KeyError:
                    f_text = ''
                functions += f_text
            return functions

        return astor.to_source(self.functions_with_invariants_ast(function_name))
    
    def function_with_invariants(self, function_name):
        return self.functions_with_invariants(function_name)
    def function_with_invariants_ast(self, function_name):
        return self.functions_with_invariants_ast(function_name)

def annotate_invariants(invariants):
    annotated_functions = {}
    
    for function_name in invariants:
        try:
            annotated_functions[function_name] = annotate_function_with_invariants(function_name, invariants[function_name])
        except KeyError:
            continue

    return annotated_functions

def annotate_function_with_invariants(function_name, function_invariants):
    function = globals()[function_name]
    function_code = inspect.getsource(function)
    function_ast = ast.parse(function_code)
    return annotate_function_ast_with_invariants(function_ast, function_invariants)

def annotate_function_ast_with_invariants(function_ast, function_invariants):
    annotated_function_ast = EmbeddedInvariantTransformer(function_invariants).visit(function_ast)
    return annotated_function_ast

class PreconditionTransformer(ast.NodeTransformer):
    def __init__(self, invariants):
        self.invariants = invariants
        super().__init__()
        
    def preconditions(self):
        preconditions = []
        for (prop, var_names) in self.invariants:
            assertion = "assert " + instantiate_prop(prop, var_names) + ', "violated precondition"'
            assertion_ast = ast.parse(assertion)

            if assertion.find(RETURN_VALUE) < 0:
                preconditions += assertion_ast.body

        return preconditions
    
    def insert_assertions(self, body):
        preconditions = self.preconditions()
        try:
            docstring = body[0].value.s
        except:
            docstring = None
            
        if docstring:
            return [body[0]] + preconditions + body[1:]
        else:
            return preconditions + body

    def visit_FunctionDef(self, node):
        """Add invariants to function"""
        # print(ast.dump(node))
        node.body = self.insert_assertions(node.body)
        return node    

class EmbeddedInvariantTransformer(PreconditionTransformer):
    pass

if __name__ == '__main__':
    with EmbeddedInvariantAnnotator() as annotator:
        my_sqrt(5)

if __name__ == '__main__':
    print_content(annotator.functions_with_invariants(), '.py')

if __name__ == '__main__':
    with EmbeddedInvariantAnnotator() as annotator:
        y = sum3(3, 4, 5)
        y = sum3(-3, -4, -5)
        y = sum3(0, 0, 0)

if __name__ == '__main__':
    print_content(annotator.functions_with_invariants(), '.py')

class EmbeddedInvariantTransformer(PreconditionTransformer):
    def postconditions(self):
        postconditions = []

        for (prop, var_names) in self.invariants:
            assertion = "assert " + instantiate_prop(prop, var_names) + ', "violated postcondition"'
            assertion_ast = ast.parse(assertion)

            if assertion.find(RETURN_VALUE) >= 0:
                postconditions += assertion_ast.body

        return postconditions
    
    def insert_assertions(self, body):
        new_body = super().insert_assertions(body)
        postconditions = self.postconditions()

        body_ends_with_return = isinstance(new_body[-1], ast.Return)
        if body_ends_with_return:
            saver = RETURN_VALUE + " = " + astor.to_source(new_body[-1].value)
        else:
            saver = RETURN_VALUE + " = None"
    
        saver_ast = ast.parse(saver)
        postconditions = [saver_ast] + postconditions

        if body_ends_with_return:
            return new_body[:-1] + postconditions + [new_body[-1]]
        else:
            return new_body + postconditions

if __name__ == '__main__':
    with EmbeddedInvariantAnnotator() as annotator:
        my_sqrt(5)

if __name__ == '__main__':
    my_sqrt_def = annotator.functions_with_invariants()

if __name__ == '__main__':
    print_content(my_sqrt_def, '.py')

if __name__ == '__main__':
    exec(my_sqrt_def.replace('my_sqrt', 'my_sqrt_annotated'))

if __name__ == '__main__':
    with ExpectError():
        my_sqrt_annotated(-1)

if __name__ == '__main__':
    with EmbeddedInvariantAnnotator() as annotator:
        y = sum3(3, 4, 5)
        y = sum3(-3, -4, -5)
        y = sum3(0, 0, 0)

if __name__ == '__main__':
    print_content(annotator.functions_with_invariants(), '.py')

if __name__ == '__main__':
    with EmbeddedInvariantAnnotator() as annotator:
        length = list_length([1, 2, 3])

    print_content(annotator.functions_with_invariants(), '.py')

if __name__ == '__main__':
    with EmbeddedInvariantAnnotator() as annotator:
        print_sum(31, 45)

if __name__ == '__main__':
    print_content(annotator.functions_with_invariants(), '.py')
