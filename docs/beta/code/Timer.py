#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Timer" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/Timer.html
# Last change: 2021-06-02 17:56:35+02:00
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
The Fuzzing Book - Timer

This file can be _executed_ as a script, running all experiments:

    $ python Timer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.Timer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/Timer.html

The `Timer` class allows you to measure elapsed real time (in fractional seconds).  Its typical usage is in conjunction with a `with` clause:

>>> with Timer() as t:
>>>     some_long_running_function()
>>> t.elapsed_time()
0.04725892299757106


For more details, source, and documentation, see
"The Fuzzing Book - Timer"
at https://www.fuzzingbook.org/html/Timer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Timer
# =====

if __name__ == '__main__':
    print('# Timer')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Measuring Time
## --------------

if __name__ == '__main__':
    print('\n## Measuring Time')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

import time

from typing import Type, Any

def clock() -> float:
    """
    Return the number of fractional seconds elapsed since some point of reference.
    """
    return time.perf_counter()

from types import TracebackType

class Timer:
    def __init__(self) -> None:
        """Constructor"""
        self.start_time = clock()
        self.end_time = None

    def __enter__(self) -> Any:
        """Begin of `with` block"""
        self.start_time = clock()
        self.end_time = None
        return self

    def __exit__(self, exc_type: Type, exc_value: BaseException,
                 tb: TracebackType) -> None:
        """End of `with` block"""
        self.end_time = clock()  # type: ignore

    def elapsed_time(self) -> float:
        """Return elapsed time in seconds"""
        if self.end_time is None:
            # still running
            return clock() - self.start_time
        else:
            return self.end_time - self.start_time  # type: ignore

def some_long_running_function() -> None:
    i = 1000000
    while i > 0:
        i -= 1

if __name__ == '__main__':
    print("Stopping total time:")
    with Timer() as t:
        some_long_running_function()
    print(t.elapsed_time())

if __name__ == '__main__':
    print("Stopping time in between:")
    with Timer() as t:
        for i in range(10):
            some_long_running_function()
            print(t.elapsed_time())

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    with Timer() as t:
        some_long_running_function()
    t.elapsed_time()

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')


