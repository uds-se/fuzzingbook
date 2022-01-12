#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Greybox Fuzzing with Grammars" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/GreyboxGrammarFuzzer.html
# Last change: 2022-01-12 14:49:17+01:00
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
The Fuzzing Book - Greybox Fuzzing with Grammars

This file can be _executed_ as a script, running all experiments:

    $ python GreyboxGrammarFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.GreyboxGrammarFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/GreyboxGrammarFuzzer.html

This chapter introduces advanced methods for language-based grey-box fuzzing inspired by the _LangFuzz_ and _AFLSmart_ fuzzers.

### Fuzzing with Dictionaries

Rather than mutating strings randomly, the `DictMutator` class allows to insert tokens from a dictionary, thus increasing fuzzer performance. The dictionary comes as a list of strings, out of which random elements are picked and inserted - in addition to the given mutations such as deleting or inserting individual bytes.

>>> dict_mutator = DictMutator(["", "", "", "='a'"])
>>> seeds = ["HelloWorld"]
>>> for i in range(10):
>>>     print(dict_mutator.mutate(seeds[0]))
HelloWorldhtml>
HelloWorldml>
HelloWorld
HelloWorld
HelloWorld
HelloWorld
HelloWorld
HelloWorld
HelloWorld
Hello|/head>World


This `DictMutator` can be used as an argument to `GreyboxFuzzer`:

>>> runner = FunctionCoverageRunner(my_parser)
>>> dict_fuzzer = GreyboxFuzzer(seeds, dict_mutator, PowerSchedule())
>>> dict_fuzzer_outcome = dict_fuzzer.runs(runner, trials=5)
### Fuzzing with Input Fragments

The `LangFuzzer` class introduces a _language-aware_ fuzzer that can recombine fragments from existing inputs – inspired by the highly effective `LangFuzz` fuzzer. At its core is a `FragmentMutator` class that that takes a [_parser_](Parser.ipynb) as argument:

>>> parser = EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS)
>>> mutator = FragmentMutator(parser)

The fuzzer itself is initialized with a list of seeds, the above `FragmentMutator`, and a power schedule:

>>> seeds = ["HelloWorld"]
>>> schedule = PowerSchedule()
>>> lang_fuzzer = LangFuzzer(seeds, mutator, schedule)
>>> for i in range(10):
>>>     print(lang_fuzzer.fuzz())
HelloWorld
HelloWorld
HelloWorld
HelloWorld
HelloWorld
HelloWorld
HelloWorld
HelloWorld
HelloWorld
HelloWorld
### Fuzzing with Input Regions

The `GreyboxGrammarFuzzer` class uses two mutators:
* a _tree mutator_ (a `RegionMutator` object) that can parse existing strings to identify _regions_ in that string to be swapped or deleted.
* a _byte mutator_ to apply bit- and character-level mutations.

>>> tree_mutator = RegionMutator(parser)
>>> byte_mutator = Mutator()

