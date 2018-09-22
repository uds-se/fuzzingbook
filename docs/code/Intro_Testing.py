#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is part of "Generating Software Tests"
# (https://www.fuzzingbook.org/)
# It is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License,
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)


# # Introduction to Software Testing
# 
# Before we get to the central parts of the book, let us introduce essential concepts of software testing.  Why is it necessary to test software at all?  How does one test software?  How can one tell whether a test has been successful?  How does one know if one has tested enough?  In this unit, let us recall the most important concepts, and at the same time get acquainted with Python and interactive notebooks.

# ## Simple Testing
# 
# Let's start with a simple example.  Your co-worker has been asked to implement a square root function $\sqrt{x}$.  (Let's assume for a moment that the environment does  not already have one.)  After studying [Newton's method](https://en.wikipedia.org/wiki/Newton%27s_method), she comes up with the following Python code, claiming that, in fact, this `my_sqrt()` function computes square roots.

def my_sqrt(x):
    """Computes the square root of x, using Newton's method"""
    approx = None
    guess = x / 2
    while approx != guess:
        approx = guess
        guess = (approx + x / approx) / 2
    return approx

# Your job is now to find out whether this function actually does what it claims to do.

# If you're new to Python, you might first have to understand what the above code does.  We very much recommend the [Python tutorial](https://docs.python.org/3/tutorial/) to get an idea on how Python works.  The most important things for you to understand the above code are these three:
# 
# 1. Python structures programs through _indentation_, so the function and `while` bodies are defined by being indented;
# 2. Python is _dynamically typed_, meaning that the type of variables like `x`, `approx`, or `guess` is determined at run-time.
# 3. Most of Python's syntactic features are inspired by other common languages, such as control structures (`while`, `if`), assignments (`=`), or comparisons (`==`, `!=`, `<`).
# 
# With that, you can already understand what the above code does: Starting with a `guess` of `x / 2`, it computes better and better approximations in `approx` until the value of `approx` no longer changes.  This is the vaue that finally is returned.

# To find our whether `my_sqrt()` works correctly, we can _test_ it with a few values.  For `x = 4`, for instance, it produces the correct value:

if __name__ == "__main__":
    my_sqrt(4)


# The upper part above `my_sqrt(4)` (a so-called _cell_) is an input to the Python interpreter, which by default _evaluates_ it.  The lower part (`2.0`) is its output.  We can see that `my_sqrt(4)` produces the correct value.

# The same holds for `x = 2.0`, apparently, too:

if __name__ == "__main__":
    my_sqrt(2)


# If you are reading this in the interactive notebook, you can try out `my_sqrt()` with other values as well.  Click on one of the above cells with invocations of `my_sqrt()` and change the value – say, to `my_sqrt(1)`.  Press Shift+Enter (or click on the play symbol) to execute it and see the result.  If you get an error message, go to the above cell with the definition of `my_sqrt()` and execute this first.  You can also run _all_ cells at once; see the Notebook menu for details.  (You can actually also change the text by cicking on it, and corect mistaks such as in this sentence.)

# Is the above value of `my_sqrt(2)` actually correct?  We can easily verify by exploiting that $\sqrt{x}$ squared again has to be $x$, or in other words $\sqrt{x} \times \sqrt{x} = x$.  Let's take a look:

if __name__ == "__main__":
    my_sqrt(2) * my_sqrt(2)


# Okay, we do have some rounding error, but otherwise, this seems just fine.

# What we have done now is that we have _tested_ the above program: We have _executed_ it on a given input and _checked_ its result whether it is correct or not.  Such a test is the bare minimum of quality assurance before a program goes into production.

# ## Automating Test Execution
# 
# So far, we have tested the above program _manually_, that is, running it by hand and checking its results by hand.  This is a very flexible way of testing, but in the long run, it is rather inefficient:
# 
# 1. Manually, you can only check a very limited number of executions and their results
# 2. After any change to the program, you have to repeat the testing process
# 
# This is why it is very useful to _automate_ tests.  One simple way of doing so is to let the computer first do the computation, and then have it check the results.

# For instance, this piece of code automatically tests whether $\sqrt{4} = 2$ holds:

