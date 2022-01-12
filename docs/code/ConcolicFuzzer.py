#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Concolic Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/ConcolicFuzzer.html
# Last change: 2022-01-12 11:20:51+01:00
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
The Fuzzing Book - Concolic Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python ConcolicFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.ConcolicFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/ConcolicFuzzer.html

This chapter defines two main classes: `SimpleConcolicFuzzer` and `ConcolicGrammarFuzzer`. The `SimpleConcolicFuzzer` first uses a sample input to collect predicates encountered. The fuzzer then negates random predicates to generate new input constraints. These, when solved, produce inputs that explore paths that are close to the original path.

### ConcolicTracer

At the heart of both fuzzers lies the concept of a _concolic tracer_, capturing symbolic variables and path conditions as a program gets executed.

`ConcolicTracer` is used in a `with` block; the syntax `tracer[function]` executes `function` within the `tracer` while capturing conditions. Here is an example for the `cgi_decode()` function:

>>> with ConcolicTracer() as _:
>>>     _[cgi_decode]('a%20d')

Once executed, we can retrieve the symbolic variables in the `decls` attribute. This is a mapping of symbolic variables to types.

>>> _.decls
{'cgi_decode_s_str_1': 'String'}

The extracted path conditions can be found in the `path` attribute:

>>> _.path
[0 < Length(cgi_decode_s_str_1),
 Not(str.substr(cgi_decode_s_str_1, 0, 1) == "+"),
 Not(str.substr(cgi_decode_s_str_1, 0, 1) == "%"),
 1 < Length(cgi_decode_s_str_1),
 Not(str.substr(cgi_decode_s_str_1, 1, 1) == "+"),
 str.substr(cgi_decode_s_str_1, 1, 1) == "%",
 Not(str.substr(cgi_decode_s_str_1, 2, 1) == "0"),
 Not(str.substr(cgi_decode_s_str_1, 2, 1) == "1"),
 str.substr(cgi_decode_s_str_1, 2, 1) == "2",
 str.substr(cgi_decode_s_str_1, 3, 1) == "0",
 4 < Length(cgi_decode_s_str_1),
 Not(str.substr(cgi_decode_s_str_1, 4, 1) == "+"),
 Not(str.substr(cgi_decode_s_str_1, 4, 1) == "%"),
 Not(5 < Length(cgi_decode_s_str_1))]

The `context` attribute holds a pair of `decls` and `path` attributes; this is useful for passing it into the `ConcolicTracer` constructor.

>>> assert _.context == (_.decls, _.path)

We can solve these constraints to obtain a value for the function parameters that follow the same path as the original (traced) invocation:

>>> _.zeval()
('sat', {'s': ('A%20B', 'String')})

The `zeval()` function also allows to pass _alternate_ or _negated_ constraints. See the chapter for examples.
### SimpleConcolicFuzzer

The constraints obtained from `ConcolicTracer` are added to the concolic fuzzer as follows:

>>> scf = SimpleConcolicFuzzer()
>>> scf.add_trace(_, 'a%20d')

The concolic fuzzer then uses the constraints added to guide its fuzzing as follows:

>>> scf = SimpleConcolicFuzzer()
>>> for i in range(20):
>>>     v = scf.fuzz()
>>>     if v is None:
>>>         break
>>>     print(repr(v))
>>>     with ExpectError(print_traceback=False):
>>>         with ConcolicTracer() as _:
>>>             _[cgi_decode](v)
>>>     scf.add_trace(_, v)
' '
'%'
'AB'
''
'ABC'

IndexError: string index out of range (expected)

'A'
'AB+'
'AB'
'ABCD'
'ABC+'
'A'
'ABC'
'ABC%'
'A%'
'ABC+DE'

IndexError: string index out of range (expected)
IndexError: string index out of range (expected)

'AB'
'AB+'
'A'
'ABCD'
'A'


We see how the additional inputs generated explore additional paths.
### ConcolicGrammarFuzzer

The `SimpleConcolicFuzzer` simply explores all paths near the original path traversed by the sample input. It uses a simple mechanism to explore the paths that are near the paths that it knows about, and other than code paths, knows nothing about the input.

The `ConcolicGrammarFuzzer` on the other hand, knows about the input grammar, and can collect feedback from the subject under fuzzing. It can lift some of the constraints encountered to the grammar, enabling deeper fuzzing. It is used as follows:

>>> from InformationFlow import INVENTORY_GRAMMAR, SQLException
>>> cgf = ConcolicGrammarFuzzer(INVENTORY_GRAMMAR)
>>> cgf.prune_tokens(prune_tokens)
>>> for i in range(10):
>>>     query = cgf.fuzz()
>>>     print(query)
>>>     with ConcolicTracer() as _:
>>>         with ExpectError(print_traceback=False):
>>>             try:
>>>                 res = _[db_select](query)
>>>                 print(repr(res))
>>>             except SQLException as e:
>>>                 print(e)
>>>         cgf.update_grammar(_)
>>>         print()
insert into W (Ru_2,.Wj186518W8) values ('@','}','h')
Table ('W') was not found

select S>R(j),A from C3 where U4==9249
Table ('C3') was not found

select I/I*U/n1(M),T/E*d(S) from months
Invalid WHERE ('(I/I*U/n1(M),T/E*d(S))')

select (v==X),t,h,E from vehicles where r8(w)B/P(g)

select x/z+.(L)-h from vehicles where -9!=Y>G(A)

delete from h4OB60J where K-w/MA) from months where B(e,R)>D


TypeError: 'NotImplementedType' object is not callable (expected)
TypeError: 'NotImplementedType' object is not callable (expected)
TypeError: 'NotImplementedType' object is not callable (expected)
TypeError: 'NotImplementedType' object is not callable (expected)

For more details, source, and documentation, see
"The Fuzzing Book - Concolic Fuzzing"
at https://www.fuzzingbook.org/html/ConcolicFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Concolic Fuzzing
# ================

if __name__ == '__main__':
    print('# Concolic Fuzzing')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo('5jBfa1njy18')

if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from typing import List, Callable, Dict, Tuple

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Tracking Constraints
## --------------------

if __name__ == '__main__':
    print('\n## Tracking Constraints')



def factorial(n):
    if n < 0:
        return None

    if n == 0:
        return 1

    if n == 1:
        return 1

    v = 1
    while n != 0:
        v = v * n
        n = n - 1

    return v

if __name__ == '__main__':
    factorial(5)

from .Coverage import Coverage

import inspect

class ArcCoverage(Coverage):
    def traceit(self, frame, event, args):
        if event != 'return':
            f = inspect.getframeinfo(frame)
            self._trace.append((f.function, f.lineno))
        return self.traceit

    def arcs(self):
        t = [i for f, i in self._trace]
        return list(zip(t, t[1:]))

if __name__ == '__main__':
    with ArcCoverage() as cov:
        factorial(5)

from .ControlFlow import to_graph, gen_cfg

if __name__ == '__main__':
    to_graph(gen_cfg(inspect.getsource(factorial)), arcs=cov.arcs())

## Concolic Execution
## ------------------

if __name__ == '__main__':
    print('\n## Concolic Execution')



if __name__ == '__main__':
    lines = [i[1] for i in cov._trace if i[0] == 'factorial']
    src = {i + 1: s for i, s in enumerate(
        inspect.getsource(factorial).split('\n'))}

if __name__ == '__main__':
    src[1]

if __name__ == '__main__':
    src[2], src[3], src[4], src[5]

## Solving Constraints
## -------------------

if __name__ == '__main__':
    print('\n## Solving Constraints')



import z3  # type: ignore

if __name__ == '__main__':
    z3_ver = z3.get_version()

if __name__ == '__main__':
    print(z3_ver)

if __name__ == '__main__':
    assert z3_ver >= (4, 8, 13, 0), \
        f"Please install z3-solver 4.8.13.0 or later - you have {z3_ver}"

if __name__ == '__main__':
    z3.set_option('timeout', 30 * 1000)  # milliseconds

if __name__ == '__main__':
    zn = z3.Int('n')

if __name__ == '__main__':
    zn < 0

if __name__ == '__main__':
    z3.Not(zn < 0)

if __name__ == '__main__':
    z3.solve(z3.Not(zn < 0))

if __name__ == '__main__':
    x = z3.Real('x')
    eqn = (2 * x**2 - 11 * x + 5 == 0)
    z3.solve(eqn)

if __name__ == '__main__':
    z3.solve(x != 5, eqn)

if __name__ == '__main__':
    z3.solve(zn < 0)

if __name__ == '__main__':
    with cov as cov:
        factorial(-1)

if __name__ == '__main__':
    to_graph(gen_cfg(inspect.getsource(factorial)), arcs=cov.arcs())

if __name__ == '__main__':
    src[5]

if __name__ == '__main__':
    predicates = [z3.Not(zn < 0), z3.Not(zn == 0)]

if __name__ == '__main__':
    src[8]

if __name__ == '__main__':
    predicates = [z3.Not(zn < 0), z3.Not(zn == 0), z3.Not(zn == 1)]

if __name__ == '__main__':
    last = len(predicates) - 1
    z3.solve(predicates[0:-1] + [z3.Not(predicates[-1])])

