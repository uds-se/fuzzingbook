#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Timeout" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/Timeout.html
# Last change: 2022-01-11 10:39:17+01:00
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
The Fuzzing Book - Timeout

This file can be _executed_ as a script, running all experiments:

    $ python Timeout.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.Timeout import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/Timeout.html

The `Timeout` class throws a `TimeoutError` exception after a given timeout has expired.
Its typical usage is in conjunction with a `with` clause:

>>> try:
>>>     with Timeout(0.2):
>>>         some_long_running_function()
>>>     print("complete!")
>>> except TimeoutError:
>>>     print("Timeout!")
Timeout!


Note: On Unix/Linux systems, the `Timeout` class uses [https://docs.python.org/3.10/library/signal.html](`SIGALRM` signals) (interrupts) to implement timeouts; this has no effect on performance of the tracked code. On other systems (notably Windows), `Timeout` uses the [`sys.settrace()`](https://docs.python.org/3.10/library/sys.html?highlight=settrace#sys.settrace) function to check the timer after each line of code, which affects performance of the tracked code.


For more details, source, and documentation, see
"The Fuzzing Book - Timeout"
at https://www.fuzzingbook.org/html/Timeout.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Timeout
# =======

if __name__ == '__main__':
    print('# Timeout')



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

from typing import Type, Any, Callable, Union, Optional

from types import FrameType, TracebackType

## Variant 1: Unix (using signals, efficient)
## ------------------------------------------

if __name__ == '__main__':
    print('\n## Variant 1: Unix (using signals, efficient)')



import signal

class SignalTimeout:
    """Execute a code block raising a timeout."""

    def __init__(self, timeout: Union[int, float]) -> None:
        """
        Constructor. Interrupt execution after `timeout` seconds.
        """
        self.timeout = timeout
        self.old_handler: Any = signal.SIG_DFL
        self.old_timeout = 0.0

    def __enter__(self) -> Any:
        """Begin of `with` block"""
        # Register timeout() as handler for signal 'SIGALRM'"
        self.old_handler = signal.signal(signal.SIGALRM, self.timeout_handler)
        self.old_timeout, _ = signal.setitimer(signal.ITIMER_REAL, self.timeout)
        return self

    def __exit__(self, exc_type: Type, exc_value: BaseException,
                 tb: TracebackType) -> None:
        """End of `with` block"""
        self.cancel()
        return  # re-raise exception, if any

    def cancel(self) -> None:
        """Cancel timeout"""
        signal.signal(signal.SIGALRM, self.old_handler)
        signal.setitimer(signal.ITIMER_REAL, self.old_timeout)

    def timeout_handler(self, signum: int, frame: Optional[FrameType]) -> None:
        """Handle timeout (SIGALRM) signal"""
        raise TimeoutError()

def some_long_running_function() -> None:
    i = 10000000
    while i > 0:
        i -= 1

if __name__ == '__main__':
    try:
        with SignalTimeout(0.2):
            some_long_running_function()
            print("Complete!")
    except TimeoutError:
        print("Timeout!")

## Variant 2: Generic / Windows (using trace, not very efficient)
## --------------------------------------------------------------

if __name__ == '__main__':
    print('\n## Variant 2: Generic / Windows (using trace, not very efficient)')



import sys

class GenericTimeout:
    """Execute a code block raising a timeout."""

    def __init__(self, timeout: Union[int, float]) -> None:
        """
        Constructor. Interrupt execution after `timeout` seconds.
        """

        self.seconds_before_timeout = timeout
        self.original_trace_function: Optional[Callable] = None
        self.end_time: Optional[float] = None

    def check_time(self, frame: FrameType, event: str, arg: Any) -> Callable:
        """Tracing function"""
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        current_time = time.time()
        if self.end_time and current_time >= self.end_time:
            raise TimeoutError

        return self.check_time

    def __enter__(self) -> Any:
        """Begin of `with` block"""
        start_time = time.time()
        self.end_time = start_time + self.seconds_before_timeout

        self.original_trace_function = sys.gettrace()
        sys.settrace(self.check_time)
        return self

    def __exit__(self, exc_type: type, 
                 exc_value: BaseException, tb: TracebackType) -> Optional[bool]:
        """End of `with` block"""
        self.cancel()
        return None  # re-raise exception, if any

    def cancel(self) -> None:
        """Cancel timeout"""
        sys.settrace(self.original_trace_function)

if __name__ == '__main__':
    try:
        with GenericTimeout(0.2):
            some_long_running_function()
            print("Complete!")
    except TimeoutError:
        print("Timeout!")

## Choosing the right variant
## --------------------------

if __name__ == '__main__':
    print('\n## Choosing the right variant')



Timeout: Type[SignalTimeout] = SignalTimeout if hasattr(signal, 'SIGALRM') else GenericTimeout  # type: ignore

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    try:
        with Timeout(0.2):
            some_long_running_function()
        print("complete!")
    except TimeoutError:
        print("Timeout!")

## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')


