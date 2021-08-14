#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Search-Based Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/SearchBasedFuzzer.html
# Last change: 2021-06-02 17:43:48+02:00
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
The Fuzzing Book - Search-Based Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python SearchBasedFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.SearchBasedFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/SearchBasedFuzzer.html

This chapter demonstrates how to use meta-heuristic search algorithms to find inputs that reach specific locations in the source code. The simplest search algorithm is hillclimbing, which is applied to the simple `test_me` example as follows:

>>> hillclimber()
Initial value: -67005, 8742 at fitness 84491.0000
New value: -67006, 8741 at fitness 84490.0000
New value: -67007, 8740 at fitness 84489.0000
New value: -67008, 8739 at fitness 84488.0000
New value: -67009, 8738 at fitness 84487.0000
New value: -67010, 8737 at fitness 84486.0000
New value: -67011, 8736 at fitness 84485.0000
New value: -67012, 8735 at fitness 84484.0000
New value: -67013, 8734 at fitness 84483.0000
New value: -67014, 8733 at fitness 84482.0000
New value: -67015, 8732 at fitness 84481.0000
New value: -67016, 8731 at fitness 84480.0000
New value: -67017, 8730 at fitness 84479.0000
New value: -67018, 8729 at fitness 84478.0000
New value: -67019, 8728 at fitness 84477.0000
New value: -67020, 8727 at fitness 84476.0000
New value: -67021, 8726 at fitness 84475.0000
New value: -67022, 8725 at fitness 84474.0000
New value: -67023, 8724 at fitness 84473.0000
New value: -67024, 8723 at fitness 84472.0000
New value: -67025, 8722 at fitness 84471.0000
...
Found optimum after 58743 iterations at -100000, -50001


Different aspects and challenges require different variations of this algorithm, such as a `steepest_ascent_hillclimber` or a `restarting_hillclimber`.

The search can be guided by different optimization goals captured in fitness functions. A fitness function to measure how close we are to reaching locations in the source code uses source code instrumentation. To produce an instrumented version of `cgi_decode`, use:

>>> cgi_decode_instrumented = create_instrumented_function(cgi_decode)

Fitness values are obtained by executing `cgi_decode_instrumented`, which is done by the `get_fitness_cgi` function:

>>> get_fitness_cgi("Foo")
5.0

Complex functions like `cgi_decode` result in vastly larger search spaces, which can be explored using evolutionary search algorithms such as genetic algorithms:

>>> genetic_algorithm()
Best fitness of initial population: '䫪Ʝ\uf42b铺뿱ጻ䗷䌮肵篭' - 5.0000000000
Best fitness at generation 1: '\u19cdꥁ캖蝻ⅹ\uf37f功ᰲ\ued7eᱨ' - 5.00000000
Best fitness at generation 2: '绑䀕\u20c5֜적\udfaeᇒ툧痮Ꮶ' - 5.00000000
Best fitness at generation 3: '끍碼ߝ䣅쾜\u0b7b죅ᦜ\uf1fd䈕' - 5.00000000
Best fitness at generation 4: '甚ᇆꏭ貰꾵訴྿ꙩᏃด' - 5.00000000
Best fitness at generation 5: '\uf644ᇆꏭ貰虀ꎍ\uf6f9嫛ሎ㺁' - 5.00000000
Best fitness at generation 6: '빫\uf61a\ud85c熆꾵訴ဍꙩᑓ\ue8e0' - 5.00000000
Best fitness at generation 7: '닅\uf307Ɗ\uefc5筂鐞嚂ᡥ⃫㺤' - 5.00000000
Best fitness at generation 8: '漻㺅揝䄩薽턫轼\u0dcc\udb87胮' - 5.00000000
Best fitness at generation 9: '甚ᇩ護㿦腄ꑗ\uf6f9嫛ም凂' - 5.00000000
Best fitness at generation 10: '끍ᇆ⁔峤羘䶦Ⓛ巖桿\ue8ac' - 5.00000000
Best fitness at generation 11: '㞮械ꏭഡ鰴勂ᇒ툧䧱㺡' - 5.00000000
Best fitness at generation 12: '닅\uf307Ɗ䣅筂鐮\uf697媭ም凂' - 5.00000000
Best fitness at generation 13: '췵㪈쾟⢥筂鐇勨憣并ꓹ' - 5.00000000
Best fitness at generation 14: '睾\uf2aaﾒ\uef8b鰴⥢邹坅櫼砳' - 5.00000000
Best fitness at generation 15: '盾㩭譂䅎웱勂ᇒ텬䧱㺡' - 5.00000000
Best fitness at generation 16: '끍ᇆ₩豻畕傞ᅢ툧䧱Ａ' - 5.00000000
Best fitness at generation 17: '뀳硺ߝ\uefdb笧勂ᇒ텬桘．' - 5.00000000
Best fitness at generation 18: '㴄ᅕ큕谉畕傞ᅢ툧䧱Ａ' - 5.00000000
Best fitness at generation 19: '滴㪈㹮䣻羘䷴⒲嵟\udc02㺤' - 5.00000000
Best fitness at generation 20: '矖㪈㺂䢶羘䶦ᇒ䙗뭜탤' - 5.00000000
...
Best individual: '쩴篊㬍鍵糄䧱﬩廁\ude21萇', fitness 5.0000000000



