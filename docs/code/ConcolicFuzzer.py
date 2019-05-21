#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/ConcolicFuzzer.html
# Last change: 2019-05-21 19:58:02+02:00
#
#
# Copyright (c) 2018-2019 Saarland University, CISPA, authors, and contributors
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


# # Concolic Fuzzing

if __name__ == "__main__":
    print('# Concolic Fuzzing')




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




# ## Tracking Constraints

if __name__ == "__main__":
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

if __name__ == "__main__":
    factorial(5)


if __package__ is None or __package__ == "":
    from Coverage import Coverage
else:
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

if __name__ == "__main__":
    with ArcCoverage() as cov:
        factorial(5)


if __package__ is None or __package__ == "":
    from ControlFlow import PyCFG, CFGNode, to_graph, gen_cfg
else:
    from .ControlFlow import PyCFG, CFGNode, to_graph, gen_cfg


if __name__ == "__main__":
    from graphviz import Source, Graph


if __name__ == "__main__":
    Source(to_graph(gen_cfg(inspect.getsource(factorial)), arcs=cov.arcs()))


# ## Concolic Execution

if __name__ == "__main__":
    print('\n## Concolic Execution')




if __name__ == "__main__":
    lines = [i[1] for i in cov._trace if i[0] == 'factorial']
    src = {i + 1: s for i, s in enumerate(
        inspect.getsource(factorial).split('\n'))}


if __name__ == "__main__":
    src[1]


if __name__ == "__main__":
    src[2], src[3], src[4]


# ## SMT Solvers

if __name__ == "__main__":
    print('\n## SMT Solvers')




import z3

if __name__ == "__main__":
    assert z3.get_version() == (4, 8, 0, 0)
    z3.set_option('smt.string_solver', 'z3str3')
    z3.set_option('timeout', 30 * 1000)  # milliseconds


if __name__ == "__main__":
    zn = z3.Int('n')


if __name__ == "__main__":
    zn < 0


if __name__ == "__main__":
    z3.Not(zn < 0)


if __name__ == "__main__":
    z3.solve(z3.Not(zn < 0))


if __name__ == "__main__":
    x = z3.Real('x')
    eqn = (2 * x**2 - 11 * x + 5 == 0)
    z3.solve(eqn)


if __name__ == "__main__":
    z3.solve(x != 5, eqn)


if __name__ == "__main__":
    z3.solve(zn < 0)


if __name__ == "__main__":
    with cov as cov:
        factorial(-1)


if __name__ == "__main__":
    Source(to_graph(gen_cfg(inspect.getsource(factorial)), arcs=cov.arcs()))


if __name__ == "__main__":
    src[4]


if __name__ == "__main__":
    predicates = [z3.Not(zn < 0), z3.Not(zn == 0)]


if __name__ == "__main__":
    src[6]


if __name__ == "__main__":
    predicates = [z3.Not(zn < 0), z3.Not(zn == 0), z3.Not(zn == 1)]


if __name__ == "__main__":
    last = len(predicates) - 1
    z3.solve(predicates[0:-1] + [z3.Not(predicates[-1])])


# ## A Concolic Tracer

if __name__ == "__main__":
    print('\n## A Concolic Tracer')




class ConcolicTracer:
    def __init__(self, context=None):
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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        _[factorial](1)


if __name__ == "__main__":
    _.context


# ### Concolic Proxy Objects

if __name__ == "__main__":
    print('\n### Concolic Proxy Objects')




def zproxy_create(cls, sname, z3var, context, zn, v=None):
    zv = cls(context, z3var(zn), v)
    context[0][zn] = sname
    return zv

# #### A Proxy Class for Booleans

if __name__ == "__main__":
    print('\n#### A Proxy Class for Booleans')




class zbool:
    @classmethod
    def create(cls, context, zn, v):
        return zproxy_create(cls, 'Bool', z3.Bool, context, zn, v)

    def __init__(self, context, z, v=None):
        self.context, self.z, self.v = context, z, v
        self.decl, self.path = self.context

if __name__ == "__main__":
    with ConcolicTracer() as _:
        za, zb = z3.Ints('a b')
        val = zbool.create(_.context, 'my_bool_arg', True)
        print(val.z, val.v)
    _.context


