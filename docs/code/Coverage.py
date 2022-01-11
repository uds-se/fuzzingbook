#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Code Coverage" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/Coverage.html
# Last change: 2022-01-11 10:05:56+01:00
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
The Fuzzing Book - Code Coverage

This file can be _executed_ as a script, running all experiments:

    $ python Coverage.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.Coverage import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/Coverage.html

This chapter introduces a `Coverage` class allowing you to measure coverage for Python programs. Within the context of this book, we use coverage information to guide fuzzing towards uncovered locations.

The typical usage of the `Coverage` class is in conjunction with a `with` clause:

>>> with Coverage() as cov:
>>>     cgi_decode("a+b")

Printing out a coverage object shows the covered functions, with covered lines prefixed as `#`:

>>> print(cov)
   1  def cgi_decode(s: str) -> str:
   2      """Decode the CGI-encoded string `s`:
   3         * replace '+' by ' '
   4         * replace "%xx" by the character with hex number xx.
   5         Return the decoded string.  Raise `ValueError` for invalid inputs."""
   6  
   7      # Mapping of hex digits to their integer values
#  8      hex_values = {
#  9          '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
# 10          '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
# 11          'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
# 12          'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
  13      }
  14  
# 15      t = ""
# 16      i = 0
# 17      while i < len(s):
# 18          c = s[i]
# 19          if c == '+':
# 20              t += ' '
# 21          elif c == '%':
  22              digit_high, digit_low = s[i + 1], s[i + 2]
  23              i += 2
  24              if digit_high in hex_values and digit_low in hex_values:
  25                  v = hex_values[digit_high] * 16 + hex_values[digit_low]
  26                  t += chr(v)
  27              else:
  28                  raise ValueError("Invalid encoding")
  29          else:
# 30              t += c
# 31          i += 1
# 32      return t



The `trace()` method returns the _trace_ – that is, the list of locations executed in order. Each location comes as a pair (`function name`, `line`).

>>> cov.trace()
[('cgi_decode', 9),
 ('cgi_decode', 10),
 ('cgi_decode', 11),
 ('cgi_decode', 12),
 ('cgi_decode', 8),
 ('cgi_decode', 15),
 ('cgi_decode', 16),
 ('cgi_decode', 17),
 ('cgi_decode', 18),
 ('cgi_decode', 19),
 ('cgi_decode', 21),
 ('cgi_decode', 30),
 ('cgi_decode', 31),
 ('cgi_decode', 17),
 ('cgi_decode', 18),
 ('cgi_decode', 19),
 ('cgi_decode', 20),
 ('cgi_decode', 31),
 ('cgi_decode', 17),
 ('cgi_decode', 18),
 ('cgi_decode', 19),
 ('cgi_decode', 21),
 ('cgi_decode', 30),
 ('cgi_decode', 31),
 ('cgi_decode', 17),
 ('cgi_decode', 32)]

The `coverage()` method returns the _coverage_, that is, the set of locations in the trace executed at least once:

>>> cov.coverage()
{('cgi_decode', 8),
 ('cgi_decode', 9),
 ('cgi_decode', 10),
 ('cgi_decode', 11),
 ('cgi_decode', 12),
 ('cgi_decode', 15),
 ('cgi_decode', 16),
 ('cgi_decode', 17),
 ('cgi_decode', 18),
 ('cgi_decode', 19),
 ('cgi_decode', 20),
 ('cgi_decode', 21),
 ('cgi_decode', 30),
 ('cgi_decode', 31),
 ('cgi_decode', 32)}

Coverage sets can be subject to set operations, such as _intersection_ (which locations are covered in multiple executions) and _difference_ (which locations are covered in run _a_, but not _b_).

The chapter also discusses how to obtain such coverage from C programs.

For more details, source, and documentation, see
"The Fuzzing Book - Code Coverage"
at https://www.fuzzingbook.org/html/Coverage.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Code Coverage
# =============

if __name__ == '__main__':
    print('# Code Coverage')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo

if __name__ == '__main__':
    YouTubeVideo('2lfgI9KdARs')

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from typing import Any, Optional, Callable, List, Type, Set, Tuple

## A CGI Decoder
## -------------

if __name__ == '__main__':
    print('\n## A CGI Decoder')