For more details, source, and documentation, see
"The Fuzzing Book - Search-Based Fuzzing"
at https://www.fuzzingbook.org/html/SearchBasedFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Search-Based Fuzzing
# ====================

if __name__ == '__main__':
    print('# Search-Based Fuzzing')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Test Generation as a Search Problem
## -----------------------------------

if __name__ == '__main__':
    print('\n## Test Generation as a Search Problem')



### Representing Program Inputs as a Search Problem

if __name__ == '__main__':
    print('\n### Representing Program Inputs as a Search Problem')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from . import Fuzzer

from .bookutils import unicode_escape, terminal_escape

def test_me(x, y):
    if x == 2 * (y + 1):
        return True
    else:
        return False

if __name__ == '__main__':
    test_me(0, 0)

if __name__ == '__main__':
    test_me(4, 2)

if __name__ == '__main__':
    test_me(22, 10)

MAX = 1000
MIN = -MAX

def neighbours(x, y):
    return [(x + dx, y + dy) for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if (dx != 0 or dy != 0)
            and ((MIN <= x + dx <= MAX)
                 and (MIN <= y + dy <= MAX))]

if __name__ == '__main__':
    print(neighbours(10, 10))

### Defining a Search Landscape: Fitness functions

if __name__ == '__main__':
    print('\n### Defining a Search Landscape: Fitness functions')



if __name__ == '__main__':
    x = 274
    y = 153
    x, 2 * (y + 1)

def calculate_distance(x, y):
    return abs(x - 2 * (y + 1))

if __name__ == '__main__':
    calculate_distance(274, 153)

if __name__ == '__main__':
    from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':
    import matplotlib.pyplot as plt

if __name__ == '__main__':
    import numpy as np

# %matplotlib inline
# 
# x = np.outer(np.linspace(-10, 10, 30), np.ones(30))
# y = x.copy().T
# z = calculate_distance(x, y)
# 
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# 
# ax.plot_surface(x, y, z, cmap=plt.cm.jet, rstride=1, cstride=1, linewidth=0);

### Instrumentation

if __name__ == '__main__':
    print('\n### Instrumentation')



def test_me_instrumented(x, y):
    print("Instrumentation: Input = (%d, %d), distance = %d" %
          (x, y, calculate_distance(x, y)))
    if x == 2 * (y + 1):
        return True
    else:
        return False

if __name__ == '__main__':
    test_me_instrumented(0, 0)

if __name__ == '__main__':
    test_me_instrumented(5, 2)

if __name__ == '__main__':
    test_me_instrumented(22, 10)

if __name__ == '__main__':
    distance = 0

def test_me_instrumented(x, y):
    global distance
    distance = calculate_distance(x, y)
    if x == 2 * (y + 1):
        return True
    else:
        return False

def get_fitness(x, y):
    global distance
    test_me_instrumented(x, y)
    fitness = distance
    return fitness

if __name__ == '__main__':
    get_fitness(0, 0)

