#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/ProbabilisticGrammarFuzzer.html
# Last change: 2018-11-08 17:50:31+01:00
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




import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer, all_terminals
else:
    from .GrammarFuzzer import GrammarFuzzer, all_terminals


if __package__ is None or __package__ == "":
    from Grammars import is_valid_grammar, EXPR_GRAMMAR, START_SYMBOL, crange
else:
    from .Grammars import is_valid_grammar, EXPR_GRAMMAR, START_SYMBOL, crange


def opts(**kwargs):
    return kwargs

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
    exp_string(PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"][0])


def exp_prob(expansion):
    """Return the specified probability, or None if unspecified"""
    if isinstance(expansion, str):
        return None
    return expansion[1]['prob']

if __name__ == "__main__":
    exp_prob(PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"][0])


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


# ## Checking Probabilities

if __name__ == "__main__":
    print('\n## Checking Probabilities')




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

    default_probability = ((1.0 - sum_of_specified_probabilities) / 
         number_of_unspecified_probabilities)
    all_probabilities = []
    for p in probabilities:
        if p is None:
            p = default_probability
        all_probabilities.append(p)

    assert abs(sum(all_probabilities) - 1.0) < epsilon
    return all_probabilities

if __name__ == "__main__":
    PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"]


if __name__ == "__main__":
    exp_probabilities(PROBABILISTIC_EXPR_GRAMMAR["<leaddigit>"])


if __name__ == "__main__":
    exp_probabilities(PROBABILISTIC_EXPR_GRAMMAR["<digit>"])


if __name__ == "__main__":
    exp_probabilities(PROBABILISTIC_EXPR_GRAMMAR["<expr>"])


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
        assert not is_valid_probabilistic_grammar({"<start>": [("1", opts(prob=0.5))]})


if __name__ == "__main__":
    with ExpectError():
        assert not is_valid_probabilistic_grammar({"<start>": [("1", opts(prob=1.5)), "2"]})


# ## Selecting by Probability

if __name__ == "__main__":
    print('\n## Selecting by Probability')




import random

class ProbabilisticGrammarFuzzer(GrammarFuzzer):
    def choose_node_expansion(self, node, possible_children):
        (symbol, tree) = node
        expansions = self.grammar[symbol]
        probabilities = exp_probabilities(expansions)

        weights = []
        for child in possible_children:
            child_weight = probabilities[all_terminals((node, child))]
            weights.append(child_weight)
            
        return random.choices(range(len(possible_children)), weights=weights)[0]

if __name__ == "__main__":
    f = ProbabilisticGrammarFuzzer(PROBABILISTIC_EXPR_GRAMMAR)
    f.fuzz()


if __name__ == "__main__":
    leaddigit_fuzzer = ProbabilisticGrammarFuzzer(PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leaddigit>")
    leaddigit_fuzzer.fuzz()


if __name__ == "__main__":
    trials = 10000

    count = {}
    for c in crange('0', '9'):
        count[c] = 0

    for i in range(trials):
        count[leaddigit_fuzzer.fuzz()] += 1

    print([(digit, count[digit] / trials) for digit in count])


# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




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
    cov_leaddigit_fuzzer = ProbabilisticGrammarCoverageFuzzer(PROBABILISTIC_EXPR_GRAMMAR, start_symbol="<leaddigit>")
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