def cgi_decode(s: str) -> str:
    """Decode the CGI-encoded string `s`:
       * replace '+' by ' '
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

if __name__ == '__main__':
    cgi_decode("Hello+world")

## Black-Box Testing
## -----------------

if __name__ == '__main__':
    print('\n## Black-Box Testing')



if __name__ == '__main__':
    assert cgi_decode('+') == ' '
    assert cgi_decode('%20') == ' '
    assert cgi_decode('abc') == 'abc'

    try:
        cgi_decode('%?a')
        assert False
    except ValueError:
        pass

## White-Box Testing
## -----------------

if __name__ == '__main__':
    print('\n## White-Box Testing')



## Tracing Executions
## ------------------

if __name__ == '__main__':
    print('\n## Tracing Executions')



if __name__ == '__main__':
    cgi_decode("a+b")

from types import FrameType, TracebackType

if __name__ == '__main__':
    coverage = []

def traceit(frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
    """Trace program execution. To be passed to sys.settrace()."""
    if event == 'line':
        global coverage
        function_name = frame.f_code.co_name
        lineno = frame.f_lineno
        coverage.append(lineno)

    return traceit

import sys

def cgi_decode_traced(s: str) -> None:
    global coverage
    coverage = []
    sys.settrace(traceit)  # Turn on
    cgi_decode(s)
    sys.settrace(None)    # Turn off

if __name__ == '__main__':
    cgi_decode_traced("a+b")
    print(coverage)

import inspect

if __name__ == '__main__':
    cgi_decode_code = inspect.getsource(cgi_decode)

from .bookutils import print_content, print_file

if __name__ == '__main__':
    print_content(cgi_decode_code[:300] + "...", ".py")

if __name__ == '__main__':
    cgi_decode_lines = [""] + cgi_decode_code.splitlines()

if __name__ == '__main__':
    cgi_decode_lines[1]

if __name__ == '__main__':
    cgi_decode_lines[9:13]

if __name__ == '__main__':
    cgi_decode_lines[15]

if __name__ == '__main__':
    covered_lines = set(coverage)
    print(covered_lines)

if __name__ == '__main__':
    for lineno in range(1, len(cgi_decode_lines)):
        if lineno not in covered_lines:
            print("# ", end="")
        else:
            print("  ", end="")
        print("%2d  " % lineno, end="")
        print_content(cgi_decode_lines[lineno], '.py')
        print()

## A Coverage Class
## ----------------

if __name__ == '__main__':
    print('\n## A Coverage Class')



Location = Tuple[str, int]

class Coverage:
    """Track coverage within a `with` block. Use as
    ```
    with Coverage() as cov:
        function_to_be_traced()
    c = cov.coverage()
    ```
    """

    def __init__(self) -> None:
        """Constructor"""
        self._trace: List[Location] = []

    # Trace function
    def traceit(self, frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
        """Tracing function. To be overloaded in subclasses."""
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        if event == "line":
            function_name = frame.f_code.co_name
            lineno = frame.f_lineno
            if function_name != '__exit__':  # avoid tracing ourselves:
                self._trace.append((function_name, lineno))

        return self.traceit

    def __enter__(self) -> Any:
        """Start of `with` block. Turn on tracing."""
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    def __exit__(self, exc_type: Type, exc_value: BaseException, 
                 tb: TracebackType) -> Optional[bool]:
        """End of `with` block. Turn off tracing."""
        sys.settrace(self.original_trace_function)
        return None  # default: pass all exceptions

    def trace(self) -> List[Location]:
        """The list of executed lines, as (function_name, line_number) pairs"""
        return self._trace

    def coverage(self) -> Set[Location]:
        """The set of executed lines, as (function_name, line_number) pairs"""
        return set(self.trace())

    def function_names(self) -> Set[str]:
        """The set of function names seen"""
        return set(function_name for (function_name, line_number) in self.coverage())

    def __repr__(self) -> str:
        """Return a string representation of this object.
           Show covered (and uncovered) program code"""
        t = ""
        for function_name in self.function_names():
            # Similar code as in the example above
            try:
                fun = eval(function_name)
            except Exception as exc:
                t += f"Skipping {function_name}: {exc}"
                continue

            source_lines, start_line_number = inspect.getsourcelines(fun)
            for lineno in range(start_line_number, start_line_number + len(source_lines)):
                if (function_name, lineno) in self.trace():
                    t += "# "
                else:
                    t += "  "
                t += "%2d  " % lineno
                t += source_lines[lineno - start_line_number]

        return t

if __name__ == '__main__':
    with Coverage() as cov:
        cgi_decode("a+b")

    print(cov.coverage())

if __name__ == '__main__':
    print(cov)

## Comparing Coverage
## ------------------

if __name__ == '__main__':
    print('\n## Comparing Coverage')



if __name__ == '__main__':
    with Coverage() as cov_plus:
        cgi_decode("a+b")
    with Coverage() as cov_standard:
        cgi_decode("abc")

    cov_plus.coverage() - cov_standard.coverage()

if __name__ == '__main__':
    with Coverage() as cov_max:
        cgi_decode('+')
        cgi_decode('%20')
        cgi_decode('abc')
        try:
            cgi_decode('%?a')
        except Exception:
            pass

if __name__ == '__main__':
    cov_max.coverage() - cov_plus.coverage()

##  Coverage of Basic Fuzzing
## --------------------------

if __name__ == '__main__':
    print('\n##  Coverage of Basic Fuzzing')



from .Fuzzer import fuzzer

if __name__ == '__main__':
    sample = fuzzer()
    sample

if __name__ == '__main__':
    with Coverage() as cov_fuzz:
        try:
            cgi_decode(sample)
        except:
            pass
    cov_fuzz.coverage()

if __name__ == '__main__':
    cov_max.coverage() - cov_fuzz.coverage()

if __name__ == '__main__':
    trials = 100

def population_coverage(population: List[str], function: Callable) \
        -> Tuple[Set[Location], List[int]]:
    cumulative_coverage: List[int] = []
    all_coverage: Set[Location] = set()

    for s in population:
        with Coverage() as cov:
            try:
                function(s)
            except:
                pass
        all_coverage |= cov.coverage()
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage

def hundred_inputs() -> List[str]:
    population = []
    for i in range(trials):
        population.append(fuzzer())
    return population

if __name__ == '__main__':
    all_coverage, cumulative_coverage = \
        population_coverage(hundred_inputs(), cgi_decode)

# %matplotlib inline

if __name__ == '__main__':
    import matplotlib.pyplot as plt  # type: ignore

if __name__ == '__main__':
    plt.plot(cumulative_coverage)
    plt.title('Coverage of cgi_decode() with random inputs')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered')

if __name__ == '__main__':
    runs = 100

    # Create an array with TRIALS elements, all zero
    sum_coverage = [0] * trials

    for run in range(runs):
        all_coverage, coverage = population_coverage(hundred_inputs(), cgi_decode)
        assert len(coverage) == trials
        for i in range(trials):
            sum_coverage[i] += coverage[i]

    average_coverage = []
    for i in range(trials):
        average_coverage.append(sum_coverage[i] / runs)

if __name__ == '__main__':
    plt.plot(average_coverage)
    plt.title('Average coverage of cgi_decode() with random inputs')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered')

## Getting Coverage from External Programs
## ---------------------------------------

if __name__ == '__main__':
    print('\n## Getting Coverage from External Programs')



if __name__ == '__main__':
    cgi_c_code = """
