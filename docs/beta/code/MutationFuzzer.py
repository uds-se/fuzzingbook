#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/MutationFuzzer.html
# Last change: 2018-09-25 14:25:13+02:00
#
# This material is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International License
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)


# # Mutation-Based Fuzzing
# 
# Most [randomly generated inputs](Fuzzer.ipynb) are syntactically _invalid_ and thus are quickly rejected by the processing program.  To exercise functionality beyond input processing, we must increase chances to obtain valid inputs.  One such way is by _mutating_ existing valid inputs – that is, introducing small changes that may still keep the input valid, yet exercise new behavior.  We show how to create such mutations, and how to guide them towards yet uncovered code, applying central concepts from the popular AFL fuzzer.

if __name__ == "__main__":
    print('# Mutation-Based Fuzzing')




# **Prerequisites**
# 
# * You should know how basic fuzzing works; for instance, from the ["Fuzzing"](Fuzzer.ipynb) chapter.

# ## Fuzzing a URL Parser
# 
# Many programs expect their inputs to come in a very specific format before they would actually process them.  As an example, think of a program that accepts a URL (a Web address).  The URL has to be in a valid format (i.e., the URL format) such that the program can deal with it.  When fuzzing with random inputs, what are our chances to actually produce a valid URL?

if __name__ == "__main__":
    print('\n## Fuzzing a URL Parser')




# To get deeper into the problem, let us explore what URLs are made of.  A URL consists of a number of elements:
# 
#     scheme://netloc/path?query#fragment
#     
# where
# * `scheme` is the protocol to be used, including `http`, `https`, `ftp`, `file`...
# * `netloc` is the name of the host to connect to, such as `www.google.com`
# * `path` is the path on that very host, such as `search`
# * `query` is a list of key/value pairs, such as `q=fuzzing`
# * `fragment` is a marker for a location in the retrieved document, such as `#result`

# In Python, we can use the `urlparse()` function to parse and decompose a URL into its parts.

# import fuzzingbook_utils

if __name__ == "__main__":
    try:
        from urlparse import urlparse      # Python 2
    except ImportError:
        from urllib.parse import urlparse  # Python 3

    urlparse("http://www.google.com/search?q=fuzzing")


# We see how the result encodes the individual parts of the URL in different attributes.

# Let us now assume we have a program that takes a URL as input.  To simplify things, we won't let it do very much; we simply have it check the passed URL for validity.  If the URL is valid, it returns True; otherwise, it raises an exception.

def http_program(url):
    supported_schemes = ["http", "https"]
    result = urlparse(url)
    if result.scheme not in supported_schemes:
        raise ValueError("Scheme must be one of " + repr(supported_schemes))
    if result.netloc == '':
        raise ValueError("Host must be non-empty")

    # Do something with the URL
    return True

# Let us now go and fuzz `http_program()`.  To fuzz, we use the full range of printable ASCII characters, such that `:`, `/`, and lowercase letters are included.

if __package__ is None or __package__ == "":
    from Fuzzer import fuzzer
else:
    from .Fuzzer import fuzzer


if __name__ == "__main__":
    fuzzer(char_start=32, char_range=96)


# Let's try to fuzz with 1000 random inputs and see whether we have some success.

if __name__ == "__main__":
    for i in range(1000):
        try:
            url = fuzzer()
            result = http_program(url)
            print("Success!")
        except ValueError:
            pass


# What are the chances of actually getting a valid URL?  We need our string to start with `"http://"` or `"https://"`.  Let's take the `"http://"` case first.  That's seven very specific characters we need to start with.  The chances of producing these seven characters randomly (with a character range of 96 different characters) is $1 : 96^7$, or

if __name__ == "__main__":
    96 ** 7


# The odds of producing a `"https://"` prefix are even worse, at $1 : 96^8$:

if __name__ == "__main__":
    96 ** 8


# which gives us a total chance of

