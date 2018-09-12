#!/usr/bin/env python

# This code is part of "Generating Software Tests"
# (https://www.fuzzingbook.org/)
# It is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License,
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)

# # Error Handling
# 
# The code in this notebook helps with handling errors.  Normally, an error in  notebook code causes the execution of the code to stop; while an infinite loop in notebook code causes the notebook to run without end.  This notebook provides two classes to help address these concerns.
# 
# **Prerequisites**
# 
# * This notebook needs some understanding on advanced concepts in Python, notably 
#     * classes
#     * the Python `with` statement
#     * tracing
#     * measuring time
#     * exceptions
# 
# ## Catching Errors
# 
# The class `ExpectError` allows to express that some code produces an exception.  A typical usage looks as follows:
# 
# ```Python
# from ExpectError import ExpectError
# 
# with ExpectError():
#     function_that_is_supposed_to_fail()
# ```
# 
# If an exception occurs, it is printed on standard error; yet, execution continues.
# 
# import fuzzingbook_utils
# 
import traceback

class ExpectError(object):
    # Begin of `with` block
    def __enter__(self):
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            # No exception
            return

        # An exception occurred - print it
        traceback.print_exception(exc_type, exc_value, tb)
        return True  # Ignore it

# Here's an example:
# 
def fail_test():
    # Trigger an exception
    x = 1 / 0

if __name__ == "__main__":
    with ExpectError():
        fail_test()
    
# ## Catching Timeouts
# 
# The class `ExpectTimeout(seconds)` allows to express that some code may run for a long or inifinite time; execution is thus interruoted after `seconds` seconds.  A typical usage looks as follows:
# 
# ```Python
# from ExpectError import ExpectTimeout
# 
# with ExpectTimeout(2) as t:
#     function_that_is_supposed_to_hang()
# ```
# 
# If an exception occurs, it is printed on standard error (as with `ExpectError`); yet, execution continues.
# 
# Should there be a need to cancel the timeout within the `with` block, `t.cancel()` will do the trick.
# 
# The implementation uses `sys.settrace()`, as this seems to be the most portable way to implement timeouts.  It is not very efficient, though.  Also, it only works on individual lines of Python code and will not interrupt a long-running system function.
# 
import sys
import time

if __name__ == "__main__":
    try:
        # Should be defined in Python 3
        x = TimeoutError
    except:
        # For Python 2
        class TimeoutError(Exception):
            def __init__(self, value = "Timeout"):
                self.value = value
            def __str__(self):
                return repr(self.value)
    
class ExpectTimeout(object):
    def __init__(self, seconds):
        self.seconds_before_timeout = seconds
        self.original_trace_function = None
        self.end_time = None

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

        # An exception occurred - print it
        traceback.print_exception(exc_type, exc_value, tb)
        return True  # Ignore it

    def cancel(self):
        sys.settrace(self.original_trace_function)

# Here's an example:
# 
def long_running_test():
    print("Start")
    for i in range(10):
        time.sleep(1)
        print(i, "seconds have passed")
    print("End")

if __name__ == "__main__":
    with ExpectTimeout(5):
        long_running_test()
    
# Note that it is possible to nest multiple timeouts.
# 
if __name__ == "__main__":
    with ExpectTimeout(2):
        with ExpectTimeout(1):
            long_running_test()
        long_running_test()
    
# That's it, folks – enjoy!
# 