/* CGI decoding as C program */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

"""

if __name__ == '__main__':
    cgi_c_code += r"""
int hex_values[256];

void init_hex_values() {
    for (int i = 0; i < sizeof(hex_values) / sizeof(int); i++) {
        hex_values[i] = -1;
    }
    hex_values['0'] = 0; hex_values['1'] = 1; hex_values['2'] = 2; hex_values['3'] = 3;
    hex_values['4'] = 4; hex_values['5'] = 5; hex_values['6'] = 6; hex_values['7'] = 7;
    hex_values['8'] = 8; hex_values['9'] = 9;

    hex_values['a'] = 10; hex_values['b'] = 11; hex_values['c'] = 12; hex_values['d'] = 13;
    hex_values['e'] = 14; hex_values['f'] = 15;

    hex_values['A'] = 10; hex_values['B'] = 11; hex_values['C'] = 12; hex_values['D'] = 13;
    hex_values['E'] = 14; hex_values['F'] = 15;
}
"""

if __name__ == '__main__':
    cgi_c_code += r"""
int cgi_decode(char *s, char *t) {
    while (*s != '\0') {
        if (*s == '+')
            *t++ = ' ';
        else if (*s == '%') {
            int digit_high = *++s;
            int digit_low = *++s;
            if (hex_values[digit_high] >= 0 && hex_values[digit_low] >= 0) {
                *t++ = hex_values[digit_high] * 16 + hex_values[digit_low];
            }
            else
                return -1;
        }
        else
            *t++ = *s;
        s++;
    }
    *t = '\0';
    return 0;
}
"""

if __name__ == '__main__':
    cgi_c_code += r"""