# ##### Negation of Encoded formula

if __name__ == "__main__":
    print('\n##### Negation of Encoded formula')




class zbool(zbool):
    def __not__(self):
        return zbool(self.context, z3.Not(self.z), not self.v)

if __name__ == "__main__":
    with ConcolicTracer() as _:
        val = zbool.create(_.context, 'my_bool_arg', True).__not__()
        print(val.z, val.v)
    _.context


# ##### Registering Predicates on Conditionals

if __name__ == "__main__":
    print('\n##### Registering Predicates on Conditionals')




class zbool(zbool):
    def __bool__(self):
        r, pred = (True, self.z) if self.v else (False, z3.Not(self.z))
        self.path.append(pred)
        return r

if __name__ == "__main__":
    ca, za = 5, z3.Int('a')


if __name__ == "__main__":
    with ConcolicTracer() as _:
        if zbool(_.context, za == z3.IntVal(5), ca == 5):
            print('success')


if __name__ == "__main__":
    _.path


# #### A Proxy Class for Integers

if __name__ == "__main__":
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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        val = zint.create(_.context, 'int_arg', 0)
        print(val.z, val.v)
    _.context


class zint(zint):
    def _zv(self, o):
        return (o.z, o.v) if isinstance(o, zint) else (z3.IntVal(o), o)

if __name__ == "__main__":
    with ConcolicTracer() as _:
        val = zint.create(_.context, 'int_arg', 0)
        print(val._zv(0))
        print(val._zv(val))


# ##### Equality between Integers

if __name__ == "__main__":
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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        ia = zint.create(_.context, 'int_a', 0)
        ib = zint.create(_.context, 'int_b', 0)
        v1 = ia == ib
        v2 = ia != ib
        v3 = 0 != ib
        print(v1.z, v2.z, v3.z)


# ##### Comparisons between Integers

if __name__ == "__main__":
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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        ia = zint.create(_.context, 'int_a', 0)
        ib = zint.create(_.context, 'int_b', 1)
        v1 = ia > ib
        v2 = ia < ib
        print(v1.z, v2.z)
        v3 = ia >= ib
        v4 = ia <= ib
        print(v3.z, v4.z)


# ##### Binary Operators for Integers

if __name__ == "__main__":
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

def make_int_binary_wrapper(fname, fun, zfun):
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

if __name__ == "__main__":
    for fname in INT_BINARY_OPS:
        fun = getattr(int, fname)
        zfun = getattr(z3.ArithRef, fname)
        setattr(zint, fname, make_int_binary_wrapper(fname, fun, zfun))


if __name__ == "__main__":
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


# ##### Integer Unary Operators

if __name__ == "__main__":
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

if __name__ == "__main__":
    for fname in INT_UNARY_OPS:
        fun = getattr(int, fname)
        zfun = getattr(z3.ArithRef, fname)
        setattr(zint, fname, make_int_unary_wrapper(fname, fun, zfun))


if __name__ == "__main__":
    with ConcolicTracer() as _:
        ia = zint.create(_.context, 'int_a', 0)
        print((-ia).z)
        print((+ia).z)


# ##### Using an Integer in a Boolean Context

if __name__ == "__main__":
    print('\n##### Using an Integer in a Boolean Context')




class zint(zint):
    def __bool__(self):
        # return zbool(self.context, self.z, self.v) <-- not allowed
        # force registering boolean condition
        if self != 0:
            return True
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        za = zint.create(_.context, 'int_a', 1)
        zb = zint.create(_.context, 'int_b', 0)
        if za and zb:
            print(1)


if __name__ == "__main__":
    _.context


# #### Remaining Methods of the  ConcolicTracer

if __name__ == "__main__":
    print('\n#### Remaining Methods of the  ConcolicTracer')




# ##### Translating to the SMT Expression Format

if __name__ == "__main__":
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

if __name__ == "__main__":
    triangle(1, 2, 1)


if __name__ == "__main__":
    with ConcolicTracer() as _:
        za = zint.create(_.context, 'int_a', 1)
        zb = zint.create(_.context, 'int_b', 1)
        zc = zint.create(_.context, 'int_c', 1)
        triangle(za, zb, zc)
    print(_.context)


