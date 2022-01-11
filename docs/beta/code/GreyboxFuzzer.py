#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Greybox Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/GreyboxFuzzer.html
# Last change: 2022-01-11 10:08:51+01:00
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
The Fuzzing Book - Greybox Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python GreyboxFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.GreyboxFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/GreyboxFuzzer.html

This chapter introduces advanced methods for grey-box fuzzing inspired by the popular AFL fuzzer. The `GreyboxFuzzer` class has three arguments. First, a list of seed inputs:

>>> seed_input = "http://www.google.com/search?q=fuzzing"
>>> seeds = [seed_input]

Second, a _mutator_ that changes individual parts of the input.

>>> mutator = Mutator()

Third, a _power schedule_ that assigns fuzzing effort across the population:

>>> schedule = PowerSchedule()

These three go into the `GreyboxFuzzer` constructor:

>>> greybox_fuzzer = GreyboxFuzzer(seeds=seeds, mutator=mutator, schedule=schedule)

The `GreyboxFuzzer` class is used in conjunction with a `FunctionCoverageRunner`:

>>> http_runner = FunctionCoverageRunner(http_program)
>>> outcomes = greybox_fuzzer.runs(http_runner, trials=10000)

After fuzzing, we can inspect the population:

>>> greybox_fuzzer.population[:20]
[http://www.google.com/search?q=fuzzing,
 h&tv[p:S/ww.googlve.com/earch?q=fuzzing,
 h&tv[p>S/wwU.googlve.com/ezarch?q=fezzing,
 http://ww.google.com/search?q=fuzzig,
 h.Dvt://w.gSleh.sUnm/eRuh!?!=fuzi',
 up:S/@kwwgo|gl\voe/co~ml/eercq=F1z~nf,
 hDvZt*+'j.esFtjm/%eZTh.!!=zi',
 hvp://ww.SgoGl|we.kosm/BcR1a6z0#h?=Quzig,
 hvq3u//ww.#SgmGl|we.kosm/Bc1a6z0#h?=Quzpig,
 upTzkuGo|l{\vOeo-~l;ern=F1&H,
 h"&];@Sw$w.-|g}oglve.0c/nearshTq=fuzzin&gB,
 wpTzjsHuWo|l\l
 eOo/~l;+evz=fB1y&]X,
 j.LDvt:/ow.gSlehsNUnm/eRuh!?k!=Qfuzm',
 h&];Sw$w%|}owgV.T0c/n3rMshVq
 fzzin&?g,
 h"&Y;@Sw$w.-|g}oglve.0cN+nearshTqC=fuzzin&gB,
 h&];Sw$w%|}mwgPV.Tc/n3rMshVq
 fzzin&?g,
 khM;Rw$e|}GowgV.T8a~k3MsV
 nBxin&9?g,
 hDvZ^t*+'w.esGFtjm/%eZh.!!=i',
 h"&Y;@Sw$w.-|g}oglve.0cN+.earFshTC=fuz:in&gB,
 r/]/VWS..Unm/Buh#='if9qz']

Besides the simple `PowerSchedule`, we can have advanced power schedules.

* `AFLFastSchedule` assigns high energy to "unusual" paths not taken very often.
* `AFLGoSchedule` assigns high energy to paths close to uncovered program locations. 

The `AFLGoSchedule` class constructor requires a `distance` metric from each node towards target locations, as determined via analysis of the program code. See the chapter for details.

For more details, source, and documentation, see
"The Fuzzing Book - Greybox Fuzzing"
at https://www.fuzzingbook.org/html/GreyboxFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Greybox Fuzzing
# ===============

if __name__ == '__main__':
    print('# Greybox Fuzzing')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo('6Dwc55FnHBg')

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## AFL: An Effective Greybox Fuzzer
## --------------------------------

if __name__ == '__main__':
    print('\n## AFL: An Effective Greybox Fuzzer')



## Ingredients for Greybox Fuzzing
## -------------------------------

if __name__ == '__main__':
    print('\n## Ingredients for Greybox Fuzzing')



### Mutators

if __name__ == '__main__':
    print('\n### Mutators')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from typing import List, Set, Any, Tuple, Dict, Union
