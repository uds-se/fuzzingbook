
# coding: utf-8

# # Fuzzing: Breaking Things with Random Inputs
# 
# In this chapter, we'll start with one of the simplest test generation techniques.  The key idea of random text generation, also known as "fuzzing", is to feed a _string of random characters_ into a program in the hope to uncover failures.

# **Prerequisites**
# 
# * You should know fundamentals of software testing; for instance, from the chapter ["Introduction to Software Testing"](Intro_Testing.ipynb).

# ## A Testing Assignment
# 
# Fuzzing was conceived by Bart Miller in 1989 as a programming exercise for his students at the University of Wisconsin-Madison.  The [assignment](http://pages.cs.wisc.edu/~bart/fuzz/CS736-Projects-f1988.pdf) read 
# 
# > The goal of this project is to evaluate the robustness of various UNIX utility programs, given an unpredictable input stream. [...] First, you will build a _fuzz generator_. This is a program that will output a random character stream. Second, you will take the fuzz generator and use it to attack as many UNIX utilities as possible, with the goal of trying to break them.
# 
# This assignment captures the essence of fuzzing: _Create random inputs, and see if they break things._  Just let it run long enough and you'll see.

# ## A Simple Fuzzer
# 
# Let us try to fulfill this assignment and build a fuzz generator.  The idea is to produce random characters, adding them to a buffer string variable (`out`), and finally returning the string.

# This implementation uses the following Python features and functions:
# 
# * `random.randrange(start, end)` – return a random number [`start`, `end`]
# * `range(start, end)` – create a list with integers from `start` to `end`.  Typically used in iterations.
# * `for elem in list: body` – execute `body` in a loop with `elem` taking each value from `list`.
# * `for i in range(start, end): body` – execute `body` in a loop with `i` from `start` to `end` - 1.
# * `chr(n)` – return a character with ASCII code `n`

# First, we'll import a standard package required for working in notebooks.

# In[1]:


# import fuzzingbook_utils # only in notebook


# Next, we'll need random numbers.

# In[2]:


import random


# Here comes the actual `fuzzer()` function.

# In[3]:


# We set a specific seed to get the same inputs each time
random.seed(53727895348829)


# In[4]:


def fuzzer(max_length=100, char_start=32, char_range=32):
    """A string of up to `max_length` characters 
       in the range [`char_start`, `char_start` + `char_range`]"""
    string_length = random.randrange(0, max_length)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out


# With its default arguments, the `fuzzer()` function returns a string of random characters:

# In[5]:


fuzzer()


# Now imagine that this string were the input to a program expecting a specific input format – say, a comma-separated list of values, or an e-mail address.  Would the program be able to process such an input without any problems?

# ## Fuzzing Alphabets
# 
# If the above fuzzing input already is intriguing, consider that fuzzing can easily be set up to produce other kinds of input.  For instance, we can also have `fuzzer()` produce a series of upercase letters.  We use `ord(c)` to return the ASCII code of the character `c`.

# In[6]:


fuzzer(1000, ord('a'), 26)


# Assume a program expects an identifier as its input.  Would it expect such a long identifier?

# ## Fuzzing External Programs
# 
# Let us see what happens if we actually invoke an external program with fuzzed inputs.  To this end, let us proceed in two steps.  First, we create an _input file_ with fuzzed test data; then we feed this input file into a program of choice.

# ### Creating Input Files
# 
# The Python `open()` function opens a file into which we can then write arbitrary contents.  It is commonly used in conjunction with the `with` statement, which ensures that the file is closed as soon as it is no longer needed.

# In[7]:


FILE = "input.txt"
data = fuzzer()
with open(FILE, "w") as f:
    f.write(data)


# We can verify that the file was actually created by reading its contents:

# In[8]:


contents = open(FILE).read()
print(contents)
assert(contents == data)


# ### Invoking External Programs
# 
# Now that we have an input file, we can invoke a program on it.  For the fun of it, let us test the `bc` calculator program, which takes an arithmetic expression and evaluates it.
# 
# To invoke `bc`, let us use the Python `subprocess` module.  This is how this works:
# 

# In[9]:


import os
import subprocess


# In[10]:


program = "bc"
with open("input.txt", "w") as f:
    f.write("2 + 2\n")
result = subprocess.run([program, "input.txt"],
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True)


# From the `result`, we can check the program output, which in this case consists of a set of typesetting commands:

# In[11]:


result.stdout


# And we can check the status; a value of 0 indicates the program terminated correctly.

# In[12]:


result.returncode


# Any error messages would be available in `results.stderr`:

# In[13]:


result.stderr


# Instead of `bc`, you can actually put in any program you like.  Be aware, though, that if your program is able to change or even damage your system, there's quite a risk that the fuzzed input contains appropriate data or commands.  
# 
# Just for the fun of it, imagine you would test a file removal program.  What is the chance of the fuzzer producing a valid file name?  (Note that `.` and `/` may be  valid directory names already.)

# ### Long-Running Fuzzing
# 
# Let us now feed a large number of inputs into our tested program, to see whether it might crash on some.  We store all results in the `runs` variable as pairs of input data and the actual result. (Note: running this may take a while.)

# In[14]:


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

# In[15]:


sum(1 for (data, result) in runs if result.stderr == "")


# Most inputs apparently are invalid – not a big surprise, as it is unlikely that a random input contains a valid arithmetic expression.  Let us take a look at the first error message: 

# In[16]:


errors = [(data, result) for (data, result) in runs if result.stderr != ""]
(first_data, first_result) = errors[0]

print(repr(first_data))
print(first_result.stderr)