if __name__ == "__main__":
    print(_.smt_expr(show_decl=True))


if __name__ == "__main__":
    z3.solve(_.path)


# ##### Generating Fresh Names

if __name__ == "__main__":
    print('\n##### Generating Fresh Names')




COUNTER = 0

def fresh_name():
    global COUNTER
    COUNTER += 1
    return COUNTER

if __name__ == "__main__":
    fresh_name()


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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        _[factorial](5)


if __name__ == "__main__":
    _.context


if __name__ == "__main__":
    print(_.smt_expr(show_decl=True))


# ##### Evaluating the Concolic Expressions

if __name__ == "__main__":
    print('\n##### Evaluating the Concolic Expressions')




class ConcolicTracer(ConcolicTracer):
    def zeval(self, python=False, log=False):
        r, sol = (zeval_py if python else zeval_smt)(self.path, self, log)
        if r == 'sat':
            return r, {k: sol.get(self.fn_args[k], None) for k in self.fn_args}
        else:
            return r, None

# ##### Using the Python API

if __name__ == "__main__":
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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        _[factorial](5)


if __name__ == "__main__":
    _.zeval(python=True)


# ##### Using the Command Line

if __name__ == "__main__":
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

if __name__ == "__main__":
    parse_sexp('abcd (hello 123 (world "hello world"))')


import tempfile

def zeval_smt(path, cc, log):
    s = cc.smt_expr(True, True, path)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.smt') as f:
        f.write(s)
        f.write("\n(check-sat)")
        f.write("\n(get-model)")
        f.flush()

        if log:
            print(s, '(check-sat)', '(get-model)', sep='\n')
        output = subprocess.getoutput("z3 " + f.name)
    
    if log:
        print(output)
    o = parse_sexp(output)
    kind = o[0]
    if kind == 'unknown':
        return 'Gave up', None
    elif kind == 'unsat':
        return 'No Solutions', {}
    assert kind == 'sat'
    assert o[1][0] == 'model'
    return 'sat', {i[1]: i[-1] for i in o[1][1:]}

if __name__ == "__main__":
    with ConcolicTracer() as _:
        _[factorial](5)


if __name__ == "__main__":
    _.zeval()


# #### A Proxy Class for Strings

if __name__ == "__main__":
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

# ##### Retrieving Ordinal Value

if __name__ == "__main__":
    print('\n##### Retrieving Ordinal Value')




def zord(context, c):
    bn = "bitvec_%d" % fresh_name()
    v = z3.BitVec(bn, 8)
    context[0][bn] = 'BitVec'
    z = (z3.Unit(v) == c)
    context[1].append(z)
    return v

if __name__ == "__main__":
    zc = z3.String('arg_%d' % fresh_name())


if __name__ == "__main__":
    with ConcolicTracer() as _:
        zi = zord(_.context, zc)


if __name__ == "__main__":
    _.context


if __name__ == "__main__":
    z3.solve(_.path + [zi == 65])


# ##### Translating an Ordinal Value to ASCII

if __name__ == "__main__":
    print('\n##### Translating an Ordinal Value to ASCII')




def zchr(context, i):
    sn = 'string_%d' % fresh_name()
    s = z3.String(sn)
    context[0][sn] = 'String'
    z = z3.And([s == z3.Unit(i), z3.Length(s) == 1])
    context[1].append(z)
    return s

if __name__ == "__main__":
    i = z3.BitVec('bv_%d' % fresh_name(), 8)


if __name__ == "__main__":
    with ConcolicTracer() as _:
        zc = zchr(_.context, i)


if __name__ == "__main__":
    _.context


if __name__ == "__main__":
    z3.solve(_.path + [zc == z3.StringVal('a')])


# ##### Equality between Strings

if __name__ == "__main__":
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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr1]('h')


if __name__ == "__main__":
    _.zeval()


def tstr1(s):
    if s == 'hello world':
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr1]('hello world')


if __name__ == "__main__":
    _.context


if __name__ == "__main__":
    _.zeval()


# ##### Concatenation of Strings

