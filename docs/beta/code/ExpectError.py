#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "The Fuzzing Book".
# Web site: https://www.fuzzingbook.org/html/ExpectError.html
# Last change: 2019-05-19 19:01:14+02:00
#
#!/
# Copyright (c) 2018-2020 CISPA, Saarland University, authors, and contributors
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


# # Error Handling

if __name__ == "__main__":
    print('# Error Handling')




# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




# ## Catching Errors

if __name__ == "__main__":
    print('\n## Catching Errors')




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


import traceback
import sys

class ExpectError(object):
    def __init__(self, print_traceback=True, mute=False):
        self.print_traceback = print_traceback
        self.mute = mute

    # Begin of `with` block
    def __enter__(self):
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            # No exception
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

def fail_test():
    # Trigger an exception
    x = 1 / 0

if __name__ == "__main__":
    with ExpectError():
        fail_test()


if __name__ == "__main__":
    with ExpectError(print_traceback=False):
        fail_test()


# ## Catching Timeouts

if __name__ == "__main__":
    print('\n## Catching Timeouts')




import sys
import time

if __name__ == "__main__":
    try:
        # Should be defined in Python 3
        x = TimeoutError
    except:
        # For Python 2
        class TimeoutError(Exception):
            def __init__(self, value="Timeout"):
                self.value = value

            def __str__(self):
                return repr(self.value)



class ExpectTimeout(object):
    def __init__(self, seconds, print_traceback=True, mute=False):
        self.seconds_before_timeout = seconds
        self.original_trace_function = None
        self.end_time = None
        self.print_traceback = print_traceback
        self.mute = mute

    # Tracing function
    def check_time(self, frame, event, arg):
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        current_time = time.time()
        if current_time >= self.end_time:
            raise TimeoutError

        return self.check_time

    # Begin of `with` block
    def __enter__(self):
        start_time = time.time()
        self.end_time = start_time + self.seconds_before_timeout

        self.original_trace_function = sys.gettrace()
        sys.settrace(self.check_time)
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
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

    def cancel(self):
        sys.settrace(self.original_trace_function)

def long_running_test():
    print("Start")
    for i in range(10):
        time.sleep(1)
        print(i, "seconds have passed")
    print("End")

if __name__ == "__main__":
    with ExpectTimeout(5, print_traceback=False):
        long_running_test()


if __name__ == "__main__":
    with ExpectTimeout(5):
        with ExpectTimeout(3):
            long_running_test()
        long_running_test()


# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




if __name__ == "__main__":
    with ExpectError():
        x = 1 / 0


if __name__ == "__main__":
    with ExpectTimeout(5):
        long_running_test()

