#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Fuzzing: Breaking Things with Random Inputs" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/Fuzzer.html
# Last change: 2021-06-02 17:40:53+02:00
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
The Fuzzing Book - Fuzzing: Breaking Things with Random Inputs

This file can be _executed_ as a script, running all experiments:

    $ python Fuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.Fuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/Fuzzer.html

This chapter provides two important classes, introduced in [A Fuzzing Architecture](#A-Fuzzing-Architecture):

* `Fuzzer` as a base class for fuzzers; and
* `Runner` as a base class for programs under test.

### Fuzzers

`Fuzzer` is a base class for fuzzers, with `RandomFuzzer` as a simple instantiation.  The `fuzz()` method of `Fuzzer` objects returns a string with a generated input.

>>> random_fuzzer = RandomFuzzer()
>>> random_fuzzer.fuzz()
'%$<1&?99$%7!!*#96=>2&-/(5*)=$;0$$+;<12"?30&'

The `RandomFuzzer()` constructor allows to specify a number of keyword arguments:

>>> print(RandomFuzzer.__init__.__doc__)
Produce strings of `min_length` to `max_length` characters
           in the range [`char_start`, `char_start` + `char_range`]

>>> random_fuzzer = RandomFuzzer(min_length=10, max_length=20, char_start=65, char_range=26)
>>> random_fuzzer.fuzz()
'XGZVDDPZOOW'

### Runners

A `Fuzzer` can be paired with a `Runner`, which takes the fuzzed strings as input. Its result is a class-specific _status_ and an _outcome_ (`PASS`, `FAIL`, or `UNRESOLVED`). A `PrintRunner` will simply print out the given input and return a `PASS` outcome:

>>> print_runner = PrintRunner()
>>> random_fuzzer.run(print_runner)
EQYGAXPTVPJGTYHXFJ

('EQYGAXPTVPJGTYHXFJ', 'UNRESOLVED')

A `ProgramRunner` will feed the generated input into an external program.  Its result is a pair of the program status (a `CompletedProcess` instance) and an _outcome_ (`PASS`, `FAIL`, or `UNRESOLVED`):

>>> cat = ProgramRunner('cat')
>>> random_fuzzer.run(cat)
(CompletedProcess(args='cat', returncode=0, stdout='BZOQTXFBTEOVYX', stderr=''),
 'PASS')


For more details, source, and documentation, see
"The Fuzzing Book - Fuzzing: Breaking Things with Random Inputs"
at https://www.fuzzingbook.org/html/Fuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Fuzzing: Breaking Things with Random Inputs
# ===========================================

if __name__ == '__main__':
    print('# Fuzzing: Breaking Things with Random Inputs')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from . import Intro_Testing

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## A Testing Assignment
## --------------------

if __name__ == '__main__':
    print('\n## A Testing Assignment')



## A Simple Fuzzer
## ---------------

if __name__ == '__main__':
    print('\n## A Simple Fuzzer')



import random

def fuzzer(max_length=100, char_start=32, char_range=32):
    """A string of up to `max_length` characters
       in the range [`char_start`, `char_start` + `char_range`]"""
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

if __name__ == '__main__':
    fuzzer()

if __name__ == '__main__':
    fuzzer(1000, ord('a'), 26)

## Fuzzing External Programs
## -------------------------

if __name__ == '__main__':
    print('\n## Fuzzing External Programs')



### Creating Input Files

if __name__ == '__main__':
    print('\n### Creating Input Files')



import os
import tempfile

if __name__ == '__main__':
    basename = "input.txt"
    tempdir = tempfile.mkdtemp()
    FILE = os.path.join(tempdir, basename)
    print(FILE)

if __name__ == '__main__':
    data = fuzzer()
    with open(FILE, "w") as f:
        f.write(data)

if __name__ == '__main__':
    contents = open(FILE).read()
    print(contents)
    assert(contents == data)

### Invoking External Programs

if __name__ == '__main__':
    print('\n### Invoking External Programs')



import os
import subprocess

if __name__ == '__main__':
    program = "bc"
    with open(FILE, "w") as f:
        f.write("2 + 2\n")
    result = subprocess.run([program, FILE],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)  # Will be "text" in Python 3.7

if __name__ == '__main__':
    result.stdout

if __name__ == '__main__':
    result.returncode

if __name__ == '__main__':
    result.stderr

### Long-Running Fuzzing

if __name__ == '__main__':
    print('\n### Long-Running Fuzzing')



if __name__ == '__main__':
    trials = 100
    program = "bc"

    runs = []

    for i in range(trials):
        data = fuzzer()
        with open(FILE, "w") as f:
            f.write(data)
        result = subprocess.run([program, FILE],
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        runs.append((data, result))

if __name__ == '__main__':
    sum(1 for (data, result) in runs if result.stderr == "")

if __name__ == '__main__':
    errors = [(data, result) for (data, result) in runs if result.stderr != ""]
    (first_data, first_result) = errors[0]

    print(repr(first_data))
    print(first_result.stderr)

if __name__ == '__main__':
    [result.stderr for (data, result) in runs if
     result.stderr != ""
     and "illegal character" not in result.stderr
     and "parse error" not in result.stderr
     and "syntax error" not in result.stderr]

if __name__ == '__main__':
    sum(1 for (data, result) in runs if result.returncode != 0)

## Bugs Fuzzers Find
## -----------------

if __name__ == '__main__':
    print('\n## Bugs Fuzzers Find')



### Buffer Overflows

if __name__ == '__main__':
    print('\n### Buffer Overflows')



def crash_if_too_long(s):
    buffer = "Thursday"
    if len(s) > len(buffer):
        raise ValueError

from .ExpectError import ExpectError

if __name__ == '__main__':
    trials = 100
    with ExpectError():
        for i in range(trials):
            s = fuzzer()
            crash_if_too_long(s)

### Missing Error Checks

if __name__ == '__main__':
    print('\n### Missing Error Checks')



def hang_if_no_space(s):
    i = 0
    while True:
        if i < len(s):
            if s[i] == ' ':
                break
        i += 1

from .ExpectError import ExpectTimeout

if __name__ == '__main__':
    trials = 100
    with ExpectTimeout(2):
        for i in range(trials):
            s = fuzzer()
            hang_if_no_space(s)

def collapse_if_too_large(s):
    if int(s) > 1000:
        raise ValueError

if __name__ == '__main__':
    long_number = fuzzer(100, ord('0'), 10)
    print(long_number)

if __name__ == '__main__':
    with ExpectError():
        collapse_if_too_large(long_number)

## Catching Errors
## ---------------

if __name__ == '__main__':
    print('\n## Catching Errors')



### Generic Checkers

if __name__ == '__main__':
    print('\n### Generic Checkers')



#### Checking Memory Accesses

if __name__ == '__main__':
    print('\n#### Checking Memory Accesses')



if __name__ == '__main__':
    with open("program.c", "w") as f:
        f.write("""
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv) {
    /* Create an array with 100 bytes, initialized with 42 */
    char *buf = malloc(100);
    memset(buf, 42, 100);

    /* Read the N-th element, with N being the first command-line argument */
    int index = atoi(argv[1]);
    char val = buf[index];

    /* Clean up memory so we don't leak */
    free(buf);
    return val;
}
    """)

from .bookutils import print_file

if __name__ == '__main__':
    print_file("program.c")

if __name__ == '__main__':
    import os
    os.system(f'clang -fsanitize=address -g -o program program.c')

if __name__ == '__main__':
    import os
    os.system(f'./program 99; echo $?')

if __name__ == '__main__':
    import os
    os.system(f'./program 110')

if __name__ == '__main__':
    import os
    os.system(f'rm -fr program program.*')

#### Information Leaks

if __name__ == '__main__':
    print('\n#### Information Leaks')



if __name__ == '__main__':
    secrets = ("<space for reply>" + fuzzer(100)
         + "<secret-certificate>" + fuzzer(100)
         + "<secret-key>" + fuzzer(100) + "<other-secrets>")

if __name__ == '__main__':
    uninitialized_memory_marker = "deadbeef"
    while len(secrets) < 2048:
        secrets += uninitialized_memory_marker

def heartbeat(reply, length, memory):
    # Store reply in memory
    memory = reply + memory[len(reply):]

    # Send back heartbeat
    s = ""
    for i in range(length):
        s += memory[i]
    return s

if __name__ == '__main__':
    heartbeat("potato", 6, memory=secrets)

if __name__ == '__main__':
    heartbeat("bird", 4, memory=secrets)

if __name__ == '__main__':
    heartbeat("hat", 500, memory=secrets)

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        for i in range(10):
            s = heartbeat(fuzzer(), random.randint(1, 500), memory=secrets)
            assert not s.find(uninitialized_memory_marker)
            assert not s.find("secret")

### Program-Specific Checkers

if __name__ == '__main__':
    print('\n### Program-Specific Checkers')



if __name__ == '__main__':
    airport_codes = {
        "YVR": "Vancouver",
        "JFK": "New York-JFK",
        "CDG": "Paris-Charles de Gaulle",
        "CAI": "Cairo",
        "LED": "St. Petersburg",
        "PEK": "Beijing",
        "HND": "Tokyo-Haneda",
        "AKL": "Auckland"
    }  # plus many more


if __name__ == '__main__':
    airport_codes["YVR"]

if __name__ == '__main__':
    "AKL" in airport_codes

def code_repOK(code):
    assert len(code) == 3, "Airport code must have three characters: " + repr(code)
    for c in code:
        assert c.isalpha(), "Non-letter in airport code: " + repr(code)
        assert c.isupper(), "Lowercase letter in airport code: " + repr(code)
    return True

if __name__ == '__main__':
    assert code_repOK("SEA")

def airport_codes_repOK():
    for code in airport_codes:
        assert code_repOK(code)
    return True

if __name__ == '__main__':
    with ExpectError():
        assert airport_codes_repOK()

if __name__ == '__main__':
    airport_codes["YMML"] = "Melbourne"

if __name__ == '__main__':
    with ExpectError():
        assert airport_codes_repOK()

def add_new_airport(code, city):
    assert code_repOK(code)
    airport_codes[code] = city

if __name__ == '__main__':
    with ExpectError():  # For BER, ExpectTimeout would be more appropriate
        add_new_airport("BER", "Berlin")

if __name__ == '__main__':
    with ExpectError():
        add_new_airport("London-Heathrow", "LHR")

def add_new_airport(code, city):
    assert code_repOK(code)
    assert airport_codes_repOK()
    airport_codes[code] = city
    assert airport_codes_repOK()

if __name__ == '__main__':
    with ExpectError():
        add_new_airport("IST", "Istanbul Yeni Havalimanı")

class RedBlackTree:
    def repOK(self):
        assert self.rootHasNoParent()
        assert self.rootIsBlack()
        assert self.rootNodesHaveOnlyBlackChildren()
        assert self.treeIsAcyclic()
        assert self.parentsAreConsistent()
        return True

    def rootIsBlack(self):
        if self.parent is None:
            assert self.color == BLACK
        return True

    def add_element(self, elem):
        assert self.repOK()
        # Add the element
        assert self.repOK()

    def delete_element(self, elem):
        assert self.repOK()
        # Delete the element
        assert self.repOK()


### Static Code Checkers

if __name__ == '__main__':
    print('\n### Static Code Checkers')



from typing import Dict

airport_codes = {
    "YVR": "Vancouver",  # etc
}  # type: Dict[str, str]


if __name__ == '__main__':
    airport_codes[1] = "First"

## A Fuzzing Architecture
## ----------------------

if __name__ == '__main__':
    print('\n## A Fuzzing Architecture')



### Runner Classes

if __name__ == '__main__':
    print('\n### Runner Classes')



class Runner(object):
    # Test outcomes
    PASS = "PASS"
    FAIL = "FAIL"
    UNRESOLVED = "UNRESOLVED"

    def __init__(self):
        """Initialize"""
        pass

    def run(self, inp):
        """Run the runner with the given input"""
        return (inp, Runner.UNRESOLVED)

class PrintRunner(Runner):
    def run(self, inp):
        """Print the given input"""
        print(inp)
        return (inp, Runner.UNRESOLVED)

if __name__ == '__main__':
    p = PrintRunner()
    (result, outcome) = p.run("Some input")

if __name__ == '__main__':
    result

if __name__ == '__main__':
    outcome

class ProgramRunner(Runner):
    def __init__(self, program):
        """Initialize.  `program` is a program spec as passed to `subprocess.run()`"""
        self.program = program

    def run_process(self, inp=""):
        """Run the program with `inp` as input.  Return result of `subprocess.run()`."""
        return subprocess.run(self.program,
                              input=inp,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True)

    def run(self, inp=""):
        """Run the program with `inp` as input.  Return test outcome based on result of `subprocess.run()`."""
        result = self.run_process(inp)

        if result.returncode == 0:
            outcome = self.PASS
        elif result.returncode < 0:
            outcome = self.FAIL
        else:
            outcome = self.UNRESOLVED

        return (result, outcome)

class BinaryProgramRunner(ProgramRunner):
    def run_process(self, inp=""):
        """Run the program with `inp` as input.  Return result of `subprocess.run()`."""
        return subprocess.run(self.program,
                              input=inp.encode(),
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

if __name__ == '__main__':
    cat = ProgramRunner(program="cat")
    cat.run("hello")

### Fuzzer Classes

if __name__ == '__main__':
    print('\n### Fuzzer Classes')



class Fuzzer(object):
    def __init__(self):
        pass

    def fuzz(self):
        """Return fuzz input"""
        return ""

    def run(self, runner=Runner()):
        """Run `runner` with fuzz input"""
        return runner.run(self.fuzz())

    def runs(self, runner=PrintRunner(), trials=10):
        """Run `runner` with fuzz input, `trials` times"""
        # Note: the list comprehension below does not invoke self.run() for subclasses
        # return [self.run(runner) for i in range(trials)]
        outcomes = []
        for i in range(trials):
            outcomes.append(self.run(runner))
        return outcomes

class RandomFuzzer(Fuzzer):
    def __init__(self, min_length=10, max_length=100,
                 char_start=32, char_range=32):
        """Produce strings of `min_length` to `max_length` characters
           in the range [`char_start`, `char_start` + `char_range`]"""
        self.min_length = min_length
        self.max_length = max_length
        self.char_start = char_start
        self.char_range = char_range

    def fuzz(self):
        string_length = random.randrange(self.min_length, self.max_length + 1)
        out = ""
        for i in range(0, string_length):
            out += chr(random.randrange(self.char_start,
                                        self.char_start + self.char_range))
        return out

if __name__ == '__main__':
    random_fuzzer = RandomFuzzer(min_length=20, max_length=20)
    for i in range(10):
        print(random_fuzzer.fuzz())

if __name__ == '__main__':
    for i in range(10):
        inp = random_fuzzer.fuzz()
        result, outcome = cat.run(inp)
        assert result.stdout == inp
        assert outcome == Runner.PASS

if __name__ == '__main__':
    random_fuzzer.run(cat)

if __name__ == '__main__':
    random_fuzzer.runs(cat, 10)

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



### Fuzzers

if __name__ == '__main__':
    print('\n### Fuzzers')



if __name__ == '__main__':
    random_fuzzer = RandomFuzzer()
    random_fuzzer.fuzz()

if __name__ == '__main__':
    print(RandomFuzzer.__init__.__doc__)

if __name__ == '__main__':
    random_fuzzer = RandomFuzzer(min_length=10, max_length=20, char_start=65, char_range=26)
    random_fuzzer.fuzz()

### Runners

if __name__ == '__main__':
    print('\n### Runners')



if __name__ == '__main__':
    print_runner = PrintRunner()
    random_fuzzer.run(print_runner)

if __name__ == '__main__':
    cat = ProgramRunner('cat')
    random_fuzzer.run(cat)

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



if __name__ == '__main__':
    os.remove(FILE)
    os.removedirs(tempdir)

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



### Exercise 1: Simulate Troff

if __name__ == '__main__':
    print('\n### Exercise 1: Simulate Troff')



import string

def no_backslash_d(inp):
    pattern = "\\D"
    index = inp.find(pattern)
    if index < 0 or index + len(pattern) >= len(inp):
        return True
    c = inp[index + len(pattern)]
    assert c in string.printable

if __name__ == '__main__':
    with ExpectError():
        no_backslash_d("\\D\0")

def no_8bit(inp):
    for i in range(len(inp) - 1):
        assert ord(inp[i]) <= 127 or inp[i + 1] != '\n'
    return True

if __name__ == '__main__':
    with ExpectError():
        no_8bit("ä\n")

def no_dot(inp):
    assert inp != ".\n"
    return True

### Exercise 2: Run Simulated Troff

if __name__ == '__main__':
    print('\n### Exercise 2: Run Simulated Troff')



class TroffRunner(Runner):
    def __init__(self):
        self.no_backslash_d_failures = 0
        self.no_8bit_failures = 0
        self.no_dot_failures = 0

    def run(self, inp):
        try:
            no_backslash_d(inp)
        except AssertionError:
            self.no_backslash_d_failures += 1

        try:
            no_8bit(inp)
        except AssertionError:
            self.no_8bit_failures += 1

        try:
            no_dot(inp)
        except:
            self.no_dot_failures += 1

        return inp


if __name__ == '__main__':
    random_fuzzer = RandomFuzzer(char_start=0, char_range=256, max_length=10)
    troff_runner = TroffRunner()

    trials = 100000
    for i in range(trials):
        random_fuzzer.run(troff_runner)

if __name__ == '__main__':
    troff_runner.no_backslash_d_failures

if __name__ == '__main__':
    troff_runner.no_8bit_failures

if __name__ == '__main__':
    troff_runner.no_dot_failures

# %matplotlib inline
# 
# ys = [troff_runner.no_backslash_d_failures,
#       troff_runner.no_8bit_failures,
#       troff_runner.no_dot_failures]
# 
# import matplotlib.pyplot as plt
# plt.bar(["\\D", "8bit", "dot"], ys)
# plt.title("Occurrences of error classes");
# 

### Exercise 3: Run Real Troff

if __name__ == '__main__':
    print('\n### Exercise 3: Run Real Troff')



if __name__ == '__main__':
    real_troff_runner = BinaryProgramRunner("troff")
    for i in range(100):
        result, outcome = random_fuzzer.run(real_troff_runner)
        if outcome == Runner.FAIL:
            print(result)