if __name__ == "__main__":
    result = my_sqrt(4)
    expected_result = 2.0
    if result == expected_result:
        print("Test passed")
    else:
        print("Test failed")


# The nice thing about this test is that we can run it again and again, thus ensuring that at least the square root of 4 is computed correctly.  But there are still a number of issues, though:
# 
# 1. We need _five lines of code_ for a single test
# 2. We do not care for rounding errors
# 3. We only check a single input (and a single result)
# 
# Let us address these issues one by one.  First, let's make the test a bit more compact.  Almost all programming languages do have a means to automatically check whether a condition holds, and stop execution if it does not.  This is called an _assertion_, and it is immensely useful for testing.

# In Python, the `assert` statement takes a condition, and if the condition is true, nothing happens.  (If everything works as it should, you should not be bothered.)  If the condition evaluates to false, though, `assert` raises an exception, indicating that a test just failed.
# 
# In our example, we can use `assert` to easily check whether `my_sqrt()` yields the expected result as above:

if __name__ == "__main__":
    assert my_sqrt(4) == 2


# As you execute this line of code, nothing happens: We just have shown (or asserted) that our implementation indeed produces $\sqrt{4} = 2$.

# Remember, though, that floating-point computations may induce rounding errors.  So we cannot simply compare two floating-point values with equality; rather, we would ensure that the difference between them stays below a certain threshold value, typically denoted as $\epsilon$ or ``epsilon``.  This is how we can do it:

EPSILON = 1e-8

def abs(x):
    if x < 0:
        return -x
    else:
        return x

if __name__ == "__main__":
    assert abs(my_sqrt(4) - 2 < EPSILON)


# We can also introduce a special function for this purpose, and now do more tests for concrete values:

def assertEquals(x, y, epsilon=1e-8):
    assert abs(x - y) < epsilon

if __name__ == "__main__":
    assertEquals(my_sqrt(4), 2)
    assertEquals(my_sqrt(9), 3)
    assertEquals(my_sqrt(100), 10)


# Seems to work, right?  If we know the expected results of a computation, we can use such assertions again and again to ensure our program works correctly.

# ## Generating Tests
# 
# Remember that the property $\sqrt{x} \times \sqrt{x} = x$ universally holds?  We can also explicitly test this with a few values:

if __name__ == "__main__":
    assertEquals(my_sqrt(2) * my_sqrt(2), 2)
    assertEquals(my_sqrt(3) * my_sqrt(3), 3)
    assertEquals(my_sqrt(42.11) * my_sqrt(42.11), 42.11)


# Still seems to work, right?  Most importantly, though, $\sqrt{x} \times \sqrt{x} = x$ is something we can very easily test for thousands of values:

if __name__ == "__main__":
    for n in range(1, 1000):
        assertEquals(my_sqrt(n) * my_sqrt(n), n)


# How much time does it take to test `my_sqrt()` with 100 values?  Let's see.

# We use our own `Timer` module to measure elapsed time.  To be able to use `Timer`, we first import our own utility module, which allows us to import other notebooks.

# import fuzzingbook_utils

from Timer import Timer

if __name__ == "__main__":
    with Timer() as t:
        for n in range(1, 100):
            assertEquals(my_sqrt(n) * my_sqrt(n), n)
    print(t.elapsed_time())


# 100 values take about a a hundredth of a second, so a single execution of `my_sqrt()` takes 1/10000 second, or about 100 microseconds.

# Let's repeat this with 10,000 values, and let's pick them at random.  The Python `random.random()` function returns a random value between 0.0 and 1.0:

import random

if __name__ == "__main__":
    with Timer() as t:
        for i in range(10000):
            x = 1 + random.random() * 1000000
            assertEquals(my_sqrt(x) * my_sqrt(x), x)
    print(t.elapsed_time())


# Within a second, we have now tested 10,000 random values, and each time, the square root was actually computed correctly.  We can repeat this test with every single change to `my_sqrt()`, each time reinforcing our confidence that `my_sqrt()` works as it should.  Note, though, that while a random function is _unbiased_ in producing random values, it is unlikely to generate special values that drastically alter program behavior.  We will discuss this later below.

# ## Run-Time Verification
# 
# Instead of writing and running tests for `my_aqrt()`, we can also go and _integrate the check right into the implementation._  This way, _each and every_ invocation of `my_sqrt()` will be automatically checked.