## A Concolic Tracer
## -----------------

if __name__ == '__main__':
    print('\n## A Concolic Tracer')



### Excursion: Implementing ConcolicTracer

if __name__ == '__main__':
    print('\n### Excursion: Implementing ConcolicTracer')



class ConcolicTracer:
    """Trace function execution, tracking variables and path conditions"""

    def __init__(self, context=None):
        """Constructor."""
        self.context = context if context is not None else ({}, [])
        self.decls, self.path = self.context

class ConcolicTracer(ConcolicTracer):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        return

class ConcolicTracer(ConcolicTracer):
    def __getitem__(self, fn):
        self.fn = fn
        self.fn_args = {i: None for i in inspect.signature(fn).parameters}
        return self

class ConcolicTracer(ConcolicTracer):
    def __call__(self, *args):
        self.result = self.fn(*self.concolic(args))
        return self.result

class ConcolicTracer(ConcolicTracer):
    def concolic(self, args):
        return args

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[factorial](1)

if __name__ == '__main__':
    _.decls

if __name__ == '__main__':
    _.path

#### Concolic Proxy Objects

if __name__ == '__main__':
    print('\n#### Concolic Proxy Objects')



def zproxy_create(cls, z_type, z3var, context, z_name, v=None):
    z_value = cls(context, z3var(z_name), v)
    context[0][z_name] = z_type  # add to decls
    return z_value

#### A Proxy Class for Booleans

if __name__ == '__main__':
    print('\n#### A Proxy Class for Booleans')



class zbool:
    @classmethod
    def create(cls, context, z_name, v):
        return zproxy_create(cls, 'Bool', z3.Bool, context, z_name, v)

    def __init__(self, context, z, v=None):
        self.context = context
        self.z = z
        self.v = v
        self.decl, self.path = self.context

if __name__ == '__main__':
    with ConcolicTracer() as _:
        val = zbool.create(_.context, 'my_bool_arg', True)

if __name__ == '__main__':
    val.z

if __name__ == '__main__':
    val.v

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    val.context

##### Negation of Encoded formula

if __name__ == '__main__':
    print('\n##### Negation of Encoded formula')



class zbool(zbool):
    def __not__(self):
        return zbool(self.context, z3.Not(self.z), not self.v)

if __name__ == '__main__':
    with ConcolicTracer() as _:
        val = zbool.create(_.context, 'my_bool_arg', True).__not__()

if __name__ == '__main__':
    val.z

if __name__ == '__main__':
    val.v

if __name__ == '__main__':
    _.context

##### Registering Predicates on Conditionals

if __name__ == '__main__':
    print('\n##### Registering Predicates on Conditionals')



class zbool(zbool):
    def __bool__(self):
        r, pred = (True, self.z) if self.v else (False, z3.Not(self.z))
        self.path.append(pred)
        return r

if __name__ == '__main__':
    ca = 5
    za = z3.Int('a')

if __name__ == '__main__':
    with ConcolicTracer() as _:
        if zbool(_.context, za == z3.IntVal(5), ca == 5):
            print('success')

if __name__ == '__main__':
    _.path

#### A Proxy Class for Integers

if __name__ == '__main__':
    print('\n#### A Proxy Class for Integers')



class zint(int):
    def __new__(cls, context, zn, v, *args, **kw):
        return int.__new__(cls, v, *args, **kw)

class zint(zint):
    @classmethod
    def create(cls, context, zn, v=None):
        return zproxy_create(cls, 'Int', z3.Int, context, zn, v)

    def __init__(self, context, z, v=None):
        self.z, self.v = z, v
        self.context = context

class zint(zint):
    def __int__(self):
        return self.v

    def __pos__(self):
        return self.v

if __name__ == '__main__':
    with ConcolicTracer() as _:
        val = zint.create(_.context, 'int_arg', 0)

if __name__ == '__main__':
    val.z

if __name__ == '__main__':
    val.v

if __name__ == '__main__':
    _.context

class zint(zint):
    def _zv(self, o):
        return (o.z, o.v) if isinstance(o, zint) else (z3.IntVal(o), o)

if __name__ == '__main__':
    with ConcolicTracer() as _:
        val = zint.create(_.context, 'int_arg', 0)

if __name__ == '__main__':
    val._zv(0)

if __name__ == '__main__':
    val._zv(val)

##### Equality between Integers

if __name__ == '__main__':
    print('\n##### Equality between Integers')



class zint(zint):
    def __ne__(self, other):
        z, v = self._zv(other)
        return zbool(self.context, self.z != z, self.v != v)

    def __eq__(self, other):
        z, v = self._zv(other)
        return zbool(self.context, self.z == z, self.v == v)

class zint(zint):
    def __req__(self, other):
        return self.__eq__(other)

if __name__ == '__main__':
    with ConcolicTracer() as _:
        ia = zint.create(_.context, 'int_a', 0)
        ib = zint.create(_.context, 'int_b', 0)
        v1 = ia == ib
        v2 = ia != ib
        v3 = 0 != ib
        print(v1.z, v2.z, v3.z)

##### Comparisons between Integers

if __name__ == '__main__':
    print('\n##### Comparisons between Integers')



class zint(zint):
    def __lt__(self, other):
        z, v = self._zv(other)
        return zbool(self.context, self.z < z, self.v < v)

    def __gt__(self, other):
        z, v = self._zv(other)
        return zbool(self.context, self.z > z, self.v > v)

class zint(zint):
    def __le__(self, other):
        z, v = self._zv(other)
        return zbool(self.context, z3.Or(self.z < z, self.z == z),
                     self.v < v or self.v == v)

    def __ge__(self, other):
        z, v = self._zv(other)
        return zbool(self.context, z3.Or(self.z > z, self.z == z),
                     self.v > v or self.v == v)

if __name__ == '__main__':
    with ConcolicTracer() as _:
        ia = zint.create(_.context, 'int_a', 0)
        ib = zint.create(_.context, 'int_b', 1)
        v1 = ia > ib
        v2 = ia < ib
        print(v1.z, v2.z)
        v3 = ia >= ib
        v4 = ia <= ib
        print(v3.z, v4.z)

##### Binary Operators for Integers

if __name__ == '__main__':
    print('\n##### Binary Operators for Integers')



INT_BINARY_OPS = [
    '__add__',
    '__sub__',
    '__mul__',
    '__truediv__',
    # '__div__',
    '__mod__',
    # '__divmod__',
    '__pow__',
    # '__lshift__',
    # '__rshift__',
    # '__and__',
    # '__xor__',
    # '__or__',
    '__radd__',
    '__rsub__',
    '__rmul__',
    '__rtruediv__',
    # '__rdiv__',
    '__rmod__',
    # '__rdivmod__',
    '__rpow__',
    # '__rlshift__',
    # '__rrshift__',
    # '__rand__',
    # '__rxor__',
    # '__ror__',
]

def make_int_binary_wrapper(fname, fun, zfun):  # type: ignore
    def proxy(self, other):
        z, v = self._zv(other)
        z_ = zfun(self.z, z)
        v_ = fun(self.v, v)
        if isinstance(v_, float):
            # we do not implement float results yet.
            assert round(v_) == v_
            v_ = round(v_)
        return zint(self.context, z_, v_)

    return proxy

INITIALIZER_LIST: List[Callable] = []

def initialize():
    for fn in INITIALIZER_LIST:
        fn()

def init_concolic_1():
    for fname in INT_BINARY_OPS:
        fun = getattr(int, fname)
        zfun = getattr(z3.ArithRef, fname)
        setattr(zint, fname, make_int_binary_wrapper(fname, fun, zfun))

INITIALIZER_LIST.append(init_concolic_1)

if __name__ == '__main__':
    init_concolic_1()

if __name__ == '__main__':
    with ConcolicTracer() as _:
        ia = zint.create(_.context, 'int_a', 0)
        ib = zint.create(_.context, 'int_b', 1)
        print((ia + ib).z)
        print((ia + 10).z)
        print((11 + ib).z)
        print((ia - ib).z)
        print((ia * ib).z)
        print((ia / ib).z)
        print((ia ** ib).z)

##### Integer Unary Operators

if __name__ == '__main__':
    print('\n##### Integer Unary Operators')



INT_UNARY_OPS = [
    '__neg__',
    '__pos__',
    # '__abs__',
    # '__invert__',
    # '__round__',
    # '__ceil__',
    # '__floor__',
    # '__trunc__',
]

def make_int_unary_wrapper(fname, fun, zfun):
    def proxy(self):
        return zint(self.context, zfun(self.z), fun(self.v))

    return proxy

def init_concolic_2():
    for fname in INT_UNARY_OPS:
        fun = getattr(int, fname)
        zfun = getattr(z3.ArithRef, fname)
        setattr(zint, fname, make_int_unary_wrapper(fname, fun, zfun))

INITIALIZER_LIST.append(init_concolic_2)

if __name__ == '__main__':
    init_concolic_2()

if __name__ == '__main__':
    with ConcolicTracer() as _:
        ia = zint.create(_.context, 'int_a', 0)
        print((-ia).z)
        print((+ia).z)

##### Using an Integer in a Boolean Context

if __name__ == '__main__':
    print('\n##### Using an Integer in a Boolean Context')