The _schedule_ for the `GreyboxGrammarFuzzer` class can be a regular `PowerSchedule` object. However, a more sophisticated schedule is provided by `AFLSmartSchedule`, which assigns more [energy](GreyboxFuzzer.ipynb#Power-Schedules) to seeds that have a higher degree of validity.

>>> schedule = AFLSmartSchedule(parser)

The `GreyboxGrammarFuzzer` constructor takes a set of seeds as well as the two mutators and the schedule:

>>> aflsmart_fuzzer = GreyboxGrammarFuzzer(seeds, byte_mutator, tree_mutator, schedule)

As it relies on code coverage, it is typically combined with a `FunctionCoverageRunner`:

>>> runner = FunctionCoverageRunner(my_parser)
>>> aflsmart_outcome = aflsmart_fuzzer.runs(runner, trials=5)

For more details, source, and documentation, see
"The Fuzzing Book - Greybox Fuzzing with Grammars"
at https://www.fuzzingbook.org/html/GreyboxGrammarFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Greybox Fuzzing with Grammars
# =============================

if __name__ == '__main__':
    print('# Greybox Fuzzing with Grammars')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo("JPSfCCkuNo0")

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from typing import List, Set, Dict, Sequence, cast

from .Fuzzer import Fuzzer
from .GreyboxFuzzer import Mutator, Seed, PowerSchedule
from .GreyboxFuzzer import AdvancedMutationFuzzer, GreyboxFuzzer
from .MutationFuzzer import FunctionCoverageRunner

if __name__ == '__main__':
    Mutator().mutate("Hello World")

if __name__ == '__main__':
    population = [Seed("A"), Seed("B"), Seed("C")]
    schedule = PowerSchedule()
    hits = {
        "A": 0,
        "B": 0,
        "C": 0
    }

    for i in range(10000):
        seed = schedule.choose(population)
        hits[seed.data] += 1

    hits

from html.parser import HTMLParser

def my_parser(inp: str) -> None:
    parser = HTMLParser()
    parser.feed(inp)

if __name__ == '__main__':
    runner = FunctionCoverageRunner(my_parser)
    runner.run("Hello World")
    cov = runner.coverage()

    list(cov)[:5]  # Print 5 statements covered in HTMLParser

import time
import random

if __name__ == '__main__':
    n = 5000
    seed_input = " "  # empty seed
    runner = FunctionCoverageRunner(my_parser)
    fuzzer = GreyboxFuzzer([seed_input], Mutator(), PowerSchedule())

if __name__ == '__main__':
    start = time.time()
    fuzzer.runs(runner, trials=n)
    end = time.time()

if __name__ == '__main__':
    "It took the fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    "During this fuzzing campaign, we covered %d statements." % len(runner.coverage())

## Fuzzing with Dictionaries
## -------------------------

if __name__ == '__main__':
    print('\n## Fuzzing with Dictionaries')



class DictMutator(Mutator):
    """Mutate strings using keywords from a dictionary"""

    def __init__(self, dictionary: List[str]) -> None:
        """Constructor. `dictionary` is the list of keywords to use."""
        super().__init__()
        self.dictionary = dictionary
        self.mutators.append(self.insert_from_dictionary)

    def insert_from_dictionary(self, s: str) -> str:
        """Returns s with a keyword from the dictionary inserted"""
        pos = random.randint(0, len(s))
        random_keyword = random.choice(self.dictionary)
        return s[:pos] + random_keyword + s[pos:]

if __name__ == '__main__':
    runner = FunctionCoverageRunner(my_parser)
    dict_mutator = DictMutator(["<a>", "</a>", "<a/>", "='a'"])
    dict_fuzzer = GreyboxFuzzer([seed_input], dict_mutator, PowerSchedule())

    start = time.time()
    dict_fuzzer.runs(runner, trials=n)
    end = time.time()

    "It took the fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    "During this fuzzing campaign, we covered %d statements." % len(runner.coverage())

from .Coverage import population_coverage

if __name__ == '__main__':
    import matplotlib.pyplot as plt  # type: ignore

if __name__ == '__main__':
    _, dict_cov = population_coverage(dict_fuzzer.inputs, my_parser)
    _, fuzz_cov = population_coverage(fuzzer.inputs, my_parser)
    line_dict, = plt.plot(dict_cov, label="With Dictionary")
    line_fuzz, = plt.plot(fuzz_cov, label="Without Dictionary")
    plt.legend(handles=[line_dict, line_fuzz])
    plt.xlim(0, n)
    plt.title('Coverage over time')
    plt.xlabel('# of inputs')
    plt.ylabel('lines covered');

## Fuzzing with Input Fragments
## ----------------------------

if __name__ == '__main__':
    print('\n## Fuzzing with Input Fragments')



### Parsing and Recombining JavaScript, or How to Make 50,000 USD in Four Weeks

if __name__ == '__main__':
    print('\n### Parsing and Recombining JavaScript, or How to Make 50,000 USD in Four Weeks')



### Parsing and Recombining HTML

if __name__ == '__main__':
    print('\n### Parsing and Recombining HTML')



import string

from .Grammars import is_valid_grammar, srange, Grammar

XML_TOKENS: Set[str] = {"<id>", "<text>"}

XML_GRAMMAR: Grammar = {
    "<start>": ["<xml-tree>"],
    "<xml-tree>": ["<text>",
                   "<xml-open-tag><xml-tree><xml-close-tag>",
                   "<xml-openclose-tag>",
                   "<xml-tree><xml-tree>"],
    "<xml-open-tag>":      ["<<id>>", "<<id> <xml-attribute>>"],
    "<xml-openclose-tag>": ["<<id>/>", "<<id> <xml-attribute>/>"],
    "<xml-close-tag>":     ["</<id>>"],
    "<xml-attribute>":     ["<id>=<id>", "<xml-attribute> <xml-attribute>"],
    "<id>":                ["<letter>", "<id><letter>"],
    "<text>":              ["<text><letter_space>", "<letter_space>"],
    "<letter>":            srange(string.ascii_letters + string.digits +
                                  "\"" + "'" + "."),
    "<letter_space>":      srange(string.ascii_letters + string.digits +
                                  "\"" + "'" + " " + "\t"),
}

if __name__ == '__main__':
    assert is_valid_grammar(XML_GRAMMAR)

from .Parser import EarleyParser, Parser
from .GrammarFuzzer import display_tree, DerivationTree

if __name__ == '__main__':
    from IPython.display import display

if __name__ == '__main__':
    parser = EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS)

    for tree in parser.parse("<html>Text</html>"):
        display(display_tree(tree))