from collections.abc import Sequence

import random

from .Coverage import population_coverage

class Mutator:
    """Mutate strings"""

    def __init__(self) -> None:
        """Constructor"""
        self.mutators = [
            self.delete_random_character,
            self.insert_random_character,
            self.flip_random_character
        ]

class Mutator(Mutator):
    def insert_random_character(self, s: str) -> str:
        """Returns s with a random character inserted"""
        pos = random.randint(0, len(s))
        random_character = chr(random.randrange(32, 127))
        return s[:pos] + random_character + s[pos:]

class Mutator(Mutator):
    def delete_random_character(self, s: str) -> str:
        """Returns s with a random character deleted"""
        if s == "":
            return self.insert_random_character(s)

        pos = random.randint(0, len(s) - 1)
        return s[:pos] + s[pos + 1:]

class Mutator(Mutator):
    def flip_random_character(self, s: str) -> str:
        """Returns s with a random bit flipped in a random position"""
        if s == "":
            return self.insert_random_character(s)

        pos = random.randint(0, len(s) - 1)
        c = s[pos]
        bit = 1 << random.randint(0, 6)
        new_c = chr(ord(c) ^ bit)
        return s[:pos] + new_c + s[pos + 1:]

class Mutator(Mutator):
    def mutate(self, inp: Any) -> Any:  # can be str or Seed (see below)
        """Return s with a random mutation applied. Can be overloaded in subclasses."""
        mutator = random.choice(self.mutators)
        return mutator(inp)

if __name__ == '__main__':
    Mutator().mutate("good")

### Seeds and Power Schedules

if __name__ == '__main__':
    print('\n### Seeds and Power Schedules')



from .Coverage import Location

class Seed:
    """Represent an input with additional attributes"""

    def __init__(self, data: str) -> None:
        """Initialize from seed data"""
        self.data = data

        # These will be needed for advanced power schedules
        self.coverage: Set[Location] = set()
        self.distance: Union[int, float] = -1
        self.energy = 0.0

    def __str__(self) -> str:
        """Returns data as string representation of the seed"""
        return self.data

    __repr__ = __str__

class PowerSchedule:
    """Define how fuzzing time should be distributed across the population."""

    def __init__(self) -> None:
        """Constructor"""
        self.path_frequency: Dict = {}

    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """Assigns each seed the same energy"""
        for seed in population:
            seed.energy = 1

    def normalizedEnergy(self, population: Sequence[Seed]) -> List[float]:
        """Normalize energy"""
        energy = list(map(lambda seed: seed.energy, population))
        sum_energy = sum(energy)  # Add up all values in energy
        assert sum_energy != 0
        norm_energy = list(map(lambda nrg: nrg / sum_energy, energy))
        return norm_energy

    def choose(self, population: Sequence[Seed]) -> Seed:
        """Choose weighted by normalized energy."""
        self.assignEnergy(population)
        norm_energy = self.normalizedEnergy(population)
        seed: Seed = random.choices(population, weights=norm_energy)[0]
        return seed

if __name__ == '__main__':
    population = [Seed("A"), Seed("B"), Seed("C")]
    schedule = PowerSchedule()
    hits = {
        "A": 0,
        "B": 0,
        "C": 0
    }

if __name__ == '__main__':
    for i in range(10000):
        seed = schedule.choose(population)
        hits[seed.data] += 1

if __name__ == '__main__':
    hits

### Runners and a Sample Program

if __name__ == '__main__':
    print('\n### Runners and a Sample Program')



from .MutationFuzzer import FunctionCoverageRunner, http_program

def crashme(s: str) -> None:
    if len(s) > 0 and s[0] == 'b':
        if len(s) > 1 and s[1] == 'a':
            if len(s) > 2 and s[2] == 'd':
                if len(s) > 3 and s[3] == '!':
                    raise Exception()

if __name__ == '__main__':
    crashme_runner = FunctionCoverageRunner(crashme)
    crashme_runner.run("good")
    list(crashme_runner.coverage())

## Advanced Blackbox Mutation-based Fuzzing
## ----------------------------------------