# Such an _automatic run-time check_ is very easy to implement:

def my_sqrt_checked(x):
    root = my_sqrt(x)
    assertEquals(root * root, x)
    return root

# Now, whenever we compute a root with `my_sqrt_checked()`$\dots$

if __name__ == "__main__":
    my_sqrt_checked(2.0)


# we already know that the result is correct, and will so for every new successful computation.

# Automatic run-time checks, as above, assume two things, though:
# 
# * One has to be able to _formulate_ such run-time checks.  Having concrete values to check against should always be possible, but formulating desired properties in an abstract fashion can be very complex.  In practice, you need to decide which properties are most crucial, and design appropriate checks for them.  Plus, run-time checks may depend not only on local properties, but on several properties of the program state, whcih all have to be identified.
# 
# * One has to be able to _afford_ such run-time checks.  In the case of `my_sqrt()`, the check is not very expensive; but if we have to check, say, a large data structure even after a simple operation, the cost of the check may soon be prohibitive.  In practice, run-time checks will typically be disabled during production, trading reliability for efficiency.  On the other hand, a comprehensive suite of run-time checks is a great way to find errors and quickly debug them; you need to decide how many such capabilities you would still want during production.

# ## System Input vs Function Input

# At this point, we may make `my_sqrt()` available to other programmers, who may then embed it in their code.  At some point, it will have to process input that comes from _third parties_, i.e. is not under control by the programmer.  Let us simulate this _system input_ by assuming a function `exposed_sqrt()` whose input is a string under third-party control:

def exposed_sqrt(s):
    x = int(s)
    print('The root of', x, 'is', my_sqrt(x))

# We can easily invoke `exposed_sqrt()` with some system input:

if __name__ == "__main__":
    exposed_sqrt("4")


# What's the problem?  Well, the problem is that we do not check external inputs for validity.  Try invoking `exposed_sqrt(-1)`, for instance.  What happens?

# Indeed, if you invoke `my_sqrt()` with a negative number, it enters an infinite loop.  For technical reasons, we cannot have infinite loops in this chapter (unless we'd want the code to run forever); so we use a special `with ExpectTimeOut(1)` construct to interrupt execution after one second.

from ExpectError import ExpectTimeout

if __name__ == "__main__":
    with ExpectTimeout(1):
        x = -1
        print('The root of', x, 'is', my_sqrt(x))


# The above message is an _error message_, indicating that something went wrong.  It lists the _call stack_ of functions and lines that were active at the time of the error.  The line at the very bottom is the line last executed; the lines above represent function invocations – in our case, up to `my_sqrt(x)`.
# 
# We don't want our code terminating with an exception.  Consequently, when accepting external input, we must ensure that it is properly validated.  We may write, for instance:

def exposed_sqrt(s):
    x = int(s)
    if x < 0:
        print("Illegal Input")
    else:
        print('The root of', x, 'is', my_sqrt(x))


# and then we can be sure that `my_sqrt()` is only invoked according to its specification.

if __name__ == "__main__":
    exposed_sqrt("-1")


# But wait!  What happens if `exposed_sqrt()` is not invoked with a number?  Then we would try to convert a non-number string, which would also result in a runtime error:

from ExpectError import ExpectError

if __name__ == "__main__":
    with ExpectError():
        exposed_sqrt("xyzzy")


# Here's a version which also checks for bad inputs:

def exposed_sqrt(s):
    try:
        x = int(s)
    except ValueError:
        print("Illegal Input")
    else:
        if x < 0:
            print("Illegal Number")
        else:
            print('The root of', x, 'is', my_sqrt(x))

if __name__ == "__main__":
    exposed_sqrt("4")


if __name__ == "__main__":
    exposed_sqrt("-1")


if __name__ == "__main__":
    exposed_sqrt("xyzzy")


# We have now seen that at the system level, the program must be able to handle any kind of input gracefully without ever entering an uncontrolled state.  This, of course, is a burden for programmers, who must struggle to make their programs robust for all circumstances.  This burden, however, becomes a _benefit_ when generating software tests: If a program can handle any kind of input (possibly with well-defined error messages), we can also _send it any kind of input_.  When calling a function with generated values, though, we have to _know_ its precise preconditions.

