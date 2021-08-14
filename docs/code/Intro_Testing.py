#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Introduction to Software Testing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/Intro_Testing.html
# Last change: 2021-06-02 17:40:24+02:00
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
The Fuzzing Book - Introduction to Software Testing

This file can be _executed_ as a script, running all experiments:

    $ python Intro_Testing.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.Intro_Testing import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/Intro_Testing.html


For more details, source, and documentation, see
"The Fuzzing Book - Introduction to Software Testing"
at https://www.fuzzingbook.org/html/Intro_Testing.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Introduction to Software Testing
# ================================

if __name__ == '__main__':
    print('# Introduction to Software Testing')



## Simple Testing
## --------------

if __name__ == '__main__':
    print('\n## Simple Testing')



def my_sqrt(x):
    """Computes the square root of x, using the Newton-Raphson method"""
    approx = None
    guess = x / 2
    while approx != guess:
        approx = guess
        guess = (approx + x / approx) / 2
    return approx

### Understanding Python Programs

if __name__ == '__main__':
    print('\n### Understanding Python Programs')



### Running a Function

if __name__ == '__main__':
    print('\n### Running a Function')



if __name__ == '__main__':
    my_sqrt(4)

if __name__ == '__main__':
    my_sqrt(2)

### Interacting with Notebooks

if __name__ == '__main__':
    print('\n### Interacting with Notebooks')



### Debugging a Function

if __name__ == '__main__':
    print('\n### Debugging a Function')



def my_sqrt_with_log(x):
    """Computes the square root of x, using the Newton–Raphson method"""
    approx = None
    guess = x / 2
    while approx != guess:
        print("approx =", approx)  # <-- New
        approx = guess
        guess = (approx + x / approx) / 2
    return approx

if __name__ == '__main__':
    my_sqrt_with_log(9)

### Checking a Function

if __name__ == '__main__':
    print('\n### Checking a Function')



if __name__ == '__main__':
    my_sqrt(2) * my_sqrt(2)

## Automating Test Execution
## -------------------------

if __name__ == '__main__':
    print('\n## Automating Test Execution')



if __name__ == '__main__':
    result = my_sqrt(4)
    expected_result = 2.0
    if result == expected_result:
        print("Test passed")
    else:
        print("Test failed")

if __name__ == '__main__':
    assert my_sqrt(4) == 2

EPSILON = 1e-8

if __name__ == '__main__':
    assert abs(my_sqrt(4) - 2) < EPSILON

def assertEquals(x, y, epsilon=1e-8):
    assert abs(x - y) < epsilon

if __name__ == '__main__':
    assertEquals(my_sqrt(4), 2)
    assertEquals(my_sqrt(9), 3)
    assertEquals(my_sqrt(100), 10)

## Generating Tests
## ----------------

if __name__ == '__main__':
    print('\n## Generating Tests')



if __name__ == '__main__':
    assertEquals(my_sqrt(2) * my_sqrt(2), 2)
    assertEquals(my_sqrt(3) * my_sqrt(3), 3)
    assertEquals(my_sqrt(42.11) * my_sqrt(42.11), 42.11)

if __name__ == '__main__':
    for n in range(1, 1000):
        assertEquals(my_sqrt(n) * my_sqrt(n), n)

if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .Timer import Timer

if __name__ == '__main__':
    with Timer() as t:
        for n in range(1, 10000):
            assertEquals(my_sqrt(n) * my_sqrt(n), n)
    print(t.elapsed_time())

import random

if __name__ == '__main__':
    with Timer() as t:
        for i in range(10000):
            x = 1 + random.random() * 1000000
            assertEquals(my_sqrt(x) * my_sqrt(x), x)
    print(t.elapsed_time())

## Run-Time Verification
## ---------------------

if __name__ == '__main__':
    print('\n## Run-Time Verification')



def my_sqrt_checked(x):
    root = my_sqrt(x)
    assertEquals(root * root, x)
    return root

if __name__ == '__main__':
    my_sqrt_checked(2.0)

## System Input vs Function Input
## ------------------------------

if __name__ == '__main__':
    print('\n## System Input vs Function Input')



def sqrt_program(arg):
    x = int(arg)
    print('The root of', x, 'is', my_sqrt(x))

if __name__ == '__main__':
    sqrt_program("4")

from .ExpectError import ExpectTimeout

if __name__ == '__main__':
    with ExpectTimeout(1):
        sqrt_program("-1")

def sqrt_program(arg):
    x = int(arg)
    if x < 0:
        print("Illegal Input")
    else:
        print('The root of', x, 'is', my_sqrt(x))

if __name__ == '__main__':
    sqrt_program("-1")

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        sqrt_program("xyzzy")

def sqrt_program(arg):
    try:
        x = float(arg)
    except ValueError:
        print("Illegal Input")
    else:
        if x < 0:
            print("Illegal Number")
        else:
            print('The root of', x, 'is', my_sqrt(x))

if __name__ == '__main__':
    sqrt_program("4")

if __name__ == '__main__':
    sqrt_program("-1")

if __name__ == '__main__':
    sqrt_program("xyzzy")

## The Limits of Testing
## ---------------------

if __name__ == '__main__':
    print('\n## The Limits of Testing')



if __name__ == '__main__':
    with ExpectError():
        root = my_sqrt(0)

def my_sqrt_fixed(x):
    assert 0 <= x
    if x == 0:
        return 0
    return my_sqrt(x)

if __name__ == '__main__':
    assert my_sqrt_fixed(0) == 0

if __name__ == '__main__':
    with ExpectError():
        root = my_sqrt_fixed(-1)

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



### Exercise 1: Get Acquainted with Notebooks and Python