if __name__ == '__main__':
    print('\n## Advanced Blackbox Mutation-based Fuzzing')



from .Fuzzer import Fuzzer

class AdvancedMutationFuzzer(Fuzzer):
    """Base class for mutation-based fuzzing."""

    def __init__(self, seeds: List[str],
                 mutator: Mutator,
                 schedule: PowerSchedule) -> None:
        """Constructor.
        `seeds` - a list of (input) strings to mutate.
        `mutator` - the mutator to apply.
        `schedule` - the power schedule to apply.
        """
        self.seeds = seeds
        self.mutator = mutator
        self.schedule = schedule
        self.inputs: List[str] = []
        self.reset()

    def reset(self) -> None:
        """Reset the initial population and seed index"""
        self.population = list(map(lambda x: Seed(x), self.seeds))
        self.seed_index = 0

    def create_candidate(self) -> str:
        """Returns an input generated by fuzzing a seed in the population"""
        seed = self.schedule.choose(self.population)

        # Stacking: Apply multiple mutations to generate the candidate
        candidate = seed.data
        trials = min(len(candidate), 1 << random.randint(1, 5))
        for i in range(trials):
            candidate = self.mutator.mutate(candidate)
        return candidate

    def fuzz(self) -> str:
        """Returns first each seed once and then generates new inputs"""
        if self.seed_index < len(self.seeds):
            # Still seeding
            self.inp = self.seeds[self.seed_index]
            self.seed_index += 1
        else:
            # Mutating
            self.inp = self.create_candidate()

        self.inputs.append(self.inp)
        return self.inp

if __name__ == '__main__':
    seed_input = "good"
    mutation_fuzzer = AdvancedMutationFuzzer([seed_input], Mutator(), PowerSchedule())
    print(mutation_fuzzer.fuzz())
    print(mutation_fuzzer.fuzz())
    print(mutation_fuzzer.fuzz())

import time

if __name__ == '__main__':
    n = 30000

if __name__ == '__main__':
    blackbox_fuzzer = AdvancedMutationFuzzer([seed_input], Mutator(), PowerSchedule())

    start = time.time()
    blackbox_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
    end = time.time()

    "It took the blackbox mutation-based fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    _, blackbox_coverage = population_coverage(blackbox_fuzzer.inputs, crashme)
    bb_max_coverage = max(blackbox_coverage)

    "The blackbox mutation-based fuzzer achieved a maximum coverage of %d statements." % bb_max_coverage

if __name__ == '__main__':
    [seed_input] + \
        [
            blackbox_fuzzer.inputs[idx] for idx in range(len(blackbox_coverage))
            if blackbox_coverage[idx] > blackbox_coverage[idx - 1]
        ]

## Greybox Mutation-based Fuzzing
## ------------------------------

if __name__ == '__main__':
    print('\n## Greybox Mutation-based Fuzzing')



class GreyboxFuzzer(AdvancedMutationFuzzer):
    """Coverage-guided mutational fuzzing."""

    def reset(self):
        """Reset the initial population, seed index, coverage information"""
        super().reset()
        self.coverages_seen = set()
        self.population = []  # population is filled during greybox fuzzing

    def run(self, runner: FunctionCoverageRunner) -> Tuple[Any, str]:  # type: ignore
        """Run function(inp) while tracking coverage.
           If we reach new coverage,
           add inp to population and its coverage to population_coverage
        """
        result, outcome = super().run(runner)
        new_coverage = frozenset(runner.coverage())
        if new_coverage not in self.coverages_seen:
            # We have new coverage
            seed = Seed(self.inp)
            seed.coverage = runner.coverage()
            self.coverages_seen.add(new_coverage)
            self.population.append(seed)

        return (result, outcome)

if __name__ == '__main__':
    seed_input = "good"
    greybox_fuzzer = GreyboxFuzzer([seed_input], Mutator(), PowerSchedule())

    start = time.time()
    greybox_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
    end = time.time()

    "It took the greybox mutation-based fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    _, greybox_coverage = population_coverage(greybox_fuzzer.inputs, crashme)
    gb_max_coverage = max(greybox_coverage)

    "Our greybox mutation-based fuzzer covers %d more statements" % (gb_max_coverage - bb_max_coverage)