# Are there any runs with messages other than `illegal character` or `parse error`?  (Say, something like `crash` or `you found a fatal bug`?)  Not very many:

# In[17]:


[result.stderr for (data, result) in runs if 
 result.stderr != "" 
 and "illegal character" not in result.stderr
 and "parse error" not in result.stderr]


# Maybe a crash would be indicated by `bc` just crashing.  Unfortunately, the return code is never nonzero:

# In[18]:


sum(1 for (data, result) in runs if result.returncode != 0)


# How about we let the above `bc` test run for some more?  While it is running, let us take a look on how the state of the art was in 1989.

# ## Bugs Fuzzers Find
# 
# When Miller and his students ran their first fuzzers in 1989, they found an alarming result: About **a third of the UNIX utilities** they fuzzed had issues – they crashed, hung, or otherwise failed when confronted with fuzzing input \cite{Miller1990}.  This also included the `bc` program, above.  (Apparently, the bugs have now been fixed!)
# 
# Considering that many of these UNIX utilities were used in scripts that would also process network input, this was an alarming result.  Programmers quickly built and ran their own fuzzers, rushed to fix the reported errors, and learned not to trust external inputs anymore.

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

# We can easily simulate this behavior in a Python function:

# In[19]:


def crash_if_too_long(s):
    buffer = "Thursday"
    if len(s) > len(buffer):
        raise ValueError


# And yes, it quickly crashes.

# In[20]:


from ExpectError import ExpectError


# In[26]:


trials = 100
with ExpectError():
    for i in range(trials):
        s = fuzzer()
        crash_if_too_long(s)


# The `with ExpectError()` line in the above code ensures that the error message is printed, yet execution continues; this is to differentiate this "expected" error from "unexpected" errors in other code examples.

# ### Missing Error Checks
# 
# Many programming languages do not have exceptions, but instead have functions return special **error codes** in exceptional circumstances.  The C function `getchar()`, for instance, normally returns a character from the standard input; if no input is available anymore, it returns the special value `EOF` (end of file).  Now assume a programmer is scanning the input for the next character, skipping space characters:
# ```c
# char read_next_nonspace() {
#     char lastc;
# 
#     do {
#         lastc = getchar();
#     } while (lastc != ’ ’);
# 
#     return (lastc);
# }
# ```
# What happens if the input ends prematurely, as would perfectly be feasible with fuzzing?  Well, `getchar()` returns `EOF`, and keeps on returning `EOF` when called again; so the code above simply enters an infinite loop.

# Again, we can simulate this behavior.  Here's a function that will effectively hang if no space is present in the input:

# In[21]:


def hang_if_no_space(s):
    i = 0
    while True:
        if i < len(s):
            if s[i] == ' ':
                break
        i += 1


# Using the timeout mechanism from our [Introduction to Testing](Intro_Testing.ipynb), we can interrupt this function after some time.  And yes, it does hang after a few fuzzing inputs.

# In[22]:


from ExpectError import ExpectTimeout


# In[22]:


trials = 100
with ExpectTimeout(2):
    for i in range(trials):
        s = fuzzer()
        hang_if_no_space(s)


# The `with ExpectTimeout()` line in the above code ensures that execution of the enclosed code is interrupted after two seconds, printing the error message.

# 
# ### Rogue Numbers
# 
# With fuzzing, it is easy to generate **uncommon value** in the input, causing all kinds of interesting behavior.  Consider the following code, again in the C language, which first reads a buffer size from the input, and then allocates a buffer of the given size:
# ```c
# char *read_input() {
#     int size = read_buffer_size();
#     char *buffer = (char *)malloc(size);
#     // fill buffer
#     return (buffer);
# }
# ```
# What happens if `size` is very large, exceeding program memory?  What happens if `size` is less then the number of characters following?  What happens if `size` is negative?  By providing a random number here, fuzzing can create all kinds of damages.
# 

# Again, we can easily simulate this in Python.  The function `collapse_if_too_large()` fails if the passed value (a string) is too large after having been converted to an integer.

# In[23]:


def collapse_if_too_large(s):
    if int(s) > 1000:
        raise ValueError


# We can have `fuzzer()` create a string of digits:

# In[24]:


long_number = fuzzer(100, ord('0'), 10)
print(long_number)


# If we feed such numbers into `collapse_if_too_large()`, it will very soon fail.

# In[25]:


with ExpectError():
    collapse_if_too_large(long_number)


# If we really wanted to allocate that much memory on a system, having it quickly fail as above actually would be the better option.  In reality, running out of memory may dramatically slow systems down, up to the point that they become totally unresponsive – and restarting is the only option.

# ## Some Famous Bugs
# 
# One might argue that these are all problems of bad programming, or of bad programming languages.  But then, there's thousands of people starting to program every day, and all of them make the same mistakes again and again, even today.  
# 
# The somewhat better news is that fuzzing can easily detect such mistakes.  Here's a non-comprehensive list of bugs found through Miller's fuzzing approach:

# 
# ### HeartBleed
# 
# 
# \todo{expand}

# ## Lessons Learned
# 
# * Randomly generating inputs ("fuzzing") is a simple, cost-effective way to quickly test arbitrary programs for their robustness.
# * Bugs fuzzers find are mainly due to errors and deficiencies in input processing.

# ## Next Steps
# 
# From here, you can explore how to
# 
# * [use _mutations_ on existing inputs to get more valid inputs](Mutation_Fuzzing.ipynb)
# * [use _grammars_ (i.e., a specification of the input format) to get even more valid inputs](Grammars.ipynb)
# * [reduce _failing inputs_ for efficient debugging](Reducing.ipynb)
# 
# Enjoy the read!

# ## Exercises