class zint(zint):
    def __bool__(self):
        # return zbool(self.context, self.z, self.v) <-- not allowed
        # force registering boolean condition
        if self != 0:
            return True
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        za = zint.create(_.context, 'int_a', 1)
        zb = zint.create(_.context, 'int_b', 0)
        if za and zb:
            print(1)

if __name__ == '__main__':
    _.context

#### Remaining Methods of the  ConcolicTracer

if __name__ == '__main__':
    print('\n#### Remaining Methods of the  ConcolicTracer')



##### Translating to the SMT Expression Format

if __name__ == '__main__':
    print('\n##### Translating to the SMT Expression Format')



class ConcolicTracer(ConcolicTracer):
    def smt_expr(self, show_decl=False, simplify=False, path=[]):
        r = []
        if show_decl:
            for decl in self.decls:
                v = self.decls[decl]
                v = '(_ BitVec 8)' if v == 'BitVec' else v
                r.append("(declare-const %s %s)" % (decl, v))
        path = path if path else self.path
        if path:
            path = z3.And(path)
            if show_decl:
                if simplify:
                    return '\n'.join([
                        *r,
                        "(assert %s)" % z3.simplify(path).sexpr()
                    ])
                else:
                    return '\n'.join(
                        [*r, "(assert %s)" % path.sexpr()])
            else:
                return z3.simplify(path).sexpr()
        else:
            return ''

def triangle(a, b, c):
    if a == b:
        if b == c:
            return 'equilateral'
        else:
            return 'isosceles'
    else:
        if b == c:
            return 'isosceles'
        else:
            if a == c:
                return 'isosceles'
            else:
                return 'scalene'

if __name__ == '__main__':
    triangle(1, 2, 1)

if __name__ == '__main__':
    with ConcolicTracer() as _:
        za = zint.create(_.context, 'int_a', 1)
        zb = zint.create(_.context, 'int_b', 1)
        zc = zint.create(_.context, 'int_c', 1)
        triangle(za, zb, zc)
    print(_.context)

if __name__ == '__main__':
    print(_.smt_expr(show_decl=True))

if __name__ == '__main__':
    z3.solve(_.path)

##### Generating Fresh Names

if __name__ == '__main__':
    print('\n##### Generating Fresh Names')



COUNTER = 0

def fresh_name():
    global COUNTER
    COUNTER += 1
    return COUNTER

if __name__ == '__main__':
    fresh_name()

def reset_counter():
    global COUNTER
    COUNTER = 0

class ConcolicTracer(ConcolicTracer):
    def __enter__(self):
        reset_counter()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        return

class ConcolicTracer(ConcolicTracer):
    def concolic(self, args):
        my_args = []
        for name, arg in zip(self.fn_args, args):
            t = type(arg).__name__
            zwrap = globals()['z' + t]
            vname = "%s_%s_%s_%s" % (self.fn.__name__, name, t, fresh_name())
            my_args.append(zwrap.create(self.context, vname, arg))
            self.fn_args[name] = vname
        return my_args

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[factorial](5)

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    print(_.smt_expr(show_decl=True))

##### Evaluating the Concolic Expressions

if __name__ == '__main__':
    print('\n##### Evaluating the Concolic Expressions')



class ConcolicTracer(ConcolicTracer):
    def zeval(self, predicates=None, *,python=False, log=False):
        """Evaluate `predicates` in current context.
        - If `python` is set, use the z3 Python API; otherwise use z3 standalone.
        - If `log` is set, show input to z3.
        Return a pair (`result`, `solution`) where
        - `result` is either `'sat'` (satisfiable); then 
           solution` is a mapping of variables to (value, type) pairs; or
        - `result` is not `'sat'`, indicating an error; then `solution` is `None`
        """
        if predicates is None:
            path = self.path
        else:
            path = list(self.path)
            for i in sorted(predicates):
                if len(path) > i:
                    path[i] = predicates[i]
                else:
                    path.append(predicates[i])
        if log:
            print('Predicates in path:')
            for i, p in enumerate(path):
                print(i, p)
            print()

        r, sol = (zeval_py if python else zeval_smt)(path, self, log)
        if r == 'sat':
            return r, {k: sol.get(self.fn_args[k], None) for k in self.fn_args}
        else:
            return r, None

##### Using the Python API

if __name__ == '__main__':
    print('\n##### Using the Python API')



def zeval_py(path, cc, log):
    for decl in cc.decls:
        if cc.decls[decl] == 'BitVec':
            v = "z3.%s('%s', 8)" % (cc.decls[decl], decl)
        else:
            v = "z3.%s('%s')" % (cc.decls[decl], decl)
        exec(v)
    s = z3.Solver()
    s.add(z3.And(path))
    if s.check() == z3.unsat:
        return 'No Solutions', {}
    elif s.check() == z3.unknown:
        return 'Gave up', None
    assert s.check() == z3.sat
    m = s.model()
    return 'sat', {d.name(): m[d] for d in m.decls()}

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[factorial](5)

if __name__ == '__main__':
    _.zeval(python=True)

##### Using the Command Line

if __name__ == '__main__':
    print('\n##### Using the Command Line')



import re

import subprocess

SEXPR_TOKEN = r'''(?mx)
    \s*(?:
        (?P<bra>\()|
        (?P<ket>\))|
        (?P<token>[^"()\s]+)|
        (?P<string>"[^"]*")
       )'''

def parse_sexp(sexp):
    stack, res = [], []
    for elements in re.finditer(SEXPR_TOKEN, sexp):
        kind, value = [(t, v) for t, v in elements.groupdict().items() if v][0]
        if kind == 'bra':
            stack.append(res)
            res = []
        elif kind == 'ket':
            last, res = res, stack.pop(-1)
            res.append(last)
        elif kind == 'token':
            res.append(value)
        elif kind == 'string':
            res.append(value[1:-1])
        else:
            assert False
    return res

if __name__ == '__main__':
    parse_sexp('abcd (hello 123 (world "hello world"))')

import tempfile
import os

Z3_BINARY = 'z3'  # Z3 binary to invoke

Z3_OPTIONS = '-t:6000'  # Z3 options - a soft timeout of 6000 milliseconds

def zeval_smt(path, cc, log):
    s = cc.smt_expr(True, True, path)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.smt',
                                     delete=False) as f:
        f.write(s + "\n")
        f.write("(check-sat)\n")
        f.write("(get-model)\n")

    if log:
        print(open(f.name).read())

    cmd = f"{Z3_BINARY} {Z3_OPTIONS} {f.name}"
    if log:
        print(cmd)

    output = subprocess.getoutput(cmd)

    os.remove(f.name)

    if log:
        print(output)

    o = parse_sexp(output)
    if not o:
        return 'Gave up', None

    kind = o[0]
    if kind == 'unknown':
        return 'Gave up', None
    elif kind == 'timeout':
        return 'Timeout', None
    elif kind == 'unsat':
        return 'No Solutions', {}

    assert kind == 'sat', kind
    if o[1][0] == 'model': # up to 4.8.8.0
        return 'sat', {i[1]: (i[-1], i[-2]) for i in o[1][1:]}
    else:
        return 'sat', {i[1]: (i[-1], i[-2]) for i in o[1][0:]}

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[factorial](5)

if __name__ == '__main__':
    _.zeval(log=True)

#### A Proxy Class for Strings

if __name__ == '__main__':
    print('\n#### A Proxy Class for Strings')



class zstr(str):
    def __new__(cls, context, zn, v):
        return str.__new__(cls, v)

class zstr(zstr):
    @classmethod
    def create(cls, context, zn, v=None):
        return zproxy_create(cls, 'String', z3.String, context, zn, v)

    def __init__(self, context, z, v=None):
        self.context, self.z, self.v = context, z, v
        self._len = zint(context, z3.Length(z), len(v))
        #self.context[1].append(z3.Length(z) == z3.IntVal(len(v)))

class zstr(zstr):
    def _zv(self, o):
        return (o.z, o.v) if isinstance(o, zstr) else (z3.StringVal(o), o)

### Hack to use the ASCII value of a character.

if __name__ == '__main__':
    print('\n### Hack to use the ASCII value of a character.')



from typing import Union, Optional, Dict, Generator, Set

def visit_z3_expr(
        e: Union[z3.ExprRef, z3.QuantifierRef],
        seen: Optional[Dict[Union[z3.ExprRef, z3.QuantifierRef], bool]] = None) -> \
        Generator[Union[z3.ExprRef, z3.QuantifierRef], None, None]:
    if seen is None:
        seen = {}
    elif e in seen:
        return

    seen[e] = True
    yield e

    if z3.is_app(e):
        for ch in e.children():
            for e in visit_z3_expr(ch, seen):
                yield e
        return

    if z3.is_quantifier(e):
        for e in visit_z3_expr(e.body(), seen):
            yield e
        return


def is_z3_var(e: z3.ExprRef) -> bool:
    return z3.is_const(e) and e.decl().kind() == z3.Z3_OP_UNINTERPRETED


def get_all_vars(e: z3.ExprRef) -> Set[z3.ExprRef]:
    return {sub for sub in visit_z3_expr(e) if is_z3_var(sub)}