if __name__ == "__main__":
    print('\n##### Concatenation of Strings')




class zstr(zstr):
    def __add__(self, other):
        z, v = self._zv(other)
        return zstr(self.context, self.z + z, self.v + v)

    def __radd__(self, other):
        return self.__add__(other)

if __name__ == "__main__":
    with ConcolicTracer() as _:
        v1, v2 = [zstr.create(_.context, 'arg_%d' % fresh_name(), s)
                  for s in ['hello', 'world']]
        if (v1 + ' ' + v2) == 'hello world':
            print('hello world')


if __name__ == "__main__":
    _.context


# ##### Producing Substrings

if __name__ == "__main__":
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

# ##### An Iterator Class for Strings

if __name__ == "__main__":
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

def tstr2(s):
    if s[0] == 'h' and s[1] == 'e' and s[3] == 'l':
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr2]('hello')


if __name__ == "__main__":
    _.context


if __name__ == "__main__":
    _.zeval()


# ##### Translating to Upper and Lower Equivalents

if __name__ == "__main__":
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

def tstr3(s):
    if s.upper() == 'H':
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr3]('h')


if __name__ == "__main__":
    _.zeval()


def tstr4(s):
    if s.lower() == 'hello world':
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr4]('Hello World')


if __name__ == "__main__":
    _.zeval()


# ##### Checking for String Prefixes

if __name__ == "__main__":
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

def tstr5(s):
    if s.startswith('hello'):
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr5]('hello world')


if __name__ == "__main__":
    _.zeval()


if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr5]('my world')


if __name__ == "__main__":
    _.zeval()


# ##### Finding Substrings

if __name__ == "__main__":
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

def tstr6(s):
    if s.find('world') != -1:
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr6]('hello world')


if __name__ == "__main__":
    _.zeval()


# ##### Remove Space from Ends

if __name__ == "__main__":
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

def tstr7(s):
    if s.rstrip(' ') == 'a b':
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr7]('a b   ')
        print(r)


if __name__ == "__main__":
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

def tstr8(s):
    if s.lstrip(' ') == 'a b':
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr8]('   a b')
        print(r)


if __name__ == "__main__":
    _.zeval()


class zstr(zstr):
    def strip(self, chars=None):
        return self.lstrip(chars).rstrip(chars)

def tstr9(s):
    if s.strip() == 'a b':
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr9]('    a b  ')
        print(r)


if __name__ == "__main__":
    _.zeval()


# ##### Splitting Strings

if __name__ == "__main__":
    print('\n##### Splitting Strings')




class zstr(zstr):
    def split(self, sep=None, maxsplit=-1):
        assert sep is not None  # default space based split is complicated
        assert maxsplit == -1  # for now.
        zsep = z3.StringVal(sep)
        zl = z3.Length(zsep)
        zi = z3.IndexOf(self.z, zsep, z3.IntVal(0))  # zi would be the length of prefix
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

def tstr10(s):
    if s.split(',') == ['a', 'b', 'c']:
        return True
    else:
        return False

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[tstr10]('a,b,c')
        print(r)


if __name__ == "__main__":
    _.zeval()


# ##### Trip Wire

if __name__ == "__main__":
    print('\n##### Trip Wire')




def make_str_abort_wrapper(fun):
    def proxy(*args, **kwargs):
        raise Exception( '%s Not implemented in `zstr`' % fun.__name__)
    return proxy

if __name__ == "__main__":
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


# ## Examples

if __name__ == "__main__":
    print('\n## Examples')




# ### Triangle

if __name__ == "__main__":
    print('\n### Triangle')




if __name__ == "__main__":
    with ConcolicTracer() as _:
        print(_[triangle](1, 2, 3))


if __name__ == "__main__":
    _.path


if __name__ == "__main__":
    _.zeval()


if __name__ == "__main__":
    za, zb, zc = [z3.Int(s) for s in _.context[0].keys()]


if __name__ == "__main__":
    _.zeval({1: zb == zc})


if __name__ == "__main__":
    triangle(1, 0, 1)


# ### Round

if __name__ == "__main__":
    print('\n### Round')




def round10(r):
    while r % 10 != 0:
        r += 1
    return r

