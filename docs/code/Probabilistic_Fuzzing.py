#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is part of "Generating Software Tests"
# (https://www.fuzzingbook.org/)
# It is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License,
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)

# # Probabilistic Grammar Fuzzing
# 
# Let us give grammars even more power by assigning probabilities to individual expansions.  This allows us to control how many of each element should be produced.  \todo{Work in progress.}
# 
# **Prerequisites**
# 
# * You should have read the [chapter on grammars](Grammars.ipynb).
# 
# import fuzzingbook_utils
# 
from Grammars import grammar_fuzzer, is_valid_grammar

# We introduce a little helper function that will allow us to add arbitrary options to an expansion.
# 
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
        [ "<digit><integer>", "<digit>" ],

    "<digit>":
        [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ],
}

assert is_valid_grammar(PROBABILISTIC_EXPR_GRAMMAR)

if __name__ == "__main__":
    grammar_fuzzer(PROBABILISTIC_EXPR_GRAMMAR)
    
# ## _Section 4_
# 
# \todo{Add}
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
# * [use _mutations_ on existing inputs to get more valid inputs](Mutation_Fuzzing.ipynb)
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