if __name__ == "__main__":
    likelihood = 1 / (96 ** 7) + 1 / (96 ** 8)
    likelihood


# And this is the number of runs (on average) we'd need to produce a valid URL:

if __name__ == "__main__":
    1 / likelihood


# Let's measure how long one run of `http_program()` takes:

if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


if __name__ == "__main__":
    trials = 1000
    with Timer() as t:
        for i in range(trials):
            try:
                url = fuzzer()
                result = http_program(url)
                print("Success!")
            except ValueError:
                pass

    duration_per_run_in_seconds = t.elapsed_time() / trials
    duration_per_run_in_seconds


# That's pretty fast, isn't it?  Unfortunately, we have a lot of runs to cover.

if __name__ == "__main__":
    seconds_until_success = duration_per_run_in_seconds * (1 / likelihood)
    seconds_until_success


# which translates into

if __name__ == "__main__":
    hours_until_success = seconds_until_success / 3600
    days_until_success = hours_until_success / 24
    years_until_success = days_until_success / 365.25
    years_until_success


# Even if we parallelize things a lot, we're still in for months to years of waiting.  And that's for getting _one_ successful run that will get deeper into `http_program()`.

# What basic fuzzing will do well is to test `urlparse()`, and if there is an error in this parsing function, it has good chances of uncovering it.  But as long as we cannot produce a valid input, we are out of luck in reaching any deeper functionality.

# ## Mutating Inputs
# 
# The alternative to generating random strings from scratch is to start with a given _valid_ input, and then to subsequently _mutate_ it.  A _mutation_ in this context is a simple string manipulation - say, inserting a (random) character, deleting a character, or flipping a bit in a character representation.  Here are some mutations to get you started:

if __name__ == "__main__":
    print('\n## Mutating Inputs')




import random