### Building the Fragment Pool

if __name__ == '__main__':
    print('\n### Building the Fragment Pool')



class FragmentMutator(Mutator):
    """Mutate inputs with input fragments from a pool"""

    def __init__(self, parser: EarleyParser) -> None:
        """Initialize empty fragment pool and add parser"""
        self.parser = parser
        self.fragments: Dict[str, List[DerivationTree]] = \
            {k: [] for k in self.parser.cgrammar}
        super().__init__()

from .Parser import terminals

class FragmentMutator(FragmentMutator):
    def add_fragment(self, fragment: DerivationTree) -> None:
        """Recursively adds fragments to the fragment pool"""
        (symbol, children) = fragment
        if not self.is_excluded(symbol):
            self.fragments[symbol].append(fragment)
            assert children is not None
            for subfragment in children:
                self.add_fragment(subfragment)

    def is_excluded(self, symbol: str) -> bool:
        """Returns true if a fragment starting with a specific
           symbol and all its decendents can be excluded"""
        return (symbol not in self.parser.grammar() or
                symbol in self.parser.tokens or
                symbol in terminals(self.parser.grammar()))

from .Timeout import Timeout

class SeedWithStructure(Seed):
    """Seeds augmented with structure info"""

    def __init__(self, data: str) -> None:
        super().__init__(data)
        self.has_structure = False
        self.structure: DerivationTree = ("<empty>", [])

class FragmentMutator(FragmentMutator):
    def add_to_fragment_pool(self, seed: SeedWithStructure) -> None:
        """Adds all fragments of a seed to the fragment pool"""
        try:  # only allow quick parsing of 200ms max
            with Timeout(0.2):
                seed.structure = next(self.parser.parse(seed.data))
                self.add_fragment(seed.structure)
            seed.has_structure = True
        except (SyntaxError, TimeoutError):
            seed.has_structure = False

from .GrammarFuzzer import tree_to_string

if __name__ == '__main__':
    valid_seed = SeedWithStructure(
        "<html><head><title>Hello</title></head><body>World<br/></body></html>")
    fragment_mutator = FragmentMutator(EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS))
    fragment_mutator.add_to_fragment_pool(valid_seed)

    for key in fragment_mutator.fragments:
        print(key)
        for f in fragment_mutator.fragments[key]:
            print("|-%s" % tree_to_string(f))

### Fragment-Based Mutation

if __name__ == '__main__':
    print('\n### Fragment-Based Mutation')



