
# coding: utf-8

# # Introduction to Software Testing
# 
# Before we get to the central parts of the book, let us introduce essential concepts of software testing.  Why is it necessary to test software at all?  How does one test software?  How can one tell whether a test has been successful?  How does one know if one has tested enough?  In this unit, let us recall the most important concepts.

# ## Simple Testing
# 
# Let's start with a simple example.  Your co-worker has been asked to implement a square root function.  (Let's assume for a moment that the environment does  not already have one.)  After studying _Newton's method_, she comes up with the following program, claiming that, in fact, this `my_sqrt()` function computes square roots:

# In[1]:


# import fuzzingbook_utils # only in notebook


# In[2]:


def my_sqrt(x):
    """Computes the square root of x, using Newton's method"""
    approx = None
    guess = x / 2
    while approx != guess:
        approx = guess
        guess = (approx + x / approx) / 2
    return approx


# Your job is now to find out whether this function actually does what it claims to do.  You can now _test_ the function with a few values.  For `x = 4`, for instance, it produces the correct value:

# In[3]:


my_sqrt(4)


# as it does for `x = 2.0`, apparently:

# In[4]:


my_sqrt(2)


# We can easily verify whether this value is correct by exploiting that $\sqrt{x}$ squared again has to be $x$, or in other words $\sqrt{x} \times \sqrt{x} = x$.  Let's take a look:

# In[5]:


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
# This is why it is very useful to _automate_ tests.  One simple way of doing so is to let the computer first do the computation, and then have it check the results.  For instance, this piece of code automatically tests whether $\sqrt{4} = 2$ holds:

# In[6]:


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
# 
# In Python, the `assert` statement takes a condition, and if the condition is true, nothing happens.  (If everything works as it should, you should not be bothered.)  If the condition evaluates to false, though, `assert` raises an exception, indicating that a test just failed.
# 
# In our example, we can use `assert` to easily check whether `my_sqrt()` yields the expected result as above:

# In[7]:


assert my_sqrt(4) == 2


# As you execute this line of code, nothing happens: We just have shown (or asserted) that our implementation indeed produces $\sqrt{4} = 2$.

# Remember, though, that floating-point computations may induce rounding errors.  So we cannot simply compare two floating-point values with equality; rather, we would ensure that the difference between them stays below a certain threshold value, typiclly denoted as $\epsilon$ or ``epsilon``.  This is how we can do it:

# In[8]:


EPSILON = 1e-8


# In[9]:


def abs(x):
    if x < 0:
        return -x
    else:
        return x


# In[10]:


assert abs(my_sqrt(4) - 2 < EPSILON)


# We can also introduce a special function for this purpose, and now do more tests for concrete values:

# In[11]:


def assertEquals(x, y, epsilon=1e-8):
    assert abs(x - y) < epsilon


# In[12]:


assertEquals(my_sqrt(4), 2)
assertEquals(my_sqrt(9), 3)
assertEquals(my_sqrt(100), 10)


# Seems to work, right?  If we know the expected results of a computation, we can use such assertions again and again to ensure our program works correctly.

# ## Generating Tests
# 
# Remember that the property $\sqrt{x} \times \sqrt{x} = x$ universally holds?  We can also explicitly test this with a few values:

# In[13]:


assertEquals(my_sqrt(2) * my_sqrt(2), 2)
assertEquals(my_sqrt(3) * my_sqrt(3), 3)
assertEquals(my_sqrt(42.11) * my_sqrt(42.11), 42.11)


# Still seems to work, right?  Most importantly, though, $\sqrt{x} \times \sqrt{x} = x$ is something we can very easily test for thousands of values:

# In[14]:


for n in range(1, 1000):
    assertEquals(my_sqrt(n) * my_sqrt(n), n)


# How much time does it take to test `my_sqrt()` with 100 values?  Let's see:

# In[35]:


from Timer import Timer


# In[36]:


with Timer() as t:
    for n in range(1, 100):
        assertEquals(my_sqrt(n) * my_sqrt(n), n)
print(t.elapsed_time())


# 100 values take about a a hundredth of a second, so a single execution of `my_sqrt()` takes 1/10000 second, or about 100 microseconds.
# 
# Let's repeat this with 10,000 values, and let's pick them at random.  The Python `random.random()` function returns a random value between 0.0 and 1.0:

# In[37]:


import random
from Timer import Timer


# In[37]:


with Timer() as t:
    for i in range(10000):
        x = 1 + random.random() * 1000000
        assertEquals(my_sqrt(x) * my_sqrt(x), x)
print(t.elapsed_time())


# Within a second, we have now tested 10,000 random values, and each time, the square root was actually computed correctly.  We can repeat this test with every single change to `my_sqrt()`, each time reinforcing our confidence that `my_sqrt()` works as it should.