def delete_random_character(s):
    """Returns s with a random character deleted"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    # print("Deleting", repr(s[pos]), "at", pos)
    return s[:pos] + s[pos + 1:]

if __name__ == "__main__":
    seed_input = "A quick brown fox"
    for i in range(10):
        x = delete_random_character(seed_input)
        print(repr(x))


def insert_random_character(s):
    """Returns s with a random character inserted"""
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 128))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]

if __name__ == "__main__":
    for i in range(10):
        print(repr(insert_random_character(seed_input)))


def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    # print("Flipping", bit, "in", repr(c) + ", giving", repr(new_c))
    return s[:pos] + new_c + s[pos + 1:]


if __name__ == "__main__":
    for i in range(10):
        print(repr(flip_random_character(seed_input)))


# Let us now create a random mutator that randomly chooses which mutation to apply:

def mutate(s):
    """Return s with a random mutation applied"""
    mutators = [
        delete_random_character,
        insert_random_character,
        flip_random_character
    ]
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(s)

if __name__ == "__main__":
    for i in range(10):
        print(repr(mutate("A quick brown fox")))


# The idea is now that _if_ we have some valid input(s) to begin with, we may create more input candidates by applying one of the above mutations.  To see how this works, let's get back to URLs.

# ## Mutating URLs

if __name__ == "__main__":
    print('\n## Mutating URLs')




# Let us now get back to our URL parsing problem.  Let us create a function `is_valid_url()` that checks whether `http_program()` accepts the input.

def is_valid_url(url):
    try:
        result = http_program(url)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    assert is_valid_url("http://www.google.com/search?q=fuzzing")
    assert not is_valid_url("xyzzy")


# Let us now apply the `mutate()` function on a given URL and see how many valid inputs we obtain.

if __name__ == "__main__":
    seed_input = "http://www.google.com/search?q=fuzzing"
    valid_inputs = set()
    trials = 20

    for i in range(trials):
        inp = mutate(seed_input)
        if is_valid_url(inp):
            valid_inputs.add(inp)


# We can now observe that by _mutating_ the original input, we get a high proportion of valid inputs:

if __name__ == "__main__":
    len(valid_inputs) / trials


# What are the odds of also producing a `https:` prefix by mutating a `http:` sample seed input?  We have to insert ($1 : 3$) the right character `'s'` ($1 : 96$) into the correct position ($1 : l$), where $l$ is the length of our seed input.  This means that on average, we need this many runs:

if __name__ == "__main__":
    trials = 3 * 96 * len(seed_input)
    trials


# We can actually afford this.  Let's try:

if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


if __name__ == "__main__":
    trials = 0
    with Timer() as t:
        while True:
            trials += 1
            inp = mutate(seed_input)
            if inp.startswith("https://"):
                print(
                    "Success after",
                    trials,
                    "trials in",
                    t.elapsed_time(),
                    "seconds")
                break



# Of course, if we wanted to get, say, an `"ftp://"` prefix, we would need more mutations and more runs – most important, though, we would need to apply _multiple_ mutations.

# ## Multiple Mutations
# 
# So far, we have only applied one single mutation on a sample string.  However, we can also apply _multiple_ mutations, further changing it.  What happens, for instance, if we apply, say, 20 mutations on our sample string?

if __name__ == "__main__":
    print('\n## Multiple Mutations')




if __name__ == "__main__":
    seed_input = "http://www.google.com/search?q=fuzzing"
    mutations = 50


if __name__ == "__main__":
    inp = seed_input
    for i in range(mutations):
        if i % 5 == 0:
            print(i, "mutations:", repr(inp))
        inp = mutate(inp)


# As you see, the original seed input is hardly recognizable anymore.  By mutating the input again and again, we get a higher variety in the input.

# To implement such multiple mutations in a single package, let us introduce a `MutationFuzzer` class.  It takes a seed (a list of strings) and a minimum and maximum number of mutations.  

if __package__ is None or __package__ == "":
    from Fuzzer import Fuzzer
else:
    from .Fuzzer import Fuzzer


class MutationFuzzer(Fuzzer):
    def __init__(self, seed, min_mutations=2, max_mutations=10):
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.reset()

    def reset(self):
        self.population = self.seed
        self.seed_index = 0

# In the following, let us develop `MutationFuzzer` further by adding more methods to it.  The Python language requires us to define an entire class with all methods as a single, continuous unit; however, we would like to introduce one method after another.  To avoid this problem, we use a special hack: Whenever we want to introduce a new method to some class `C`, we use the construct
# 
# ```python
# class C(C):
#     def new_method(self, args):
#         pass
# ```
# 
# This seems to define `C` as a subclass of itself, which would make no sense – but actually, it introduces a new `C` class as subclass of the old `C` class, and then shadowing the old `C` definition.  What this gets us is a `C` class with `new_method()` as a method, which is just what we want.  (`C` objects defined earlier will retain the earlier `C` definition, though, and thus must be rebuilt.)

# Using this hack, we can now add a `mutate()` method that actually invokes the above `mutate()` function.  Having `mutate()` as a method is useful when we want to extend a `MutationFuzzer` later.

class MutationFuzzer(MutationFuzzer):
    def mutate(self, inp):
        return mutate(inp)

# Let's get back to our strategy, maximizing _diversity in coverage_ in our population.  First, let us create a method `create_candidate()`, which randomly picks some input from our current population (`self.population`), and then applies between `min_mutations` and `max_mutations` mutation steps, returning the final result:

class MutationFuzzer(MutationFuzzer):
    def create_candidate(self):
        candidate = random.choice(self.population)
        trials = random.randint(self.min_mutations, self.max_mutations)
        for i in range(trials):
            candidate = self.mutate(candidate)
        return candidate

# The `fuzz()` method is set to first pick the seeds; when these are gone, we mutate:

class MutationFuzzer(MutationFuzzer):
    def fuzz(self):
        if self.seed_index < len(self.seed):
            # Still seeding
            self.inp = self.seed[self.seed_index]
            self.seed_index += 1
        else:
            # Mutating
            self.inp = self.create_candidate()
        return self.inp

if __name__ == "__main__":
    seed_input = "http://www.google.com/search?q=fuzzing"
    mutation_fuzzer = MutationFuzzer(seed=[seed_input])
    mutation_fuzzer.fuzz()


if __name__ == "__main__":
    mutation_fuzzer.fuzz()


if __name__ == "__main__":
    mutation_fuzzer.fuzz()


# With every new invocation of `fuzz()`, we get another variant with multiple mutations applied.  The higher variety in inputs, though, increases the risk of having an invalid input.  The key to success lies in the idea of _guiding_ these mutations – that is, _keeping those that are especially valuable._

# ## Guiding by Coverage
# 
# To cover as much functionality as possible, one can rely on either _specified_ or _implemented_ functionality, as discussed in the ["Coverage"](Coverage.ipynb) chapter.  For now, we will not assume that there is a specification of program behavior (although it _definitely_ would be good to have one!).  We _will_ assume, though, that the program to be tested exists – and that we can leverage its structure to guide test generation.
# 
# Since testing always executes the program at hand, one can always gather information about its execution – the least is the information needed to decide whether a test passes or fails.  Since coverage is frequently measured as well to determine test quality, let us also assume we can retrieve coverage of a test run.  The question is then: _How can we leverage coverage to guide test generation?_

if __name__ == "__main__":
    print('\n## Guiding by Coverage')




# One particularly successful idea is implemented in the popular fuzzer named [_American fuzzy lop_](http://lcamtuf.coredump.cx/afl/), or AFL for short.  Just like our examples above, AFL evolves test cases that have been successful – but for AFL, "success" means _finding a new path through the program execution_.  This way, AFL can keep on mutating inputs that so far have found new paths; and if an input finds another path, it will be retained as well.

# Let us build such a strategy.  We start with introducing a `Runner` class that captures the coverage for a given function.  First, a `FunctionRunner` class:

if __package__ is None or __package__ == "":
    from Fuzzer import Runner
else:
    from .Fuzzer import Runner


class FunctionRunner(Runner):
    def __init__(self, function):
        """Initialize.  `function` is a function to be executed"""
        self.function = function

    def run(self, inp):
        return self.function(inp)

if __name__ == "__main__":
    http_runner = FunctionRunner(http_program)
    http_runner.run("https://foo.bar/")


# We can now extend the `FunctionRunner` class such that it also measures coverage.  After invoking `run()`, the `coverage()` method returns the coverage achieved in the last run, and `valid_input()` returns whether the input was accepted by the program.

if __package__ is None or __package__ == "":
    from Coverage import Coverage, population_coverage
else:
    from .Coverage import Coverage, population_coverage


class FunctionCoverageRunner(FunctionRunner):
    def run(self, inp):
        result = None
        with Coverage() as cov:
            try:
                result = self.function(inp)
                self._valid_input = True
            except:
                self._valid_input = False
        self._coverage = cov.coverage()
        return result

    def coverage(self):
        return self._coverage

    def valid_input(self):
        return self._valid_input

if __name__ == "__main__":
    http_runner = FunctionCoverageRunner(http_program)
    http_runner.run("https://foo.bar/")


# Here's some of the locations covered: 

if __name__ == "__main__":
    list(http_runner.coverage())[:5]


# Now for the main class.  We maintain the population and a set of coverages already achieved (`coverages_seen`).  The `fuzz()` helper function takes an input and runs the given `function()` on it.  If its coverage is new (i.e. not in `coverages_seen`), the input is added to `population` and the coverage to `coverages_seen`.

class MutationCoverageFuzzer(MutationFuzzer):
    def reset(self):
        super().reset()
        self.coverages_seen = set()
        self.population = []

    def run(self, runner):
        """Run function(inp) while tracking coverage.
           If we reach new coverage,
           add inp to population and its coverage to population_coverage
        """
        result = super().run(runner)
        new_coverage = frozenset(runner.coverage())
        if runner.valid_input() and new_coverage not in self.coverages_seen:
            # We have new coverage
            self.population.append(self.inp)
            self.coverages_seen.add(new_coverage)

        return result

# Let us now put this to use:

if __name__ == "__main__":
    seed_input = "http://www.google.com/search?q=fuzzing"
    mutation_fuzzer = MutationCoverageFuzzer(seed=[seed_input])
    mutation_fuzzer.runs(http_runner, trials=10000)
    mutation_fuzzer.population


# Success!  In our population, _each and every input_ now is valid and has a different coverage, coming from various combinations of schemes, paths, queries, and fragments.

if __name__ == "__main__":
    all_coverage, cumulative_coverage = population_coverage(
        mutation_fuzzer.population, http_program)

    import matplotlib.pyplot as plt
    plt.plot(cumulative_coverage)
    plt.title('Coverage of urlparse() with random inputs')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');


# The nice thing about this strategy is that, applied to larger programs, it will happily explore one path after the other – covering functionality after functionality.  All that is needed is a means to capture the coverage.

# ## Lessons Learned
# 
# * Randomly generated inputs are frequently invalid – and thus exercise mostly input processing functionality.
# * Mutations from existing valid inputs have much higher chances to be valid, and thus to exercise functionality beyond input processing.
# 

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps
# 
# Our aim is still to sufficiently cover functionality.  From here, we can continue with:
# 
# 1. Try to cover as much _implemented_ functionality as possible.  To this end, we need to access the program implementation, measure which parts would actually be reached with our inputs, and use this _coverage_ to guide our search.  We will explore this in the next chapter, which discusses [guided mutations](Guided_Mutations.ipynb).
# 
# 2. Try to cover as much _specified_ functionality as possible.  Here, we would need a _specification of the input format,_ distinguishing between individual input elements such as (in our case) numbers, operators, comments, and strings – and attempting to cover as many of these as possible.  We will explore this as it comes to [grammar-based testing](Grammar_Testing.ipynb), and especially in [grammar-based mutations](Grammar_Mutations.ipynb).
# 
# Finally, the concept of a "population" that is systematically "evolved" through "mutations" will be explored in depth when discussing [search-based testing](Search_Based_Testing.ipynb).  Enjoy!
# 

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Exercises
# 

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1: Fuzzing CGI decode with Mutations
# 
# Apply the above _guided_ mutation-based fuzzing technique on `cgi_decode()` from the ["Coverage"](Coverage.ipynb) chapter.  How many trials do you need until you cover all variations of `+`, `%` (valid and invalid), and regular characters?

if __name__ == "__main__":
    print('\n### Exercise 1: Fuzzing CGI decode with Mutations')




if __package__ is None or __package__ == "":
    from Coverage import cgi_decode
else:
    from .Coverage import cgi_decode


if __name__ == "__main__":
    seed = ["Hello World"]
    cgi_runner = FunctionCoverageRunner(cgi_decode)
    m = MutationCoverageFuzzer(seed)
    results = m.runs(cgi_runner, 10000)


if __name__ == "__main__":
    m.population


if __name__ == "__main__":
    cgi_runner.coverage()


if __name__ == "__main__":
    all_coverage, cumulative_coverage = population_coverage(
        m.population, cgi_decode)

    import matplotlib.pyplot as plt
    plt.plot(cumulative_coverage)
    plt.title('Coverage of cgi_decode() with random inputs')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');


# After 10,000 runs, we have managed to synthesize a `+` character and a valid `%xx` form.  We can still do better.

# ### Exercise 2: Fuzzing bc with Mutations
# 
# Apply the above mutation-based fuzzing technique on `bc`, as in the chapter ["Introduction to Fuzzing"](Fuzzer.ipynb).
# 
# #### Part 1: Non-Guided Mutations
# 
# Start with non-guided mutations.  How many of the inputs are valid?

if __name__ == "__main__":
    print('\n### Exercise 2: Fuzzing bc with Mutations')




# **Solution.** This is just a matter of tying a `ProgramRunner` to a `MutationFuzzer`:

if __package__ is None or __package__ == "":
    from Fuzzer import ProgramRunner
else:
    from .Fuzzer import ProgramRunner


if __name__ == "__main__":
    seed = ["1 + 1"]
    bc = ProgramRunner(program="bc")
    m = MutationFuzzer(seed)
    runs = m.runs(bc, trials=100)


if __name__ == "__main__":
    runs[:3]


if __name__ == "__main__":
    sum(1 for completed_process in runs if completed_process.stderr == "")


# #### Part 2: Guided Mutations
# 
# Continue with _guided_ mutations.  To this end, you will have to find a way to extract coverage from a C program such as `bc`.  Proceed in these steps:
# 
# First, get GNU bc [from the source](https://www.gnu.org/software/bc/); download, say, `bc-1.07.1.tar.gz` and unpack it:

if __name__ == "__main__":
    print('\n#### Part 2: Guided Mutations')




if __name__ == "__main__":
    import os
    os.system(r'curl -O http://ftp.gnu.org/gnu/bc/bc-1.07.1.tar.gz')


if __name__ == "__main__":
    import os
    os.system(r'tar xfz bc-1.07.1.tar.gz')


# Second, configure the package:

if __name__ == "__main__":
    import os
    os.system(r'cd bc-1.07.1; ./configure')


# Third, compile the package with special flags:

if __name__ == "__main__":
    import os
    os.system(r'cd bc-1.07.1; make CFLAGS="--coverage"')


# The file `bc/bc` should now be executable...

if __name__ == "__main__":
    import os
    os.system(r'cd bc-1.07.1/bc; echo 2 + 2 | ./bc')


# ...and you should be able to run the `gcov` program to retrieve coverage information.

if __name__ == "__main__":
    import os
    os.system(r'cd bc-1.07.1/bc; gcov main.c')


# As sketched in the ["Coverage" chapter](Coverage.ipynb), the file [bc-1.07.1/bc/main.c.gcov](bc-1.07.1/bc/main.c.gcov) now holds the coverage information for `bc.c`.  Each line is prefixed with the number of times it was executed. `#####` means zero times; `-` means non-executable line.

# Parse the GCOV file for `bc` and create a `coverage` set, as in `FunctionCoverageRunner`.  Make this a `ProgramCoverageRunner` class that would be constructed with a list of source files (`bc.c`, `main.c`, `load.c`) to run `gcov` on.

# When you're done, don't forget to clean up:

if __name__ == "__main__":
    import os
    os.system(r'rm -fr bc-1.07.1 bc-1.07.1.tar.gz')


# ### Exercise 3
# 
# In this [blog post](https://lcamtuf.blogspot.com/2014/08/binary-fuzzing-strategies-what-works.html), the author of _American Fuzzy Lop_ (AFL), a very popular mutation-based fuzzer discusses the efficiency of various mutation operators.  Implement four of them and evaluate their efficiency as in the examples above.

if __name__ == "__main__":
    print('\n### Exercise 3')




# ### Exercise 4
# 
# When adding a new element to the list of candidates, AFL does actually not compare the _coverage_, but adds an element if it exercises a new _branch_.  Using branch coverage from the exercises of the ["Coverage"](Coverage.ipynb) chapter, implement this "branch" strategy and compare it against the "coverage" strategy, above.

if __name__ == "__main__":
    print('\n### Exercise 4')




# ### Exercise 5
# 
# Design and implement a system that will gather a population of URLs from the Web.  Can you achieve a higher coverage with these samples?  What if you use them as initial population for further mutation?

if __name__ == "__main__":
    print('\n### Exercise 5')



