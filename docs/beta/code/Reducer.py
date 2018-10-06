#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Reducer.html
# Last change: 2018-10-06 17:41:02+02:00
#
#
# Copyright (c) 2018 Saarland University, CISPA, authors, and contributors
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


# # Reducing Failure-Inducing Inputs

if __name__ == "__main__":
    print('# Reducing Failure-Inducing Inputs')




# ## Why Reducing?

if __name__ == "__main__":
    print('\n## Why Reducing?')




# import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from Fuzzer import Runner
else:
    from .Fuzzer import Runner


# ## Text-Based Input Reduction

if __name__ == "__main__":
    print('\n## Text-Based Input Reduction')




class Reducer(object):
    def __init__(self, runner, log=False):
        """Attach reducer to the given `runner`"""
        self.runner = runner
        self.log = log
        self.reset()

    def reset(self):
        self.tests = 0
        
    def test(self, inp):
        result, outcome = self.runner.run(inp)
        self.tests += 1
        if self.log:
            print("Test #%d" % self.tests, repr(inp), repr(len(inp)), outcome)
        return outcome

    def reduce(self, inp):
        self.reset()
        # Default: Don't reduce
        return inp

class DeltaDebuggingReducer(Reducer):
    def reduce(self, inp):
        self.reset()
        assert self.test(inp) == Runner.FAIL
        
        n = 2     # Initial granularity
        while len(inp) >= 2:
            start = 0
            subset_length = len(inp) // n   # Integer Division
            some_complement_is_failing = False

            while start < len(inp):
                complement = inp[:start] + inp[start + subset_length:]

                if self.test(complement) == Runner.FAIL:
                    inp = complement
                    n = max(n - 1, 2)
                    some_complement_is_failing = True
                    break

                start += subset_length

            if not some_complement_is_failing:
                if n == len(inp):
                    break
                n = min(n * 2, len(inp))

        return inp

class ParenRunner(Runner):
    def run(self, inp):
        if '(' in inp and ')' in inp:
            return (inp, self.FAIL)
        else:
            return (inp, self.PASS)

if __name__ == "__main__":
    paren_runner = ParenRunner()
    dd_reducer = DeltaDebuggingReducer(paren_runner, log=True)
    dd_reducer.reduce('foo(2 + 24)')


# ## Grammar-Based Input Reduction

if __name__ == "__main__":
    print('\n## Grammar-Based Input Reduction')




class GrammarReducer(Reducer):
    pass

# ## _Section 4_

if __name__ == "__main__":
    print('\n## _Section 4_')




# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1: _Title_

if __name__ == "__main__":
    print('\n### Exercise 1: _Title_')




if __name__ == "__main__":
    # Some code that is part of the exercise
    pass


if __name__ == "__main__":
    # Some code for the solution
    2 + 2


# ### Exercise 2: _Title_

if __name__ == "__main__":
    print('\n### Exercise 2: _Title_')