class FragmentMutator(FragmentMutator):
    def __init__(self, parser: EarleyParser) -> None:
        """Initialize mutators"""
        super().__init__(parser)
        self.seen_seeds: List[SeedWithStructure] = []

    def mutate(self, seed: SeedWithStructure) -> SeedWithStructure:
        """Implement structure-aware mutation. Memoize seeds."""
        if seed not in self.seen_seeds:
            self.seen_seeds.append(seed)
            self.add_to_fragment_pool(seed)

        return super().mutate(seed)

class FragmentMutator(FragmentMutator):
    def count_nodes(self, fragment: DerivationTree) -> int:
        """Returns the number of nodes in the fragment"""
        symbol, children = fragment
        if self.is_excluded(symbol):
            return 0

        assert children is not None
        return 1 + sum(map(self.count_nodes, children))

class FragmentMutator(FragmentMutator):
    def recursive_swap(self, fragment: DerivationTree) -> DerivationTree:
        """Recursively finds the fragment to swap."""
        symbol, children = fragment
        if self.is_excluded(symbol):
            return symbol, children

        self.to_swap -= 1
        if self.to_swap == 0: 
            return random.choice(list(self.fragments[symbol]))

        assert children is not None
        return symbol, list(map(self.recursive_swap, children))

class FragmentMutator(FragmentMutator):
    def __init__(self, parser: EarleyParser) -> None:  # type: ignore
        super().__init__(parser)
        self.mutators = [self.swap_fragment]  # type: ignore

    def swap_fragment(self, seed: SeedWithStructure) -> SeedWithStructure:
        """Substitutes a random fragment with another with the same symbol"""
        if seed.has_structure:  # type: ignore
            n_nodes = self.count_nodes(seed.structure)
            self.to_swap = random.randint(2, n_nodes)
            new_structure = self.recursive_swap(seed.structure)

            new_seed = SeedWithStructure(tree_to_string(new_structure))
            new_seed.has_structure = True
            new_seed.structure = new_structure
            return new_seed

        return seed

if __name__ == '__main__':
    valid_seed = SeedWithStructure(
        "<html><head><title>Hello</title></head><body>World<br/></body></html>")
    lf_mutator = FragmentMutator(parser)
    print(valid_seed)
    lf_mutator.mutate(valid_seed)

class FragmentMutator(FragmentMutator):
    def recursive_delete(self, fragment: DerivationTree) -> DerivationTree:
        """Recursively finds the fragment to delete"""
        symbol, children = fragment
        if self.is_excluded(symbol):
            return symbol, children

        self.to_delete -= 1
        if self.to_delete == 0:
            return symbol, []

        assert children is not None
        return symbol, list(map(self.recursive_delete, children))

class FragmentMutator(FragmentMutator):
    def __init__(self, parser):  # type: ignore
        super().__init__(parser)
        self.mutators.append(self.delete_fragment)

    def delete_fragment(self, seed: SeedWithStructure) -> SeedWithStructure:
        """Delete a random fragment"""
        if seed.has_structure:
            n_nodes = self.count_nodes(seed.structure)
            self.to_delete = random.randint(2, n_nodes)
            new_structure = self.recursive_delete(seed.structure)

            new_seed = SeedWithStructure(tree_to_string(new_structure))
            new_seed.has_structure = True
            new_seed.structure = new_structure
            # do not return an empty new_seed
            if not new_seed.data:
                return seed
            else:
                return new_seed

        return seed

### Fragment-Based Fuzzing

if __name__ == '__main__':
    print('\n### Fragment-Based Fuzzing')



class LangFuzzer(AdvancedMutationFuzzer):
    """Blackbox fuzzer mutating input fragments. Roughly based on `LangFuzz`."""

    def create_candidate(self) -> Seed:  # type: ignore
        """Returns an input generated by fuzzing a seed in the population"""
        candidate = self.schedule.choose(self.population)
        trials = random.randint(1, 4)
        for i in range(trials):
            candidate = self.mutator.mutate(candidate)

        return candidate