def z3_ord(str_expr: z3.SeqRef) -> z3.ArithRef:
    return z3.parse_smt2_string(
        f"(assert (= 42 (str.to_code {str_expr.sexpr()})))",
        decls={str(c): c for c in get_all_vars(str_expr)}
    )[0].children()[1]


def z3_chr(int_expr: z3.ArithRef) -> z3.SeqRef:
    return z3.parse_smt2_string(
        f"(assert (= \"4\" (str.from_code {int_expr.sexpr()})))",
        decls={str(c): c for c in get_all_vars(int_expr)}
    )[0].children()[1]

##### Retrieving Ordinal Value

if __name__ == '__main__':
    print('\n##### Retrieving Ordinal Value')



def zord(context, c):
    return z3_ord(c)

if __name__ == '__main__':
    zc = z3.String('arg_%d' % fresh_name())

if __name__ == '__main__':
    with ConcolicTracer() as _:
        zi = zord(_.context, zc)

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    zi.sexpr()

if __name__ == '__main__':
    (zi == 65).sexpr()

if __name__ == '__main__':
    z3.solve([zi == 65])

##### Translating an Ordinal Value to ASCII

if __name__ == '__main__':
    print('\n##### Translating an Ordinal Value to ASCII')



def zchr(context, i):
    return z3_chr(i)

if __name__ == '__main__':
    i = z3.Int('ival_%d' % fresh_name())

if __name__ == '__main__':
    with ConcolicTracer() as _:
        zc = zchr(_.context, i)

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    (zc== z3.StringVal('a')).sexpr()

if __name__ == '__main__':
    z3.solve([zc == z3.StringVal('a')])

##### Equality between Strings

if __name__ == '__main__':
    print('\n##### Equality between Strings')



class zstr(zstr):
    def __eq__(self, other):
        z, v = self._zv(other)
        return zbool(self.context, self.z == z, self.v == v)

    def __req__(self, other):
        return self.__eq__(other)

def tstr1(s):
    if s == 'h':
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr1]('h')

if __name__ == '__main__':
    _.zeval()

def tstr1(s):  # type: ignore
    if s == 'hello world':
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr1]('hello world')

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    _.zeval()

##### Length of Strings

if __name__ == '__main__':
    print('\n##### Length of Strings')



class zstr(zstr):
    def __len__(self):
        raise NotImplemented()

class zstr(zstr):
    def length(self):
        return self._len

if __name__ == '__main__':
    with ConcolicTracer() as _:
        za = zstr.create(_.context, 'str_a', "s")
        if za.length() > 0:
            print(1)

if __name__ == '__main__':
    _.context

def tstr2(s):
    if s.length() > 1:
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr2]('hello world')

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    _.zeval(log=True)

##### Concatenation of Strings

if __name__ == '__main__':
    print('\n##### Concatenation of Strings')



class zstr(zstr):
    def __add__(self, other):
        z, v = self._zv(other)
        return zstr(self.context, self.z + z, self.v + v)

    def __radd__(self, other):
        return self.__add__(other)

if __name__ == '__main__':
    with ConcolicTracer() as _:
        v1, v2 = [zstr.create(_.context, 'arg_%d' % fresh_name(), s)
                  for s in ['hello', 'world']]
        if (v1 + ' ' + v2) == 'hello world':
            print('hello world')

if __name__ == '__main__':
    _.context

##### Producing Substrings

if __name__ == '__main__':
    print('\n##### Producing Substrings')



class zstr(zstr):
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            start, stop, step = idx.indices(len(self.v))
            assert step == 1  # for now
            assert stop >= start  # for now
            rz = z3.SubString(self.z, start, stop - start)
            rv = self.v[idx]
        elif isinstance(idx, int):
            rz = z3.SubString(self.z, idx, 1)
            rv = self.v[idx]
        else:
            assert False  # for now
        return zstr(self.context, rz, rv)

    def __iter__(self):
        return zstr_iterator(self.context, self)

##### An Iterator Class for Strings

if __name__ == '__main__':
    print('\n##### An Iterator Class for Strings')



class zstr_iterator():
    def __init__(self, context, zstr):
        self.context = context
        self._zstr = zstr
        self._str_idx = 0
        self._str_max = zstr._len  # intz is not an _int_

    def __next__(self):
        if self._str_idx == self._str_max:  # intz#eq
            raise StopIteration
        c = self._zstr[self._str_idx]
        self._str_idx += 1
        return c

    def __len__(self):
        return self._len

def tstr3(s):
    if s[0] == 'h' and s[1] == 'e' and s[3] == 'l':
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr3]('hello')

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    _.zeval()

##### Translating to Upper and Lower Equivalents

if __name__ == '__main__':
    print('\n##### Translating to Upper and Lower Equivalents')



class zstr(zstr):
    def upper(self):
        empty = ''
        ne = 'empty_%d' % fresh_name()
        result = zstr.create(self.context, ne, empty)
        self.context[1].append(z3.StringVal(empty) == result.z)
        cdiff = (ord('a') - ord('A'))
        for i in self:
            oz = zord(self.context, i.z)
            uz = zchr(self.context, oz - cdiff)
            rz = z3.And([oz >= ord('a'), oz <= ord('z')])
            ov = ord(i.v)
            uv = chr(ov - cdiff)
            rv = ov >= ord('a') and ov <= ord('z')
            if zbool(self.context, rz, rv):
                i = zstr(self.context, uz, uv)
            else:
                i = zstr(self.context, i.z, i.v)
            result += i
        return result

class zstr(zstr):
    def lower(self):
        empty = ''
        ne = 'empty_%d' % fresh_name()
        result = zstr.create(self.context, ne, empty)
        self.context[1].append(z3.StringVal(empty) == result.z)
        cdiff = (ord('a') - ord('A'))
        for i in self:
            oz = zord(self.context, i.z)
            uz = zchr(self.context, oz + cdiff)
            rz = z3.And([oz >= ord('A'), oz <= ord('Z')])
            ov = ord(i.v)
            uv = chr(ov + cdiff)
            rv = ov >= ord('A') and ov <= ord('Z')
            if zbool(self.context, rz, rv):
                i = zstr(self.context, uz, uv)
            else:
                i = zstr(self.context, i.z, i.v)
            result += i
        return result

def tstr4(s):
    if s.upper() == 'H':
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr4]('h')

if __name__ == '__main__':
    _.zeval()

def tstr5(s):
    if s.lower() == 'hello world':
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr5]('Hello World')

if __name__ == '__main__':
    _.zeval()

##### Checking for String Prefixes

if __name__ == '__main__':
    print('\n##### Checking for String Prefixes')



class zstr(zstr):
    def startswith(self, other, beg=0, end=None):
        assert end is None  # for now
        assert isinstance(beg, int)  # for now
        zb = z3.IntVal(beg)

        others = other if isinstance(other, tuple) else (other, )

        last = False
        for o in others:
            z, v = self._zv(o)
            r = z3.IndexOf(self.z, z, zb)
            last = zbool(self.context, r == zb, self.v.startswith(v))
            if last:
                return last
        return last

def tstr6(s):
    if s.startswith('hello'):
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr6]('hello world')

if __name__ == '__main__':
    _.zeval()

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr6]('my world')

if __name__ == '__main__':
    _.zeval()

##### Finding Substrings

if __name__ == '__main__':
    print('\n##### Finding Substrings')



class zstr(zstr):
    def find(self, other, beg=0, end=None):
        assert end is None  # for now
        assert isinstance(beg, int)  # for now
        zb = z3.IntVal(beg)
        z, v = self._zv(other)
        zi = z3.IndexOf(self.z, z, zb)
        vi = self.v.find(v, beg, end)
        return zint(self.context, zi, vi)

def tstr7(s):
    if s.find('world') != -1:
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr7]('hello world')

if __name__ == '__main__':
    _.zeval()

##### Remove Space from Ends

if __name__ == '__main__':
    print('\n##### Remove Space from Ends')



import string

class zstr(zstr):
    def rstrip(self, chars=None):
        if chars is None:
            chars = string.whitespace
        if self._len == 0:
            return self
        else:
            last_idx = self._len - 1
            cz = z3.SubString(self.z, last_idx.z, 1)
            cv = self.v[-1]
            zcheck_space = z3.Or([cz == z3.StringVal(char) for char in chars])
            vcheck_space = any(cv == char for char in chars)
            if zbool(self.context, zcheck_space, vcheck_space):
                return zstr(self.context, z3.SubString(self.z, 0, last_idx.z),
                            self.v[0:-1]).rstrip(chars)
            else:
                return self

def tstr8(s):
    if s.rstrip(' ') == 'a b':
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr8]('a b   ')
        print(r)

if __name__ == '__main__':
    _.zeval()

class zstr(zstr):
    def lstrip(self, chars=None):
        if chars is None:
            chars = string.whitespace
        if self._len == 0:
            return self
        else:
            first_idx = 0
            cz = z3.SubString(self.z, 0, 1)
            cv = self.v[0]
            zcheck_space = z3.Or([cz == z3.StringVal(char) for char in chars])
            vcheck_space = any(cv == char for char in chars)
            if zbool(self.context, zcheck_space, vcheck_space):
                return zstr(self.context, z3.SubString(
                    self.z, 1, self._len.z), self.v[1:]).lstrip(chars)
            else:
                return self

