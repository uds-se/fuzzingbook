#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/InformationFlow.html
# Last change: 2018-11-28 18:53:34+01:00
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


# # Information Flow

if __name__ == "__main__":
    print('# Information Flow')




import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from ExpectError import ExpectError
else:
    from .ExpectError import ExpectError


import inspect
import enum

# %%html
# <div>
# <style>
# div.todo {
#     color:red;
#     font-weight: bold;
# }
# div.todo::before {
#     content: "TODO: ";
# }
# div.done {
#     color:blue;
#     font-weight: bold;
# }
# div.done::after {
#     content: " :DONE";
# }
# 
# </style>
# <script>
#   function todo_toggle() {
#     if (todo_shown){
#       $('div.todo').hide('500');
#       $('div.done').hide('500');
#       $('#toggleButton').val('Show Todo')
#     } else {
#       $('div.todo').show('500');
#       $('div.done').show('500');
#       $('#toggleButton').val('Hide Todo')
#     }
#     todo_shown = !todo_shown
#   }
#   $( document ).ready(function(){
#     todo_shown=false;
#     $('div.todo').hide()
#   });
# </script>
# <form action="javascript:todo_toggle()"><input type="submit" id="toggleButton" value="Show Todo"></form>

def my_calculator(my_input):
    result = eval(my_input, {}, {})
    print("The result of %s was %d" % (my_input, result))

if __name__ == "__main__":
    my_calculator('1+2')


if __name__ == "__main__":
    with ExpectError():
        my_calculator('__import__("os").popen("ls").read()')


if __name__ == "__main__":
    my_calculator("1 if __builtins__['print'](__import__('os').popen('ls').read()) else 0")


def my_calculator(my_input):
    result = eval(my_input, {"__builtins__":None}, {})
    print("The result of %s was %d" % (my_input, result))

if __name__ == "__main__":
    with ExpectError():
        my_calculator("1 if __builtins__['print'](__import__('os').popen('ls').read()) else 0")


if __name__ == "__main__":
    my_calculator("1 if [x['print'](x['__import__']('os').popen('ls').read()) for x in ([x for x in (1).__class__.__base__.__subclasses__() if x.__name__ == 'Sized'][0].__len__.__globals__['__builtins__'],)] else 0")


# ## A Simple Taint Tracker

if __name__ == "__main__":
    print('\n## A Simple Taint Tracker')




class tstr_(str):
    def __new__(cls, value, *args, **kw):
        return super(tstr_, cls).__new__(cls, value)


class tstr(tstr_):
    def __init__(self, value, taint=None, parent=None):
        self.parent = parent
        l = len(self)
        if taint:
            if isinstance(taint, int):
                self._taint = list(range(taint, taint + len(self)))
            else:
                assert len(taint) == len(self)
                self._taint = taint
        else:
            self._taint = list(range(0, len(self)))

    def has_taint(self):
        return any(True for i in self._taint if i >= 0)

    def __repr__(self):
        return str.__repr__(self)

    def __str__(self):
        return str.__str__(self)

if __name__ == "__main__":
    t = tstr('hello')
    t.has_taint(), t._taint


if __name__ == "__main__":
    t = tstr('world', taint = 6)
    t._taint


class tstr(tstr):
    def untaint(self):
        self._taint =  [-1] * len(self)
        return self

if __name__ == "__main__":
    t = tstr('hello world')
    t.untaint()
    t.has_taint()


if __name__ == "__main__":
    with ExpectError():
        t = tstr('hello world')
        t[0:5].has_taint()


# ### Slice

if __name__ == "__main__":
    print('\n### Slice')