if __name__ == '__main__':
    greybox_fuzzer.population

# %matplotlib inline

if __name__ == '__main__':
    import matplotlib.pyplot as plt  # type: ignore

if __name__ == '__main__':
    line_bb, = plt.plot(blackbox_coverage, label="Blackbox")
    line_gb, = plt.plot(greybox_coverage, label="Greybox")
    plt.legend(handles=[line_bb, line_gb])
    plt.title('Coverage over time')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');

## Boosted Greybox Fuzzing
## -----------------------

if __name__ == '__main__':
    print('\n## Boosted Greybox Fuzzing')



import pickle   # serializes an object by producing a byte array from all the information in the object
import hashlib  # produces a 128-bit hash value from a byte array

def getPathID(coverage: Any) -> str:
    """Returns a unique hash for the covered statements"""
    pickled = pickle.dumps(coverage)
    return hashlib.md5(pickled).hexdigest()

class AFLFastSchedule(PowerSchedule):
    """Exponential power schedule as implemented in AFL"""

    def __init__(self, exponent: float) -> None:
        self.exponent = exponent

    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """Assign exponential energy inversely proportional to path frequency"""
        for seed in population:
            seed.energy = 1 / (self.path_frequency[getPathID(seed.coverage)] ** self.exponent)

class CountingGreyboxFuzzer(GreyboxFuzzer):
    """Count how often individual paths are exercised."""

    def reset(self):
        """Reset path frequency"""
        super().reset()
        self.schedule.path_frequency = {}

    def run(self, runner: FunctionCoverageRunner) -> Tuple[Any, str]:  # type: ignore
        """Inform scheduler about path frequency"""
        result, outcome = super().run(runner)

        path_id = getPathID(runner.coverage())
        if path_id not in self.schedule.path_frequency:
            self.schedule.path_frequency[path_id] = 1
        else:
            self.schedule.path_frequency[path_id] += 1

        return(result, outcome)

if __name__ == '__main__':
    n = 10000
    seed_input = "good"
    fast_schedule = AFLFastSchedule(5)
    fast_fuzzer = CountingGreyboxFuzzer([seed_input], Mutator(), fast_schedule)
    start = time.time()
    fast_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
    end = time.time()

    "It took the fuzzer w/ exponential schedule %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    import numpy as np

if __name__ == '__main__':
    x_axis = np.arange(len(fast_schedule.path_frequency))
    y_axis = list(fast_schedule.path_frequency.values())

    plt.bar(x_axis, y_axis)
    plt.xticks(x_axis)
    plt.ylim(0, n)
    # plt.yscale("log")
    # plt.yticks([10,100,1000,10000])
    plt;

if __name__ == '__main__':
    print("             path id 'p'           : path frequency 'f(p)'")
    fast_schedule.path_frequency

if __name__ == '__main__':
    seed_input = "good"
    orig_schedule = PowerSchedule()
    orig_fuzzer = CountingGreyboxFuzzer([seed_input], Mutator(), orig_schedule)
    start = time.time()
    orig_fuzzer.runs(FunctionCoverageRunner(crashme), trials=n)
    end = time.time()

    "It took the fuzzer w/ original schedule %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    x_axis = np.arange(len(orig_schedule.path_frequency))
    y_axis = list(orig_schedule.path_frequency.values())

    plt.bar(x_axis, y_axis)
    plt.xticks(x_axis)
    plt.ylim(0, n)
    # plt.yscale("log")
    # plt.yticks([10,100,1000,10000])
    plt;

if __name__ == '__main__':
    print("             path id 'p'           : path frequency 'f(p)'")
    orig_schedule.path_frequency

if __name__ == '__main__':
    orig_energy = orig_schedule.normalizedEnergy(orig_fuzzer.population)

    for (seed, norm_energy) in zip(orig_fuzzer.population, orig_energy):
        print("'%s', %0.5f, %s" % (getPathID(seed.coverage),  # type: ignore
                                   norm_energy, repr(seed.data)))

