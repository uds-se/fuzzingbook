
# coding: utf-8

# # Timer
# 
# The code in this notebook helps with measuring time.

# **Prerequisites**
# 
# * This notebook needs some understanding on advanced concepts in Python, notably 
#     * classes
#     * the Python `with` statement
#     * measuring time

# ## Measuring Time
# 
# The class `Timer` allows to measure the elapsed time during some code execution.  A typical usage looks as follows:
# 
# ```Python
# from Timer import Timer
# 
# with Timer() as t:
#     function_that_is_supposed_to_be_timed()
# 
# print(t.elapsed_time())
# ```
# 

# In[4]:


# import fuzzingbook_utils # only in notebook


# In[5]:


import time


# In[6]:


def clock():
    try:
        return time.perf_counter()  # Python 3
    except:
        return time.clock()         # Python 2


# In[7]:


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


# Here's an example:

# In[8]:


def some_long_running_function():
    i = 1000000
    while i > 0:
        i -= 1


# In[9]:


print("Stopping total time:")
with Timer() as t:
    some_long_running_function()
print(t.elapsed_time())


# In[11]:


print("Stopping time in between:")
with Timer() as t:
    for i in range(10):
        print(t.elapsed_time())


# That's it, folks – enjoy!