def tstr9(s):
    if s.lstrip(' ') == 'a b':
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr9]('   a b')
        print(r)

if __name__ == '__main__':
    _.zeval()

class zstr(zstr):
    def strip(self, chars=None):
        return self.lstrip(chars).rstrip(chars)

def tstr10(s):
    if s.strip() == 'a b':
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr10]('    a b  ')
        print(r)

if __name__ == '__main__':
    _.zeval()

##### Splitting Strings

if __name__ == '__main__':
    print('\n##### Splitting Strings')



class zstr(zstr):
    def split(self, sep=None, maxsplit=-1):
        assert sep is not None  # default space based split is complicated
        assert maxsplit == -1  # for now.
        zsep = z3.StringVal(sep)
        zl = z3.Length(zsep)
        # zi would be the length of prefix
        zi = z3.IndexOf(self.z, zsep, z3.IntVal(0))
        # Z3Bug: There is a bug in the `z3.IndexOf` method which returns
        # `z3.SeqRef` instead of `z3.ArithRef`. So we need to fix it.
        zi = z3.ArithRef(zi.ast, zi.ctx)

        vi = self.v.find(sep)
        if zbool(self.context, zi >= z3.IntVal(0), vi >= 0):
            zprefix = z3.SubString(self.z, z3.IntVal(0), zi)
            zmid = z3.SubString(self.z, zi, zl)
            zsuffix = z3.SubString(self.z, zi + zl,
                                   z3.Length(self.z))
            return [zstr(self.context, zprefix, self.v[0:vi])] + zstr(
                self.context, zsuffix, self.v[vi + len(sep):]).split(
                    sep, maxsplit)
        else:
            return [self]

def tstr11(s):
    if s.split(',') == ['a', 'b', 'c']:
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[tstr11]('a,b,c')
        print(r)

if __name__ == '__main__':
    _.zeval()

##### Trip Wire

if __name__ == '__main__':
    print('\n##### Trip Wire')



def make_str_abort_wrapper(fun):
    def proxy(*args, **kwargs):
        raise Exception('%s Not implemented in `zstr`' % fun.__name__)
    return proxy

def init_concolic_3():
    strmembers = inspect.getmembers(zstr, callable)
    zstrmembers = {m[0] for m in strmembers if len(
        m) == 2 and 'zstr' in m[1].__qualname__}
    for name, fn in inspect.getmembers(str, callable):
        # Omitted 'splitlines' as this is needed for formatting output in
        # IPython/Jupyter
        if name not in zstrmembers and name not in [
            'splitlines',
            '__class__',
            '__contains__',
            '__delattr__',
            '__dir__',
            '__format__',
            '__ge__',
            '__getattribute__',
            '__getnewargs__',
            '__gt__',
            '__hash__',
            '__le__',
            '__len__',
            '__lt__',
            '__mod__',
            '__mul__',
            '__ne__',
            '__reduce__',
            '__reduce_ex__',
            '__repr__',
            '__rmod__',
            '__rmul__',
            '__setattr__',
            '__sizeof__',
                '__str__']:
            setattr(zstr, name, make_str_abort_wrapper(fn))

INITIALIZER_LIST.append(init_concolic_3)

if __name__ == '__main__':
    init_concolic_3()

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



### Example: Triangle

if __name__ == '__main__':
    print('\n### Example: Triangle')



if __name__ == '__main__':
    with ConcolicTracer() as _:
        print(_[triangle](1, 2, 3))

if __name__ == '__main__':
    _.decls

if __name__ == '__main__':
    _.path

if __name__ == '__main__':
    _.zeval()

if __name__ == '__main__':
    triangle(0, -2, -1)

if __name__ == '__main__':
    za, zb, zc = [z3.Int(s) for s in _.decls.keys()]

if __name__ == '__main__':
    za, zb, zc

if __name__ == '__main__':
    _.zeval({1: zb == zc})

if __name__ == '__main__':
    triangle(1, 0, 1)

### Example: Decoding CGI Strings

if __name__ == '__main__':
    print('\n### Example: Decoding CGI Strings')



def cgi_decode(s):
    """Decode the CGI-encoded string `s`:
       * replace "+" by " "
       * replace "%xx" by the character with hex number xx.
       Return the decoded string.  Raise `ValueError` for invalid inputs."""

    # Mapping of hex digits to their integer values
    hex_values = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
    }

    t = ''
    i = 0
    while i < s.length():
        c = s[i]
        if c == '+':
            t += ' '
        elif c == '%':
            digit_high, digit_low = s[i + 1], s[i + 2]
            i = i + 2
            found = 0
            v = 0
            for key in hex_values:
                if key == digit_high:
                    found = found + 1
                    v = hex_values[key] * 16
                    break
            for key in hex_values:
                if key == digit_low:
                    found = found + 1
                    v = v + hex_values[key]
                    break
            if found == 2:
                if v >= 128:
                    # z3.StringVal(urllib.parse.unquote('%80')) <-- bug in z3
                    raise ValueError("Invalid encoding")
                t = t + chr(v)
            else:
                raise ValueError("Invalid encoding")
        else:
            t = t + c
        i = i + 1
    return t

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[cgi_decode]('')

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[cgi_decode]('a%20d')

if __name__ == '__main__':
    _.decls

if __name__ == '__main__':
    _.path

if __name__ == '__main__':
    assert _.context == (_.decls, _.path)

if __name__ == '__main__':
    _.zeval()

if __name__ == '__main__':
    _.path[0]

if __name__ == '__main__':
    zs = z3.String('cgi_decode_s_str_1')

if __name__ == '__main__':
    z3.SubString(zs, 0, 1) == z3.StringVal('a')

if __name__ == '__main__':
    (result, new_vars) = _.zeval({1: z3.SubString(zs, 0, 1) == z3.StringVal('+')})


if __name__ == '__main__':
    new_vars

if __name__ == '__main__':
    (new_s, new_s_type) = new_vars['s']

if __name__ == '__main__':
    new_s

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[cgi_decode](new_s)

if __name__ == '__main__':
    _.path

### Example: Round

if __name__ == '__main__':
    print('\n### Example: Round')



def round10(r):
    while r % 10 != 0:
        r += 1
    return r

if __name__ == '__main__':
    with ConcolicTracer() as _:
        r = _[round10](1)

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    _.zeval()

### Example: Absolute Maximum

if __name__ == '__main__':
    print('\n### Example: Absolute Maximum')



def abs_value(a):
    if a > 0:
        return a
    else:
        return -a

def abs_max(a, b):
    a1 = abs_value(a)
    b1 = abs_value(b)
    if a1 > b1:
        c = a1
    else:
        c = b1
    return c

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[abs_max](2, 1)

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    _.zeval()

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[abs_max](-2, -1)

if __name__ == '__main__':
    _.context

if __name__ == '__main__':
    _.zeval()

### Example: Binomial Coefficient

if __name__ == '__main__':
    print('\n### Example: Binomial Coefficient')



def factorial(n):  # type: ignore
    v = 1
    while n != 0:
        v *= n
        n -= 1

    return v

def permutation(n, k):
    return factorial(n) / factorial(n - k)

def combination(n, k):
    return permutation(n, k) / factorial(k)

def binomial(n, k):
    if n < 0 or k < 0 or n < k:
        raise Exception('Invalid values')
    return combination(n, k)

if __name__ == '__main__':
    with ConcolicTracer() as _:
        v = _[binomial](4, 2)

if __name__ == '__main__':
    _.zeval()

### Example: Database

if __name__ == '__main__':
    print('\n### Example: Database')



if __name__ == '__main__':
    if __name__ == '__main__':
        if z3.get_version() > (4, 8, 7, 0):
            print("""Note: The following example may not work with your Z3 version;
see https://github.com/Z3Prover/z3/issues/5763 for details.
Consider `pip install z3-solver==4.8.7.0` as a workaround.""")

from .InformationFlow import DB, sample_db, update_inventory

from .GrammarMiner import VEHICLES  # minor dependency

if __name__ == '__main__':
    db = sample_db()
    for V in VEHICLES:
        update_inventory(db, V)

if __name__ == '__main__':
    db.db

class ConcolicDB(DB):
    def table(self, t_name):
        for k, v in self.db:
            if t_name == k:
                return v
        raise SQLException('Table (%s) was not found' % repr(t_name))

    def column(self, decl, c_name):
        for k in decl:
            if c_name == k:
                return decl[k]
        raise SQLException('Column (%s) was not found' % repr(c_name))

def db_select(s):
    my_db = ConcolicDB()
    my_db.db = [(k, v) for (k, v) in db.db.items()]
    r = my_db.sql(s)
    return r

if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[db_select]('select kind from inventory')

if __name__ == '__main__':
    _.path

if __name__ == '__main__':
    _.zeval()

## Fuzzing with Constraints
## ------------------------

if __name__ == '__main__':
    print('\n## Fuzzing with Constraints')



### Excursion: Implementing SimpleConcolicFuzzer

if __name__ == '__main__':
    print('\n### Excursion: Implementing SimpleConcolicFuzzer')



from .Fuzzer import Fuzzer