# ## Run-Time Verification
# 
# Instead of writing and running tests for `my_aqrt()`, we can also go and integrate the check right into the implementation.  This way, _each and every_ invocation of `my_sqrt()` will be automatically checked.  This is very easy to implement:

# In[38]:


def my_sqrt_checked(x):
    root = my_sqrt(x)
    assertEquals(root * root, x)
    return root


# Now, whenever we compute a root with `my_sqrt_checked()`$\dots$

# In[19]:


my_sqrt_checked(2.0)


# we already know that the result is correct, and will so for every new successful computation.
# 
# This, of course, assumes two things:
# 
# 1. One has to be able to _formulate_ such run-time checks.  Having concrete values to check against should always be possible, but formulating desired properties in an abstract fashion can be very complex.  In practice, you need to decide which properties are most crucial, and design appropriate checks for them.
# 
# 2. One has to be able to _afford_ such run-time checks.  In the case of `my_sqrt()`, the check is not very expensive; but if we have to check, say, a large data structure even after a simple operation, the cost of the check may soon be prohibitive.  On the other hand, a comprehensive suite of run-time checks is a great way to find errors and quickly debug them; you need to decide how many such capabilities you would still want during production.

# ## System Input vs Function Input

# At this point, we may make `my_sqrt()` available to other programmers, who may then embed it in their code.  At some point, it will have to process input that comes from _third parties_, i.e. is not under control by the programmer.  Let us simulate this _system input_ by assuming a function `exposed_sqrt()` whose input is a string under third-party control:

# In[20]:


def exposed_sqrt(s):
    x = int(s)
    print('The root of', x, 'is', my_sqrt(x))


# We can easily invoke `exposed_sqrt()` with some system input:

# In[21]:


exposed_sqrt("4")


# What's the problem?  Well, the problem is that we do not check external inputs for validity.  Try invoking `exposed_sqrt(-1)`, for instance.  What happens?

# Indeed, if you invoke `my_sqrt()` with a negative number, it enters an infinite loop.  For technical reasons, we cannot have infinite loops in this chapter (unless we'd want the code to run forever); so we use a special `with ExpectTimeOut(1)` construct to interrupt execution after one second.

# In[39]:


from ExpectError import ExpectTimeout


# In[40]:


with ExpectTimeout(1):
    x = -1
    print('The root of', x, 'is', my_sqrt(x))


# Consequently, when accepting external input, we must ensure that it is properly validated.  We may write, for instance:

# In[41]:


def exposed_sqrt(s):
    x = int(s)
    if x < 0:
        print("Illegal Input")
    else:        
        print('The root of', x, 'is', my_sqrt(x))


# and then we can be sure that `my_sqrt()` is only invoked according to its specification.

# In[42]:


exposed_sqrt("-1")


# But wait!  What happens if `exposed_sqrt()` is not invoked with a number?  Then we would try to convert a non-number string, which would also result in a runtime error:

# In[43]:


from ExpectError import ExpectError


# In[44]:


with ExpectError():
    exposed_sqrt("xyzzy")


# Here's a version which also checks for bad inputs:

# In[45]:


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


# In[46]:


exposed_sqrt("4")


# In[47]:


exposed_sqrt("-1")


# In[48]:


exposed_sqrt("xyzzy")


# We have now seen that at the system level, the program must be able to handle any kind of input gracefully without ever entering an uncontrolled state.  This, of course, is a burden for programmers, who must struggle to make their programs robust for all circumstances.  This burden, however, becomes a _benefit_ when generating software tests: If a program can handle any kind of input (possibly with well-defined error messages), we can also _send it any kind of input_.  When calling a function with generated values, though, we have to _know_ its precise preconditions.

# ## The Limits of Testing
# 
# Despite best efforts in testing, keep in mind that you are always checking functionality for a _finite_ set of inputs.  Thus, there may always be _untested_ inputs for which the function may still fail.  In the case of `my_sqrt()`, for instance, computing $\sqrt{0}$ results in a division by zero:

# In[49]:


with ExpectError():
    root = my_sqrt(0)


# In our tests so far, we have not checked this condition, meaning that a program which builds on $\sqrt{0} = 0$ will surprisingly fail.  We can, of course, fix the function accordingly, documenting the accepted values for `x` and handling the special case `x = 0`:

# In[50]:


def my_sqrt_fixed(x):
    assert 0 <= x
    if x == 0:
        return 0
    return my_sqrt(x)


# With this, we can now correctly compute $\sqrt{0} = 0$:

# In[51]:


assert my_sqrt_fixed(0) == 0


# Illegal values now result in an exception:
# 

# In[52]:


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
# * [use _fuzzing_ to test programs with random inputs](Basic_Fuzzing.ipynb)
# 
# Enjoy the read!

# ## Exercises
# 
# ### Shellsort
# 
# Consider the following implementation of a shellsort function.  \todo{Expand it}
# 