if __name__ == '__main__':
    get_fitness(1, 2)

if __name__ == '__main__':
    get_fitness(22, 10)

### Hillclimbing the Example

if __name__ == '__main__':
    print('\n### Hillclimbing the Example')



if __name__ == '__main__':
    x, y = 274, 153
    print("Origin %d, %d has fitness %d" % (x, y, get_fitness(x, y)))
    for nx, ny in neighbours(x, y):
        print("Neighbour %d, %d has fitness %d" % (nx, ny, get_fitness(nx, ny)))

import random

LOG_VALUES = 20  # Number of values to log

def hillclimber():
    # Create and evaluate starting point
    x, y = random.randint(MIN, MAX), random.randint(MIN, MAX)
    fitness = get_fitness(x, y)
    print("Initial value: %d, %d at fitness %.4f" % (x, y, fitness))
    iterations = 0
    logs = 0

    # Stop once we have found an optimal solution
    while fitness > 0:
        iterations += 1
        # Move to first neighbour with a better fitness
        for (nextx, nexty) in neighbours(x, y):
            new_fitness = get_fitness(nextx, nexty)

            # Smaller fitness values are better
            if new_fitness < fitness:
                x, y = nextx, nexty
                fitness = new_fitness
                if logs < LOG_VALUES:
                    print("New value: %d, %d at fitness %.4f" % (x, y, fitness))
                elif logs == LOG_VALUES:
                    print("...")
                logs += 1
                break

    print("Found optimum after %d iterations at %d, %d" % (iterations, x, y))

if __name__ == '__main__':
    hillclimber()

def steepest_ascent_hillclimber():
    # Create and evaluate starting point
    x, y = random.randint(MIN, MAX), random.randint(MIN, MAX)
    fitness = get_fitness(x, y)
    print("Initial value: %d, %d at fitness %.4f" % (x, y, fitness))
    iterations = 0
    logs = 0

    # Stop once we have found an optimal solution
    while fitness > 0:
        iterations += 1
        # Move to first neighbour with a better fitness
        for (nextx, nexty) in neighbours(x, y):
            new_fitness = get_fitness(nextx, nexty)
            if new_fitness < fitness:
                x, y = nextx, nexty
                fitness = new_fitness
                if logs < LOG_VALUES:
                    print("New value: %d, %d at fitness %.4f" % (x, y, fitness))
                elif logs == LOG_VALUES:
                    print("...")
                logs += 1

    print("Found optimum after %d iterations at %d, %d" % (iterations, x, y))

if __name__ == '__main__':
    steepest_ascent_hillclimber()

def plotting_hillclimber(fitness_function):
    data = []

    # Create and evaluate starting point
    x, y = random.randint(MIN, MAX), random.randint(MIN, MAX)
    fitness = fitness_function(x, y)
    data += [fitness]
    iterations = 0

    # Stop once we have found an optimal solution
    while fitness > 0:
        iterations += 1
        # Move to first neighbour with a better fitness
        for (nextx, nexty) in neighbours(x, y):
            new_fitness = fitness_function(nextx, nexty)
            if new_fitness < fitness:
                x, y = nextx, nexty
                fitness = new_fitness
                data += [fitness]
                break

    print("Found optimum after %d iterations at %d, %d" % (iterations, x, y))
    return data

if __name__ == '__main__':
    data = plotting_hillclimber(get_fitness)

if __name__ == '__main__':
    import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig = plt.figure()
    ax = plt.axes()

    x = range(len(data))
    ax.plot(x, data);

def test_me2(x, y):
    if(x * x == y * y * (x % 20)):
        return True
    else:
        return False

def test_me2_instrumented(x, y):
    global distance
    distance = abs(x * x - y * y * (x % 20))
    if(x * x == y * y * (x % 20)):
        return True
    else:
        return False

def bad_fitness(x, y):
    global distance
    test_me2_instrumented(x, y)
    fitness = distance
    return fitness

if __name__ == '__main__':
    from mpl_toolkits.mplot3d import Axes3D

from math import exp, tan

if __name__ == '__main__':
    x = np.outer(np.linspace(-10, 10, 30), np.ones(30))
    y = x.copy().T
    z = abs(x * x - y * y * (x % 20))

