#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is part of "Generating Software Tests"
# (https://www.fuzzingbook.org/)
# It is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License,
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)

# # Fuzzing: Breaking Things with Random Inputs
# 
# In this chapter, we'll start with one of the simplest test generation techniques.  The key idea of random text generation, also known as "fuzzing", is to feed a _string of random characters_ into a program in the hope to uncover failures.
# 
# **Prerequisites**
# 
# * You should know fundamentals of software testing; for instance, from the chapter ["Introduction to Software Testing"](Intro_Testing.ipynb).
# 
# ## A Testing Assignment
# 
# Fuzzing was conceived by Bart Miller in 1989 as a programming exercise for his students at the University of Wisconsin-Madison.  The [assignment](http://pages.cs.wisc.edu/~bart/fuzz/CS736-Projects-f1988.pdf) read 
# 
# > The goal of this project is to evaluate the robustness of various UNIX utility programs, given an unpredictable input stream. [...] First, you will build a _fuzz generator_. This is a program that will output a random character stream. Second, you will take the fuzz generator and use it to attack as many UNIX utilities as possible, with the goal of trying to break them.
# 
# This assignment captures the essence of fuzzing: _Create random inputs, and see if they break things._  Just let it run long enough and you'll see.
# 
# ## A Simple Fuzzer
# 
# Let us try to fulfill this assignment and build a fuzz generator.  The idea is to produce random characters, adding them to a buffer string variable (`out`), and finally returning the string.
# 
# This implementation uses the following Python features and functions:
# 
# * `random.randrange(start, end)` – return a random number $[$ `start`, `end` $)$
# * `range(start, end)` – create a list with integers from `start` to `end`.  Typically used in iterations.
# * `for elem in list: body` – execute `body` in a loop with `elem` taking each value from `list`.
# * `for i in range(start, end): body` – execute `body` in a loop with `i` from `start` to `end` $-$ 1.
# * `chr(n)` – return a character with ASCII code `n`
# 
# First, we'll import a standard package required for working in notebooks.
# 
# import fuzzingbook_utils
# 
# Next, we'll need random numbers.  We set a specific _seed_ to obtain the same sequence of random numbers each time; if you run this notebook interactively, thoguh, you will get different (well, random) results with each new invocation.
# 
import random

if __name__ == "__main__":
    random.seed(53727895348829)
    
# Here comes the actual `fuzzer()` function.
# 
def fuzzer(max_length=100, char_start=32, char_range=32):
    """A string of up to `max_length` characters 
       in the range [`char_start`, `char_start` + `char_range`]"""
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

# With its default arguments, the `fuzzer()` function returns a string of random characters:
# 
if __name__ == "__main__":
    fuzzer()
    
# get_ipython().set_next_input('Now imagine that this string was the input to a program expecting a specific input format –\xa0say, a comma-separated list of values, or an e-mail address.  Would the program be able to process such an input without any problems');get_ipython().run_line_magic('pinfo', 'problems')
# 
# If the above fuzzing input already is intriguing, consider that fuzzing can easily be set up to produce other kinds of input.  For instance, we can also have `fuzzer()` produce a series of uppercase letters.  We use `ord(c)` to return the ASCII code of the character `c`.
# 
if __name__ == "__main__":
    fuzzer(1000, ord('a'), 26)
    
# get_ipython().set_next_input('Assume a program expects an identifier as its input.  Would it expect such a long identifier');get_ipython().run_line_magic('pinfo', 'identifier')
# 
# ## Fuzzing External Programs
# 
# Let us see what happens if we actually invoke an external program with fuzzed inputs.  To this end, let us proceed in two steps.  First, we create an _input file_ with fuzzed test data; then we feed this input file into a program of choice.
# 
# ### Creating Input Files
# 
# The Python `open()` function opens a file into which we can then write arbitrary contents.  It is commonly used in conjunction with the `with` statement, which ensures that the file is closed as soon as it is no longer needed.
# 
FILE = "input.txt"
data = fuzzer()
with open(FILE, "w") as f:
    f.write(data)

# We can verify that the file was actually created by reading its contents:
# 
if __name__ == "__main__":
    contents = open(FILE).read()
    print(contents)
    assert(contents == data)
    
# ### Invoking External Programs
# 
# Now that we have an input file, we can invoke a program on it.  For the fun of it, let us test the `bc` calculator program, which takes an arithmetic expression and evaluates it.
# 
# To invoke `bc`, let us use the Python `subprocess` module.  This is how this works:
# 
import os
import subprocess

