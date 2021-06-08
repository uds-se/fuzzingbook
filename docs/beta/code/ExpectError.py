#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Error Handling" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/ExpectError.html
# Last change: 2021-06-02 17:56:28+02:00
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
The Fuzzing Book - Error Handling

This file can be _executed_ as a script, running all experiments:

    $ python ExpectError.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.ExpectError import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/ExpectError.html

The `ExpectError` class allows you to catch and report exceptions, yet resume execution.  This is useful in notebooks, as they would normally interrupt execution as soon as an exception is raised.  Its typical usage is in conjunction with a `with` clause:

>>> with ExpectError():
>>>     x = 1 / 0
Traceback (most recent call last):
  File "", line 2, in 
    x = 1 / 0
ZeroDivisionError: division by zero (expected)


The `ExpectTimeout` class allows you to interrupt execution after the specified time.  This is useful for interrupting code that might otherwise run forever.

>>> with ExpectTimeout(5):
>>>     long_running_test()
Start
0 seconds have passed
1 seconds have passed
2 seconds have passed
3 seconds have passed

Traceback (most recent call last):
  File "", line 2, in 
    long_running_test()
  File "", line 5, in long_running_test
    print(i, "seconds have passed")
  File "", line 5, in long_running_test
    print(i, "seconds have passed")
  File "", line 25, in check_time
    raise TimeoutError
TimeoutError (expected)


The exception and the associated traceback are printed as error messages.  If you do not want that, 
use these keyword options:

* `print_traceback` (default True) can be set to `False` to avoid the traceback being printed
* `mute` (default False) can be set to `True` to completely avoid any output.


For more details, source, and documentation, see
"The Fuzzing Book - Error Handling"
at https://www.fuzzingbook.org/html/ExpectError.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Error Handling
# ==============

if __name__ == '__main__':
    print('# Error Handling')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Catching Errors
## ---------------

if __name__ == '__main__':
    print('\n## Catching Errors')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

import traceback
import sys

from types import FrameType, TracebackType

from typing import Union, Optional, Callable, Any

class ExpectError:
    """Execute a code block expecting (and catching) an error."""

    def __init__(self, exc_type: Optional[type] = None, 
                 print_traceback: bool = True, mute: bool = False):
        """
        Constructor. Expect an exception of type `exc_type` (`None`: any exception).
        If `print_traceback` is set (default), print a traceback to stderr.
        If `mute` is set (default: False), do not print anything.
        """
        self.print_traceback = print_traceback
        self.mute = mute
        self.expected_exc_type = exc_type

    def __enter__(self) -> Any:
        """Begin of `with` block"""
        return self

    def __exit__(self, exc_type: type, 
                 exc_value: BaseException, tb: TracebackType) -> Optional[bool]:
        """End of `with` block"""
        if exc_type is None:
            # No exception
            return

        if (self.expected_exc_type is not None
            and exc_type != self.expected_exc_type):
            raise  # Unexpected exception

        # An exception occurred
        if self.print_traceback:
            lines = ''.join(
                traceback.format_exception(
                    exc_type,
                    exc_value,
                    tb)).strip()
        else:
            lines = traceback.format_exception_only(
                exc_type, exc_value)[-1].strip()

        if not self.mute:
            print(lines, "(expected)", file=sys.stderr)
        return True  # Ignore it

def fail_test() -> None:
    # Trigger an exception
    x = 1 / 0

if __name__ == '__main__':
    with ExpectError():
        fail_test()

if __name__ == '__main__':
    with ExpectError(print_traceback=False):
        fail_test()

if __name__ == '__main__':
    with ExpectError(ZeroDivisionError):
        fail_test()

if __name__ == '__main__':
    with ExpectError():
        with ExpectError(ZeroDivisionError):
            some_nonexisting_function()  # type: ignore

## Catching Timeouts
## -----------------

if __name__ == '__main__':
    print('\n## Catching Timeouts')



import sys
import time

class ExpectTimeout:
    """Execute a code block expecting (and catching) a timeout."""

    def __init__(self, seconds: Union[int, float], 
                 print_traceback: bool = True, mute: bool = False):
        """
        Constructor. Interrupe execution after `seconds` seconds.
        If `print_traceback` is set (default), print a traceback to stderr.
        If `mute` is set (default: False), do not print anything.
        """

        self.seconds_before_timeout = seconds
        self.original_trace_function: Optional[Callable] = None
        self.end_time: Optional[float] = None
        self.print_traceback = print_traceback
        self.mute = mute

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

        if exc_type is None:
            return

        # An exception occurred
        if self.print_traceback:
            lines = ''.join(
                traceback.format_exception(
                    exc_type,
                    exc_value,
                    tb)).strip()
        else:
            lines = traceback.format_exception_only(
                exc_type, exc_value)[-1].strip()

        if not self.mute:
            print(lines, "(expected)", file=sys.stderr)
        return True  # Ignore it

    def cancel(self) -> None:
        sys.settrace(self.original_trace_function)

def long_running_test() -> None:
    print("Start")
    for i in range(10):
        time.sleep(1)
        print(i, "seconds have passed")
    print("End")

if __name__ == '__main__':
    with ExpectTimeout(5, print_traceback=False):
        long_running_test()

if __name__ == '__main__':
    with ExpectTimeout(5):
        with ExpectTimeout(3):
            long_running_test()
        long_running_test()

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    with ExpectError():
        x = 1 / 0

if __name__ == '__main__':
    with ExpectTimeout(5):
        long_running_test()

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')