if __name__ == '__main__':
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.plot_surface(x, y, z, cmap=plt.cm.jet, rstride=1, cstride=1, linewidth=0);

def restarting_hillclimber(fitness_function):
    data = []

    # Create and evaluate starting point
    x, y = random.randint(MIN, MAX), random.randint(MIN, MAX)
    fitness = fitness_function(x, y)
    data += [fitness]
    print("Initial value: %d, %d at fitness %.4f" % (x, y, fitness))
    iterations = 0

    # Stop once we have found an optimal solution
    while fitness > 0:
        changed = False
        iterations += 1
        # Move to first neighbour with a better fitness
        for (nextx, nexty) in neighbours(x, y):
            new_fitness = fitness_function(nextx, nexty)
            if new_fitness < fitness:
                x, y = nextx, nexty
                fitness = new_fitness
                data += [fitness]
                changed = True
                break
        if not changed:
            x, y = random.randint(MIN, MAX), random.randint(MIN, MAX)
            fitness = fitness_function(x, y)
            data += [fitness]

    print("Found optimum after %d iterations at %d, %d" % (iterations, x, y))
    return data

MAX = 1000
MIN = -MAX

if __name__ == '__main__':
    data = restarting_hillclimber(bad_fitness)

if __name__ == '__main__':
    import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig = plt.figure()
    ax = plt.axes()

    x = range(len(data))
    ax.plot(x, data);

MAX = 100000
MIN = -MAX

from .Timer import Timer

if __name__ == '__main__':
    with Timer() as t:
        restarting_hillclimber(get_fitness)
        print("Search time: %.2fs" % t.elapsed_time())

## Testing a More Complex Program
## ------------------------------

if __name__ == '__main__':
    print('\n## Testing a More Complex Program')



def cgi_decode(s):
    """Decode the CGI-encoded string `s`:
       * replace "+" by " "
       * replace "%xx" by the character with hex number xx.
       Return the decoded string.  Raise `ValueError` for invalid inputs."""

    # Mapping of hex digits to their integer values
    hex_values = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
    }

    t = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c == '+':
            t += ' '
        elif c == '%':
            digit_high, digit_low = s[i + 1], s[i + 2]
            i += 2
            if digit_high in hex_values and digit_low in hex_values:
                v = hex_values[digit_high] * 16 + hex_values[digit_low]
                t += chr(v)
            else:
                raise ValueError("Invalid encoding")
        else:
            t += c
        i += 1
    return t

### CGI Decoder as a Search Problem

if __name__ == '__main__':
    print('\n### CGI Decoder as a Search Problem')



def neighbour_strings(x):
    n = []
    for pos in range(len(x)):
        c = ord(x[pos])
        if c < 126:
            n += [x[:pos] + chr(c + 1) + x[pos + 1:]]
        if c > 32:
            n += [x[:pos] + chr(c - 1) + x[pos + 1:]]
    return n

if __name__ == '__main__':
    print(neighbour_strings("Hello"))

### Branch Distances

if __name__ == '__main__':
    print('\n### Branch Distances')



import sys

def distance_character(target, values):

    # Initialize with very large value so that any comparison is better
    minimum = sys.maxsize

    for elem in values:
        distance = abs(target - elem)
        if distance < minimum:
            minimum = distance
    return minimum

if __name__ == '__main__':
    distance_character(10, [1, 5, 12, 100])

if __name__ == '__main__':
    distance_character(10, [0, 50, 80, 200])

### Dealing with Complex Conditions

if __name__ == '__main__':
    print('\n### Dealing with Complex Conditions')



### Instrumentation for Atomic Conditions

if __name__ == '__main__':
    print('\n### Instrumentation for Atomic Conditions')



def evaluate_condition(num, op, lhs, rhs):
    distance_true = 0
    distance_false = 0
    if op == "Eq":
        if lhs == rhs:
            distance_false = 1
        else:
            distance_true = abs(lhs - rhs)

    # ... code for other types of conditions

    if distance_true == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    evaluate_condition(1, "Eq", 10, 20)

