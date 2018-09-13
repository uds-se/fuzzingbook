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
from Grammars import grammar_fuzzer, DIGIT_GRAMMAR, EXPR_GRAMMAR, CGI_GRAMMAR, START_SYMBOL
from Grammars import display_tree, all_terminals, expansion_to_children, expand_tree_once_randomly
import random

if __name__ == "__main__":
    covered_expansions = set()
    
def expansion_key(symbol, children):
    return symbol + " -> " + all_terminals((symbol, children))

def expand_uncovered_node(node, grammar):
    (symbol, children) = node
    assert children is None
    global covered_expansions

    # print("Expanding", all_terminals(node) + ", preferring uncovered expansions")
    
    # Fetch the possible expansions from grammar...
    expansions = grammar[symbol]
    possible_children = [expansion_to_children(expansion) for expansion in expansions]
    
    # Prefer uncovered expansions
    uncovered_children = [children for children in possible_children 
                          if expansion_key(symbol, children) not in covered_expansions]
    if len(uncovered_children) > 0:
        possible_children = uncovered_children

    # ... and select a random expansion
    children = random.choice(possible_children)
    
    # Save the expansion as covered
    covered_expansions.add(expansion_key(symbol, children))

    # Return with new children
    return (symbol, children)

def covering_grammar_fuzzer(grammar, max_nonterminals=10, start_symbol=START_SYMBOL, 
    expand_tree_once=expand_tree_once_randomly,
    expand_node=expand_uncovered_node,
    disp=False, log=False):
    return grammar_fuzzer(grammar, max_nonterminals=max_nonterminals, start_symbol=start_symbol,
                         expand_node=expand_node, disp=disp, log=log)

# By returning the set of expansions covered so far, we can invoke the fuzzer multiple times, each time adding to the grammar coverage.  With the `DIGIT_GRAMMAR` grammar, for instance, this lets the grammar produce one digit after the other:
# 
if __name__ == "__main__":
    covered_expansions = set()
    covering_grammar_fuzzer(DIGIT_GRAMMAR)
    
if __name__ == "__main__":
    covered_expansions
    
if __name__ == "__main__":
    covering_grammar_fuzzer(DIGIT_GRAMMAR)
    
if __name__ == "__main__":
    covered_expansions
    
if __name__ == "__main__":
    covering_grammar_fuzzer(DIGIT_GRAMMAR)
    
if __name__ == "__main__":
    covered_expansions
    
# At the end, all expansions are covered:
# 
def all_expansions(grammar):
    """Return set of all expansions in a grammar"""
    expansions = set()
    for nonterminal in grammar:
        for expansion in grammar[nonterminal]:
            children = expansion_to_children(expansion)
            expansions.add(expansion_key(nonterminal, children))
    return expansions

if __name__ == "__main__":
    all_expansions(DIGIT_GRAMMAR)
    
if __name__ == "__main__":
    all_expansions(DIGIT_GRAMMAR) - covered_expansions
    
# Let us now create some more expressions:
# 
if __name__ == "__main__":
    covered_expansions = set()
    for i in range(10):
        print(covering_grammar_fuzzer(EXPR_GRAMMAR))
    
# Again, all expansions are covered:
# 
if __name__ == "__main__":
    all_expansions(EXPR_GRAMMAR) - covered_expansions
    
# ## Grammar Coverage and Code Coverage
# 
if __name__ == "__main__":
    covered_expansions = set()
    for i in range(10):
        print(covering_grammar_fuzzer(CGI_GRAMMAR))
    
if __name__ == "__main__":
    covered_expansions
    
# ## Choosing Elements to Expand
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