if __name__ == '__main__':
    fast_energy = fast_schedule.normalizedEnergy(fast_fuzzer.population)

    for (seed, norm_energy) in zip(fast_fuzzer.population, fast_energy):
        print("'%s', %0.5f, %s" % (getPathID(seed.coverage),  # type: ignore
                                   norm_energy, repr(seed.data)))

if __name__ == '__main__':
    _, orig_coverage = population_coverage(orig_fuzzer.inputs, crashme)
    _, fast_coverage = population_coverage(fast_fuzzer.inputs, crashme)
    line_orig, = plt.plot(orig_coverage, label="Original Greybox Fuzzer")
    line_fast, = plt.plot(fast_coverage, label="Boosted Greybox Fuzzer")
    plt.legend(handles=[line_orig, line_fast])
    plt.title('Coverage over time')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');

## A Complex Example: HTMLParser
## -----------------------------

if __name__ == '__main__':
    print('\n## A Complex Example: HTMLParser')



from html.parser import HTMLParser

def my_parser(inp: str) -> None:
    parser = HTMLParser()  # resets the HTMLParser object for every fuzz input
    parser.feed(inp)

if __name__ == '__main__':
    n = 5000
    seed_input = " "  # empty seed
    blackbox_fuzzer = AdvancedMutationFuzzer([seed_input], Mutator(), PowerSchedule())
    greybox_fuzzer = GreyboxFuzzer([seed_input], Mutator(), PowerSchedule())
    boosted_fuzzer = CountingGreyboxFuzzer([seed_input], Mutator(), AFLFastSchedule(5))

if __name__ == '__main__':
    start = time.time()
    blackbox_fuzzer.runs(FunctionCoverageRunner(my_parser), trials=n)
    greybox_fuzzer.runs(FunctionCoverageRunner(my_parser), trials=n)
    boosted_fuzzer.runs(FunctionCoverageRunner(my_parser), trials=n)
    end = time.time()

    "It took all three fuzzers %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    _, black_coverage = population_coverage(blackbox_fuzzer.inputs, my_parser)
    _, grey_coverage = population_coverage(greybox_fuzzer.inputs, my_parser)
    _, boost_coverage = population_coverage(boosted_fuzzer.inputs, my_parser)
    line_black, = plt.plot(black_coverage, label="Blackbox Fuzzer")
    line_grey, = plt.plot(grey_coverage, label="Greybox Fuzzer")
    line_boost, = plt.plot(boost_coverage, label="Boosted Greybox Fuzzer")
    plt.legend(handles=[line_boost, line_grey, line_black])
    plt.title('Coverage over time')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');

if __name__ == '__main__':
    blackbox_fuzzer.inputs[-10:]

if __name__ == '__main__':
    greybox_fuzzer.inputs[-10:]

## Directed Greybox Fuzzing
## ------------------------

if __name__ == '__main__':
    print('\n## Directed Greybox Fuzzing')



### Solving the Maze

if __name__ == '__main__':
    print('\n### Solving the Maze')



if __name__ == '__main__':
    maze_string = """
+-+-----+
|X|     |
| | --+ |
| |   | |
| +-- | |
|     |#|
+-----+-+
"""

from .ControlFlow import generate_maze_code

def maze(s: str) -> str:
    return ""  # Will be overwritten by exec()

def target_tile() -> str:
    return ' '  # Will be overwritten by exec()

if __name__ == '__main__':
    maze_code = generate_maze_code(maze_string)

if __name__ == '__main__':
    exec(maze_code)

if __name__ == '__main__':
    print(maze("DDDDRRRRUULLUURRRRDDDD"))  # Appending one more 'D', you have reached the target.

from .ControlFlow import callgraph

if __name__ == '__main__':
    callgraph(maze_code)

### A First Attempt

if __name__ == '__main__':
    print('\n### A First Attempt')



class DictMutator(Mutator):
    """Variant of `Mutator` inserting keywords from a dictionary"""

    def __init__(self, dictionary: Sequence[str]) -> None:
        """Constructor.
        `dictionary` - a list of strings that can be used as keywords
        """
        super().__init__()
        self.dictionary = dictionary
        self.mutators.append(self.insert_from_dictionary)

    def insert_from_dictionary(self, s: str) -> str:
        """Returns `s` with a keyword from the dictionary inserted"""
        pos = random.randint(0, len(s))
        random_keyword = random.choice(self.dictionary)
        return s[:pos] + random_keyword + s[pos:]