if __name__ == '__main__':
    evaluate_condition(2, "Eq", 20, 20)

def update_maps(condition_num, d_true, d_false):
    global distances_true, distances_false

    if condition_num in distances_true.keys():
        distances_true[condition_num] = min(
            distances_true[condition_num], d_true)
    else:
        distances_true[condition_num] = d_true

    if condition_num in distances_false.keys():
        distances_false[condition_num] = min(
            distances_false[condition_num], d_false)
    else:
        distances_false[condition_num] = d_false

def evaluate_condition(num, op, lhs, rhs):
    distance_true = 0
    distance_false = 0

    # Make sure the distance can be calculated on number and character
    # comparisons
    if isinstance(lhs, str):
        lhs = ord(lhs)
    if isinstance(rhs, str):
        rhs = ord(rhs)

    if op == "Eq":
        if lhs == rhs:
            distance_false = 1
        else:
            distance_true = abs(lhs - rhs)

    elif op == "Lt":
        if lhs < rhs:
            distance_false = rhs - lhs
        else:
            distance_true = lhs - rhs + 1
    # ...
    # handle other comparison operators
    # ...

    elif op == "In":
        minimum = sys.maxsize
        for elem in rhs.keys():
            distance = abs(lhs - ord(elem))
            if distance < minimum:
                minimum = distance

        distance_true = minimum
        if distance_true == 0:
            distance_false = 1

    update_maps(num, distance_true, distance_false)

    if distance_true == 0:
        return True
    else:
        return False

### Instrumenting Source Code Automatically

if __name__ == '__main__':
    print('\n### Instrumenting Source Code Automatically')



import ast

class BranchTransformer(ast.NodeTransformer):

    branch_num = 0

    def visit_FunctionDef(self, node):
        node.name = node.name + "_instrumented"
        return self.generic_visit(node)

    def visit_Compare(self, node):
        if node.ops[0] in [ast.Is, ast.IsNot, ast.In, ast.NotIn]:
            return node

        self.branch_num += 1
        return ast.Call(func=ast.Name("evaluate_condition", ast.Load()),
                        args=[ast.Num(self.branch_num),
                              ast.Str(node.ops[0].__class__.__name__),
                              node.left,
                              node.comparators[0]],
                        keywords=[],
                        starargs=None,
                        kwargs=None)

import inspect
import ast
import astor

from .bookutils import print_content

if __name__ == '__main__':
    source = inspect.getsource(cgi_decode)
    node = ast.parse(source)
    BranchTransformer().visit(node)

    # Make sure the line numbers are ok before printing
    node = ast.fix_missing_locations(node)
    print_content(astor.to_source(node), '.py')

def create_instrumented_function(f):
    source = inspect.getsource(f)
    node = ast.parse(source)
    node = BranchTransformer().visit(node)

    # Make sure the line numbers are ok so that it compiles
    node = ast.fix_missing_locations(node)

    # Compile and add the instrumented function to the current module
    current_module = sys.modules[__name__]
    code = compile(node, filename="<ast>", mode="exec")
    exec(code, current_module.__dict__)

if __name__ == '__main__':
    distances_true = {}
    distances_false = {}

if __name__ == '__main__':
    create_instrumented_function(cgi_decode)

if __name__ == '__main__':
    assert cgi_decode("Hello+Reader") == cgi_decode_instrumented("Hello+Reader")

if __name__ == '__main__':
    cgi_decode_instrumented("Hello+Reader")

if __name__ == '__main__':
    distances_true

if __name__ == '__main__':
    distances_false

### Fitness Function to Create Valid Hexadecimal Inputs

if __name__ == '__main__':
    print('\n### Fitness Function to Create Valid Hexadecimal Inputs')



def normalize(x):
    return x / (1.0 + x)

if __name__ == '__main__':
    import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig = plt.figure()
    ax = plt.axes()

    x = range(100)
    y = [value / (value + 1.0) for value in x]
    ax.plot(x, y);