def hang_if_no_space(s):
    i = 0
    while True:
        if i < s.length():
            if s[i] == ' ':
                break
        i += 1

from .ExpectError import ExpectTimeout, ExpectError

import random

#### Representing Decisions

if __name__ == '__main__':
    print('\n#### Representing Decisions')



class TraceNode:
    def __init__(self, smt_val, parent, info):
        # This is the smt that lead to this node
        self._smt_val = z3.simplify(smt_val) if smt_val is not None else None

        # This is the predicate that this node might perform at a future point
        self.smt = None
        self.info = info
        self.parent = parent
        self.children = {}
        self.path = None
        self.tree = None
        self._pattern = None
        self.log = True

    def no(self): return self.children.get(self.tree.no_bit)

    def yes(self): return self.children.get(self.tree.yes_bit)

    def get_children(self): return (self.no(), self.yes())

    def __str__(self):
        return 'TraceNode[%s]' % ','.join(self.children.keys())

class PlausibleChild:
    def __init__(self, parent, cond, tree):
        self.parent = parent
        self.cond = cond
        self.tree = tree
        self._smt_val = None

    def __repr__(self):
        return 'PlausibleChild[%s]' % (self.parent.pattern() + ':' + self.cond)

class PlausibleChild(PlausibleChild):
    def smt_val(self):
        if self._smt_val is not None:
            return self._smt_val
        # if the parent has other children, then that child would have updatd the parent's smt
        # Hence, we can use that child's smt_value's opposite as our value.
        assert self.parent.smt is not None
        if self.cond == self.tree.no_bit:
            self._smt_val = z3.Not(self.parent.smt)
        else:
            self._smt_val = self.parent.smt
        return self._smt_val

    def cc(self):
        if self.parent.info.get('cc') is not None:
            return self.parent.info['cc']
        # if there is a plausible child node, it means that there can
        # be at most one child.
        siblings = list(self.parent.children.values())
        assert len(siblings) == 1
        # We expect at the other child to have cc
        return siblings[0].info['cc']

class PlausibleChild(PlausibleChild):
    def path_expression(self):
        path_to_root = self.parent.get_path_to_root()
        assert path_to_root[0]._smt_val is None
        return [i._smt_val for i in path_to_root[1:]] + [self.smt_val()]

class TraceTree:
    def __init__(self):
        self.root = TraceNode(smt_val=None, parent=None, info={'num': 0})
        self.root.tree = self
        self.leaves = {}
        self.no_bit, self.yes_bit = '0', '1'

        pprefix = ':'
        for bit in [self.no_bit, self.yes_bit]:
            self.leaves[pprefix + bit] = PlausibleChild(self.root, bit, self)
        self.completed_paths = {}

class TraceTree(TraceTree):
    def add_trace(self, tracer, string):
        last = self.root
        i = 0
        for i, elt in enumerate(tracer.path):
            last = last.add_child(elt=elt, i=i + 1, cc=tracer, string=string)
        last.add_child(elt=z3.BoolVal(True), i=i + 1, cc=tracer, string=string)

class TraceNode(TraceNode):
    def bit(self):
        if self._smt_val is None:
            return None
        return self.tree.no_bit if self._smt_val.decl(
        ).name() == 'not' else self.tree.yes_bit

    def pattern(self):
        if self._pattern is not None:
            return self._pattern
        path = self.get_path_to_root()
        assert path[0]._smt_val is None
        assert path[0].parent is None

        self._pattern = ''.join([p.bit() for p in path[1:]])
        return self._pattern

class TraceNode(TraceNode):
    def add_child(self, elt, i, cc, string):
        if elt == z3.BoolVal(True):
            # No more exploration here. Simply unregister the leaves of *this*
            # node and possibly register them in completed nodes, and exit
            for bit in [self.tree.no_bit, self.tree.yes_bit]:
                child_leaf = self.pattern() + ':' + bit
                if child_leaf in self.tree.leaves:
                    del self.tree.leaves[child_leaf]
            self.tree.completed_paths[self.pattern()] = self
            return None

        child_node = TraceNode(smt_val=elt,
                               parent=self,
                               info={'num': i, 'cc': cc, 'string': string})
        child_node.tree = self.tree

        # bit represents the path that child took from this node.
        bit = child_node.bit()

        # first we update our smt decision
        if bit == self.tree.yes_bit:  # yes, which means the smt can be used as is
            if self.smt is not None:
                assert self.smt == child_node._smt_val
            else:
                self.smt = child_node._smt_val
        # no, which means we have to negate it to get the decision.
        elif bit == self.tree.no_bit:
            smt_ = z3.simplify(z3.Not(child_node._smt_val))
            if self.smt is not None:
                assert smt_ == self.smt
            else:
                self.smt = smt_
        else:
            assert False

        if bit in self.children:
            #    if self.log:
            #print(elt, child_node.bit(), i, string)
            #print(i,'overwriting', bit,'=>',self.children[bit],'with',child_node)
            child_node = self.children[bit]
            #self.children[bit] = child_node
            #child_node.children = old.children
        else:
            self.children[bit] = child_node

        # At this point, we have to unregister any leaves that correspond to this child from tree,
        # and add the plausible children of this child as leaves to be explored. Note that
        # if it is the end (z3.True), we do not have any more children.
        child_leaf = self.pattern() + ':' + bit
        if child_leaf in self.tree.leaves:
            del self.tree.leaves[child_leaf]

        pprefix = child_node.pattern() + ':'

        # Plausible children.
        for bit in [self.tree.no_bit, self.tree.yes_bit]:
            self.tree.leaves[pprefix +
                             bit] = PlausibleChild(child_node, bit, self.tree)
        return child_node

class TraceNode(TraceNode):
    def get_path_to_root(self):
        if self.path is not None:
            return self.path
        parent_path = []
        if self.parent is not None:
            parent_path = self.parent.get_path_to_root()
        self.path = parent_path + [self]
        return self.path

#### The SimpleConcolicFuzzer class

if __name__ == '__main__':
    print('\n#### The SimpleConcolicFuzzer class')



class SimpleConcolicFuzzer(Fuzzer):
    def __init__(self):
        self.ct = TraceTree()
        self.max_tries = 1000
        self.last = None
        self.last_idx = None

if __name__ == '__main__':
    with ExpectTimeout(2):
        with ConcolicTracer() as _:
            _[hang_if_no_space]('ab d')

if __name__ == '__main__':
    _.path

if __name__ == '__main__':
    scf = SimpleConcolicFuzzer()
    scf.ct.add_trace(_, 'ab d')

if __name__ == '__main__':
    [i._smt_val for i in scf.ct.root.get_children(
    )[0].get_children(
    )[0].get_children(
    )[0].get_children(
    )[0].get_children(
    )[0].get_children(
    )[1].get_path_to_root()]

if __name__ == '__main__':
    for key in scf.ct.leaves:
        print(key, '\t', scf.ct.leaves[key])

from .GrammarFuzzer import display_tree

TREE_NODES = {}

def my_extract_node(tnode, id):
    key, node, parent = tnode
    if node is None:
        # return '? (%s:%s)' % (parent.pattern(), key) , [], ''
        return '?', [], ''
    if node.smt is None:
        return '* %s' % node.info.get('string', ''), [], ''

    no, yes = node.get_children()
    num = str(node.info.get('num'))
    children = [('0', no, node), ('1', yes, node)]
    TREE_NODES[id] = 0
    return "(%s) %s" % (num, str(node.smt)), children, ''

def my_edge_attr(dot, start_node, stop_node):
    # the edges are always drawn '0:NO' first.
    if TREE_NODES[start_node] == 0:
        color, label = 'red', '0'
        TREE_NODES[start_node] = 1
    else:
        color, label = 'blue', '1'
        TREE_NODES[start_node] = 2
    dot.edge(repr(start_node), repr(stop_node), color=color, label=label)

def display_trace_tree(root):
    TREE_NODES.clear()
    return display_tree(
        ('', root, None), extract_node=my_extract_node, edge_attr=my_edge_attr)

if __name__ == '__main__':
    display_trace_tree(scf.ct.root)

if __name__ == '__main__':
    scf.ct.leaves['00000:0']

if __name__ == '__main__':
    scf.ct.leaves['00000:0'].path_expression()

if __name__ == '__main__':
    scf.ct.leaves[':1']

if __name__ == '__main__':
    scf.ct.leaves[':1'].path_expression()

class SimpleConcolicFuzzer(SimpleConcolicFuzzer):
    def add_trace(self, trace, s):
        self.ct.add_trace(trace, s)

    def next_choice(self):
        #lst = sorted(list(self.ct.leaves.keys()), key=len)
        c = random.choice(list(self.ct.leaves.keys()))
        #c = lst[0]
        return self.ct.leaves[c]

if __name__ == '__main__':
    scf = SimpleConcolicFuzzer()
    scf.add_trace(_, 'ab d')
    node = scf.next_choice()

if __name__ == '__main__':
    node

if __name__ == '__main__':
    node.path_expression()

class SimpleConcolicFuzzer(SimpleConcolicFuzzer):
    def get_newpath(self):
        node = self.next_choice()
        path = node.path_expression()
        return path, node.cc()

