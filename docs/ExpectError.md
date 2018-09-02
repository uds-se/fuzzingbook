
_This notebook is a chapter of the book ["Generating Software Tests"](https://uds-se.github.io/fuzzingbook/Main.html)._ <br>
<a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/ExpectError.ipynb"><img style="float:right" src="https://mybinder.org/badge.svg" alt="Launch Binder (beta)"></a>
[Interactive version (beta)](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/ExpectError.ipynb) • 
[Download code](https://uds-se.github.io/fuzzingbook/code/ExpectError.py) • 
[Table of contents](https://uds-se.github.io/fuzzingbook/Main.html) • 
[Change history](https://github.com/uds-se/fuzzingbook/commits/master/notebooks/ExpectError.ipynb) • 
[Issues and comments](https://github.com/uds-se/fuzzingbook/issues) • 
[Main project page](https://github.com/uds-se/fuzzingbook/)
<hr>

# Error Handling

The code in this notebook helps with handling errors.  Normally, an error in  notebook code causes the execution of the code to stop; while an infinite loop in notebook code causes the notebook to run without end.  This notebook provides two classes to help address these concerns.

**Prerequisites**

* This notebook needs some understanding on advanced concepts in Python, notably 
    * classes
    * the Python `with` statement
    * tracing
    * measuring time
    * exceptions

## Catching Errors

The class `ExpectError` allows to express that some code produces an exception.  A typical usage looks as follows:

```Python
from ExpectError import ExpectError

with ExpectError():
    function_that_is_supposed_to_fail()
```

If an exception occurs, it is printed on standard error; yet, execution continues.


```python
import fuzzingbook_utils
```


```python
import traceback
```


```python
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
```

Here's an example:


```python
def fail_test():
    # Trigger an exception
    x = 1 / 0
```


```python
with ExpectError():
    fail_test()
```

    Traceback (most recent call last):
      File "<ipython-input-33-67c629a2a842>", line 2, in <module>
        fail_test()
      File "<ipython-input-32-2e8a6dbc7b2c>", line 3, in fail_test
        x = 1 / 0
    ZeroDivisionError: division by zero


## Catching Timeouts

The class `ExpectTimeout(seconds)` allows to express that some code may run for a long or inifinite time; execution is thus interruoted after `seconds` seconds.  A typical usage looks as follows:

```Python
from ExpectError import ExpectTimeout

with ExpectTimeout(2) as t:
    function_that_is_supposed_to_hang()
```

If an exception occurs, it is printed on standard error (as with `ExpectError`); yet, execution continues.

Should there be a need to cancel the timeout within the `with` block, `t.cancel()` will do the trick.

The implementation uses `sys.settrace()`, as this seems to be the most portable way to implement timeouts.  It is not very efficient, though.  Also, it only works on individual lines of Python code and will not interrupt a long-running system function.


```python
import sys
import time
```


```python
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
```


```python
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
```

Here's an example:


```python
def long_running_test():
    print("Start")
    for i in range(10):
        time.sleep(1)
        print(i, "seconds have passed")
    print("End")
```


```python
with ExpectTimeout(5):
    long_running_test()
```

    Start
    0 seconds have passed
    1 seconds have passed
    2 seconds have passed
    3 seconds have passed


    Traceback (most recent call last):
      File "<ipython-input-38-7e5136e65261>", line 2, in <module>
        long_running_test()
      File "<ipython-input-37-8d0f8e53f106>", line 5, in long_running_test
        print(i, "seconds have passed")
      File "<ipython-input-37-8d0f8e53f106>", line 5, in long_running_test
        print(i, "seconds have passed")
      File "<ipython-input-36-25e161c719c7>", line 14, in check_time
        raise TimeoutError
    TimeoutError


Note that it is possible to nest multiple timeouts.


```python
with ExpectTimeout(2):
    with ExpectTimeout(1):
        long_running_test()
    long_running_test()
```

    Start


    Traceback (most recent call last):
      File "<ipython-input-39-b194d3a94b81>", line 3, in <module>
        long_running_test()
      File "<ipython-input-37-8d0f8e53f106>", line 5, in long_running_test
        print(i, "seconds have passed")
      File "<ipython-input-37-8d0f8e53f106>", line 5, in long_running_test
        print(i, "seconds have passed")
      File "<ipython-input-36-25e161c719c7>", line 14, in check_time
        raise TimeoutError
    TimeoutError


    Start


    Traceback (most recent call last):
      File "<ipython-input-39-b194d3a94b81>", line 4, in <module>
        long_running_test()
      File "<ipython-input-37-8d0f8e53f106>", line 5, in long_running_test
        print(i, "seconds have passed")
      File "<ipython-input-37-8d0f8e53f106>", line 5, in long_running_test
        print(i, "seconds have passed")
      File "<ipython-input-36-25e161c719c7>", line 14, in check_time
        raise TimeoutError
    TimeoutError


That's it, folks – enjoy!

<hr>

<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">

_This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)._<br>