if __name__ == '__main__':
    print('\n### Exercise 1: Get Acquainted with Notebooks and Python')



#### Beginner Level: Run Notebooks in Your Browser

if __name__ == '__main__':
    print('\n#### Beginner Level: Run Notebooks in Your Browser')



#### Advanced Level: Run Python Code on Your Machine

if __name__ == '__main__':
    print('\n#### Advanced Level: Run Python Code on Your Machine')



#### Pro Level: Run Notebooks on Your Machine

if __name__ == '__main__':
    print('\n#### Pro Level: Run Notebooks on Your Machine')



#### Boss Level: Contribute!

if __name__ == '__main__':
    print('\n#### Boss Level: Contribute!')



### Exercise 2: Testing Shellsort

if __name__ == '__main__':
    print('\n### Exercise 2: Testing Shellsort')



def shellsort(elems):
    sorted_elems = elems.copy()
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]
    for gap in gaps:
        for i in range(gap, len(sorted_elems)):
            temp = sorted_elems[i]
            j = i
            while j >= gap and sorted_elems[j - gap] > temp:
                sorted_elems[j] = sorted_elems[j - gap]
                j -= gap
            sorted_elems[j] = temp

    return sorted_elems

if __name__ == '__main__':
    shellsort([3, 2, 1])

if __name__ == '__main__':
    a = [5, 6, 99, 7]
    print("First element:", a[0], "length:", len(a))

if __name__ == '__main__':
    for x in range(1, 5):
        print(x)

#### Part 1: Manual Test Cases

if __name__ == '__main__':
    print('\n#### Part 1: Manual Test Cases')



if __name__ == '__main__':
    assert shellsort([3, 2, 1]) == [1, 2, 3]
    assert shellsort([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert shellsort([6, 5]) == [5, 6]

if __name__ == '__main__':
    assert shellsort([2, 2, 1]) == [1, 2, 2]

if __name__ == '__main__':
    assert shellsort([]) == []

#### Part 2: Random Inputs

if __name__ == '__main__':
    print('\n#### Part 2: Random Inputs')



def is_sorted(elems):
    return all(elems[i] <= elems[i + 1] for i in range(len(elems) - 1))

if __name__ == '__main__':
    is_sorted([3, 5, 9])

def is_permutation(a, b):
    return len(a) == len(b) and all(a.count(elem) == b.count(elem) for elem in a)

if __name__ == '__main__':
    is_permutation([3, 2, 1], [1, 3, 2])

def random_list():
    length = random.randint(1, 10)
    elems = []
    for i in range(length):
        elems.append(random.randint(0, 100))
    return elems

if __name__ == '__main__':
    random_list()

if __name__ == '__main__':
    elems = random_list()
    print(elems)

if __name__ == '__main__':
    sorted_elems = shellsort(elems)
    print(sorted_elems)

if __name__ == '__main__':
    assert is_sorted(sorted_elems) and is_permutation(sorted_elems, elems)

if __name__ == '__main__':
    for i in range(1000):
        elems = random_list()
        sorted_elems = shellsort(elems)
        assert is_sorted(sorted_elems) and is_permutation(sorted_elems, elems)

### Exercise 3: Quadratic Solver

if __name__ == '__main__':
    print('\n### Exercise 3: Quadratic Solver')



def quadratic_solver(a, b, c):
    q = b * b - 4 * a * c
    solution_1 = (-b + my_sqrt_fixed(q)) / (2 * a)
    solution_2 = (-b - my_sqrt_fixed(q)) / (2 * a)
    return (solution_1, solution_2)

if __name__ == '__main__':
    quadratic_solver(3, 4, 1)

#### Part 1: Find bug-triggering inputs

if __name__ == '__main__':
    print('\n#### Part 1: Find bug-triggering inputs')



if __name__ == '__main__':
    with ExpectError():
        print(quadratic_solver(3, 2, 1))

if __name__ == '__main__':
    with ExpectError():
        print(quadratic_solver(0, 0, 1))

#### Part 2: Fix the problem

if __name__ == '__main__':
    print('\n#### Part 2: Fix the problem')



def quadratic_solver_fixed(a, b, c):
    if a == 0:
        if b == 0:
            if c == 0:
                # Actually, any value of x
                return (0, None)
            else:
                # No value of x can satisfy c = 0
                return (None, None)
        else:
            return (-c / b, None)

    q = b * b - 4 * a * c
    if q < 0:
        return (None, None)

    if q == 0:
        solution = -b / 2 * a
        return (solution, None)

    solution_1 = (-b + my_sqrt_fixed(q)) / (2 * a)
    solution_2 = (-b - my_sqrt_fixed(q)) / (2 * a)
    return (solution_1, solution_2)

if __name__ == '__main__':
    with ExpectError():
        print(quadratic_solver_fixed(3, 2, 1))

if __name__ == '__main__':
    with ExpectError():
        print(quadratic_solver_fixed(0, 0, 1))

#### Part 3: Odds and Ends

if __name__ == '__main__':
    print('\n#### Part 3: Odds and Ends')



if __name__ == '__main__':
    combinations = 2 ** 32 * 2 ** 32
    combinations

if __name__ == '__main__':
    tests_per_second = 1000000000
    seconds_per_year = 60 * 60 * 24 * 365.25
    tests_per_year = tests_per_second * seconds_per_year
    combinations / tests_per_year

### Exercise 4: To Infinity and Beyond

if __name__ == '__main__':
    print('\n### Exercise 4: To Infinity and Beyond')



from .ExpectError import ExpectTimeout

if __name__ == '__main__':
    infinity = float('inf')  # that's how to get an infinite number

    with ExpectTimeout(1):
        y = my_sqrt_fixed(infinity)