class tstr(tstr):
    def __iter__(self):
        return tstr_iterator(self)

    def __getitem__(self, key):
        def get_interval(key):
            return ((0 if key.start is None else key.start),
                    (len(res) if key.stop is None else key.stop))

        res = super().__getitem__(key)
        if type(key) == int:
            key = len(self) + key if key < 0 else key
            return tstr(res, [self._taint[key]], self)
        elif type(key) == slice:
            if res:
                return tstr(res, self._taint[key], self)
            # Result is an empty string
            t = tstr(res, self._taint[key], self)
            key_start, key_stop = get_interval(key)
            cursor = 0
            if key_start < len(self):
                assert key_stop < len(self)
                cursor = self._taint[key_stop]
            else:
                if len(self) == 0:
                    # if the original string was empty, we assume that any
                    # empty string produced from it should carry the same taint.
                    cursor = self.x()
                else:
                    # Key start was not in the string. We can reply only
                    # if the key start was just outside the string, in
                    # which case, we guess.
                    if key_start != len(self):
                        raise taint.TaintException('Can\'t guess the taint')
                    cursor = self._taint[len(self) - 1] + 1
            # _tcursor gets created only for empty strings.
            t._tcursor = cursor
            return t

        else:
            assert False

# #### The iterator class

if __name__ == "__main__":
    print('\n#### The iterator class')




class tstr_iterator():
    def __init__(self, tstr):
        self._tstr = tstr
        self._str_idx = 0

    def __next__(self):
        if self._str_idx == len(self._tstr): raise StopIteration
        # calls tstr getitem should be tstr
        c = self._tstr[self._str_idx]
        assert type(c) is tstr
        self._str_idx += 1
        return c

if __name__ == "__main__":
    t = tstr('hello world')
    t[0:5].has_taint()


# ### Helper Methods

if __name__ == "__main__":
    print('\n### Helper Methods')




class tstr(tstr):
    class TaintException(Exception):
        pass

    def x(self, i=0):
        v = self._x(i)
        if v < 0:
            raise taint.TaintException('Invalid mapped char idx in tstr')
        return v

    def _x(self, i=0):
        return self.get_mapped_char_idx(i)

    def get_mapped_char_idx(self, i):
        if self._taint:
            return self._taint[i]
        else:
            if i != 0:
                raise taint.TaintException('Invalid request idx')
            # self._tcursor gets created only for empty strings.
            # use the exception to determine which ones need it.
            return self._tcursor

    def get_first_mapped_char(self):
        for i in self._taint:
            if i >= 0:
                return i
        return -1

    def is_tpos_contained(self, tpos):
        return tpos in self._taint

    def is_idx_tainted(self, idx):
        return self._taint[idx] != -1

if __name__ == "__main__":
    print(repr(t[11:]))
    print(t[11:].x(), t[11:]._taint)


if __name__ == "__main__":
    my_str = tstr('abcdefghijkl', taint=list(range(4,16)))
    my_str[0].x(),my_str[-1].x(),my_str[-2].x()


if __name__ == "__main__":
    s = my_str[0:4]
    s.x(0),s.x(3)


if __name__ == "__main__":
    s = my_str[0:-1]
    len(s),s.x(10)


# ### Concatenation

if __name__ == "__main__":
    print('\n### Concatenation')




class tstr(tstr):
    def __add__(self, other):  #concatenation (+)
        if type(other) is tstr:
            return tstr(str.__add__(self, other), (self._taint + other._taint), self)
        else:
            return tstr(str.__add__(self, other), (self._taint + [-1 for i in other]), self)

if __name__ == "__main__":
    my_str1 = tstr("hello")
    my_str2 = tstr("world", taint=6)
    my_str3 = "bye"
    v = my_str1 + my_str2
    print(v._taint)

    w = my_str1 + my_str3 + my_str2
    print(w._taint)


class tstr(tstr):
    def __radd__(self, other):  #concatenation (+) -- other is not tstr
        if type(other) is tstr:
            return tstr(str.__add__(other, self), (other._taint + self._taint), self)
        else:
            return tstr(str.__add__(other, self), ([-1 for i in other] + self._taint), self)

if __name__ == "__main__":
    my_str1 = "hello"
    my_str2 = tstr("world")
    v = my_str1 + my_str2
    v._taint


# ### Replace

if __name__ == "__main__":
    print('\n### Replace')




class tstr(tstr):
    def replace(self, a, b, n=None):
        old_taint = self._taint
        b_taint = b._taint if type(b) is tstr else [-1] * len(b)
        mystr = str(self)
        i = 0
        while True:
            if n and i >= n: break
            idx = mystr.find(a)
            if idx == -1: break
            last = idx + len(a)
            mystr = mystr.replace(a, b, 1)
            partA, partB = old_taint[0:idx], old_taint[last:]
            old_taint = partA + b_taint + partB
            i += 1
        return tstr(mystr, old_taint, self)

