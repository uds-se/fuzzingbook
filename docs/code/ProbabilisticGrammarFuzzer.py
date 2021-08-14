#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Probabilistic Grammar Fuzzing" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/ProbabilisticGrammarFuzzer.html
# Last change: 2021-06-04 14:56:08+02:00
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
The Fuzzing Book - Probabilistic Grammar Fuzzing

This file can be _executed_ as a script, running all experiments:

    $ python ProbabilisticGrammarFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.ProbabilisticGrammarFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/ProbabilisticGrammarFuzzer.html

A _probabilistic_ grammar allows to attach individual _probabilities_ to production rules.  To set the probability of an individual expansion `S` to the value `X` (between 0 and 1), replace it with a pair

(opts(S, prob=X))


If we want to ensure that 90% of phone numbers generated have an area code starting with `9`, we can write:

>>> from Grammars import US_PHONE_GRAMMAR, extend_grammar, opts
>>> PROBABILISTIC_US_PHONE_GRAMMAR = extend_grammar(US_PHONE_GRAMMAR,
>>> {
>>>       "": ["2", "3", "4", "5", "6", "7", "8", 
>>>                       ("9", opts(prob=0.9))],                                              
>>> })

A `ProbabilisticGrammarFuzzer` will extract and interpret these options.  Here is an example:

>>> probabilistic_us_phone_fuzzer = ProbabilisticGrammarFuzzer(PROBABILISTIC_US_PHONE_GRAMMAR)
>>> [probabilistic_us_phone_fuzzer.fuzz() for i in range(5)]
['(965)906-9430',
 '(977)953-0547',
 '(973)971-2092',
 '(944)961-7546',
 '(929)918-3600']

As you can see, the large majority of area codes now starts with `9`.


For more details, source, and documentation, see
"The Fuzzing Book - Probabilistic Grammar Fuzzing"
at https://www.fuzzingbook.org/html/ProbabilisticGrammarFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Probabilistic Grammar Fuzzing
# =============================

if __name__ == '__main__':
    print('# Probabilistic Grammar Fuzzing')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## The Law of Leading Digits
## -------------------------

if __name__ == '__main__':
    print('\n## The Law of Leading Digits')



def first_digit_via_string(x):
    return ord(repr(x)[0]) - ord('0')

if __name__ == '__main__':
    first_digit_via_string(2001)

import math

def first_digit_via_log(x):
    frac, whole = math.modf(math.log10(x))
    return int(10 ** frac)

if __name__ == '__main__':
    first_digit_via_log(2001)

if __name__ == '__main__':
    (math.log10(1), math.log10(2))

if __name__ == '__main__':
    (math.log10(2), math.log10(3))

def prob_leading_digit(d):
    return math.log10(d + 1) - math.log10(d)

if __name__ == '__main__':
    digit_probs = [prob_leading_digit(d) for d in range(1, 10)]
    [(d, "%.2f" % digit_probs[d - 1]) for d in range(1, 10)]

if __name__ == '__main__':
    import matplotlib.pyplot as plt

if __name__ == '__main__':
    labels = range(1, 10)
    fig1, ax1 = plt.subplots()
    ax1.pie(digit_probs, labels=labels, shadow=True, autopct='%1.1f%%',
            counterclock=False, startangle=90)
    ax1.axis('equal');

## Specifying Probabilities
## ------------------------

if __name__ == '__main__':
    print('\n## Specifying Probabilities')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .GrammarFuzzer import GrammarFuzzer, all_terminals, display_tree

from .Grammars import is_valid_grammar, EXPR_GRAMMAR, START_SYMBOL, crange, syntax_diagram
from .Grammars import opts, exp_string, exp_opt, set_opts