if __name__ == '__main__':
    scf = SimpleConcolicFuzzer()
    scf.add_trace(_, 'abcd')
    path, cc = scf.get_newpath()
    path

#### The fuzzing method

if __name__ == '__main__':
    print('\n#### The fuzzing method')



class SimpleConcolicFuzzer(SimpleConcolicFuzzer):
    def fuzz(self):
        if self.ct.root.children == {}:
            # a random value to generate comparisons. This would be
            # the initial value around which we explore with concolic
            # fuzzing.
            # str_len = random.randint(1,100)
            # return ' '*str_len
            return ' '
        for i in range(self.max_tries):
            path, last = self.get_newpath()
            s, v = zeval_smt(path, last, log=False)
            if s != 'sat':
                # raise Exception("Unexpected UNSAT")
                continue

            val = list(v.values())[0]
            elt, typ = val

            # make sure that we do not retry the tried paths
            # The tracer we add here is incomplete. This gets updated when
            # the add_trace is called from the concolic fuzzer context.
            # self.add_trace(ConcolicTracer((last.decls, path)), elt)
            if typ == 'Int':
                if len(elt) == 2 and elt[0] == '-':  # negative numbers are [-, x]
                    return -1*int(elt[1])
                return int(elt)
            elif typ == 'String':
                return elt
            return elt
        return None

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[cgi_decode]('a+c')

if __name__ == '__main__':
    _.path

if __name__ == '__main__':
    scf = SimpleConcolicFuzzer()
    scf.add_trace(_, 'a+c')

if __name__ == '__main__':
    display_trace_tree(scf.ct.root)

if __name__ == '__main__':
    v = scf.fuzz()
    print(v)

if __name__ == '__main__':
    with ExpectError():
        with ConcolicTracer() as _:
            _[cgi_decode](v)

if __name__ == '__main__':
    scf.add_trace(_, v)

if __name__ == '__main__':
    display_trace_tree(scf.ct.root)

if __name__ == '__main__':
    scf = SimpleConcolicFuzzer()
    for i in range(10):
        v = scf.fuzz()
        print(repr(v))
        if v is None:
            continue
        with ConcolicTracer() as _:
            with ExpectError(print_traceback=False):
                # z3.StringVal(urllib.parse.unquote('%80')) <-- bug in z3
                _[cgi_decode](v)
        scf.add_trace(_, v)

if __name__ == '__main__':
    display_trace_tree(scf.ct.root)

## Concolic Grammar Fuzzing
## ------------------------

if __name__ == '__main__':
    print('\n## Concolic Grammar Fuzzing')



### Excursion: Implementing ConcolicGrammarFuzzer

if __name__ == '__main__':
    print('\n### Excursion: Implementing ConcolicGrammarFuzzer')



from .InformationFlow import INVENTORY_GRAMMAR, SQLException

from .GrammarFuzzer import GrammarFuzzer

class ConcolicGrammarFuzzer(GrammarFuzzer):
    def tree_to_string(self, tree):
        symbol, children, *_ = tree
        e = ''
        if children:
            return e.join([self.tree_to_string(c) for c in children])
        else:
            return e if symbol in self.grammar else symbol

    def prune_tree(self, tree, tokens):
        name, children = tree
        children = self.coalesce(children)
        if name in tokens:
            return (name, [(self.tree_to_string(tree), [])])
        else:
            return (name, [self.prune_tree(c, tokens) for c in children])

    def coalesce(self, children):
        last = ''
        new_lst = []
        for cn, cc in children:
            if cn not in self.grammar:
                last += cn
            else:
                if last:
                    new_lst.append((last, []))
                    last = ''
                new_lst.append((cn, cc))
        if last:
            new_lst.append((last, []))
        return new_lst

if __name__ == '__main__':
    tgf = ConcolicGrammarFuzzer(INVENTORY_GRAMMAR)
    while True:
        qtree = tgf.fuzz_tree()
        query = str(tgf.tree_to_string(qtree))
        if query.startswith('select'):
            break

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        print(repr(query))
        with ConcolicTracer() as _:
            res = _[db_select](str(query))
        print(repr(res))

if __name__ == '__main__':
    for i, p in enumerate(_.path):
        print(i, p)

if __name__ == '__main__':
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]

if __name__ == '__main__':
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args

if __name__ == '__main__':
    new_.zeval()

if __name__ == '__main__':
    print(_.path[-1])
    z3.solve(z3.Not(_.path[-1]))

from .GrammarFuzzer import display_tree

if __name__ == '__main__':
    prune_tokens = [
        '<value>', '<table>', '<column>', '<literals>', '<exprs>', '<bexpr>'
    ]
    dt = tgf.prune_tree(qtree, prune_tokens)
    display_tree(dt)

from .GrammarFuzzer import START_SYMBOL

def span(node, g, node_start=0):
    hm = {}
    k, cs = node
    end_i = node_start
    new_cs = []
    for c in cs:
        chm, (ck, child_start, child_end, gcs) = span(c, g, end_i)
        new_cs.append((ck, child_start, child_end, gcs))
        end_i = child_end
        hm.update(chm)
    node_end = end_i if cs else node_start + len(k)
    if k in g and k != START_SYMBOL:
        hm[k] = (node_start, node_end - node_start)
    return hm, (k, node_start, node_end, new_cs)

if __name__ == '__main__':
    span_hm, _n = span(dt, INVENTORY_GRAMMAR)

if __name__ == '__main__':
    span_hm

if __name__ == '__main__':
    print("query:", query)
    for k in span_hm:
        start, l = span_hm[k]
        print(k, query[start:start + l])

def unwrap_substrings(s):
    assert s.decl().name() == 'str.substr'
    cs, frm, l = s.children()
    fl = frm.as_long()
    ll = l.as_long()
    if cs.decl().name() == 'str.substr':
        newfrm, _l = unwrap_substrings(cs)
        return (fl + newfrm, ll)
    else:
        return (fl, ll)

def traverse_z3(p, hm):
    def z3_as_string(v):
        return v.as_string()

    n = p.decl().name()
    if n == 'not':
        return traverse_z3(p.children()[0], hm)
    elif n == '=':
        i, j = p.children()
        if isinstance(i, (int, z3.IntNumRef)):
            return traverse_z3(j, hm)
        elif isinstance(j, (int, z3.IntNumRef)):
            return traverse_z3(i, hm)
        else:
            if i.is_string() and j.is_string():
                if i.is_string_value():
                    cs, frm, l = j.children()
                    if (isinstance(frm, z3.IntNumRef)
                            and isinstance(l, z3.IntNumRef)):
                        hm[z3_as_string(i)] = unwrap_substrings(j)
                elif j.is_string_value():
                    cs, frm, l = i.children()
                    if (isinstance(frm, z3.IntNumRef)
                            and isinstance(l, z3.IntNumRef)):
                        hm[z3_as_string(j)] = unwrap_substrings(i)
            else:
                assert False  # for now
    elif n == '<' or n == '>':
        i, j = p.children()
        if isinstance(i, (int, z3.IntNumRef)):
            return traverse_z3(j, hm)
        elif isinstance(j, (int, z3.IntNumRef)):
            return traverse_z3(i, hm)
        else:
            assert False
    return p

if __name__ == '__main__':
    comparisons: Dict[str, Tuple] = {}
    for p in _.path:
        traverse_z3(p, comparisons)
    comparisons

def find_alternatives(spans, cmp):
    alts = {}
    for key in spans:
        start, l = spans[key]
        rset = set(range(start, start + l))
        for ckey in cmp:
            cstart, cl = cmp[ckey]
            cset = set(range(cstart, cstart + cl))
            # if rset.issubset(cset): <- ignoring subsets for now.
            if rset == cset:
                if key not in alts:
                    alts[key] = set()
                alts[key].add(ckey)
    return alts

if __name__ == '__main__':
    alternatives = find_alternatives(span_hm, comparisons)
    alternatives

INVENTORY_GRAMMAR_NEW = dict(INVENTORY_GRAMMAR)

if __name__ == '__main__':
    for k in alternatives:
        INVENTORY_GRAMMAR_NEW[k] = INVENTORY_GRAMMAR_NEW[k] + list(alternatives[k])

if __name__ == '__main__':
    INVENTORY_GRAMMAR_NEW['<table>']

if __name__ == '__main__':
    cgf = ConcolicGrammarFuzzer(INVENTORY_GRAMMAR_NEW)

if __name__ == '__main__':
    for i in range(10):
        qtree = cgf.fuzz_tree()
        query = cgf.tree_to_string(qtree)
        print(query)
        with ExpectError(print_traceback=False):
            try:
                with ConcolicTracer() as _:
                    res = _[db_select](query)
                print(repr(res))
            except SQLException as e:
                print(e)
            print()

if __name__ == '__main__':
    gf = GrammarFuzzer(INVENTORY_GRAMMAR)
    for i in range(10):
        query = gf.fuzz()
        print(query)
        with ExpectError(print_traceback=False):
            try:
                res = db_select(query)
                print(repr(res))
            except SQLException as e:
                print(e)
            print()

#### Pruning and Updating

if __name__ == '__main__':
    print('\n#### Pruning and Updating')