def get_fitness_cgi(x):
    # Reset any distance values from previous executions
    global distances_true, distances_false
    distances_true = {}
    distances_false = {}

    # Run the function under test
    try:
        cgi_decode_instrumented(x)
    except BaseException:
        pass

    # Sum up branch distances
    fitness = 0.0
    for branch in [1, 3, 4, 5]:
        if branch in distances_true:
            fitness += normalize(distances_true[branch])
        else:
            fitness += 1.0

    for branch in [2]:
        if branch in distances_false:
            fitness += normalize(distances_false[branch])
        else:
            fitness += 1.0

    return fitness

if __name__ == '__main__':
    get_fitness_cgi("")

if __name__ == '__main__':
    get_fitness_cgi("Hello+Reader")

if __name__ == '__main__':
    get_fitness_cgi("%UU")

if __name__ == '__main__':
    get_fitness_cgi("%AU")

if __name__ == '__main__':
    get_fitness_cgi("%AA")

### Hillclimbing Valid Hexadecimal Inputs

if __name__ == '__main__':
    print('\n### Hillclimbing Valid Hexadecimal Inputs')



def random_string(l):
    s = ""
    for i in range(l):
        random_character = chr(random.randrange(32, 127))
        s = s + random_character
    return s

def hillclimb_cgi():
    x = random_string(10)
    fitness = get_fitness_cgi(x)
    print("Initial input: %s at fitness %.4f" % (x, fitness))

    while fitness > 0:
        changed = False
        for (nextx) in neighbour_strings(x):
            new_fitness = get_fitness_cgi(nextx)
            if new_fitness < fitness:
                x = nextx
                fitness = new_fitness
                changed = True
                print("New value: %s at fitness %.4f" % (x, fitness))
                break

        # Random restart if necessary
        if not changed:
            x = random_string(10)
            fitness = get_fitness_cgi(x)

    print("Optimum at %s, fitness %.4f" % (x, fitness))

if __name__ == '__main__':
    hillclimb_cgi()

## Evolutionary Search
## -------------------

if __name__ == '__main__':
    print('\n## Evolutionary Search')



def random_unicode_string(l):
    s = ""
    for i in range(l):
        # Limits to reflect range of UTF-16
        random_character = chr(random.randrange(0, 65536))
        s = s + random_character
    return s

def unicode_string_neighbours(x):
    n = []
    for pos in range(len(x)):
        c = ord(x[pos])
        # Limits to reflect range of UTF-16
        if c < 65536:
            n += [x[:pos] + chr(c + 1) + x[pos + 1:]]
        if c > 0:
            n += [x[:pos] + chr(c - 1) + x[pos + 1:]]

    return n

def terminal_repr(s):
    return terminal_escape(repr(s))

def hillclimb_cgi_limited(max_iterations):
    x = random_unicode_string(10)
    fitness = get_fitness_cgi(x)
    print("Initial input: %s at fitness %.4f" % (terminal_repr(x), fitness))

    iteration = 0
    logs = 0
    while fitness > 0 and iteration < max_iterations:
        changed = False
        for (nextx) in unicode_string_neighbours(x):
            new_fitness = get_fitness_cgi(nextx)
            if new_fitness < fitness:
                x = nextx
                fitness = new_fitness
                changed = True
                if logs < LOG_VALUES:
                    print("New value: %s at fitness %.4f" %
                          (terminal_repr(x), fitness))
                elif logs == LOG_VALUES:
                    print("...")
                logs += 1
                break

        # Random restart if necessary
        if not changed:
            x = random_string(10)
            fitness = get_fitness_cgi(x)
        iteration += 1

    print("Optimum at %s, fitness %.4f" % (terminal_repr(x), fitness))

if __name__ == '__main__':
    hillclimb_cgi_limited(100)

### Global Search

if __name__ == '__main__':
    print('\n### Global Search')



def flip_random_character(s):
    pos = random.randint(0, len(s) - 1)
    new_c = chr(random.randrange(0, 65536))
    return s[:pos] + new_c + s[pos + 1:]