int main(int argc, char *argv[]) {
    init_hex_values();

    if (argc >= 2) {
        char *s = argv[1];
        char *t = malloc(strlen(s) + 1); /* output is at most as long as input */
        int ret = cgi_decode(s, t);
        printf("%s\n", t);
        return ret;
    }
    else
    {
        printf("cgi_decode: usage: cgi_decode STRING\n");
        return 1;
    }
}
"""

if __name__ == '__main__':
    with open("cgi_decode.c", "w") as f:
        f.write(cgi_c_code)

from .bookutils import print_file

if __name__ == '__main__':
    print_file("cgi_decode.c")

if __name__ == '__main__':
    import os
    os.system(f'cc --coverage -o cgi_decode cgi_decode.c')

if __name__ == '__main__':
    import os
    os.system(f"./cgi_decode 'Send+mail+to+me%40fuzzingbook.org'")

if __name__ == '__main__':
    import os
    os.system(f'gcov cgi_decode.c')

if __name__ == '__main__':
    lines = open('cgi_decode.c.gcov').readlines()
    for i in range(30, 50):
        print(lines[i], end='')

def read_gcov_coverage(c_file):
    gcov_file = c_file + ".gcov"
    coverage = set()
    with open(gcov_file) as file:
        for line in file.readlines():
            elems = line.split(':')
            covered = elems[0].strip()
            line_number = int(elems[1].strip())
            if covered.startswith('-') or covered.startswith('#'):
                continue
            coverage.add((c_file, line_number))
    return coverage

if __name__ == '__main__':
    coverage = read_gcov_coverage('cgi_decode.c')

if __name__ == '__main__':
    list(coverage)[:5]

## Finding Errors with Basic Fuzzing
## ---------------------------------

if __name__ == '__main__':
    print('\n## Finding Errors with Basic Fuzzing')



from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        for i in range(trials):
            try:
                s = fuzzer()
                cgi_decode(s)
            except ValueError:
                pass

if __name__ == '__main__':
    s

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    with Coverage() as cov:
        cgi_decode("a+b")

if __name__ == '__main__':
    print(cov)

if __name__ == '__main__':
    cov.trace()

if __name__ == '__main__':
    cov.coverage()

from .ClassDiagram import display_class_hierarchy

if __name__ == '__main__':
    display_class_hierarchy(Coverage,
                            public_methods=[
                                Coverage.__init__,
                                Coverage.__enter__,
                                Coverage.__exit__,
                                Coverage.coverage,
                                Coverage.trace,
                                Coverage.function_names,
                                Coverage.__repr__,
                            ],
                            types={'Location': Location},
                            project='fuzzingbook')

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



import os
import glob

if __name__ == '__main__':
    for file in glob.glob("cgi_decode") + glob.glob("cgi_decode.*"):
        os.remove(file)

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



### Exercise 1: Fixing `cgi_decode()`

if __name__ == '__main__':
    print('\n### Exercise 1: Fixing `cgi_decode()`')



if __name__ == '__main__':
    with ExpectError():
        assert cgi_decode('%') == '%'

if __name__ == '__main__':
    with ExpectError():
        assert cgi_decode('%4') == '%4'

if __name__ == '__main__':
    assert cgi_decode('%40') == '@'

def fixed_cgi_decode(s):
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
        elif c == '%' and i + 2 < len(s):  # <--- *** FIX ***
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

if __name__ == '__main__':
    assert fixed_cgi_decode('%') == '%'

if __name__ == '__main__':
    assert fixed_cgi_decode('%4') == '%4'

if __name__ == '__main__':
    assert fixed_cgi_decode('%40') == '@'

if __name__ == '__main__':
    for i in range(trials):
        try:
            s = fuzzer()
            fixed_cgi_decode(s)
        except ValueError:
            pass

if __name__ == '__main__':
    cgi_c_code = cgi_c_code.replace(
        r"if (*s == '%')",  # old code
        r"if (*s == '%' && s[1] != '\0' && s[2] != '\0')"  # new code
    )

### Exercise 2: Branch Coverage

if __name__ == '__main__':
    print('\n### Exercise 2: Branch Coverage')



if __name__ == '__main__':
    with Coverage() as cov:
        cgi_decode("a+b")
    trace = cov.trace()
    trace[:5]

#### Part 1: Compute branch coverage

if __name__ == '__main__':
    print('\n#### Part 1: Compute branch coverage')



def branch_coverage(trace):
    coverage = set()
    past_line = None
    for line in trace:
        if past_line is not None:
            coverage.add((past_line, line))
        past_line = line

    return coverage

if __name__ == '__main__':
    branch_coverage(trace)

class BranchCoverage(Coverage):
    def coverage(self):
        """The set of executed line pairs"""
        coverage = set()
        past_line = None
        for line in self.trace():
            if past_line is not None:
                coverage.add((past_line, line))
            past_line = line

        return coverage

#### Part 2: Comparing statement coverage and branch coverage

if __name__ == '__main__':
    print('\n#### Part 2: Comparing statement coverage and branch coverage')



if __name__ == '__main__':
    with BranchCoverage() as cov:
        cgi_decode("a+b")

    print(cov.coverage())

if __name__ == '__main__':
    with BranchCoverage() as cov_plus:
        cgi_decode("a+b")
    with BranchCoverage() as cov_standard:
        cgi_decode("abc")

    cov_plus.coverage() - cov_standard.coverage()

if __name__ == '__main__':
    with BranchCoverage() as cov_max:
        cgi_decode('+')
        cgi_decode('%20')
        cgi_decode('abc')
        try:
            cgi_decode('%?a')
        except:
            pass

if __name__ == '__main__':
    cov_max.coverage() - cov_plus.coverage()

if __name__ == '__main__':
    sample

if __name__ == '__main__':
    with BranchCoverage() as cov_fuzz:
        try:
            cgi_decode(s)
        except:
            pass
    cov_fuzz.coverage()

if __name__ == '__main__':
    cov_max.coverage() - cov_fuzz.coverage()

def population_branch_coverage(population, function):
    cumulative_coverage = []
    all_coverage = set()

    for s in population:
        with BranchCoverage() as cov:
            try:
                function(s)
            except Exception:
                pass
        all_coverage |= cov.coverage()
        cumulative_coverage.append(len(all_coverage))

    return all_coverage, cumulative_coverage

if __name__ == '__main__':
    all_branch_coverage, cumulative_branch_coverage = population_branch_coverage(
        hundred_inputs(), cgi_decode)

if __name__ == '__main__':
    plt.plot(cumulative_branch_coverage)
    plt.title('Branch coverage of cgi_decode() with random inputs')
    plt.xlabel('# of inputs')
    plt.ylabel('line pairs covered')

if __name__ == '__main__':
    len(cov_max.coverage())

if __name__ == '__main__':
    all_branch_coverage - cov_max.coverage()

if __name__ == '__main__':
    cov_max.coverage() - all_branch_coverage

#### Part 3: Average coverage

if __name__ == '__main__':
    print('\n#### Part 3: Average coverage')



if __name__ == '__main__':
    runs = 100

    # Create an array with TRIALS elements, all zero
    sum_coverage = [0] * trials

    for run in range(runs):
        all_branch_coverage, coverage = population_branch_coverage(
            hundred_inputs(), cgi_decode)
        assert len(coverage) == trials
        for i in range(trials):
            sum_coverage[i] += coverage[i]

    average_coverage = []
    for i in range(trials):
        average_coverage.append(sum_coverage[i] / runs)

if __name__ == '__main__':
    plt.plot(average_coverage)
    plt.title('Average branch coverage of cgi_decode() with random inputs')
    plt.xlabel('# of inputs')
    plt.ylabel('line pairs covered')