if __name__ == '__main__':
    n = 300
    runner = FunctionCoverageRunner(my_parser)
    mutator = FragmentMutator(EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS))
    schedule = PowerSchedule()

    lang_fuzzer = LangFuzzer([valid_seed.data], mutator, schedule)

    start = time.time()
    lang_fuzzer.runs(runner, trials=n)
    end = time.time()

    "It took LangFuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    runner = FunctionCoverageRunner(my_parser)
    mutator = Mutator()
    schedule = PowerSchedule()

    blackFuzzer = AdvancedMutationFuzzer([valid_seed.data], mutator, schedule)

    start = time.time()
    blackFuzzer.runs(runner, trials=n)
    end = time.time()

    "It took a blackbox fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    blackbox_coverage = len(runner.coverage())
    "During this fuzzing campaign, the blackbox fuzzer covered %d statements." % blackbox_coverage

from .Coverage import population_coverage

def print_stats(fuzzer, parser: Parser) -> None:
    coverage, _ = population_coverage(fuzzer.inputs, my_parser)

    has_structure = 0
    for seed in fuzzer.inputs:
        # reuse memoized information
        if hasattr(seed, "has_structure"):
            if seed.has_structure: 
                has_structure += 1
        else:
            if isinstance(seed, str):
                seed = Seed(seed)
            try:
                with Timeout(0.2):
                    next(parser.parse(seed.data))  # type: ignore
                has_structure += 1
            except (SyntaxError, TimeoutError):
                pass

    print("From the %d generated inputs, %d (%0.2f%%) can be parsed.\n"
          "In total, %d statements are covered." % (
            len(fuzzer.inputs),
            has_structure,
            100 * has_structure / len(fuzzer.inputs),
            len(coverage)))

if __name__ == '__main__':
    print_stats(lang_fuzzer, EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS))

if __name__ == '__main__':
    print_stats(blackFuzzer, EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS))

### Integration with Greybox Fuzzing

if __name__ == '__main__':
    print('\n### Integration with Greybox Fuzzing')



class GreyboxGrammarFuzzer(GreyboxFuzzer):
    """Greybox fuzzer using grammars."""

    def __init__(self, seeds: List[str],
                 byte_mutator: Mutator, tree_mutator: FragmentMutator,
                 schedule: PowerSchedule) -> None:
        """Constructor.
        `seeds` - set of inputs to mutate.
        `byte_mutator` - a byte-level mutator.
        `tree_mutator` = a tree-level mutator.
        `schedule` - a power schedule.
        """
        super().__init__(seeds, byte_mutator, schedule)
        self.tree_mutator = tree_mutator

    def create_candidate(self) -> str:
        """Returns an input generated by structural mutation 
           of a seed in the population"""
        seed = cast(SeedWithStructure, self.schedule.choose(self.population))

        # Structural mutation
        trials = random.randint(0, 4)
        for i in range(trials):
            seed = self.tree_mutator.mutate(seed)

        # Byte-level mutation
        candidate = seed.data
        if trials == 0 or not seed.has_structure or random.randint(0, 1) == 1:
            dumb_trials = min(len(seed.data), 1 << random.randint(1, 5))
            for i in range(dumb_trials):
                candidate = self.mutator.mutate(candidate)

        return candidate

if __name__ == '__main__':
    runner = FunctionCoverageRunner(my_parser)
    byte_mutator = Mutator()
    tree_mutator = FragmentMutator(EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS))
    schedule = PowerSchedule()

    gg_fuzzer = GreyboxGrammarFuzzer([valid_seed.data], byte_mutator, tree_mutator, schedule)

    start = time.time()
    gg_fuzzer.runs(runner, trials=n)
    end = time.time()

    "It took the greybox grammar fuzzer %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    print_stats(gg_fuzzer, EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS))

## Fuzzing with Input Regions
## --------------------------

if __name__ == '__main__':
    print('\n## Fuzzing with Input Regions')



### Determining Symbol Regions

if __name__ == '__main__':
    print('\n### Determining Symbol Regions')



if __name__ == '__main__':
    invalid_seed = Seed("<html><body><i>World</i><br/>>/body></html>")
    parser = EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS)
    table = parser.chart_parse(invalid_seed.data, parser.start_symbol())
    for column in table:
        print(column)
        print("---")