if __name__ == "__main__":
    my_str = tstr("aa cde aa")
    res = my_str.replace('aa', 'bb')
    res, res._taint


# ### Split

if __name__ == "__main__":
    print('\n### Split')




class tstr(tstr):
    def _split_helper(self, sep, splitted):
        result_list = []
        last_idx = 0
        first_idx = 0
        sep_len = len(sep)

        for s in splitted:
            last_idx = first_idx + len(s)
            item = self[first_idx:last_idx]
            result_list.append(item)
            first_idx = last_idx + sep_len
        return result_list

    def _split_space(self, splitted):
        result_list = []
        last_idx = 0
        first_idx = 0
        sep_len = 0
        for s in splitted:
            last_idx = first_idx + len(s)
            item = self[first_idx:last_idx]
            result_list.append(item)
            v = str(self[last_idx:])
            sep_len = len(v) - len(v.lstrip(' '))
            first_idx = last_idx + sep_len
        return result_list

    def rsplit(self, sep=None, maxsplit=-1):
        splitted = super().rsplit(sep, maxsplit)
        if not sep:
            return self._split_space(splitted)
        return self._split_helper(sep, splitted)

    def split(self, sep=None, maxsplit=-1):
        splitted = super().split(sep, maxsplit)
        if not sep:
            return self._split_space(splitted)
        return self._split_helper(sep, splitted)

if __name__ == "__main__":
    my_str = tstr('ab cdef ghij kl')
    ab, cdef, ghij, kl = my_str.rsplit(sep=' ')
    print(ab._taint, cdef._taint, ghij._taint, kl._taint)

    my_str = tstr('ab   cdef ghij    kl', taint=100)
    ab, cdef, ghij, kl = my_str.rsplit()
    print(ab._taint, cdef._taint, ghij._taint, kl._taint)


if __name__ == "__main__":
    my_str = tstr('ab cdef ghij kl', taint=list(range(0, 15)))
    ab, cdef, ghij, kl = my_str.split(sep=' ')
    print(ab._taint, cdef._taint, kl._taint)

    my_str = tstr('ab   cdef ghij    kl', taint=list(range(0, 20)))
    ab, cdef, ghij, kl = my_str.split()
    print(ab._taint, cdef._taint, kl._taint)


# ### Strip

if __name__ == "__main__":
    print('\n### Strip')




class tstr(tstr):
    def strip(self, cl=None):
        return self.lstrip(cl).rstrip(cl)

    def lstrip(self, cl=None):
        res = super().lstrip(cl)
        i = self.find(res)
        return self[i:]

    def rstrip(self, cl=None):
        res = super().rstrip(cl)
        return self[0:len(res)]


if __name__ == "__main__":
    my_str1 = tstr("  abc  ")
    v = my_str1.strip()
    v, v._taint


if __name__ == "__main__":
    my_str1 = tstr("  abc  ")
    v = my_str1.lstrip()
    v, v._taint


if __name__ == "__main__":
    my_str1 = tstr("  abc  ")
    v = my_str1.rstrip()
    v, v._taint


# ### Expand Tabs

if __name__ == "__main__":
    print('\n### Expand Tabs')




class tstr(tstr):
    def expandtabs(self, n=8):
        parts = self.split('\t')
        res = super().expandtabs(n)
        all_parts = []
        for i, p in enumerate(parts):
            all_parts.extend(p._taint)
            if i < len(parts) - 1:
                l = len(all_parts) % n
                all_parts.extend([p._taint[-1]] * l)
        return tstr(res, all_parts, self)

if __name__ == "__main__":
    my_tstr = tstr("ab\tcd")
    my_str = str("ab\tcd")
    v1 = my_str.expandtabs(4)
    v2 = my_tstr.expandtabs(4)
    print(len(v1), repr(my_tstr), repr(v2), v2._taint)