if __name__ == "__main__":
    program = "bc"
    with open("input.txt", "w") as f:
        f.write("2 + 2\n")
    result = subprocess.run([program, "input.txt"],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    
# From the `result`, we can check the program output, which in this case consists of a set of typesetting commands:
# 
if __name__ == "__main__":
    result.stdout
    
# We can also check the status. A value of 0 indicates that the program terminated correctly.
# 
if __name__ == "__main__":
    result.returncode
    
# Any error messages would be available in `results.stderr`:
# 
if __name__ == "__main__":
    result.stderr
    
# Instead of `bc`, you can actually put in any program you like.  Be aware, though, that if your program is able to change or even damage your system, there's quite a risk that the fuzzed input contains data or commands that do precisely this.
# 
# Just for the fun of it, imagine you would test a file removal program.  What is the chance of the fuzzer producing a valid file name?  (Note that `.` and `/` may be  valid directory names already.)
# 
# ### Long-Running Fuzzing
# 
# Let us now feed a large number of inputs into our tested program, to see whether it might crash on some.  We store all results in the `runs` variable as pairs of input data and the actual result. (Note: running this may take a while.)
# 
if __name__ == "__main__":
    trials = 100
    program = "bc"
    
    runs = []
    
    for i in range(trials):
        data = fuzzer()
        with open("input.txt", "w") as f:
            f.write(data)
        result = subprocess.run([program, "input.txt"],
                                stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True)
        runs.append((data, result))
    
    os.remove("input.txt")
    
# We can now query `runs` for some statistics.  For instance, we can query how many runs actually passed -- that is, there were no error messages:
# 
if __name__ == "__main__":
    sum(1 for (data, result) in runs if result.stderr == "")
    
# Most inputs apparently are invalid – not a big surprise, as it is unlikely that a random input contains a valid arithmetic expression.
# 
# Let us take a look at the first error message: 
# 
if __name__ == "__main__":
    errors = [(data, result) for (data, result) in runs if result.stderr != ""]
    (first_data, first_result) = errors[0]
    
    print(repr(first_data))
    print(first_result.stderr)
    
# Are there any runs with messages other than `illegal character` or `parse error`?  (Say, something like `crash` or `you found a fatal bug`?)  Not very many:
# 
if __name__ == "__main__":
    [result.stderr for (data, result) in runs if 
     result.stderr != "" 
     and "illegal character" not in result.stderr
     and "parse error" not in result.stderr]
    
# Maybe a crash would be indicated by `bc` just crashing.  Unfortunately, the return code is never nonzero:
# 
if __name__ == "__main__":
    sum(1 for (data, result) in runs if result.returncode != 0)
    
# How about we let the above `bc` test run for some more?  While it is running, let us take a look on how the state of the art was in 1989.
# 
# ## Bugs Fuzzers Find
# 
# When Miller and his students ran their first fuzzers in 1989, they found an alarming result: About **a third of the UNIX utilities** they fuzzed had issues – they crashed, hung, or otherwise failed when confronted with fuzzing input \cite{Miller1990}.  This also included the `bc` program, above.  (Apparently, the bugs have now been fixed!)
# 
# Considering that many of these UNIX utilities were used in scripts that would also process network input, this was an alarming result.  Programmers quickly built and ran their own fuzzers, rushed to fix the reported errors, and learned not to trust external inputs anymore.
# 
# What kind of problems did Miller's fuzzing experiment find?  It turns out that the mistakes programmers made in 1990 are still the same mistakes being made today.
# 
# ### Buffer Overflows
# 
# Many programs have built-in maximum lengths for inputs and input elements.  In languages like C, it is easy to excess these lengths without the program (or the programmer) even noticing, triggering so-called **buffer overflows**.  The following code, for instance, happily copies the `input` string into a `weekday` string even if `input` has more than eight characters:
# ```c
# char weekday[9]; // 8 characters + trailing '\0' terminator
# strcpy (weekday, input);
# ```
# Ironically, this already fails if `input` is `"Wednesday"` (9 characters); any excess characters (here, `'y'` and the following `'\0'` string terminator) are simply copied to whatever resides in memory after `weekday`, triggering arbitrary behavior; maybe some boolean character variable which would be set from `'n'` to `'y'`.  With fuzzing, it is very easy to produce arbitrary long inputs and input elements.
# 
# We can easily simulate this buffer overflow behavior in a Python function:
# 
def crash_if_too_long(s):
    buffer = "Thursday"
    if len(s) > len(buffer):
        raise ValueError

# And yes, it quickly crashes.
# 
from ExpectError import ExpectError

if __name__ == "__main__":
    trials = 100
    with ExpectError():
        for i in range(trials):
            s = fuzzer()
            crash_if_too_long(s)
    
# The `with ExpectError()` line in the above code ensures that the error message is printed, yet execution continues; this is to differentiate this "expected" error from "unexpected" errors in other code examples.
# 
# ### Missing Error Checks
# 
# Many programming languages do not have exceptions, but instead have functions return special **error codes** in exceptional circumstances.  The C function `getchar()`, for instance, normally returns a character from the standard input; if no input is available anymore, it returns the special value `EOF` (end of file).  Now assume a programmer is scanning the input for the next character, skipping space characters:
# ```c
# char read_next_nonspace() {
#     char lastc;
# 
#     do {
#         lastc = getchar();
#     } while (lastc != ' ');
# 
#     return (lastc);
# }
# ```
# What happens if the input ends prematurely, as would perfectly be feasible with fuzzing?  Well, `getchar()` returns `EOF`, and keeps on returning `EOF` when called again; so the code above simply enters an infinite loop.
# 
# Again, we can simulate such missing error checks.  Here's a function that will effectively hang if no space is present in the input:
# 
def hang_if_no_space(s):
    i = 0
    while True:
        if i < len(s):
            if s[i] == ' ':
                break
        i += 1

# Using the timeout mechanism from our [Introduction to Testing](Intro_Testing.ipynb), we can interrupt this function after some time.  And yes, it does hang after a few fuzzing inputs.
# 
from ExpectError import ExpectTimeout

if __name__ == "__main__":
    trials = 100
    with ExpectTimeout(2):
        for i in range(trials):
            s = fuzzer()
            hang_if_no_space(s)
    
# The `with ExpectTimeout()` line in the above code ensures that execution of the enclosed code is interrupted after two seconds, printing the error message.
# 
# 
# ### Rogue Numbers
# 
# With fuzzing, it is easy to generate **uncommon value** in the input, causing all kinds of interesting behavior.  Consider the following code, again in the C language, which first reads a buffer size from the input, and then allocates a buffer of the given size:
# ```c
# char *read_input() {
#     size_t size = read_buffer_size();
#     char *buffer = (char *)malloc(size);
#     // fill buffer
#     return (buffer);
# }
# ```
# What happens if `size` is very large, exceeding program memory?  What happens if `size` is less than the number of characters following?  What happens if `size` is negative?  By providing a random number here, fuzzing can create all kinds of damages.
# 
# Again, we can easily simulate such rogue numbers in Python.  The function `collapse_if_too_large()` fails if the passed value (a string) is too large after having been converted to an integer.
# 
def collapse_if_too_large(s):
    if int(s) > 1000:
        raise ValueError

# We can have `fuzzer()` create a string of digits:
# 
if __name__ == "__main__":
    long_number = fuzzer(100, ord('0'), 10)
    print(long_number)
    
# If we feed such numbers into `collapse_if_too_large()`, it will very soon fail.
# 
if __name__ == "__main__":
    with ExpectError():
        collapse_if_too_large(long_number)
    
# If we really wanted to allocate that much memory on a system, having it quickly fail as above actually would be the better option.  In reality, running out of memory may dramatically slow systems down, up to the point that they become totally unresponsive – and restarting is the only option.
# 
# ### HeartBleed
# 
# One might argue that these are all problems of bad programming, or of bad programming languages.  But then, there's thousands of people starting to program every day, and all of them make the same mistakes again and again, even today.  
# 
# The somewhat better news is that fuzzing can easily detect such mistakes.  Here's a non-comprehensive list of bugs found through Miller's fuzzing approach:
# 
# 
# \todo{expand}
# 
# ## A Fuzzing Architecture
# 
# Since we'd like to reuse some parts of this chapter in the following ones, let us define things in a way that are easier to reuse, and in particular easier to _extend_.  To this end, we introduce a number of _classes_ that encapsulate the functionality above in a reusable way. 
# 
# ### Runner
# 
# The first thing we introduce is the notion of a `Runner` – that is, an object whose job it is to execute some object with a given input.  A runner typically is some program or function under test, but we can also have simpler runners.
# 
# Let us start with a base class for runners.  A runner essentially provides a method `run(input)` that is used to pass `input` (a string) to the runner.  `run()` returns a result; by default, this is the input.
# 
class Runner(object):
    def __init__(self):
        """Initialize"""
        pass
    
    def run(self, inp):
        """Run the consumer with the given input"""
        return inp

# A more interesting class is `PrintRunner`, which simply prints out everything that is given to it.  This is the default runner in many situations.
# 
class PrintRunner(Runner):
    def run(self, inp):
        """Print the given input"""
        print(inp)
        return inp

if __name__ == "__main__":
    p = PrintRunner()
    result = p.run("Some input")
    
if __name__ == "__main__":
    result
    
# The `ProgramRunner` class sends the input to the standard input of a program instead.  The program is specified when creating a `ProgramRunner` object.
# 
class ProgramRunner(Runner):
    def __init__(self, program):
        """Initialize.  `program` is a program spec as passed to `subprocess.run()`"""
        self.program = program

    def run(self, inp):
        """Run the program with `inp` as input.  Return result of `subprocess.run()`."""
        self.result = subprocess.run(self.program,
                        input=inp,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True)
        return self.result

# Let us demonstrate a `ProgramRunner` using the `cat` program – a program that copies its input to its output.
# We see that the output of `cat` is the same as its input:
# 
if __name__ == "__main__":
    cat = ProgramRunner(program="cat")
    cat.run("hello")
    
# ### Fuzzers
# 
# Let us now define _fuzzers_ that actually feed data into a consumer.  The base class for fuzzers provides one central method `fuzz()` that creates some input.  The `run()` function then sends the fuzz() input to a consumer, returning the result; `runs()` does this for a given number (`trials`) of times.
# 
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
        return [runner.run(self.fuzz()) for i in range(trials)]

# By default, `Fuzzer` objects do not do much, as their `fuzz()` function is merley an abstract placeholder.  The subclass `RandomFuzzer`, however, implements the functionality of the `fuzzer()` function, above, adding an additional parameter `min_length` to specify a minimum length.
# 
class RandomFuzzer(Fuzzer):
    def __init__(self, min_length=10, max_length=100, char_start=32, char_range=32):
        self.min_length = min_length
        self.max_length = max_length
        self.char_start = char_start
        self.char_range = char_range

    def fuzz(self):
        """A string of `min_length` to `max_length` characters 
           in the range [`char_start`, `char_start` + `char_range`]"""
        string_length = random.randrange(self.min_length, self.max_length + 1)
        out = ""
        for i in range(0, string_length):
            out += chr(random.randrange(self.char_start, self.char_start + self.char_range))
        return out

# With `RandomFuzzer`, we can now create a fuzzer whose configuration needs to be specified only once when creating the fuzzer.
# 
if __name__ == "__main__":
    random_fuzzer = RandomFuzzer(min_length=20, max_length=20)
    for i in range(10):
        print(random_fuzzer.fuzz())
    
# We can now send such generated inputs to our previously defined `cat` runner, verifying that `cat` actually does copy its (fuzzed) input to its output.
# 
if __name__ == "__main__":
    for i in range(10):
        inp = random_fuzzer.fuzz()
        assert cat.run(inp).stdout == inp
    
# Combining a `Fuzzer` with a `Runner`, however, is so common that we can use the `run()` method supplied by the `Fuzzer` class for this purpose:
# 
if __name__ == "__main__":
    random_fuzzer.run(cat)
    
# With `runs()`, we can repeat a fuzzing run a number of times, obtaining a list of results.
# 
if __name__ == "__main__":
    random_fuzzer.runs(cat, 10)
    
# With this, we have all in place to create fuzzers – starting with the simple random fuzzers introduced in this chapter, but even far more advanced ones.  Stay tuned!
# 
# ## Lessons Learned
# 
# * Randomly generating inputs ("fuzzing") is a simple, cost-effective way to quickly test arbitrary programs for their robustness.
# * Bugs fuzzers find are mainly due to errors and deficiencies in input processing.
# 
# ## Next Steps
# 
# From here, you can explore how to
# 
# * [use _mutations_ on existing inputs to get more valid inputs](MutationFuzzer.ipynb)
# * [use _grammars_ (i.e., a specification of the input format) to get even more valid inputs](Grammars.ipynb)
# * [reduce _failing inputs_ for efficient debugging](Reducing.ipynb)
# 
# Enjoy the read!
# 
# ## Exercises
# 