if __name__ == '__main__':
    cols = [col for col in table if col.states]
    parsable = invalid_seed.data[:len(cols)-1]

    print("'%s'" % invalid_seed)
    parsable

if __name__ == '__main__':
    validity = 100 * len(parsable) / len(invalid_seed.data)

    "%0.1f%% of the string can be parsed successfully." % validity

### Region-Based Mutation

if __name__ == '__main__':
    print('\n### Region-Based Mutation')



class SeedWithRegions(SeedWithStructure):
    """Seeds augmented with structure info"""

    def __init__(self, data: str) -> None:
        super().__init__(data)
        self.has_regions = False
        self.regions: Dict[str, Set] = {}

class RegionMutator(FragmentMutator):
    def add_to_fragment_pool(self, seed: SeedWithRegions) -> None:  # type: ignore
        """Mark fragments and regions in a seed file"""
        super().add_to_fragment_pool(seed)
        if not seed.has_structure:
            try:
                with Timeout(0.2):
                    seed.regions = {k: set() for k in self.parser.cgrammar}
                    for column in self.parser.chart_parse(seed.data,
                                                          self.parser.start_symbol()):
                        for state in column.states:
                            if (not self.is_excluded(state.name) and
                                    state.e_col.index - state.s_col.index > 1 and
                                    state.finished()):
                                seed.regions[state.name].add((state.s_col.index,
                                                              state.e_col.index))
                seed.has_regions = True
            except TimeoutError:
                seed.has_regions = False
        else:
            seed.has_regions = False

if __name__ == '__main__':
    invalid_seed = SeedWithRegions("<html><body><i>World</i><br/>>/body></html>")
    mutator = RegionMutator(parser)
    mutator.add_to_fragment_pool(invalid_seed)
    for symbol in invalid_seed.regions:  # type: ignore
        print(symbol)
        for (s, e) in invalid_seed.regions[symbol]:  # type: ignore
            print("|-(%d,%d) : %s" % (s, e, invalid_seed.data[s:e]))

class RegionMutator(RegionMutator):
    def swap_fragment(self, seed: SeedWithRegions) -> SeedWithRegions:  # type: ignore
        """Chooses a random region and swaps it with a fragment
           that starts with the same symbol"""
        if not seed.has_structure and seed.has_regions:
            regions = [r for r in seed.regions
                       if (len(seed.regions[r]) > 0 and
                           len(self.fragments[r]) > 0)]
            if len(regions) == 0:
                return seed

            key = random.choice(list(regions))
            s, e = random.choice(list(seed.regions[key]))
            swap_structure = random.choice(self.fragments[key])
            swap_string = tree_to_string(swap_structure)
            new_seed = SeedWithRegions(seed.data[:s] + swap_string + seed.data[e:])
            new_seed.has_structure = False
            new_seed.has_regions = False
            return new_seed
        else:
            return super().swap_fragment(seed)  # type: ignore

class RegionMutator(RegionMutator):
    def delete_fragment(self, seed: SeedWithRegions) -> SeedWithRegions:  # type: ignore
        """Deletes a random region"""
        if not seed.has_structure and seed.has_regions:
            regions = [r for r in seed.regions
                       if len(seed.regions[r]) > 0]
            if len(regions) == 0:
                return seed

            key = random.choice(list(regions))
            s, e = (0, 0)
            while (e - s < 2):
                s, e = random.choice(list(seed.regions[key]))

            new_seed = SeedWithRegions(seed.data[:s] + seed.data[e:])
            new_seed.has_structure = False
            new_seed.has_regions = False
            return new_seed
        else:
            return super().delete_fragment(seed)  # type: ignore

if __name__ == '__main__':
    simple_seed = SeedWithRegions("<b>Text</b>")
    mutator = RegionMutator(parser)
    mutator.add_to_fragment_pool(simple_seed)

    print(invalid_seed)
    mutator.mutate(invalid_seed)

### Integration with Greybox Fuzzing