# ## The Limits of Testing
# 
# Despite best efforts in testing, keep in mind that you are always checking functionality for a _finite_ set of inputs.  Thus, there may always be _untested_ inputs for which the function may still fail.

# In the case of `my_sqrt()`, for instance, computing $\sqrt{0}$ results in a division by zero:

if __name__ == "__main__":
    with ExpectError():
        root = my_sqrt(0)


# In our tests so far, we have not checked this condition, meaning that a program which builds on $\sqrt{0} = 0$ will surprisingly fail.  But even if we had set up our random generator to produce inputs in the range of 0–1000000 rather than 1–1000000, the chances of it producing a zero value by chance would still have been one in a million.  If the behavior of a function is radically different for few individual values, plain random testign has few chances to produce these.

# We can, of course, fix the function accordingly, documenting the accepted values for `x` and handling the special case `x = 0`:

def my_sqrt_fixed(x):
    assert 0 <= x
    if x == 0:
        return 0
    return my_sqrt(x)

# With this, we can now correctly compute $\sqrt{0} = 0$:

if __name__ == "__main__":
    assert my_sqrt_fixed(0) == 0


# Illegal values now result in an exception:
# 

if __name__ == "__main__":
    with ExpectError():
        root = my_sqrt_fixed(-1)


# Still, we have to remember that while extensive testing may give us a high confidence into the correctness of a program, it does not provide a guarantee that all future executions will be correct.  Even run-time verification, which checks every result, can only guarantee that _if_ it produces a result, the result will be correct; but there is no guarantee that future executions may not lead to a failing check.  As I am writing this, I _believe_ that `my_sqrt_fixed(x)` is a correct implementation of $\sqrt{x}$, but I cannot be 100% certain.

# With Newton's method, we may still have a good chance of actually _proving_ that the implementation is correct: The implementation is simple, the math is well-understood.  Alas, this is only the case for few domains.  If we do not want to go into full-fledged correctness proofs, our best chance with testing is to 
# 
# 1. Test the program on several, well-chosen inputs; and
# 2. Check results extensively and automatically.
# 
# This is what we do in the remainder of this course: Devise techniques that help us to thoroughly test a program, as well as techniques that help us checking its state for correctness.  Enjoy!

# ## Lessons Learned
# 
# * The aim of testing is to execute a program such that we find bugs.
# * Test execution, test generation, and checking test results can be automated.
# * Testing is _incomplete_; it provides no 100% guarantee that the code is free of errors.

# ## Next Steps
# 
# From here, you can move on how to
# 
# * [use _fuzzing_ to test programs with random inputs](Fuzzer.ipynb)
# 
# Enjoy the read!

# ## Exercises

# ### Exercise 1: Testing Shellsort
# 
# Consider the following implementation of a [Shellsort](https://en.wikipedia.org/wiki/Shellsort) function, taking a list of elements and (presumably) sorting it.

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

# A first test indicates that `shellsort()` might actually work:

if __name__ == "__main__":
    shellsort([3, 2, 1])


# The implementation uses a _list_ as argument `elems` (which it copies into `sorted_elems`) as well as for the fixed list `gaps`.  Lists work like _arrays_ in other languages:

if __name__ == "__main__":
    a = [5, 6, 99, 7]
    print("First element:", a[0], "length:", len(a))


# The `range()` function returns an iterable list of elements.  It is often used in conjunction with `for` loops, as in the above implementation.

if __name__ == "__main__":
    for x in range(1, 5):
        print(x)


# #### Part 1: Manual Test Cases

# Your job is now to thoroughly test `shellsort()` with a variety of inputs.

# First, set up `assert` statements with a number of manually written test cases.  Select your test cases such that extreme cases are covered.  Use `==` to compare two lists.

# **Solution.** Here's a few selected test cases:

