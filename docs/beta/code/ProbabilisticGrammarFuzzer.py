#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/ProbabilisticGrammarFuzzer.html
# Last change: 2018-11-13 11:11:11+01:00
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


# # Probabilistic Grammar Fuzzing

if __name__ == "__main__":
    print('# Probabilistic Grammar Fuzzing')




# ## The Law of Leading Digits

if __name__ == "__main__":
    print('\n## The Law of Leading Digits')




def first_digit_via_string(x):
    return ord(repr(x)[0]) - ord('0')

if __name__ == "__main__":
    first_digit_via_string(2001)


import math

def first_digit_via_log(x):
    frac, whole = math.modf(math.log10(x))
    return int(10 ** frac)

if __name__ == "__main__":
    first_digit_via_log(2001)


if __name__ == "__main__":
    (math.log10(1), math.log10(2))


if __name__ == "__main__":
    (math.log10(2), math.log10(3))


def prob_leading_digit(d):
    return math.log10(d + 1) - math.log10(d)

if __name__ == "__main__":
    digit_probs = [prob_leading_digit(d) for d in range(1, 10)]
    [(d, "%.2f" % digit_probs[d - 1]) for d in range(1, 10)]


import matplotlib.pyplot as plt

if __name__ == "__main__":
    labels = range(1, 10)
    fig1, ax1 = plt.subplots()
    ax1.pie(digit_probs, labels=labels, shadow=True, autopct='%1.1f%%',
            counterclock=False, startangle=90)
    ax1.axis('equal')


# ## Specifying Probabilities

if __name__ == "__main__":
    print('\n## Specifying Probabilities')




def opts(**kwargs):
    return kwargs

if __name__ == "__main__":
    opts(prob=0.50)


import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer, all_terminals
else:
    from .GrammarFuzzer import GrammarFuzzer, all_terminals


if __package__ is None or __package__ == "":
    from Grammars import is_valid_grammar, EXPR_GRAMMAR, START_SYMBOL, crange
else:
    from .Grammars import is_valid_grammar, EXPR_GRAMMAR, START_SYMBOL, crange


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

if __name__ == "__main__":
    assert is_valid_grammar(PROBABILISTIC_EXPR_GRAMMAR)


if __name__ == "__main__":
    PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"]


def exp_string(expansion):
    """Return the string to be expanded"""
    if isinstance(expansion, str):
        return expansion
    return expansion[0]

if __name__ == "__main__":
    leaddigit_expansion = PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"][0]
    leaddigit_expansion


if __name__ == "__main__":
    exp_string(leaddigit_expansion)


def exp_opts(expansion):
    """Return the options of an expansion"""
    if isinstance(expansion, str):
        return None
    return expansion[1]

if __name__ == "__main__":
    exp_opts(leaddigit_expansion)


def exp_prob(expansion):
    """Return the specified probability, or None if unspecified"""
    if isinstance(expansion, str):
        return None
    return exp_opts(expansion)['prob']

if __name__ == "__main__":
    exp_prob(leaddigit_expansion)


if __name__ == "__main__":
    f = GrammarFuzzer(PROBABILISTIC_EXPR_GRAMMAR)
    f.fuzz()


if __package__ is None or __package__ == "":
    from GrammarCoverageFuzzer import GrammarCoverageFuzzer
else:
    from .GrammarCoverageFuzzer import GrammarCoverageFuzzer


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(PROBABILISTIC_EXPR_GRAMMAR)
    f.fuzz()


# ## Computing Probabilities

if __name__ == "__main__":
    print('\n## Computing Probabilities')




# ### Distributing Probabilities

if __name__ == "__main__":
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