class tstr(tstr):
    def join(self, iterable):
        mystr = ''
        mytaint = []
        sep_taint = self._taint
        lst = list(iterable)
        for i, s in enumerate(lst):
            staint = s._taint if type(s) is tstr else [-1] * len(s)
            mytaint.extend(staint)
            mystr += str(s)
            if i < len(lst)-1:
                mytaint.extend(sep_taint)
                mystr += str(self)
        res = super().join(iterable)
        assert len(res) == len(mystr)
        return tstr(res, mytaint, self)

if __name__ == "__main__":
    my_str = tstr("ab cd", taint=100)
    (v1, v2), v3 = my_str.split(), 'ef'
    print(v1._taint, v2._taint)
    v4 = tstr('').join([v2,v3,v1])
    print(v4, v4._taint)


if __name__ == "__main__":
    my_str = tstr("ab cd", taint=100)
    (v1, v2), v3 = my_str.split(), 'ef'
    print(v1._taint, v2._taint)
    v4 = tstr(',').join([v2,v3,v1])
    print(v4, v4._taint)


# ### Partitions

if __name__ == "__main__":
    print('\n### Partitions')




class tstr(tstr):
    def partition(self, sep):
        partA, sep, partB = super().partition(sep)
        return (tstr(partA, self._taint[0:len(partA)], self), tstr(sep, self._taint[len(partA): len(partA) + len(sep)], self), tstr(partB, self._taint[len(partA) + len(sep):], self))

    def rpartition(self, sep):
        partA, sep, partB = super().rpartition(sep)
        return (tstr(partA, self._taint[0:len(partA)], self), tstr(sep, self._taint[len(partA): len(partA) + len(sep)], self), tstr(partB, self._taint[len(partA) + len(sep):], self))

# ### Justify

if __name__ == "__main__":
    print('\n### Justify')




class tstr(tstr):
    def ljust(self, width, fillchar=' '):
        res = super().ljust(width, fillchar)
        initial = len(res) - len(self)
        if type(fillchar) is tstr:
            t = fillchar.x()
        else:
            t = -1
        return tstr(res, [t] * initial + self._taint, self)

    def rjust(self, width, fillchar=' '):
        res = super().rjust(width, fillchar)
        final = len(res) - len(self)
        if type(fillchar) is tstr:
            t = fillchar.x()
        else:
            t = -1
        return tstr(res, self._taint + [t] * final, self)

# ### String methods that do not change taint

if __name__ == "__main__":
    print('\n### String methods that do not change taint')




def make_str_wrapper_eq_taint(fun):
    def proxy(*args, **kwargs):
        res = fun(*args, **kwargs)
        return tstr(res, args[0]._taint, args[0])
    return proxy

for name, fn in inspect.getmembers(str, callable):
    if name in ['swapcase', 'upper', 'lower', 'capitalize', 'title']:
        setattr(tstr, name, make_str_wrapper_eq_taint(fn))


if __name__ == "__main__":
    a = tstr('aa', taint=100).upper()
    a, a._taint


# ### General wrappers

if __name__ == "__main__":
    print('\n### General wrappers')




def make_str_wrapper(fun):
    def proxy(*args, **kwargs):
        res = fun(*args, **kwargs)
        return res
    return proxy

import types
tstr_members = [name for name, fn in inspect.getmembers(tstr,callable)
if type(fn) == types.FunctionType and fn.__qualname__.startswith('tstr')]

for name, fn in inspect.getmembers(str, callable):
    if name not in set(['__class__', '__new__', '__str__', '__init__',
                        '__repr__','__getattribute__']) | set(tstr_members):
        setattr(tstr, name, make_str_wrapper(fn))

# ### Methods yet to be translated

if __name__ == "__main__":
    print('\n### Methods yet to be translated')




def make_str_abort_wrapper(fun):
    def proxy(*args, **kwargs):
        raise TaintException('%s Not implemented in TSTR' % fun.__name__)
    return proxy

for name, fn in inspect.getmembers(str, callable):
    if name in ['__format__', '__rmod__', '__mod__', 'format_map', 'format',
               '__mul__','__rmul__','center','zfill', 'decode', 'encode', 'splitlines']:
        setattr(tstr, name, make_str_abort_wrapper(fn))

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