if __name__ == "__main__":
    # Standard lists
    assert shellsort([3, 2, 1]) == [1, 2, 3]
    assert shellsort([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert shellsort([6, 5]) == [5, 6]


if __name__ == "__main__":
    # Check for duplicates
    assert shellsort([2, 2, 1]) == [1, 2, 2]


if __name__ == "__main__":
    # Empty list
    assert shellsort([]) == []


# #### Part 2: Random Inputs

# Second, create random lists as arguments to `shellsort()`.   Make use of the following helper predicates to check whether the result is (a) sorted, and (b) a permutation of the original.

def is_sorted(elems):
    return all(elems[i] <= elems[i + 1] for i in range(len(elems) - 1))

if __name__ == "__main__":
    is_sorted([3, 5, 9])


def is_permutation(a, b):
    return all(a.count(elem) == b.count(elem) for elem in a)

if __name__ == "__main__":
    is_permutation([3, 2, 1], [1, 3, 2])


# Start with a random list generator, using `[]` as the empty list and `elems.append(x)` to append an element `x` to the list `elems`.  Use the above helper functions to assess the results.  Generate and test 1,000 lists.

# **Solution.** Here's a simple random list generator:

def random_list():
    length = random.randint(1, 10)
    elems = []
    for i in range(length):
        elems.append(random.randint(0, 100))
    return elems

if __name__ == "__main__":
    random_list()


if __name__ == "__main__":
    elems = random_list()
    print(elems)


if __name__ == "__main__":
    sorted_elems = shellsort(elems)
    print(sorted_elems)


if __name__ == "__main__":
    assert is_sorted(sorted_elems) and is_permutation(sorted_elems, elems)


# Here's the test for 1,000 lists:

if __name__ == "__main__":
    for i in range(1000):
        elems = random_list()
        sorted_elems = shellsort(elems)
        assert is_sorted(sorted_elems) and is_permutation(sorted_elems, elems)


# ### Exercise 2: Quadratic Solver

# Given an equation $ax^2 + bx + c = 0$, we want to find solutions for $x$ given the values of $a$, $b$, and $c$.  The following code is supposed to do this, using the equation $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

def quadratic_solver(a, b, c):
    q = b * b - 4 * a * c
    solution_1 = (-b + my_sqrt_fixed(q)) / (2 * a)
    solution_2 = (-b - my_sqrt_fixed(q)) / (2 * a)
    return (solution_1, solution_2)

if __name__ == "__main__":
    quadratic_solver(3, 4, 1)


# The above implementation is incomplete, though.  You can trigger 
# 
# 1. a division by zero; and
# 2. violate the precondition of `my_sqrt_fixed()`.
# 
# How does one do that, and how can one prevent this?

# #### Part 1: Find bug-triggering inputs
# 
# For each of the two cases above, identify values for `a`, `b`, `c` that trigger the bug.

# **Solution**.  Here are two inputs that trigger the bugs:

if __name__ == "__main__":
    with ExpectError():
        print(quadratic_solver(3, 2, 1))


if __name__ == "__main__":
    with ExpectError():
        print(quadratic_solver(0, 0, 1))


# #### Part 2: Fix the problem
# 
# Extend the code appropriately such that the cases are handled.  Return `None` for nonexistent values.

# **Solution.** Here is an approriate extension of `quadratic_solver()` that takes care of all the corner cases:

def quadratic_solver_fixed(a, b, c):
    if a == 0:
        if b == 0:
            return (-c, None)
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


if __name__ == "__main__":
    with ExpectError():
        print(quadratic_solver_fixed(3, 2, 1))


if __name__ == "__main__":
    with ExpectError():
        print(quadratic_solver_fixed(0, 0, 1))


# #### Part 3: Odds and Ends
# 
# What are the chances of discovering these conditions with random inputs?  Assuming one can do a billion tests per second, how long would one have to wait on average until a bug gets triggered?

# **Solution.**  Consider the code above.  If we choose the full range of 32-bit integers for `a`, `b`, and `c`, then the first condition alone, both `a` and `b` being zero, has a chance of $p = 1 / (2^{32} * 2^{32})$; that is, one in 18.4 quintillions:

if __name__ == "__main__":
    combinations = 2 ** 32 * 2 ** 32
    combinations


# If we can do a billion tests per second, how many years would we have to wait?

if __name__ == "__main__":
    tests_per_second = 1000000000
    seconds_per_year = 60 * 60 * 24 * 365.25
    tests_per_year = tests_per_second * seconds_per_year
    combinations / tests_per_year


# We see that on average, we'd have to wait for 584 years.  Clearly, pure random choices are not sufficient as sole testing strategy.