if __name__ == "__main__":
    print(exp_probabilities(PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"]))


if __name__ == "__main__":
    print(exp_probabilities(PROBABILISTIC_EXPR_GRAMMAR["<digit>"]))


if __name__ == "__main__":
    exp_probabilities(PROBABILISTIC_EXPR_GRAMMAR["<expr>"])


# ### Checking Probabilities

if __name__ == "__main__":
    print('\n### Checking Probabilities')




def is_valid_probabilistic_grammar(grammar, start_symbol=START_SYMBOL):
    if not is_valid_grammar(grammar, start_symbol):
        return False

    for nonterminal in grammar:
        expansions = grammar[nonterminal]
        prob_dist = exp_probabilities(expansions, nonterminal)

    return True

if __name__ == "__main__":
    assert is_valid_probabilistic_grammar(PROBABILISTIC_EXPR_GRAMMAR)


if __name__ == "__main__":
    assert is_valid_probabilistic_grammar(EXPR_GRAMMAR)


if __package__ is None or __package__ == "":
    from ExpectError import ExpectError
else:
    from .ExpectError import ExpectError


if __name__ == "__main__":
    with ExpectError():
        assert is_valid_probabilistic_grammar({"<start>": [("1", opts(prob=0.5))]})


if __name__ == "__main__":
    with ExpectError():
        assert is_valid_probabilistic_grammar(
            {"<start>": [("1", opts(prob=1.5)), "2"]})


# ## Expanding by Probability

if __name__ == "__main__":
    print('\n## Expanding by Probability')




import random

class ProbabilisticGrammarFuzzer(GrammarFuzzer):
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

        return random.choices(range(len(possible_children)), weights=weights)[0]

if __name__ == "__main__":
    natural_fuzzer = ProbabilisticGrammarFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leadinteger>")
    print([natural_fuzzer.fuzz() for i in range(20)])


if __name__ == "__main__":
    integer_fuzzer = GrammarFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leadinteger>")
    print([integer_fuzzer.fuzz() for i in range(20)])


if __name__ == "__main__":
    leaddigit_fuzzer = ProbabilisticGrammarFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leaddigit>")
    leaddigit_fuzzer.fuzz()


if __name__ == "__main__":
    trials = 10000

    count = {}
    for c in crange('0', '9'):
        count[c] = 0

    for i in range(trials):
        count[leaddigit_fuzzer.fuzz()] += 1

    print([(digit, count[digit] / trials) for digit in count])


# ## Directed Fuzzing

if __name__ == "__main__":
    print('\n## Directed Fuzzing')




if __package__ is None or __package__ == "":
    from Grammars import URL_GRAMMAR
else:
    from .Grammars import URL_GRAMMAR


def set_opts(grammar, symbol, expansion, opts=None):
    """Set the options of the given expansion of grammar[symbol] to opts"""
    expansions = grammar[symbol]
    for i in range(len(expansions)):
        exp = expansions[i]
        if exp_string(exp) == expansion:
            new_opts = exp_opts(exp)
            if opts is None or new_opts is None:
                new_opts = opts
            else:
                for key in opts:
                    new_opts[key] = opts[key]
            if new_opts is None:
                grammar[symbol][i] = exp_string(exp)
            else:
                grammar[symbol][i] = (exp_string(exp), new_opts)
            return

def set_prob(grammar, symbol, expansion, prob):
    """Set the probability of the given expansion of grammar[symbol]"""
    set_opts(grammar, symbol, expansion, opts(prob=prob))

import copy

if __name__ == "__main__":
    probabilistic_url_grammar = copy.deepcopy(URL_GRAMMAR)
    set_prob(probabilistic_url_grammar, "<scheme>", "ftps", 0.8)
    assert is_valid_probabilistic_grammar(probabilistic_url_grammar)


if __name__ == "__main__":
    probabilistic_url_grammar["<scheme>"]


if __name__ == "__main__":
    prob_url_fuzzer = ProbabilisticGrammarFuzzer(probabilistic_url_grammar)
    for i in range(10):
        print(prob_url_fuzzer.fuzz())


if __name__ == "__main__":
    set_prob(probabilistic_url_grammar, "<scheme>", "ftps", 0.0)
    assert is_valid_probabilistic_grammar(probabilistic_url_grammar)


if __name__ == "__main__":
    prob_url_fuzzer = ProbabilisticGrammarFuzzer(probabilistic_url_grammar)
    for i in range(10):
        print(prob_url_fuzzer.fuzz())


if __package__ is None or __package__ == "":
    from Grammars import EXPR_GRAMMAR
else:
    from .Grammars import EXPR_GRAMMAR


if __name__ == "__main__":
    probabilistic_expr_grammar = copy.deepcopy(EXPR_GRAMMAR)
    probabilistic_expr_grammar["<expr>"]


if __name__ == "__main__":
    set_prob(probabilistic_expr_grammar, "<expr>", "<term>", 0.0)
    assert is_valid_probabilistic_grammar(probabilistic_expr_grammar)


if __name__ == "__main__":
    prob_expr_fuzzer = ProbabilisticGrammarFuzzer(probabilistic_expr_grammar)
    prob_expr_fuzzer.fuzz()


# ## Probabilities in Context

if __name__ == "__main__":
    print('\n## Probabilities in Context')




def decrange(start, end):
    """Return a list with string representations of numbers in the range [start, end)"""
    return [repr(n) for n in range(start, end)]

IP_ADDRESS_GRAMMAR = {
    "<start>": ["<address>"],
    "<address>": ["<octet>.<octet>.<octet>.<octet>"],
    # ["0", "1", "2", ..., "255"]
    "<octet>": list(sorted(decrange(0, 256), reverse=True))
}

if __name__ == "__main__":
    IP_ADDRESS_GRAMMAR["<octet>"]


if __name__ == "__main__":
    assert is_valid_grammar(IP_ADDRESS_GRAMMAR)


if __name__ == "__main__":
    ip_fuzzer = ProbabilisticGrammarFuzzer(IP_ADDRESS_GRAMMAR)
    ip_fuzzer.fuzz()


if __name__ == "__main__":
    probabilistic_ip_address_grammar = copy.deepcopy(IP_ADDRESS_GRAMMAR)
    set_prob(probabilistic_ip_address_grammar, "<octet>", "127", 0.8)


if __name__ == "__main__":
    probabilistic_ip_fuzzer = ProbabilisticGrammarFuzzer(
        probabilistic_ip_address_grammar)
    probabilistic_ip_fuzzer.fuzz()


if __package__ is None or __package__ == "":
    from GrammarCoverageFuzzer import duplicate_context
else:
    from .GrammarCoverageFuzzer import duplicate_context


if __name__ == "__main__":
    probabilistic_ip_address_grammar = copy.deepcopy(IP_ADDRESS_GRAMMAR)
    duplicate_context(probabilistic_ip_address_grammar, "<address>")


if __name__ == "__main__":
    probabilistic_ip_address_grammar["<address>"]


if __name__ == "__main__":
    del probabilistic_ip_address_grammar["<octet>"]


if __name__ == "__main__":
    set_prob(probabilistic_ip_address_grammar, "<octet-1>", "127", 1.0)
    set_prob(probabilistic_ip_address_grammar, "<octet-2>", "0", 1.0)


if __name__ == "__main__":
    assert is_valid_probabilistic_grammar(probabilistic_ip_address_grammar)


if __name__ == "__main__":
    probabilistic_ip_fuzzer = ProbabilisticGrammarFuzzer(
        probabilistic_ip_address_grammar)
    [probabilistic_ip_fuzzer.fuzz() for i in range(5)]


# ## Learning Probabilities from Samples

if __name__ == "__main__":
    print('\n## Learning Probabilities from Samples')




if __package__ is None or __package__ == "":
    from GrammarFuzzer import display_tree
else:
    from .GrammarFuzzer import display_tree


if __package__ is None or __package__ == "":
    from Parser import PEGParser
else:
    from .Parser import PEGParser


if __name__ == "__main__":
    parser = PEGParser(IP_ADDRESS_GRAMMAR)
    tree = parser.parse("127.0.0.1")[0]
    display_tree(tree)


if __package__ is None or __package__ == "":
    from Parser import EarleyParser
else:
    from .Parser import EarleyParser


if __name__ == "__main__":
    parser = EarleyParser(IP_ADDRESS_GRAMMAR)


if __name__ == "__main__":
    tree = parser.parse("127.0.0.1")[0]
    display_tree(tree)


# ## Auto-Tuning Probabilities

if __name__ == "__main__":
    print('\n## Auto-Tuning Probabilities')




if __package__ is None or __package__ == "":
    from Coverage import Coverage, cgi_decode
else:
    from .Coverage import Coverage, cgi_decode

from Grammars import CGI_GRAMMAR

if __name__ == "__main__":
    cgi_fuzzer = GrammarFuzzer(CGI_GRAMMAR)

    trials = 100
    coverage = {}

    for i in range(trials):
        cgi_input = cgi_fuzzer.fuzz()
        with Coverage() as cov:
            cgi_decode(cgi_input)
        coverage[cgi_input] = cov.coverage()


if __name__ == "__main__":
    coverage_slice = [cgi_input for cgi_input in coverage if (
        'cgi_decode', 25) in coverage[cgi_input]]


if __name__ == "__main__":
    print(coverage_slice)


if __name__ == "__main__":
    len(coverage_slice) / trials


# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Background

if __name__ == "__main__":
    print('\n## Background')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1

if __name__ == "__main__":
    print('\n### Exercise 1')




class ProbabilisticGrammarCoverageFuzzer(GrammarCoverageFuzzer, ProbabilisticGrammarFuzzer):
    # Choose uncovered expansions first
    def choose_node_expansion(self, node, possible_children):
        return GrammarCoverageFuzzer.choose_node_expansion(self, node, possible_children)

    # Among uncovered expansions, pick by (relative) probability
    def choose_uncovered_node_expansion(self, node, possible_children):
        return ProbabilisticGrammarFuzzer.choose_node_expansion(self, node, possible_children)

    # For covered nodes, pick by probability, too
    def choose_covered_node_expansion(self, node, possible_children):
        return ProbabilisticGrammarFuzzer.choose_node_expansion(self, node, possible_children)

if __name__ == "__main__":
    cov_leaddigit_fuzzer = ProbabilisticGrammarCoverageFuzzer(
        PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leaddigit>")
    print([cov_leaddigit_fuzzer.fuzz() for i in range(9)])


if __name__ == "__main__":
    trials = 10000

    count = {}
    for c in crange('0', '9'):
        count[c] = 0

    for i in range(trials):
        count[cov_leaddigit_fuzzer.fuzz()] += 1

    print([(digit, count[digit] / trials) for digit in count])


# ### Exercise 2

if __name__ == "__main__":
    print('\n### Exercise 2')



