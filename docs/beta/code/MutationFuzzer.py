#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Mutation-Based Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/MutationFuzzer.html
# Last change: 2023-11-12 13:40:28+01:00
#
# Copyright (c) 2021-2023 CISPA Helmholtz Center for Information Security
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
The Fuzzing Book - Mutation-Based Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python MutationFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.MutationFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/MutationFuzzer.html

This chapter introduces a `MutationFuzzer` class that takes a list of _seed inputs_ which are then mutated:

>>> seed_input = "http://www.google.com/search?q=fuzzing"
>>> mutation_fuzzer = MutationFuzzer(seed=[seed_input])
>>> [mutation_fuzzer.fuzz() for i in range(10)]
['http://www.google.com/search?q=fuzzing',
 'http://wwBw.google.com/searh?q=fuzzing',
 'http8//wswgoRogle.am/secch?qU=fuzzing',
 'ittp://www.googLe.com/serch?q=fuzzingZ',
 'httP://wgw.google.com/seasch?Q=fuxzanmgY',
 'http://www.google.cxcom/search?q=fuzzing',
 'hFttp://ww.-g\x7fog+le.com/s%arch?q=f-uzz#ing',
 'http://www\x0egoogle.com/seaNrch?q=fuZzing',
 'http//www.Ygooge.comsarch?q=fuz~Ijg',
 'http8//ww.goog5le.com/sezarc?q=fuzzing']

The `MutationCoverageFuzzer` maintains a _population_ of inputs, which are then evolved in order to maximize coverage.

>>> mutation_fuzzer = MutationCoverageFuzzer(seed=[seed_input])
>>> mutation_fuzzer.runs(http_runner, trials=10000)
>>> mutation_fuzzer.population[:5]
['http://www.google.com/search?q=fuzzing',
 'http://wwv.oogle>co/search7Eq=fuzing',
 'http://wwv\x0eOogleb>co/seakh7Eq\x1d;fuzing',
 'http://wwv\x0eoglebkooqeakh7Eq\x1d;fuzing',
 'http://wwv\x0eoglekol=oekh7Eq\x1d\x1bf~ing']

For more details, source, and documentation, see
"The Fuzzing Book - Mutation-Based Fuzzing"
at https://www.fuzzingbook.org/html/MutationFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Mutation-Based Fuzzing
# ======================

if __name__ == '__main__':
    print('# Mutation-Based Fuzzing')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo('5ROhc_42jQU')

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Fuzzing with Mutations
## ----------------------

if __name__ == '__main__':
    print('\n## Fuzzing with Mutations')



## Fuzzing a URL Parser
## --------------------

if __name__ == '__main__':
    print('\n## Fuzzing a URL Parser')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from typing import Tuple, List, Callable, Set, Any

from urllib.parse import urlparse

if __name__ == '__main__':
    urlparse("http://www.google.com/search?q=fuzzing")

def http_program(url: str) -> bool:
    supported_schemes = ["http", "https"]
    result = urlparse(url)
    if result.scheme not in supported_schemes:
        raise ValueError("Scheme must be one of " + 
                         repr(supported_schemes))
    if result.netloc == '':
        raise ValueError("Host must be non-empty")

    # Do something with the URL
    return True

from .Fuzzer import fuzzer

if __name__ == '__main__':
    fuzzer(char_start=32, char_range=96)

if __name__ == '__main__':
    for i in range(1000):
        try:
            url = fuzzer()
            result = http_program(url)
            print("Success!")
        except ValueError:
            pass

if __name__ == '__main__':
    96 ** 7

if __name__ == '__main__':
    96 ** 8

if __name__ == '__main__':
    likelihood = 1 / (96 ** 7) + 1 / (96 ** 8)
    likelihood

if __name__ == '__main__':
    1 / likelihood

from .Timer import Timer

if __name__ == '__main__':
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

if __name__ == '__main__':
    seconds_until_success = duration_per_run_in_seconds * (1 / likelihood)
    seconds_until_success

if __name__ == '__main__':
    hours_until_success = seconds_until_success / 3600
    days_until_success = hours_until_success / 24
    years_until_success = days_until_success / 365.25
    years_until_success

## Mutating Inputs
## ---------------

if __name__ == '__main__':
    print('\n## Mutating Inputs')



import random

