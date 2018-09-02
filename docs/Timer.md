
_This notebook is a chapter of the book ["Generating Software Tests"](https://uds-se.github.io/fuzzingbook/Main.html)._ <br>
<a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Timer.ipynb"><img style="float:right" src="https://mybinder.org/badge.svg" alt="Launch Binder (beta)"></a>
[Interactive version (beta)](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Timer.ipynb) • 
[Download code](https://uds-se.github.io/fuzzingbook/code/Timer.py) • 
[Table of contents](https://uds-se.github.io/fuzzingbook/Main.html) • 
[Change history](https://github.com/uds-se/fuzzingbook/commits/master/notebooks/Timer.ipynb) • 
[Issues and comments](https://github.com/uds-se/fuzzingbook/issues) • 
[Main project page](https://github.com/uds-se/fuzzingbook/)
<hr>

# Timer

The code in this notebook helps with measuring time.

**Prerequisites**

* This notebook needs some understanding on advanced concepts in Python, notably 
    * classes
    * the Python `with` statement
    * measuring time

## Measuring Time

The class `Timer` allows to measure the elapsed time during some code execution.  A typical usage looks as follows:

```Python
from Timer import Timer

with Timer() as t:
    function_that_is_supposed_to_be_timed()

print(t.elapsed_time())
```



```python
import fuzzingbook_utils
```


```python
import time
```


```python
def clock():
    try:
        return time.perf_counter()  # Python 3
    except:
        return time.clock()         # Python 2
```


```python
class Timer(object):
    # Begin of `with` block
    def __enter__(self):
        self.start_time = clock()
        self.end_time = None
        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        self.end_time = clock()

    def elapsed_time(self):
        """Return elapsed time in seconds"""
        if self.end_time is None:
            # still running
            return clock() - self.start_time
        else:
            return self.end_time - self.start_time
```

Here's an example:


```python
def some_long_running_function():
    i = 1000000
    while i > 0:
        i -= 1
```


```python
print("Stopping total time:")
with Timer() as t:
    some_long_running_function()
print(t.elapsed_time())
```

    Stopping total time:
    0.07850043196231127



```python
print("Stopping time in between:")
with Timer() as t:
    for i in range(10):
        print(t.elapsed_time())
```

    Stopping time in between:
    7.79307447373867e-06
    5.2840099669992924e-05
    8.764106314629316e-05
    0.00012146006338298321
    0.00015374808572232723
    0.00018622609786689281
    0.0002182930475100875
    0.0002508650068193674
    0.00028321705758571625
    0.0003162421053275466


That's it, folks – enjoy!

<hr>

<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">

_This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)._<br>