PROBABILISTIC_EXPR_GRAMMAR = {
    "<start>":
        ["<expr>"],

    "<expr>":
        [("<term> + <expr>", opts(prob=0.1)),
         ("<term> - <expr>", opts(prob=0.2)),
         "<term>"],

    "<term>":
        [("<factor> * <term>", opts(prob=0.1)),
         ("<factor> / <term>", opts(prob=0.1)),
         "<factor>"
         ],

    "<factor>":
        ["+<factor>", "-<factor>", "(<expr>)",
            "<leadinteger>", "<leadinteger>.<integer>"],

    "<leadinteger>":
        ["<leaddigit><integer>", "<leaddigit>"],

    # Benford's law: frequency distribution of leading digits
    "<leaddigit>":
        [("1", opts(prob=0.301)),
         ("2", opts(prob=0.176)),
         ("3", opts(prob=0.125)),
         ("4", opts(prob=0.097)),
         ("5", opts(prob=0.079)),
         ("6", opts(prob=0.067)),
         ("7", opts(prob=0.058)),
         ("8", opts(prob=0.051)),
         ("9", opts(prob=0.046)),
         ],

    # Remaining digits are equally distributed
    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}

if __name__ == '__main__':
    assert is_valid_grammar(PROBABILISTIC_EXPR_GRAMMAR, supported_opts={'prob'})

if __name__ == '__main__':
    PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"]

if __name__ == '__main__':
    leaddigit_expansion = PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"][0]
    leaddigit_expansion

if __name__ == '__main__':
    exp_string(leaddigit_expansion)

def exp_prob(expansion):
    """Return the options of an expansion"""
    return exp_opt(expansion, 'prob')

if __name__ == '__main__':
    exp_prob(leaddigit_expansion)

if __name__ == '__main__':
    f = GrammarFuzzer(PROBABILISTIC_EXPR_GRAMMAR)
    f.fuzz()

from .GrammarCoverageFuzzer import GrammarCoverageFuzzer  # minor dependency

if __name__ == '__main__':
    f = GrammarCoverageFuzzer(PROBABILISTIC_EXPR_GRAMMAR)
    f.fuzz()

## Computing Probabilities
## -----------------------

if __name__ == '__main__':
    print('\n## Computing Probabilities')



### Distributing Probabilities

if __name__ == '__main__':
    print('\n### Distributing Probabilities')



def exp_probabilities(expansions, nonterminal="<symbol>"):
    probabilities = [exp_prob(expansion) for expansion in expansions]
    prob_dist = prob_distribution(probabilities, nonterminal)

    prob_mapping = {}
    for i in range(len(expansions)):
        expansion = exp_string(expansions[i])
        prob_mapping[expansion] = prob_dist[i]

    return prob_mapping

def prob_distribution(probabilities, nonterminal="<symbol>"):
    epsilon = 0.00001

    number_of_unspecified_probabilities = probabilities.count(None)
    if number_of_unspecified_probabilities == 0:
        assert abs(sum(probabilities) - 1.0) < epsilon, \
            nonterminal + ": sum of probabilities must be 1.0"
        return probabilities

    sum_of_specified_probabilities = 0.0
    for p in probabilities:
        if p is not None:
            sum_of_specified_probabilities += p
    assert 0 <= sum_of_specified_probabilities <= 1.0, \
        nonterminal + ": sum of specified probabilities must be between 0.0 and 1.0"

    default_probability = ((1.0 - sum_of_specified_probabilities)
                           / number_of_unspecified_probabilities)
    all_probabilities = []
    for p in probabilities:
        if p is None:
            p = default_probability
        all_probabilities.append(p)

    assert abs(sum(all_probabilities) - 1.0) < epsilon
    return all_probabilities