class ConcolicGrammarFuzzer(ConcolicGrammarFuzzer):
    def prune_tokens(self, tokens):
        self.prune_tokens = tokens

    def update_grammar(self, trace):
        self.comparisons = {}
        for p in trace.path:
            traverse_z3(p, self.comparisons)
        alternatives = find_alternatives(self.span_range, self.comparisons)
        if self.log:
            print('Alternatives:', alternatives, 'Span:', self.span_range)
        new_grammar = dict(self.grammar)
        for k in alternatives:
            new_grammar[k] = list(set(new_grammar[k] + list(alternatives[k])))
        self.grammar = new_grammar

class ConcolicGrammarFuzzer(ConcolicGrammarFuzzer):
    def fuzz(self):
        qtree = self.fuzz_tree()
        self.pruned_tree = self.prune_tree(qtree, self.prune_tokens)
        query = self.tree_to_string(qtree)
        self.span_range, _n = span(self.pruned_tree, self.grammar)
        return query

if __name__ == '__main__':
    inventory = db.db.pop('inventory', None)

if __name__ == '__main__':
    db.db['vehicles'] = inventory
    db.db['months'] = ({
        'month': int,
        'name': str
    }, [{
        'month': i + 1,
        'name': m
    } for i, m in enumerate([
        'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct',
        'nov', 'dec'
    ])])
    db.db

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



if __name__ == '__main__':
    cgf = ConcolicGrammarFuzzer(INVENTORY_GRAMMAR)
    cgf.prune_tokens(prune_tokens)
    for i in range(10):
        query = cgf.fuzz()
        print(query)
        with ConcolicTracer() as _:
            with ExpectError(print_traceback=False):
                try:
                    res = _[db_select](query)
                    print(repr(res))
                except SQLException as e:
                    print(e)
            cgf.update_grammar(_)
            print()

## Limitations
## -----------

if __name__ == '__main__':
    print('\n## Limitations')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



### ConcolicTracer

if __name__ == '__main__':
    print('\n### ConcolicTracer')



if __name__ == '__main__':
    with ConcolicTracer() as _:
        _[cgi_decode]('a%20d')

if __name__ == '__main__':
    _.decls

if __name__ == '__main__':
    _.path

if __name__ == '__main__':
    assert _.context == (_.decls, _.path)

if __name__ == '__main__':
    _.zeval()

from .ClassDiagram import display_class_hierarchy
display_class_hierarchy(ConcolicTracer)

### SimpleConcolicFuzzer

if __name__ == '__main__':
    print('\n### SimpleConcolicFuzzer')



if __name__ == '__main__':
    scf = SimpleConcolicFuzzer()
    scf.add_trace(_, 'a%20d')

if __name__ == '__main__':
    scf = SimpleConcolicFuzzer()
    for i in range(20):
        v = scf.fuzz()
        if v is None:
            break
        print(repr(v))
        with ExpectError(print_traceback=False):
            with ConcolicTracer() as _:
                _[cgi_decode](v)
        scf.add_trace(_, v)

if __name__ == '__main__':
    display_class_hierarchy(SimpleConcolicFuzzer)

### ConcolicGrammarFuzzer

if __name__ == '__main__':
    print('\n### ConcolicGrammarFuzzer')



from .InformationFlow import INVENTORY_GRAMMAR, SQLException

if __name__ == '__main__':
    cgf = ConcolicGrammarFuzzer(INVENTORY_GRAMMAR)
    cgf.prune_tokens(prune_tokens)
    for i in range(10):
        query = cgf.fuzz()
        print(query)
        with ConcolicTracer() as _:
            with ExpectError(print_traceback=False):
                try:
                    res = _[db_select](query)
                    print(repr(res))
                except SQLException as e:
                    print(e)
            cgf.update_grammar(_)
            print()

if __name__ == '__main__':
    display_class_hierarchy(ConcolicGrammarFuzzer)

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



### Exercise 1: Implment a Concolic Float Proxy Class

if __name__ == '__main__':
    print('\n### Exercise 1: Implment a Concolic Float Proxy Class')



class zfloat(float):
    def __new__(cls, context, zn, v, *args, **kw):
        return float.__new__(cls, v, *args, **kw)

class zfloat(zfloat):
    @classmethod
    def create(cls, context, zn, v=None):
        return zproxy_create(cls, 'Real', z3.Real, context, zn, v)

    def __init__(self, context, z, v=None):
        self.z, self.v = z, v
        self.context = context

class zfloat(zfloat):
    def _zv(self, o):
        return (o.z, o.v) if isinstance(o, zfloat) else (z3.RealVal(o), o)

class zfloat(zfloat):
    def __bool__(self):
        # force registering boolean condition
        if self != 0.0:
            return True
        return False

def make_float_bool_wrapper(fname, fun, zfun):
    def proxy(self, other):
        z, v = self._zv(other)
        z_ = zfun(self.z, z)
        v_ = fun(self.v, v)
        return zbool(self.context, z_, v_)

    return proxy

FLOAT_BOOL_OPS = [
    '__eq__',
    # '__req__',
    '__ne__',
    # '__rne__',
    '__gt__',
    '__lt__',
    '__le__',
    '__ge__',
]

if __name__ == '__main__':
    for fname in FLOAT_BOOL_OPS:
        fun = getattr(float, fname)
        zfun = getattr(z3.ArithRef, fname)
        setattr(zfloat, fname, make_float_bool_wrapper(fname, fun, zfun))

def make_float_binary_wrapper(fname, fun, zfun):
    def proxy(self, other):
        z, v = self._zv(other)
        z_ = zfun(self.z, z)
        v_ = fun(self.v, v)
        return zfloat(self.context, z_, v_)

    return proxy

FLOAT_BINARY_OPS = [
    '__add__',
    '__sub__',
    '__mul__',
    '__truediv__',
    # '__div__',
    '__mod__',
    # '__divmod__',
    '__pow__',
    # '__lshift__',
    # '__rshift__',
    # '__and__',
    # '__xor__',
    # '__or__',
    '__radd__',
    '__rsub__',
    '__rmul__',
    '__rtruediv__',
    # '__rdiv__',
    '__rmod__',
    # '__rdivmod__',
    '__rpow__',
    # '__rlshift__',
    # '__rrshift__',
    # '__rand__',
    # '__rxor__',
    # '__ror__',
]

if __name__ == '__main__':
    for fname in FLOAT_BINARY_OPS:
        fun = getattr(float, fname)
        zfun = getattr(z3.ArithRef, fname)
        setattr(zfloat, fname, make_float_binary_wrapper(fname, fun, zfun))

if __name__ == '__main__':
    with ConcolicTracer() as _:
        za = zfloat.create(_.context, 'float_a', 1.0)
        zb = zfloat.create(_.context, 'float_b', 0.0)
        if za * zb:
            print(1)

if __name__ == '__main__':
    _.context

def make_int_binary_wrapper(fname, fun, zfun):  # type: ignore
    def proxy(self, other):
        z, v = self._zv(other)
        z_ = zfun(self.z, z)
        v_ = fun(self.v, v)
        if isinstance(v_, float):
            return zfloat(self.context, z_, v_)
        elif isinstance(v_, int):
            return zint(self.context, z_, v_)
        else:
            assert False

    return proxy

if __name__ == '__main__':
    for fname in INT_BINARY_OPS:
        fun = getattr(int, fname)
        zfun = getattr(z3.ArithRef, fname)
        setattr(zint, fname, make_int_binary_wrapper(fname, fun, zfun))

if __name__ == '__main__':
    with ConcolicTracer() as _:
        v = _[binomial](4, 2)

if __name__ == '__main__':
    _.zeval()

### Exercise 2: Bit Manipulation

if __name__ == '__main__':
    print('\n### Exercise 2: Bit Manipulation')



def make_int_bit_wrapper(fname, fun, zfun):
    def proxy(self, other):
        z, v = self._zv(other)
        z_ = z3.BV2Int(
            zfun(
                z3.Int2BV(
                    self.z, num_bits=64), z3.Int2BV(
                    z, num_bits=64)))
        v_ = fun(self.v, v)
        return zint(self.context, z_, v_)

    return proxy

BIT_OPS = [
    '__lshift__',
    '__rshift__',
    '__and__',
    '__xor__',
    '__or__',
    '__rlshift__',
    '__rrshift__',
    '__rand__',
    '__rxor__',
    '__ror__',
]

def init_concolic_4():
    for fname in BIT_OPS:
        fun = getattr(int, fname)
        zfun = getattr(z3.BitVecRef, fname)
        setattr(zint, fname, make_int_bit_wrapper(fname, fun, zfun))

INITIALIZER_LIST.append(init_concolic_4)

if __name__ == '__main__':
    init_concolic_4()

class zint(zint):
    def __invert__(self):
        return zint(self.context, z3.BV2Int(
            ~z3.Int2BV(self.z, num_bits=64)), ~self.v)

def my_fn(a, b):
    o_ = (a | b)
    a_ = (a & b)
    if o_ & ~a_:
        return True
    else:
        return False

if __name__ == '__main__':
    with ConcolicTracer() as _:
        print(_[my_fn](2, 1))

if __name__ == '__main__':
    _.zeval(log=True)

### Exercise 3: String Translation Functions

if __name__ == '__main__':
    print('\n### Exercise 3: String Translation Functions')