if __name__ == "__main__":
    with ConcolicTracer() as _:
        r = _[round10](1)


if __name__ == "__main__":
    _.context


if __name__ == "__main__":
    _.zeval()


# ### Absolute Maximum

if __name__ == "__main__":
    print('\n### Absolute Maximum')




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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        _[abs_max](2, 1)


if __name__ == "__main__":
    _.context


if __name__ == "__main__":
    _.zeval()


if __name__ == "__main__":
    with ConcolicTracer() as _:
        _[abs_max](-2, -1)


if __name__ == "__main__":
    _.context


if __name__ == "__main__":
    _.zeval()


# ### Binomial Coefficient

if __name__ == "__main__":
    print('\n### Binomial Coefficient')




def factorial(n):
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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        v = _[binomial](4, 2)


if __name__ == "__main__":
    _.zeval()


# ### Database

if __name__ == "__main__":
    print('\n### Database')




if __package__ is None or __package__ == "":
    from InformationFlow import DB, sample_db, update_inventory
else:
    from .InformationFlow import DB, sample_db, update_inventory


if __package__ is None or __package__ == "":
    from GrammarMiner import VEHICLES  # minor dependency
else:
    from .GrammarMiner import VEHICLES  # minor dependency


if __name__ == "__main__":
    db = sample_db()
    for V in VEHICLES:
        update_inventory(db, V)


if __name__ == "__main__":
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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        _[db_select]('select kind from inventory')


if __name__ == "__main__":
    _.path


if __name__ == "__main__":
    _.zeval()


# ## Fuzzing with Constraints

if __name__ == "__main__":
    print('\n## Fuzzing with Constraints')




if __package__ is None or __package__ == "":
    from Fuzzer import Fuzzer, hang_if_no_space
else:
    from .Fuzzer import Fuzzer, hang_if_no_space


if __package__ is None or __package__ == "":
    from ExpectError import ExpectTimeout
else:
    from .ExpectError import ExpectTimeout


import random

class SimpleConcolicFuzzer(Fuzzer):
    def __init__(self):
        self.ct = []
        self.seen = set()
        self.seen_strs = set()
        self.max_tries = 1000
        self.last = None
        self.last_idx = None

class SimpleConcolicFuzzer(SimpleConcolicFuzzer):
    def add_trace(self, tracer):
        self.ct.append(tracer)
        self.last = tracer
        self.last_idx = len(tracer.context[1]) - 1

class SimpleConcolicFuzzer(SimpleConcolicFuzzer):
    def to_num(self, arr):
        return int(
            ''.join(
                reversed([
                    '0' if z3.simplify(i).decl().name() == 'not' else '1'
                    for i in arr
                ] + ['1'])), 2)

if __name__ == "__main__":
    scf = SimpleConcolicFuzzer()
    a, b = z3.Ints('a b')
    print(bin(scf.to_num([z3.Not(a == b)])))
    print(bin(scf.to_num([z3.Not(a == b), a == b])))
    print(bin(scf.to_num([z3.Not(a == b), a == b, z3.Not(a == b)])))


class SimpleConcolicFuzzer(SimpleConcolicFuzzer):
    def get_newpath(self):
        switch = random.randint(0, self.last_idx)
        if self.seen:
            param = list(self.last.fn_args.values())[0]
            sparam = z3.String(param)
            seen = [sparam != z3.StringVal(i) for i in self.seen_strs]
        else:
            seen = []
        new_path = self.last.path[0:switch] + \
            [z3.Not(self.last.path[switch])] + seen
        return self.to_num(new_path), new_path

class SimpleConcolicFuzzer(SimpleConcolicFuzzer):
    def fuzz(self):
        for i in range(self.max_tries):
            pattern, path = self.get_newpath()
            if pattern in self.seen:
                continue
            self.seen.add(pattern)
            s, v = zeval_smt(path, self.last, log=False)
            if s != 'sat':
                continue
            s = list(v.values())[0]
            self.seen_strs.add(s)
            return s
        return None

if __name__ == "__main__":
    with ExpectTimeout(2):
        with ConcolicTracer() as _:
            _[hang_if_no_space]('abcd')