if __name__ == '__main__':
    print('\n### Integration with Greybox Fuzzing')



if __name__ == '__main__':
    runner = FunctionCoverageRunner(my_parser)
    byte_mutator = Mutator()
    tree_mutator = RegionMutator(EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS))
    schedule = PowerSchedule()

    regionFuzzer = GreyboxGrammarFuzzer([valid_seed.data], byte_mutator, tree_mutator, schedule)

    start = time.time()
    regionFuzzer.runs(runner, trials = n)
    end = time.time()

    """
It took the structural greybox fuzzer with region mutator
%0.2f seconds to generate and execute %d inputs.
""" % (end - start, n)

def print_more_stats(fuzzer: GreyboxGrammarFuzzer, parser: EarleyParser):
    print_stats(fuzzer, parser)
    validity = 0.0
    total = 0
    for seed in fuzzer.population:
        if not seed.data: continue
        table = parser.chart_parse(seed.data, parser.start_symbol())
        cols = [col for col in table if col.states]
        parsable = invalid_seed.data[:len(cols)-1]
        validity += len(parsable) / len(seed.data)
        total += 1

    print("On average, %0.1f%% of a seed in the population can be successfully parsed." % (100 * validity / total))

if __name__ == '__main__':
    print_more_stats(regionFuzzer, parser)

### Focusing on Valid Seeds

if __name__ == '__main__':
    print('\n### Focusing on Valid Seeds')



import math

class AFLSmartSchedule(PowerSchedule):
    def __init__(self, parser: EarleyParser, exponent: float = 1.0):
        self.parser = parser
        self.exponent = exponent

    def parsable(self, seed: Seed) -> str:
        """Returns the substring that is parsable"""
        table = self.parser.chart_parse(seed.data, self.parser.start_symbol())
        cols = [col for col in table if col.states]
        return seed.data[:len(cols)-1]

    def degree_of_validity(self, seed: Seed) -> float:
        """Returns the proportion of a seed that is parsable"""
        if not hasattr(seed, 'validity'):
            seed.validity = (len(self.parsable(seed)) / len(seed.data)  # type: ignore
                             if len(seed.data) > 0 else 0)
        return seed.validity  # type: ignore

    def assignEnergy(self, population: Sequence[Seed]):
        """Assign exponential energy proportional to degree of validity"""
        for seed in population:
            seed.energy = ((self.degree_of_validity(seed) / math.log(len(seed.data))) ** self.exponent
                           if len(seed.data) > 1 else 0)

if __name__ == '__main__':
    smart_schedule = AFLSmartSchedule(parser)
    print("%11s: %s" % ("Entire seed", simple_seed))
    print("%11s: %s" % ("Parsable", smart_schedule.parsable(simple_seed)))

    "Degree of validity: %0.2f%%" % (100 * smart_schedule.degree_of_validity(simple_seed))

if __name__ == '__main__':
    print("%11s: %s" % ("Entire seed", invalid_seed))
    print("%11s: %s" % ("Parsable", smart_schedule.parsable(invalid_seed)))

    "Degree of validity: %0.2f%%" % (100 * smart_schedule.degree_of_validity(invalid_seed))

if __name__ == '__main__':
    runner = FunctionCoverageRunner(my_parser)
    byte_mutator = Mutator()
    tree_mutator = RegionMutator(EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS))
    schedule = AFLSmartSchedule(parser)

    aflsmart_fuzzer = GreyboxGrammarFuzzer([valid_seed.data], byte_mutator, 
                                           tree_mutator, schedule)

    start = time.time()
    aflsmart_fuzzer.runs(runner, trials=n)
    end = time.time()

    "It took AFLSmart %0.2f seconds to generate and execute %d inputs." % (end - start, n)

if __name__ == '__main__':
    print_more_stats(aflsmart_fuzzer, parser)

## Mining Seeds
## ------------

if __name__ == '__main__':
    print('\n## Mining Seeds')



## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



### Fuzzing with Dictionaries

if __name__ == '__main__':
    print('\n### Fuzzing with Dictionaries')