class MazeMutator(DictMutator):
    def __init__(self, dictionary: Sequence[str]) -> None:
        super().__init__(dictionary)
        self.mutators.append(self.delete_last_character)
        self.mutators.append(self.append_from_dictionary)

    def append_from_dictionary(self, s: str) -> str:
        """Returns s with a keyword from the dictionary appended"""
        random_keyword = random.choice(self.dictionary)
        return s + random_keyword

    def delete_last_character(self, s: str) -> str:
        """Returns s without the last character"""
        if len(s) > 0:
            return s[:-1]
        return s

if __name__ == '__main__':
    n = 20000
    seed_input = " "  # empty seed

    maze_mutator = MazeMutator(["L", "R", "U", "D"])
    maze_schedule = PowerSchedule()
    maze_fuzzer = GreyboxFuzzer([seed_input], maze_mutator, maze_schedule)

    start = time.time()
    maze_fuzzer.runs(FunctionCoverageRunner(maze), trials=n)
    end = time.time()

    "It took the fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

def print_stats(fuzzer: GreyboxFuzzer) -> None:
    total = len(fuzzer.population)
    solved = 0
    invalid = 0
    valid = 0
    for seed in fuzzer.population:
        s = maze(str(seed.data))
        if "INVALID" in s:
            invalid += 1
        elif "VALID" in s:
            valid += 1
        elif "SOLVED" in s:
            solved += 1
            if solved == 1:
                print("First solution: %s" % repr(seed))
        else:
            print("??")

    print("""Out of %d seeds,
* %4d solved the maze,
* %4d were valid but did not solve the maze, and
* %4d were invalid""" % (total, solved, valid, invalid))

if __name__ == '__main__':
    print_stats(maze_fuzzer)

### Computing Function-Level Distance

if __name__ == '__main__':
    print('\n### Computing Function-Level Distance')



if __name__ == '__main__':
    target = target_tile()
    target

import networkx as nx  # type: ignore

from .ControlFlow import get_callgraph

if __name__ == '__main__':
    cg = get_callgraph(maze_code)
    for node in cg.nodes():
        if target in node:
            target_node = node
            break

if __name__ == '__main__':
    target_node

if __name__ == '__main__':
    distance = {}
    for node in cg.nodes():
        if "__" in node:
            name = node.split("__")[-1]
        else:
            name = node
        try:
            distance[name] = nx.shortest_path_length(cg, node, target_node)
        except:
            distance[name] = 0xFFFF

if __name__ == '__main__':
    {k: distance[k] for k in list(distance) if distance[k] < 0xFFFF}

### Directed Power Schedule

if __name__ == '__main__':
    print('\n### Directed Power Schedule')



class DirectedSchedule(PowerSchedule):
    """Assign high energy to seeds close to some target"""

    def __init__(self, distance: Dict[str, int], exponent: float) -> None:
        self.distance = distance
        self.exponent = exponent

    def __getFunctions__(self, coverage: Set[Location]) -> Set[str]:
        functions = set()
        for f, _ in set(coverage):
            functions.add(f)
        return functions

    def assignEnergy(self, population: Sequence[Seed]) -> None:
        """Assigns each seed energy inversely proportional
           to the average function-level distance to target."""
        for seed in population:
            if seed.distance < 0:
                num_dist = 0
                sum_dist = 0
                for f in self.__getFunctions__(seed.coverage):
                    if f in list(self.distance):
                        sum_dist += self.distance[f]
                        num_dist += 1
                seed.distance = sum_dist / num_dist
                seed.energy = (1 / seed.distance) ** self.exponent

if __name__ == '__main__':
    directed_schedule = DirectedSchedule(distance, 3)
    directed_fuzzer = GreyboxFuzzer([seed_input], maze_mutator, directed_schedule)

    start = time.time()
    directed_fuzzer.runs(FunctionCoverageRunner(maze), trials=n)
    end = time.time()

    "It took the fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    print_stats(directed_fuzzer)