if __name__ == "__main__":
    scf = SimpleConcolicFuzzer()
    scf.add_trace(_)


if __name__ == "__main__":
    for i in range(10):
        v = scf.fuzz()
        if v is None:
            break
        print(v)


if __package__ is None or __package__ == "":
    from Coverage import cgi_decode
else:
    from .Coverage import cgi_decode


if __name__ == "__main__":
    with ConcolicTracer() as _:
        _[cgi_decode]('abcd')


if __name__ == "__main__":
    scf = SimpleConcolicFuzzer()
    scf.add_trace(_)


if __name__ == "__main__":
    for i in range(10):
        v = scf.fuzz()
        if v is None:
            break
        print(v)


# ### ConcolicGrammarFuzzer

if __name__ == "__main__":
    print('\n### ConcolicGrammarFuzzer')




if __package__ is None or __package__ == "":
    from InformationFlow import INVENTORY_GRAMMAR, SQLException
else:
    from .InformationFlow import INVENTORY_GRAMMAR, SQLException


if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer
else:
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

if __name__ == "__main__":
    tgf = ConcolicGrammarFuzzer(INVENTORY_GRAMMAR)
    while True:
        qtree = tgf.fuzz_tree()
        query = str(tgf.tree_to_string(qtree))
        if query.startswith('select'):
            break


if __package__ is None or __package__ == "":
    from ExpectError import ExpectError
else:
    from .ExpectError import ExpectError


if __name__ == "__main__":
    with ExpectError():
        print(repr(query))
        with ConcolicTracer() as _:
            res = _[db_select](str(query))
        print(repr(res))


if __name__ == "__main__":
    for i, p in enumerate(_.path):
        print(i, p)


if __name__ == "__main__":
    new_path = _.path[0:-1] + [z3.Not(_.path[-1])]


if __name__ == "__main__":
    new_ = ConcolicTracer((_.decls, new_path))
    new_.fn = _.fn
    new_.fn_args = _.fn_args


if __name__ == "__main__":
    new_.zeval()


if __name__ == "__main__":
    print(_.path[-1])
    z3.solve(z3.Not(_.path[-1]))


if __package__ is None or __package__ == "":
    from GrammarFuzzer import display_tree
else:
    from .GrammarFuzzer import display_tree


if __name__ == "__main__":
    prune_tokens = [
        '<value>', '<table>', '<column>', '<literals>', '<exprs>', '<bexpr>'
    ]
    dt = tgf.prune_tree(qtree, prune_tokens)
    display_tree(dt)


if __package__ is None or __package__ == "":
    from GrammarFuzzer import START_SYMBOL
else:
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

if __name__ == "__main__":
    span_hm, _n = span(dt, INVENTORY_GRAMMAR)


if __name__ == "__main__":
    span_hm


if __name__ == "__main__":
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
        s = v.as_string()
        # Z3 bug: Python z3 API returns quoted strings for as_string
        assert s[0] == '"' and s[-1] == '"'
        return s[1:-1]

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

if __name__ == "__main__":
    comparisons = {}
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

if __name__ == "__main__":
    alternatives = find_alternatives(span_hm, comparisons)
    alternatives


INVENTORY_GRAMMAR_NEW = dict(INVENTORY_GRAMMAR)

if __name__ == "__main__":
    for k in alternatives:
        INVENTORY_GRAMMAR_NEW[k] = INVENTORY_GRAMMAR_NEW[k] + list(alternatives[k])


if __name__ == "__main__":
    INVENTORY_GRAMMAR_NEW['<table>']


if __name__ == "__main__":
    cgf = ConcolicGrammarFuzzer(INVENTORY_GRAMMAR_NEW)


if __name__ == "__main__":
    for i in range(10):
        qtree = cgf.fuzz_tree()
        query = cgf.tree_to_string(qtree)
        print(query)
        with ExpectError():
            try:
                with ConcolicTracer() as _:
                    res = _[db_select](query)
                print(repr(res))
            except SQLException as e:
                print(e)
            print()