if __name__ == '__main__':
    dict_mutator = DictMutator(["<a>", "</a>", "<a/>", "='a'"])

if __name__ == '__main__':
    seeds = ["<html><head><title>Hello</title></head><body>World<br/></body></html>"]
    for i in range(10):
        print(dict_mutator.mutate(seeds[0]))

if __name__ == '__main__':
    runner = FunctionCoverageRunner(my_parser)
    dict_fuzzer = GreyboxFuzzer(seeds, dict_mutator, PowerSchedule())

if __name__ == '__main__':
    dict_fuzzer_outcome = dict_fuzzer.runs(runner, trials=5)

from .ClassDiagram import display_class_hierarchy
from .Coverage import Location  # minor dependency

if __name__ == '__main__':
    display_class_hierarchy([DictMutator],
                            public_methods=[
                                Mutator.__init__,
                                DictMutator.__init__,
                            ],
                            types={'DerivationTree': DerivationTree,
                                   'Location': Location},
                            project='fuzzingbook')

### Fuzzing with Input Fragments

if __name__ == '__main__':
    print('\n### Fuzzing with Input Fragments')



if __name__ == '__main__':
    parser = EarleyParser(XML_GRAMMAR, tokens=XML_TOKENS)
    mutator = FragmentMutator(parser)

if __name__ == '__main__':
    seeds = ["<html><head><title>Hello</title></head><body>World<br/></body></html>"]
    schedule = PowerSchedule()
    lang_fuzzer = LangFuzzer(seeds, mutator, schedule)

if __name__ == '__main__':
    for i in range(10):
        print(lang_fuzzer.fuzz())

if __name__ == '__main__':
    display_class_hierarchy([LangFuzzer, FragmentMutator],
                            public_methods=[
                                Fuzzer.__init__,
                                Fuzzer.fuzz,
                                Fuzzer.run,
                                Fuzzer.runs,
                                AdvancedMutationFuzzer.__init__,
                                AdvancedMutationFuzzer.fuzz,
                                GreyboxFuzzer.run,
                                Mutator.__init__,
                                FragmentMutator.__init__,
                                FragmentMutator.add_to_fragment_pool,
                            ],
                            types={'DerivationTree': DerivationTree,
                                   'Location': Location},
                            project='fuzzingbook')

### Fuzzing with Input Regions

if __name__ == '__main__':
    print('\n### Fuzzing with Input Regions')



if __name__ == '__main__':
    tree_mutator = RegionMutator(parser)
    byte_mutator = Mutator()

if __name__ == '__main__':
    schedule = AFLSmartSchedule(parser)

if __name__ == '__main__':
    aflsmart_fuzzer = GreyboxGrammarFuzzer(seeds, byte_mutator, tree_mutator, schedule)

if __name__ == '__main__':
    runner = FunctionCoverageRunner(my_parser)
    aflsmart_outcome = aflsmart_fuzzer.runs(runner, trials=5)

if __name__ == '__main__':
    display_class_hierarchy([GreyboxGrammarFuzzer, AFLSmartSchedule, RegionMutator],
                            public_methods=[
                                Fuzzer.__init__,
                                Fuzzer.fuzz,
                                Fuzzer.run,
                                Fuzzer.runs,
                                AdvancedMutationFuzzer.__init__,
                                AdvancedMutationFuzzer.fuzz,
                                GreyboxFuzzer.run,
                                GreyboxGrammarFuzzer.__init__,
                                GreyboxGrammarFuzzer.run,
                                AFLSmartSchedule.__init__,
                                PowerSchedule.__init__,
                                Mutator.__init__,
                                FragmentMutator.__init__,
                                FragmentMutator.add_to_fragment_pool,
                                RegionMutator.__init__,
                            ],
                            types={'DerivationTree': DerivationTree,
                                   'Location': Location},
                            project='fuzzingbook')

## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: The Big Greybox Fuzzer Shoot-Out

if __name__ == '__main__':
    print('\n### Exercise 1: The Big Greybox Fuzzer Shoot-Out')