def randomized_hillclimb():
    x = random_unicode_string(10)
    fitness = get_fitness_cgi(x)
    print("Initial value: %s at fitness %.4f" %
          (terminal_repr(x), fitness))

    iterations = 0
    while fitness > 0:
        mutated = flip_random_character(x)
        new_fitness = get_fitness_cgi(mutated)
        if new_fitness <= fitness:
            x = mutated
            fitness = new_fitness
            #print("New value: %s at fitness %.4f" %(terminal_repr(x), fitness))
        iterations += 1

    print("Optimum at %s after %d iterations" %
          (terminal_repr(x), iterations))

if __name__ == '__main__':
    randomized_hillclimb()

### Genetic Algorithms

if __name__ == '__main__':
    print('\n### Genetic Algorithms')



def create_population(size):
    return [random_unicode_string(10) for i in range(size)]

if __name__ == '__main__':
    create_population(10)

def evaluate_population(population):
    fitness = [get_fitness_cgi(x) for x in population]
    return list(zip(population, fitness))

if __name__ == '__main__':
    population = create_population(10)

if __name__ == '__main__':
    for (individual, fitness) in evaluate_population(population):
        print("%s: %.4f" % (terminal_repr(individual), fitness))

def selection(evaluated_population, tournament_size):
    competition = random.sample(evaluated_population, tournament_size)
    winner = min(competition, key=lambda individual: individual[1])[0]

    # Return a copy of the selected individual
    return winner[:]

if __name__ == '__main__':
    population = create_population(10)
    fitness = evaluate_population(population)
    selected = selection(fitness, 10)

if __name__ == '__main__':
    for (individual, fitness_value) in fitness:
        print("%s: %.4f" % (terminal_repr(individual), fitness_value))

if __name__ == '__main__':
    print("Winner: %s" % terminal_repr(selected))

def crossover(parent1, parent2):
    pos = random.randint(1, len(parent1))

    offspring1 = parent1[:pos] + parent2[pos:]
    offspring2 = parent2[:pos] + parent1[pos:]

    return (offspring1, offspring2)

if __name__ == '__main__':
    parent1 = "Hello World"
    parent2 = "Goodbye Book"

    crossover(parent1, parent2)

def mutate(chromosome):
    mutated = chromosome[:]
    P = 1.0 / len(mutated)

    for pos in range(len(mutated)):
        if random.random() < P:
            new_c = chr(int(random.gauss(ord(mutated[pos]), 100) % 65536))
            mutated = mutated[:pos] + new_c + mutated[pos + 1:]
    return mutated

def genetic_algorithm():
    # Generate and evaluate initial population
    generation = 0
    population = create_population(100)
    fitness = evaluate_population(population)
    best = min(fitness, key=lambda item: item[1])
    best_individual = best[0]
    best_fitness = best[1]
    print("Best fitness of initial population: %s - %.10f" %
        (terminal_repr(best_individual), best_fitness))
    logs = 0

    # Stop when optimum found, or we run out of patience
    while best_fitness > 0 and generation < 1000:

        # The next generation will have the same size as the current one
        new_population = []
        while len(new_population) < len(population):
            # Selection
            offspring1 = selection(fitness, 10)
            offspring2 = selection(fitness, 10)

            # Crossover
            if random.random() < 0.7:
                (offspring1, offspring2) = crossover(offspring1, offspring2)

            # Mutation
            offspring1 = mutate(offspring1)
            offspring2 = mutate(offspring2)

            new_population.append(offspring1)
            new_population.append(offspring2)

        # Once full, the new population replaces the old one
        generation += 1
        population = new_population
        fitness = evaluate_population(population)

        best = min(fitness, key=lambda item: item[1])
        best_individual = best[0]
        best_fitness = best[1]
        if logs < LOG_VALUES:
            print(
                "Best fitness at generation %d: %s - %.8f" %
                (generation, terminal_repr(best_individual), best_fitness))
        elif logs == LOG_VALUES:
            print("...")
        logs += 1

    print(
        "Best individual: %s, fitness %.10f" %
        (terminal_repr(best_individual), best_fitness))

if __name__ == '__main__':
    genetic_algorithm()

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    hillclimber()

if __name__ == '__main__':
    cgi_decode_instrumented = create_instrumented_function(cgi_decode)

if __name__ == '__main__':
    get_fitness_cgi("Foo")

if __name__ == '__main__':
    genetic_algorithm()

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