def delete_random_character(s: str) -> str:
    """Returns s with a random character deleted"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    # print("Deleting", repr(s[pos]), "at", pos)
    return s[:pos] + s[pos + 1:]

if __name__ == '__main__':
    seed_input = "A quick brown fox"
    for i in range(10):
        x = delete_random_character(seed_input)
        print(repr(x))

def insert_random_character(s: str) -> str:
    """Returns s with a random character inserted"""
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]

if __name__ == '__main__':
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

if __name__ == '__main__':
    for i in range(10):
        print(repr(flip_random_character(seed_input)))

def mutate(s: str) -> str:
    """Return s with a random mutation applied"""
    mutators = [
        delete_random_character,
        insert_random_character,
        flip_random_character
    ]
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(s)

if __name__ == '__main__':
    for i in range(10):
        print(repr(mutate("A quick brown fox")))

## Mutating URLs
## -------------

if __name__ == '__main__':
    print('\n## Mutating URLs')



def is_valid_url(url: str) -> bool:
    try:
        result = http_program(url)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    assert is_valid_url("http://www.google.com/search?q=fuzzing")
    assert not is_valid_url("xyzzy")

if __name__ == '__main__':
    seed_input = "http://www.google.com/search?q=fuzzing"
    valid_inputs = set()
    trials = 20

    for i in range(trials):
        inp = mutate(seed_input)
        if is_valid_url(inp):
            valid_inputs.add(inp)

if __name__ == '__main__':
    len(valid_inputs) / trials

if __name__ == '__main__':
    trials = 3 * 96 * len(seed_input)
    trials

from .Timer import Timer

if __name__ == '__main__':
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

## Multiple Mutations
## ------------------

if __name__ == '__main__':
    print('\n## Multiple Mutations')



if __name__ == '__main__':
    seed_input = "http://www.google.com/search?q=fuzzing"
    mutations = 50

if __name__ == '__main__':
    inp = seed_input
    for i in range(mutations):
        if i % 5 == 0:
            print(i, "mutations:", repr(inp))
        inp = mutate(inp)

from .Fuzzer import Fuzzer

class MutationFuzzer(Fuzzer):
    """Base class for mutational fuzzing"""

    def __init__(self, seed: List[str],
                 min_mutations: int = 2,
                 max_mutations: int = 10) -> None:
        """Constructor.
        `seed` - a list of (input) strings to mutate.
        `min_mutations` - the minimum number of mutations to apply.
        `max_mutations` - the maximum number of mutations to apply.
        """
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.reset()

    def reset(self) -> None:
        """Set population to initial seed.
        To be overloaded in subclasses."""
        self.population = self.seed
        self.seed_index = 0

class MutationFuzzer(MutationFuzzer):
    def mutate(self, inp: str) -> str:
        return mutate(inp)

class MutationFuzzer(MutationFuzzer):
    def create_candidate(self) -> str:
        """Create a new candidate by mutating a population member"""
        candidate = random.choice(self.population)
        trials = random.randint(self.min_mutations, self.max_mutations)
        for i in range(trials):
            candidate = self.mutate(candidate)
        return candidate

class MutationFuzzer(MutationFuzzer):
    def fuzz(self) -> str:
        if self.seed_index < len(self.seed):
            # Still seeding
            self.inp = self.seed[self.seed_index]
            self.seed_index += 1
        else:
            # Mutating
            self.inp = self.create_candidate()
        return self.inp

if __name__ == '__main__':
    seed_input = "http://www.google.com/search?q=fuzzing"
    mutation_fuzzer = MutationFuzzer(seed=[seed_input])
    mutation_fuzzer.fuzz()

if __name__ == '__main__':
    mutation_fuzzer.fuzz()

if __name__ == '__main__':
    mutation_fuzzer.fuzz()

## Guiding by Coverage
## -------------------

if __name__ == '__main__':
    print('\n## Guiding by Coverage')



from .Fuzzer import Runner

class FunctionRunner(Runner):
    def __init__(self, function: Callable) -> None:
        """Initialize.  `function` is a function to be executed"""
        self.function = function

    def run_function(self, inp: str) -> Any:
        return self.function(inp)

    def run(self, inp: str) -> Tuple[Any, str]:
        try:
            result = self.run_function(inp)
            outcome = self.PASS
        except Exception:
            result = None
            outcome = self.FAIL

        return result, outcome

if __name__ == '__main__':
    http_runner = FunctionRunner(http_program)
    http_runner.run("https://foo.bar/")

from .Coverage import Coverage, population_coverage, Location

class FunctionCoverageRunner(FunctionRunner):
    def run_function(self, inp: str) -> Any:
        with Coverage() as cov:
            try:
                result = super().run_function(inp)
            except Exception as exc:
                self._coverage = cov.coverage()
                raise exc

        self._coverage = cov.coverage()
        return result

    def coverage(self) -> Set[Location]:
        return self._coverage

if __name__ == '__main__':
    http_runner = FunctionCoverageRunner(http_program)
    http_runner.run("https://foo.bar/")

if __name__ == '__main__':
    print(list(http_runner.coverage())[:5])

class MutationCoverageFuzzer(MutationFuzzer):
    """Fuzz with mutated inputs based on coverage"""

    def reset(self) -> None:
        super().reset()
        self.coverages_seen: Set[frozenset] = set()
        # Now empty; we fill this with seed in the first fuzz runs
        self.population = []

    def run(self, runner: FunctionCoverageRunner) -> Any:  # type: ignore
        """Run function(inp) while tracking coverage.
           If we reach new coverage,
           add inp to population and its coverage to population_coverage
        """
        result, outcome = super().run(runner)
        new_coverage = frozenset(runner.coverage())
        if outcome == Runner.PASS and new_coverage not in self.coverages_seen:
            # We have new coverage
            self.population.append(self.inp)
            self.coverages_seen.add(new_coverage)

        return result

if __name__ == '__main__':
    seed_input = "http://www.google.com/search?q=fuzzing"
    mutation_fuzzer = MutationCoverageFuzzer(seed=[seed_input])
    mutation_fuzzer.runs(http_runner, trials=10000)
    mutation_fuzzer.population

if __name__ == '__main__':
    all_coverage, cumulative_coverage = population_coverage(
        mutation_fuzzer.population, http_program)

if __name__ == '__main__':
    import matplotlib.pyplot as plt  # type: ignore

if __name__ == '__main__':
    plt.plot(cumulative_coverage)
    plt.title('Coverage of urlparse() with random inputs')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    seed_input = "http://www.google.com/search?q=fuzzing"
    mutation_fuzzer = MutationFuzzer(seed=[seed_input])
    [mutation_fuzzer.fuzz() for i in range(10)]

if __name__ == '__main__':
    mutation_fuzzer = MutationCoverageFuzzer(seed=[seed_input])
    mutation_fuzzer.runs(http_runner, trials=10000)
    mutation_fuzzer.population[:5]

from .ClassDiagram import display_class_hierarchy

if __name__ == '__main__':
    display_class_hierarchy(MutationCoverageFuzzer,
                            public_methods=[
                                Fuzzer.run,
                                Fuzzer.__init__,
                                Fuzzer.runs,
                                Fuzzer.fuzz,
                                MutationFuzzer.__init__,
                                MutationFuzzer.fuzz,
                                MutationCoverageFuzzer.run,
                            ],
                            types={'Location': Location},
                            project='fuzzingbook')

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Fuzzing CGI decode with Mutations

if __name__ == '__main__':
    print('\n### Exercise 1: Fuzzing CGI decode with Mutations')



from .Coverage import cgi_decode

if __name__ == '__main__':
    seed = ["Hello World"]
    cgi_runner = FunctionCoverageRunner(cgi_decode)
    m = MutationCoverageFuzzer(seed)
    results = m.runs(cgi_runner, 10000)

if __name__ == '__main__':
    m.population

if __name__ == '__main__':
    cgi_runner.coverage()

if __name__ == '__main__':
    all_coverage, cumulative_coverage = population_coverage(
        m.population, cgi_decode)

    import matplotlib.pyplot as plt
    plt.plot(cumulative_coverage)
    plt.title('Coverage of cgi_decode() with random inputs')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');

### Exercise 2: Fuzzing bc with Mutations

if __name__ == '__main__':
    print('\n### Exercise 2: Fuzzing bc with Mutations')



from .Fuzzer import ProgramRunner

if __name__ == '__main__':
    seed = ["1 + 1"]
    bc = ProgramRunner(program="bc")
    m = MutationFuzzer(seed)
    outcomes = m.runs(bc, trials=100)

if __name__ == '__main__':
    outcomes[:3]

if __name__ == '__main__':
    sum(1 for completed_process, outcome in outcomes if completed_process.stderr == "")

#### Part 2: Guided Mutations

if __name__ == '__main__':
    print('\n#### Part 2: Guided Mutations')



if __name__ == '__main__':
    import os
    os.system(f'curl -O mirrors.kernel.org/gnu/bc/bc-1.07.1.tar.gz')

if __name__ == '__main__':
    import os
    os.system(f'tar xfz bc-1.07.1.tar.gz')

if __name__ == '__main__':
    import os
    os.system(f'cd bc-1.07.1; ./configure')

if __name__ == '__main__':
    import os
    os.system(f'cd bc-1.07.1; make CFLAGS="--coverage"')

if __name__ == '__main__':
    import os
    os.system(f'cd bc-1.07.1/bc; echo 2 + 2 | ./bc')

if __name__ == '__main__':
    import os
    os.system(f'cd bc-1.07.1/bc; gcov main.c')

if __name__ == '__main__':
    import os
    os.system(f'rm -fr bc-1.07.1 bc-1.07.1.tar.gz')

### Exercise 3

if __name__ == '__main__':
    print('\n### Exercise 3')



### Exercise 4

if __name__ == '__main__':
    print('\n### Exercise 4')



### Exercise 5

if __name__ == '__main__':
    print('\n### Exercise 5')


