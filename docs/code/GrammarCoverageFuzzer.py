#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is part of "Generating Software Tests"
# (https://www.fuzzingbook.org/)
# It is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License,
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)

# # Grammar Coverage
# 
# In this chapter, we explore how to systematically cover elements of a grammar, as well as element combinations.  \todo{Work in progress.}
# 
# **Prerequisites**
# 
# * You should have read the [chapter on grammars](Grammars.ipynb).
# * You should have read the [chapter on efficient grammar fuzzing](GrammarFuzzing.ipynb).
# 
# ## Covering Grammar Elements
# 
# Producing from grammars, as discussed in the [chapter on grammars](Grammars.ipynb), gives all possible expansions of a rule the same likelihood.  For producing a comprehensive test suite, however, it makes more sense to maximize _variety_ – for instance, by avoiding repeating the same expansions over and over again.  To achieve this, we can track the _coverage_ of individual expansions: If we have seen some expansion already, we can prefer other possible expansions in the future.  The idea of ensuring that each expansion in the grammar is used at least once goes back to Paul Purdom \cite{purdom1972}.
# 
# As an example, consider the grammar
# 
# ```grammar
# <start> ::= <digit><digit>
# <digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# ```
# 
# Let us assume we have already produced a `0` in the first expansion of `<digit>`.  As it comes to expand the next digit, we would mark the `0` expansion as already covered, and choose one of the yet uncovered alternatives.  Only when we have covered all alternatives would we go back and consider expansions covered before.
# 
# This concept of coverage is very easy to implement.
# 
# import fuzzingbook_utils
# 
from Grammars import DIGIT_GRAMMAR, EXPR_GRAMMAR, CGI_GRAMMAR, START_SYMBOL
from GrammarFuzzer import GrammarFuzzer, all_terminals
import random

class GrammarCoverageFuzzer(GrammarFuzzer):
    def __init__(self, *args, **kwargs):
        # invoke superclass __init__(), passing all arguments
        super(GrammarFuzzer, self).__init__(*args, **kwargs)
        self.reset_coverage()
        
    def reset_coverage(self):
        self.covered_expansions = set()
    
    def expansion_coverage(self):
        return self.covered_expansions

if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR)
    f.fuzz()
    
class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def expansion_key(self, symbol, children):
        return symbol + " -> " + all_terminals((symbol, children))

    def max_expansion_coverage(self):
        """Return set of all expansions in a grammar"""
        expansions = set()
        for nonterminal in self.grammar:
            for expansion in self.grammar[nonterminal]:
                children = self.expansion_to_children(expansion)
                expansions.add(self.expansion_key(nonterminal, children))
        return expansions

if __name__ == "__main__":
    f = GrammarCoverageFuzzer(DIGIT_GRAMMAR)
    f.max_expansion_coverage()
    
class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def choose_node_expansion(self, node, possible_children):
        # Prefer uncovered expansions
        (symbol, children) = node
        uncovered_children = [(i, c) for (i, c) in enumerate(possible_children) 
                              if self.expansion_key(symbol, c) not in self.covered_expansions]

        # print("Uncovered:", uncovered_children)

        if len(uncovered_children) == 0:
            # All expansions covered - use superclass method
            if self.log:
                print("All", symbol, "alternatives covered")

            return super(GrammarFuzzer, self).choose_node_expansion(node, possible_children)

        # select a random expansion
        index = random.randrange(len(uncovered_children))
        (new_children_index, new_children) = uncovered_children[index]

        # Save the expansion as covered
        key = self.expansion_key(symbol, new_children)
        assert key not in self.covered_expansions
        
        if self.log:
            print("Now covered:", key)
        self.covered_expansions.add(key)

        return new_children_index

# By returning the set of expansions covered so far, we can invoke the fuzzer multiple times, each time adding to the grammar coverage.  With the `DIGIT_GRAMMAR` grammar, for instance, this lets the grammar produce one digit after the other:
# 
if __name__ == "__main__":
    f = GrammarCoverageFuzzer(DIGIT_GRAMMAR, log=True)
    f.fuzz()
    
if __name__ == "__main__":
    f.fuzz()
    
if __name__ == "__main__":
    f.fuzz()
    
if __name__ == "__main__":
    f.covered_expansions
    
# At the end, all expansions are covered:
# 
if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()
    
# Let us now create some more expressions:
# 
if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR)
    for i in range(10):
        print(f.fuzz())
    
# Again, all expansions are covered:
# 
if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()
    
# ## Grammar Coverage and Code Coverage
# 
if __name__ == "__main__":
    f = GrammarCoverageFuzzer(CGI_GRAMMAR)
    for i in range(10):
        print(f.fuzz())
    
if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()
    
# ## Choosing Subtrees to Expand
# 
# On top of `choose_node_expansion()`, we can also extend `choose_tree_expansion()` to guide expansion towards subtrees with uncovered nodes.
# 
# \todo{Expand.}
# 
# ## Advanced Grammar Coverage Metrics
# 
# \todo{Expand.}
# 
# ## Lessons Learned
# 
# * _Lesson one_
# * _Lesson two_
# * _Lesson three_
# 
# ## Next Steps
# 
# _Link to subsequent chapters (notebooks) here, as in:_
# 
# * [use _mutations_ on existing inputs to get more valid inputs](MutationFuzzer.ipynb)
# * [use _grammars_ (i.e., a specification of the input format) to get even more valid inputs](Grammars.ipynb)
# * [reduce _failing inputs_ for efficient debugging](Reducing.ipynb)
# 
# ## Exercises
# 
# Close the chapter with a few exercises such that people have things to do.  In Jupyter Notebook, use the `exercise2` nbextension to add solutions that can be interactively viewed or hidden:
# 
# * Mark the _last_ cell of the exercise (this should be a _text_ cell) as well as _all_ cells of the solution.  (Use the `rubberband` nbextension and use Shift+Drag to mark multiple cells.)
# * Click on the `solution` button at the top.
# 
# (Alternatively, just copy the exercise and solution cells below with their metadata.)
# 
# ### Exercise 1
# 
# _Text of the exercise_
# 
if __name__ == "__main__":
    # Some code that is part of the exercise
    pass
    
# _Some more text for the exercise_
# 
# _Some text for the solution_
# 
if __name__ == "__main__":
    # Some code for the solution
    2 + 2
    
# _Some more text for the solution_
# 
# ### Exercise 2
# 
# _Text of the exercise_
# 
# _Solution for the exercise_
# 