if __name__ == '__main__':
    y = [seed.distance for seed in directed_fuzzer.population]  # type: ignore
    x = range(len(y))
    plt.scatter(x, y)
    plt.ylim(0, max(y))
    plt.xlabel("Seed ID")
    plt.ylabel("Distance");

### Improved Directed Power Schedule

if __name__ == '__main__':
    print('\n### Improved Directed Power Schedule')



class AFLGoSchedule(DirectedSchedule):
    """Assign high energy to seeds close to the target"""

    def assignEnergy(self, population: Sequence[Seed]):
        """Assigns each seed energy inversely proportional
           to the average function-level distance to target."""
        min_dist: Union[int, float] = 0xFFFF
        max_dist: Union[int, float] = 0

        for seed in population:
            if seed.distance < 0:
                num_dist = 0
                sum_dist = 0
                for f in self.__getFunctions__(seed.coverage):
                    if f in list(self.distance):
                        sum_dist += self.distance[f]
                        num_dist += 1
                seed.distance = sum_dist / num_dist
            if seed.distance < min_dist:
                min_dist = seed.distance
            if seed.distance > max_dist:
                max_dist = seed.distance

        for seed in population:
            if seed.distance == min_dist:
                if min_dist == max_dist:
                    seed.energy = 1
                else:
                    seed.energy = max_dist - min_dist
            else:
                seed.energy = (max_dist - min_dist) / (seed.distance - min_dist)

if __name__ == '__main__':
    aflgo_schedule = AFLGoSchedule(distance, 3)
    aflgo_fuzzer = GreyboxFuzzer([seed_input], maze_mutator, aflgo_schedule)

    start = time.time()
    aflgo_fuzzer.runs(FunctionCoverageRunner(maze), trials=n)
    end = time.time()

    "It took the fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    print_stats(aflgo_fuzzer)

if __name__ == '__main__':
    for seed in aflgo_fuzzer.population:
        s = maze(str(seed.data))
        if "SOLVED" in s:
            filtered = "".join(list(filter(lambda c: c in "UDLR", seed.data)))
            print(filtered)
            break

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    seed_input = "http://www.google.com/search?q=fuzzing"
    seeds = [seed_input]

if __name__ == '__main__':
    mutator = Mutator()

if __name__ == '__main__':
    schedule = PowerSchedule()

if __name__ == '__main__':
    greybox_fuzzer = GreyboxFuzzer(seeds=seeds, mutator=mutator, schedule=schedule)

if __name__ == '__main__':
    http_runner = FunctionCoverageRunner(http_program)
    outcomes = greybox_fuzzer.runs(http_runner, trials=10000)

if __name__ == '__main__':
    greybox_fuzzer.population[:20]

from .ClassDiagram import display_class_hierarchy

if __name__ == '__main__':
    display_class_hierarchy([CountingGreyboxFuzzer, AFLFastSchedule, AFLGoSchedule,
                             DictMutator, Seed],
                            public_methods=[
                                Fuzzer.run,
                                Fuzzer.__init__,
                                Fuzzer.runs,
                                Fuzzer.fuzz,
                                AdvancedMutationFuzzer.__init__,
                                AdvancedMutationFuzzer.fuzz,
                                GreyboxFuzzer.run,
                                CountingGreyboxFuzzer.run,
                                PowerSchedule.__init__,
                                DirectedSchedule.__init__,
                                AFLGoSchedule.__init__,
                                AFLFastSchedule.__init__,
                                Seed.__init__,
                                Mutator.__init__,
                                DictMutator.__init__,
                            ],
                            types={'Location': Location},
                            project='fuzzingbook')

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



import os

if __name__ == '__main__':
    if os.path.exists('callgraph.dot'):
        os.remove('callgraph.dot')

    if os.path.exists('callgraph.py'):
        os.remove('callgraph.py')

## Compatibility
## -------------

if __name__ == '__main__':
    print('\n## Compatibility')



class MutationFuzzer(AdvancedMutationFuzzer):
    pass

## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')