if __name__ == '__main__':
    print(exp_probabilities(PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"]))

if __name__ == '__main__':
    print(exp_probabilities(PROBABILISTIC_EXPR_GRAMMAR["<digit>"]))

if __name__ == '__main__':
    exp_probabilities(PROBABILISTIC_EXPR_GRAMMAR["<expr>"])

### Checking Probabilities

if __name__ == '__main__':
    print('\n### Checking Probabilities')



def is_valid_probabilistic_grammar(grammar, start_symbol=START_SYMBOL):
    if not is_valid_grammar(grammar, start_symbol):
        return False

    for nonterminal in grammar:
        expansions = grammar[nonterminal]
        prob_dist = exp_probabilities(expansions, nonterminal)

    return True

if __name__ == '__main__':
    assert is_valid_probabilistic_grammar(PROBABILISTIC_EXPR_GRAMMAR)

if __name__ == '__main__':
    assert is_valid_probabilistic_grammar(EXPR_GRAMMAR)

from .ExpectError import ExpectError

if __name__ == '__main__':
    with ExpectError():
        assert is_valid_probabilistic_grammar({"<start>": [("1", opts(prob=0.5))]})

if __name__ == '__main__':
    with ExpectError():
        assert is_valid_probabilistic_grammar(
            {"<start>": [("1", opts(prob=1.5)), "2"]})

## Expanding by Probability
## ------------------------

if __name__ == '__main__':
    print('\n## Expanding by Probability')



import random

class ProbabilisticGrammarFuzzer(GrammarFuzzer):
    def check_grammar(self):
        super().check_grammar()
        assert is_valid_probabilistic_grammar(self.grammar)

    def supported_opts(self):
        return super().supported_opts() | {'prob'}

class ProbabilisticGrammarFuzzer(ProbabilisticGrammarFuzzer):
    def choose_node_expansion(self, node, possible_children):
        (symbol, tree) = node
        expansions = self.grammar[symbol]
        probabilities = exp_probabilities(expansions)

        weights = []
        for child in possible_children:
            expansion = all_terminals((node, child))
            child_weight = probabilities[expansion]
            if self.log:
                print(repr(expansion), "p =", child_weight)
            weights.append(child_weight)

        if sum(weights) == 0:
            # No alternative (probably expanding at minimum cost)
            weights = None

        return random.choices(
            range(len(possible_children)), weights=weights)[0]

if __name__ == '__main__':
    natural_fuzzer = ProbabilisticGrammarFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leadinteger>")
    print([natural_fuzzer.fuzz() for i in range(20)])

if __name__ == '__main__':
    integer_fuzzer = GrammarFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leadinteger>")
    print([integer_fuzzer.fuzz() for i in range(20)])

if __name__ == '__main__':
    leaddigit_fuzzer = ProbabilisticGrammarFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leaddigit>")
    leaddigit_fuzzer.fuzz()

if __name__ == '__main__':
    trials = 10000

    count = {}
    for c in crange('0', '9'):
        count[c] = 0

    for i in range(trials):
        count[leaddigit_fuzzer.fuzz()] += 1

    print([(digit, count[digit] / trials) for digit in count])

## Directed Fuzzing
## ----------------

if __name__ == '__main__':
    print('\n## Directed Fuzzing')



def set_prob(grammar, symbol, expansion, prob):
    """Set the probability of the given expansion of grammar[symbol]"""
    set_opts(grammar, symbol, expansion, opts(prob=prob))

from .Grammars import URL_GRAMMAR, extend_grammar

if __name__ == '__main__':
    probabilistic_url_grammar = extend_grammar(URL_GRAMMAR)
    set_prob(probabilistic_url_grammar, "<scheme>", "ftps", 0.8)
    assert is_valid_probabilistic_grammar(probabilistic_url_grammar)

if __name__ == '__main__':
    probabilistic_url_grammar["<scheme>"]

if __name__ == '__main__':
    prob_url_fuzzer = ProbabilisticGrammarFuzzer(probabilistic_url_grammar)
    for i in range(10):
        print(prob_url_fuzzer.fuzz())

if __name__ == '__main__':
    set_prob(probabilistic_url_grammar, "<scheme>", "ftps", 0.0)
    assert is_valid_probabilistic_grammar(probabilistic_url_grammar)

if __name__ == '__main__':
    prob_url_fuzzer = ProbabilisticGrammarFuzzer(probabilistic_url_grammar)
    for i in range(10):
        print(prob_url_fuzzer.fuzz())

from .Grammars import EXPR_GRAMMAR

if __name__ == '__main__':
    probabilistic_expr_grammar = extend_grammar(EXPR_GRAMMAR)
    probabilistic_expr_grammar["<expr>"]

if __name__ == '__main__':
    set_prob(probabilistic_expr_grammar, "<expr>", "<term>", 0.0)
    assert is_valid_probabilistic_grammar(probabilistic_expr_grammar)

if __name__ == '__main__':
    prob_expr_fuzzer = ProbabilisticGrammarFuzzer(probabilistic_expr_grammar)
    prob_expr_fuzzer.fuzz()

## Probabilities in Context
## ------------------------

if __name__ == '__main__':
    print('\n## Probabilities in Context')



def decrange(start, end):
    """Return a list with string representations of numbers in the range [start, end)"""
    return [repr(n) for n in range(start, end)]

IP_ADDRESS_GRAMMAR = {
    "<start>": ["<address>"],
    "<address>": ["<octet>.<octet>.<octet>.<octet>"],
    # ["0", "1", "2", ..., "255"]
    "<octet>": decrange(0, 256)
}

if __name__ == '__main__':
    print(IP_ADDRESS_GRAMMAR["<octet>"][:20])

if __name__ == '__main__':
    assert is_valid_grammar(IP_ADDRESS_GRAMMAR)

if __name__ == '__main__':
    ip_fuzzer = ProbabilisticGrammarFuzzer(IP_ADDRESS_GRAMMAR)
    ip_fuzzer.fuzz()

if __name__ == '__main__':
    probabilistic_ip_address_grammar = extend_grammar(IP_ADDRESS_GRAMMAR)
    set_prob(probabilistic_ip_address_grammar, "<octet>", "127", 0.8)

if __name__ == '__main__':
    probabilistic_ip_fuzzer = ProbabilisticGrammarFuzzer(
        probabilistic_ip_address_grammar)
    probabilistic_ip_fuzzer.fuzz()

from .GrammarCoverageFuzzer import duplicate_context  # minor dependency

if __name__ == '__main__':
    probabilistic_ip_address_grammar = extend_grammar(IP_ADDRESS_GRAMMAR)
    duplicate_context(probabilistic_ip_address_grammar, "<address>")

if __name__ == '__main__':
    probabilistic_ip_address_grammar["<address>"]

if __name__ == '__main__':
    set_prob(probabilistic_ip_address_grammar, "<octet-1>", "127", 1.0)
    set_prob(probabilistic_ip_address_grammar, "<octet-2>", "0", 1.0)

if __name__ == '__main__':
    assert is_valid_probabilistic_grammar(probabilistic_ip_address_grammar)

if __name__ == '__main__':
    probabilistic_ip_fuzzer = ProbabilisticGrammarFuzzer(
        probabilistic_ip_address_grammar)
    [probabilistic_ip_fuzzer.fuzz() for i in range(5)]

## Learning Probabilities from Samples
## -----------------------------------

if __name__ == '__main__':
    print('\n## Learning Probabilities from Samples')



### Counting Expansions

if __name__ == '__main__':
    print('\n### Counting Expansions')



from .Parser import Parser, EarleyParser, PEGParser

IP_ADDRESS_TOKENS = {"<octet>"}  # EarleyParser needs explicit tokens

if __name__ == '__main__':
    parser = EarleyParser(IP_ADDRESS_GRAMMAR)

if __name__ == '__main__':
    tree, *_ = parser.parse("127.0.0.1")
    display_tree(tree)

class ExpansionCountMiner(object):
    def __init__(self, parser, log=False):
        assert isinstance(parser, Parser)
        self.grammar = extend_grammar(parser.grammar())
        self.parser = parser
        self.log = log
        self.reset()

from .GrammarCoverageFuzzer import expansion_key  # minor dependency

from .Grammars import is_nonterminal

class ExpansionCountMiner(ExpansionCountMiner):
    def reset(self):
        self.expansion_counts = {}

    def add_coverage(self, symbol, children):
        key = expansion_key(symbol, children)

        if self.log:
            print("Found", key)

        if key not in self.expansion_counts:
            self.expansion_counts[key] = 0
        self.expansion_counts[key] += 1

    def add_tree(self, tree):
        (symbol, children) = tree
        if not is_nonterminal(symbol):
            return

        direct_children = [
            (symbol, None) if is_nonterminal(symbol) else (
                symbol, []) for symbol, c in children]
        self.add_coverage(symbol, direct_children)

        for c in children:
            self.add_tree(c)

class ExpansionCountMiner(ExpansionCountMiner):
    def count_expansions(self, inputs):
        for inp in inputs:
            tree, *_ = self.parser.parse(inp)
            self.add_tree(tree)

    def counts(self):
        return self.expansion_counts

if __name__ == '__main__':
    expansion_count_miner = ExpansionCountMiner(EarleyParser(IP_ADDRESS_GRAMMAR))

if __name__ == '__main__':
    expansion_count_miner.count_expansions(["127.0.0.1", "1.2.3.4"])
    expansion_count_miner.counts()

### Assigning Probabilities

if __name__ == '__main__':
    print('\n### Assigning Probabilities')



class ProbabilisticGrammarMiner(ExpansionCountMiner):
    def set_probabilities(self, counts):
        for symbol in self.grammar:
            self.set_expansion_probabilities(symbol, counts)

    def set_expansion_probabilities(self, symbol, counts):
        expansions = self.grammar[symbol]
        if len(expansions) == 1:
            set_prob(self.grammar, symbol, expansions[0], None)
            return

        expansion_counts = [
            counts.get(
                expansion_key(
                    symbol,
                    expansion),
                0) for expansion in expansions]
        total = sum(expansion_counts)
        for i, expansion in enumerate(expansions):
            p = expansion_counts[i] / total if total > 0 else None
            # if self.log:
            #     print("Setting", expansion_key(symbol, expansion), p)
            set_prob(self.grammar, symbol, expansion, p)

class ProbabilisticGrammarMiner(ProbabilisticGrammarMiner):
    def mine_probabilistic_grammar(self, inputs):
        self.count_expansions(inputs)
        self.set_probabilities(self.counts())
        return self.grammar

if __name__ == '__main__':
    probabilistic_grammar_miner = ProbabilisticGrammarMiner(
        EarleyParser(IP_ADDRESS_GRAMMAR))

if __name__ == '__main__':
    probabilistic_ip_address_grammar = probabilistic_grammar_miner.mine_probabilistic_grammar([
                                                                                              "127.0.0.1", "1.2.3.4"])

if __name__ == '__main__':
    assert is_valid_probabilistic_grammar(probabilistic_ip_address_grammar)

if __name__ == '__main__':
    [expansion for expansion in probabilistic_ip_address_grammar['<octet>']
        if exp_prob(expansion) > 0]

if __name__ == '__main__':
    probabilistic_ip_fuzzer = ProbabilisticGrammarFuzzer(
        probabilistic_ip_address_grammar)
    [probabilistic_ip_fuzzer.fuzz() for i in range(10)]

### Testing Common Features

if __name__ == '__main__':
    print('\n### Testing Common Features')



URL_SAMPLE = [
    "https://user:password@cispa.saarland:80/",
    "https://fuzzingbook.com?def=56&x89=3&x46=48&def=def",
    "https://cispa.saarland:80/def?def=7&x23=abc",
    "https://fuzzingbook.com:80/",
    "https://fuzzingbook.com:80/abc?def=abc&abc=x14&def=abc&abc=2&def=38",
    "ftps://fuzzingbook.com/x87",
    "https://user:password@fuzzingbook.com:6?def=54&x44=abc",
    "http://fuzzingbook.com:80?x33=25&def=8",
    "http://fuzzingbook.com:8080/def",
]

URL_TOKENS = {"<scheme>", "<userinfo>", "<host>", "<port>", "<id>"}

if __name__ == '__main__':
    url_parser = EarleyParser(URL_GRAMMAR, tokens=URL_TOKENS)
    url_input = URL_SAMPLE[2]
    print(url_input)
    tree, *_ = url_parser.parse(url_input)
    display_tree(tree)

if __name__ == '__main__':
    probabilistic_grammar_miner = ProbabilisticGrammarMiner(url_parser)
    probabilistic_url_grammar = probabilistic_grammar_miner.mine_probabilistic_grammar(
        URL_SAMPLE)

if __name__ == '__main__':
    print(probabilistic_grammar_miner.counts())

if __name__ == '__main__':
    probabilistic_url_grammar['<scheme>']

if __name__ == '__main__':
    probabilistic_url_grammar['<params>']

if __name__ == '__main__':
    g = ProbabilisticGrammarFuzzer(probabilistic_url_grammar)
    [g.fuzz() for i in range(10)]

### Testing Uncommon Features

if __name__ == '__main__':
    print('\n### Testing Uncommon Features')



import copy

def invert_expansion(expansion):
    def sort_by_prob(x):
        index, prob = x
        return prob if prob is not None else 0

    inverted_expansion = copy.deepcopy(expansion)
    indexes = [(index, exp_prob(alternative))
               for index, alternative in enumerate(expansion)]
    indexes.sort(key=sort_by_prob)
    indexes = [i for (i, _) in indexes]

    for j in range(len(indexes)):
        k = len(indexes) - 1 - j
        # print(indexes[j], "gets", indexes[k])
        inverted_expansion[indexes[j]
                           ][1]['prob'] = expansion[indexes[k]][1]['prob']

    return inverted_expansion

if __name__ == '__main__':
    probabilistic_url_grammar['<scheme>']

if __name__ == '__main__':
    invert_expansion(probabilistic_url_grammar['<scheme>'])

if __name__ == '__main__':
    invert_expansion(invert_expansion(probabilistic_url_grammar['<scheme>']))

def invert_probs(grammar):
    inverted_grammar = extend_grammar(grammar)
    for symbol in grammar:
        inverted_grammar[symbol] = invert_expansion(grammar[symbol])
    return inverted_grammar

if __name__ == '__main__':
    probabilistic_url_grammar["<digit>"]

if __name__ == '__main__':
    inverted_probabilistic_url_grammar = invert_probs(probabilistic_url_grammar)
    inverted_probabilistic_url_grammar["<digit>"]

if __name__ == '__main__':
    g = ProbabilisticGrammarFuzzer(inverted_probabilistic_url_grammar)
    [g.fuzz() for i in range(10)]

### Learning Probabilities from Input Slices

if __name__ == '__main__':
    print('\n### Learning Probabilities from Input Slices')



from .Coverage import Coverage, cgi_decode
from .Grammars import CGI_GRAMMAR

if __name__ == '__main__':
    cgi_fuzzer = GrammarFuzzer(CGI_GRAMMAR)

if __name__ == '__main__':
    trials = 100
    coverage = {}

    for i in range(trials):
        cgi_input = cgi_fuzzer.fuzz()
        with Coverage() as cov:
            cgi_decode(cgi_input)
        coverage[cgi_input] = cov.coverage()

if __name__ == '__main__':
    coverage_slice = [cgi_input for cgi_input in coverage
                      if ('cgi_decode', 25) in coverage[cgi_input]]

if __name__ == '__main__':
    print(coverage_slice)

if __name__ == '__main__':
    len(coverage_slice) / trials

if __name__ == '__main__':
    probabilistic_grammar_miner = ProbabilisticGrammarMiner(
        EarleyParser(CGI_GRAMMAR))
    probabilistic_cgi_grammar = probabilistic_grammar_miner.mine_probabilistic_grammar(
        coverage_slice)

if __name__ == '__main__':
    assert is_valid_probabilistic_grammar(probabilistic_cgi_grammar)

if __name__ == '__main__':
    probabilistic_cgi_grammar['<letter>']

if __name__ == '__main__':
    probabilistic_cgi_fuzzer = ProbabilisticGrammarFuzzer(
        probabilistic_cgi_grammar)
    print([probabilistic_cgi_fuzzer.fuzz() for i in range(20)])

if __name__ == '__main__':
    trials = 100
    coverage = {}

    for i in range(trials):
        cgi_input = probabilistic_cgi_fuzzer.fuzz()
        with Coverage() as cov:
            cgi_decode(cgi_input)
        coverage[cgi_input] = cov.coverage()

if __name__ == '__main__':
    coverage_slice = [cgi_input for cgi_input in coverage
                      if ('cgi_decode', 25) in coverage[cgi_input]]

if __name__ == '__main__':
    len(coverage_slice) / trials

if __name__ == '__main__':
    for run in range(3):
        probabilistic_cgi_grammar = probabilistic_grammar_miner.mine_probabilistic_grammar(
            coverage_slice)
        probabilistic_cgi_fuzzer = ProbabilisticGrammarFuzzer(
            probabilistic_cgi_grammar)

        trials = 100
        coverage = {}

        for i in range(trials):
            cgi_input = probabilistic_cgi_fuzzer.fuzz()
            with Coverage() as cov:
                cgi_decode(cgi_input)
            coverage[cgi_input] = cov.coverage()

        coverage_slice = [cgi_input for cgi_input in coverage
                          if ('cgi_decode', 25) in coverage[cgi_input]]

if __name__ == '__main__':
    len(coverage_slice) / trials

## Detecting Unnatural Numbers
## ---------------------------

if __name__ == '__main__':
    print('\n## Detecting Unnatural Numbers')



if __name__ == '__main__':
    sample_size = 1000
    random_integer_fuzzer = GrammarFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR,
        start_symbol="<leaddigit>")
    random_integers = [random_integer_fuzzer.fuzz() for i in range(sample_size)]

if __name__ == '__main__':
    random_counts = [random_integers.count(c) for c in crange('1', '9')]
    random_counts

if __name__ == '__main__':
    expected_prob_counts = [
        exp_prob(
            PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"][i]) *
        sample_size for i in range(9)]
    print(expected_prob_counts)

if __name__ == '__main__':
    expected_random_counts = [sample_size / 9 for i in range(9)]
    print(expected_random_counts)

if __name__ == '__main__':
    from scipy.stats import chisquare

if __name__ == '__main__':
    chisquare(random_counts, expected_prob_counts)

if __name__ == '__main__':
    chisquare(random_counts, expected_random_counts)

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



from .Grammars import US_PHONE_GRAMMAR, extend_grammar, opts

PROBABILISTIC_US_PHONE_GRAMMAR = extend_grammar(US_PHONE_GRAMMAR,
{
      "<lead-digit>": ["2", "3", "4", "5", "6", "7", "8", 
                      ("9", opts(prob=0.9))],                                              
})

if __name__ == '__main__':
    probabilistic_us_phone_fuzzer = ProbabilisticGrammarFuzzer(PROBABILISTIC_US_PHONE_GRAMMAR)
    [probabilistic_us_phone_fuzzer.fuzz() for i in range(5)]

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Probabilistic Fuzzing with Coverage

if __name__ == '__main__':
    print('\n### Exercise 1: Probabilistic Fuzzing with Coverage')



from .bookutils import inheritance_conflicts

if __name__ == '__main__':
    inheritance_conflicts(GrammarCoverageFuzzer, ProbabilisticGrammarFuzzer)

class ProbabilisticGrammarCoverageFuzzer(
        GrammarCoverageFuzzer, ProbabilisticGrammarFuzzer):
    # Choose uncovered expansions first
    def choose_node_expansion(self, node, possible_children):
        return GrammarCoverageFuzzer.choose_node_expansion(
            self, node, possible_children)

    # Among uncovered expansions, pick by (relative) probability
    def choose_uncovered_node_expansion(self, node, possible_children):
        return ProbabilisticGrammarFuzzer.choose_node_expansion(
            self, node, possible_children)

    # For covered nodes, pick by probability, too
    def choose_covered_node_expansion(self, node, possible_children):
        return ProbabilisticGrammarFuzzer.choose_node_expansion(
            self, node, possible_children)

if __name__ == '__main__':
    cov_leaddigit_fuzzer = ProbabilisticGrammarCoverageFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leaddigit>")
    print([cov_leaddigit_fuzzer.fuzz() for i in range(9)])

if __name__ == '__main__':
    trials = 10000

    count = {}
    for c in crange('0', '9'):
        count[c] = 0

    for i in range(trials):
        count[cov_leaddigit_fuzzer.fuzz()] += 1

    print([(digit, count[digit] / trials) for digit in count])

### Exercise 2: Learning from Past Bugs

if __name__ == '__main__':
    print('\n### Exercise 2: Learning from Past Bugs')