if __name__ == "__main__":
    gf = GrammarFuzzer(INVENTORY_GRAMMAR)
    for i in range(10):
        query = gf.fuzz()
        print(query)
        with ExpectError():
            try:
                res = db_select(query)
                print(repr(res))
            except SQLException as e:
                print(e)
            print()


# #### All together

if __name__ == "__main__":
    print('\n#### All together')




class ConcolicGrammarFuzzer(ConcolicGrammarFuzzer):
    def prune_tokens(self, tokens):
        self.prune_tokens = tokens

    def update_grammar(self, trace):
        self.comparisons = {}
        for p in trace.path:
            traverse_z3(p, comparisons)
        alternatives = find_alternatives(self.span_range, comparisons)
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

if __name__ == "__main__":
    inventory = db.db.pop('inventory', None)


if __name__ == "__main__":
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


if __name__ == "__main__":
    cgf = ConcolicGrammarFuzzer(INVENTORY_GRAMMAR)
    cgf.prune_tokens(prune_tokens)
    for i in range(10):
        query = cgf.fuzz()
        print(query)
        with ConcolicTracer() as _:
            with ExpectError():
                try:
                    res = _[db_select](query)
                    print(repr(res))
                except SQLException as e:
                    print(e)
            cgf.update_grammar(_)
            print()


# ## Limitations

if __name__ == "__main__":
    print('\n## Limitations')




# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




if __package__ is None or __package__ == "":
    from Coverage import cgi_decode
else:
    from .Coverage import cgi_decode


if __name__ == "__main__":
    with ConcolicTracer() as _:
        _[cgi_decode]('abcd')


if __name__ == "__main__":
    scf = SimpleConcolicFuzzer()
    scf.add_trace(_)


if __name__ == "__main__":
    for i in range(10):
        v = scf.fuzz()
        if v is None:
            break
        print(v)


if __package__ is None or __package__ == "":
    from InformationFlow import INVENTORY_GRAMMAR, SQLException
else:
    from .InformationFlow import INVENTORY_GRAMMAR, SQLException


if __name__ == "__main__":
    cgf = ConcolicGrammarFuzzer(INVENTORY_GRAMMAR)
    cgf.prune_tokens(prune_tokens)
    for i in range(10):
        query = cgf.fuzz()
        print(query)
        with ConcolicTracer() as _:
            with ExpectError():
                try:
                    res = _[db_select](query)
                    print(repr(res))
                except SQLException as e:
                    print(e)
            cgf.update_grammar(_)
            print()


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




# ### Exercise 1: Implment a Concolic Float Proxy Class

if __name__ == "__main__":
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

if __name__ == "__main__":
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

if __name__ == "__main__":
    for fname in FLOAT_BINARY_OPS:
        fun = getattr(float, fname)
        zfun = getattr(z3.ArithRef, fname)
        setattr(zfloat, fname, make_float_binary_wrapper(fname, fun, zfun))


if __name__ == "__main__":
    with ConcolicTracer() as _:
        za = zfloat.create(_.context, 'float_a', 1.0)
        zb = zfloat.create(_.context, 'float_b', 0.0)
        if za * zb:
            print(1)


if __name__ == "__main__":
    _.context


def make_int_binary_wrapper(fname, fun, zfun):
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

if __name__ == "__main__":
    for fname in INT_BINARY_OPS:
        fun = getattr(int, fname)
        zfun = getattr(z3.ArithRef, fname)
        setattr(zint, fname, make_int_binary_wrapper(fname, fun, zfun))


if __name__ == "__main__":
    with ConcolicTracer() as _:
        v = _[binomial](4, 2)


if __name__ == "__main__":
    _.zeval()


# ### Exercise 2: Bit Manipulation

if __name__ == "__main__":
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

if __name__ == "__main__":
    for fname in BIT_OPS:
        fun = getattr(int, fname)
        zfun = getattr(z3.BitVecRef, fname)
        setattr(zint, fname, make_int_bit_wrapper(fname, fun, zfun))


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

if __name__ == "__main__":
    with ConcolicTracer() as _:
        print(_[my_fn](2, 1))


if __name__ == "__main__":
    _.zeval(log=True)


# ### Exercise 3: String Translation Functions

if __name__ == "__main__":
    print('\n### Exercise 3: String Translation Functions')



