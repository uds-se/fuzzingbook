
# coding: utf-8

# # Fuzzing with Derivation Trees
# 
# In the chapter on ["Grammars"](Grammars.ipynb), we have introduced the concept of _grammars_ that specify input formats and _producers_ that randomly generate a valid input from a grammar.  Our implementation was not very efficient, though.  In this chapter, we introduce _derivation trees_ that encode a (produced) string as a syntactic structure.  This allows for efficient production of inputs from grammars, as well as easy manipulation.

# **Prerequisites**
# 
# * You should know how grammar-based fuzzing works, e.g. from the ["Grammars" chapter](Grammars.ipynb).

# ## The Trouble with String Replacement
# 
# In our [previous chapter](Grammars.ipynb), we had introduced a simple fuzzer that would produce a random string from a grammar, using string replacement.  With each iteration, this fuzzer would go search the string produced so far for symbols to expand.  How expensive is this in the long run?  Let us plot the time required for strings of different lengths.

# In[218]:


# import fuzzingbook_utils # only in notebook


# In[219]:


from Grammars import simple_grammar_fuzzer, EXPR_GRAMMAR


# In[220]:


from Timer import Timer


# In[221]:


xs = []
ys = []
for i in range(100):
    with Timer() as t:
        s = simple_grammar_fuzzer(EXPR_GRAMMAR, max_symbols=15)
    xs.append(len(s))
    ys.append(t.elapsed_time())
    print(i, end=" ")


# In[222]:


# get_ipython().run_line_magic('matplotlib', 'inline') # only in notebook

import matplotlib.pyplot as plt
plt.scatter(xs, ys)
plt.title('Time required for generating an output');


# We see that the effort increases quadratically.

# \todo{Discuss how we can have outputs that are 20,000 characters long}

# ## Derivation Trees

# ## Representing Derivation
# 
# e.g. `<expr> + <expr>`

# In[223]:


import re
import random


# In[224]:


from Grammars import START_SYMBOL, RE_SYMBOL, EXPR_GRAMMAR, symbols


# In[225]:


derivation_tree = ("<start>", 
        [("<expr>", 
          [("<expr>", None),
           (" + ", []),
           ("<expr>", None)]
         )])


# Let's visualize this tree!

# In[226]:


from IPython.display import display


# In[227]:


from graphviz import Digraph


# In[228]:


import re


# In[229]:


def dot_escape(s):
    """Return s in a form suitable for dot"""
    # s = s.replace("\\", "\\\\")
    s = re.sub(r"([^a-zA-Z0-9 ])", r"\\\1", s)
    return s


# In[230]:


assert dot_escape("hello") == "hello"
assert dot_escape("<hello>, world") == "\\<hello\\>\\, world"
assert dot_escape("\\n") == "\\\\n"


# In[231]:


def display_tree(derivation_tree):
    """Visualize a derivation tree as SVG using the graphviz/dot package."""
    
    counter = 0
    def traverse_tree(dot, tree, id=0):
        (symbol, children) = tree
        dot.node(repr(id), dot_escape(symbol))
        
        if children is not None:
            for child in children:
                nonlocal counter
                counter += 1
                child_id = counter
                dot.edge(repr(id), repr(child_id))
                traverse_tree(dot, child, child_id)

    dot = Digraph(comment="Derivation Tree")
    dot.attr('node', shape='plain')
    traverse_tree(dot, derivation_tree)
    display(dot)


# In[232]:


display_tree(derivation_tree)


# ## Expanding a Node

# In[233]:


def init_tree(start_symbol=START_SYMBOL):
    return (start_symbol, None)


# In[234]:


def is_symbol(s):
    return re.match(RE_SYMBOL, s)


# In[235]:


assert is_symbol("<abc>")
assert not is_symbol("+")


# In[236]:


def expansion_to_children(expansion):
    # print("Converting " + repr(expansion))
    # strings contains all substrings -- both terminals and non-terminals such
    # that ''.join(strings) == expansion
    strings  = re.split(RE_SYMBOL, expansion)
    return [(s, None) if is_symbol(s) else (s, []) for s in strings if len(s) > 0]


# In[237]:


expansion_to_children("<term> + <expr>")


# In[238]:


def expand_random_node(node, grammar):
    (symbol, children) = node
    assert children is None

    # Fetch the possible expansions from grammar...
    expansions = grammar[symbol]

    possible_children = [expansion_to_children(expansion) for expansion in expansions]

    # TODO: Consider preferring children not expanded yet,
    # and other forms of grammar coverage (or code coverage)
    children = random.choice(possible_children)

    # Return with a new list
    return (symbol, children)


# In[239]:


example_node = ("<term>", None)
example_tree = expand_random_node(example_node, EXPR_GRAMMAR)
display_tree(example_tree)


# ## Expanding a Tree

# In[240]:


def possible_expansions(tree):
    (symbol, children) = tree
    if children is None:
        return 1

    number_of_expansions = sum(possible_expansions(c) for c in children)
    return number_of_expansions


# In[241]:


print(possible_expansions(example_tree))


# In[242]:


def any_possible_expansions(tree):
    (symbol, children) = tree
    if children is None: return True

    return any(any_possible_expansions(c) for c in children)


# In[243]:


print(any_possible_expansions(example_tree))


# In[244]:


def expand_tree_once(tree, grammar, expand_node=expand_random_node):
    (symbol, children) = tree
    if children is None:
        # Expand this node
        return expand_node(tree, grammar)

    # print("Expanding tree " + repr(tree))

    # Find all children with possible expansions
    expandable_children = [i for (i, c) in enumerate(children) if any_possible_expansions(c)]

    # Select a random child
    # TODO: Various heuristics for choosing a child here,
    # e.g. grammar or code coverage
    child_to_be_expanded = random.choice(expandable_children)

    # Expand in place
    children[child_to_be_expanded] = expand_tree_once(children[child_to_be_expanded], grammar, expand_node)

    return tree


# In[245]:


example_tree_expanded = expand_tree_once(example_tree, EXPR_GRAMMAR)
display_tree(example_tree_expanded)


# In[246]:


example_tree_expanded_twice = expand_tree_once(example_tree_expanded, EXPR_GRAMMAR)
display_tree(example_tree_expanded_twice)


# ## Closing the Expansion

# In[247]:


def symbol_min_cost(symbol, grammar, seen=set()):
    expansions = grammar[symbol]
    return min(min_expansions(e, grammar, seen | {symbol}) for e in expansions)


# In[248]:


def min_expansions(expansion, grammar, seen=set()):
    syms = symbols(expansion)
    # at least one expansion has no variable to expand.
    if len(syms) == 0:
        return 1

    # if a variable present in the expansion is already in the stack, then it is
    # recursion
    if any(s in seen for s in syms):
        return float('inf')

    # the value of a expansion is the sum of all expandable variables inside + 1
    return sum(symbol_min_cost(s, grammar, seen) for s in syms) + 1


# In[249]:


assert symbol_min_cost("<digit>", EXPR_GRAMMAR) == 1


# In[250]:


assert symbol_min_cost("<expr>", EXPR_GRAMMAR) == 5


# In[251]:


def expand_min_expansions(node, grammar):
    (symbol, children) = node
    # print("Expanding " + repr(symbol))
    assert children is None

    # Fetch the possible expansions from grammar...
    expansions = grammar[symbol]

    possible_children_with_cost = [(expansion_to_children(expansion),
                                    min_expansions(expansion, grammar, {symbol}))
                                  for expansion in expansions]

    min_cost = min(cost for (child, cost) in possible_children_with_cost)
    children_with_min_cost = [child for (child, child_cost) in possible_children_with_cost
                              if child_cost == min_cost]

    children = random.choice(children_with_min_cost)

    # Return with a new list
    return (symbol, children)


# ## All Together

# In[252]:


def expand_tree(tree, grammar, max_symbols=10, disp=False, log=False):
    
    def _expand_tree_once(tree, grammar, expand_node, disp, log):
        tree = expand_tree_once(tree, grammar, expand_node)
        if disp:
            display_tree(tree)
            print(possible_expansions(tree), "possible expansion(s) left")
        if log:
            print(tree)
        return tree

    if disp or log:
        print("Stage 1: Expanding until we reach", max_symbols, "unexpanded symbols")

    while 0 < possible_expansions(tree) < max_symbols:
        tree = _expand_tree_once(tree, grammar, expand_random_node, disp, log)

    if disp or log:
        print("Stage 2: Keep on expanding using shortest expansions only")

    while any_possible_expansions(tree):
        tree = _expand_tree_once(tree, grammar, expand_min_expansions, disp, log)
        
    assert possible_expansions(tree) == 0

    return tree


# In[253]:


expanded_tree = expand_tree(example_tree, EXPR_GRAMMAR, max_symbols=5, disp=False)
print("Final tree")
display_tree(expanded_tree)


# In[254]:


def all_terminals(tree):
    (symbol, children) = tree
    if children is None:
        # This is a nonterminal symbol not expanded yet
        return symbol

    if len(children) == 0:
        # This is a terminal symbol
        return symbol

    # This is an expanded symbol:
    # Concatenate all terminal symbols from all children
    return ''.join([all_terminals(c) for c in children])


# In[255]:


all_terminals(expanded_tree)


# In[256]:


def grammar_tree_fuzzer(grammar, max_symbols=10, start_symbol=START_SYMBOL, disp=False, log=False):
    # Create an initial derivation tree
    tree = init_tree(start_symbol)
    # print(tree)

    # Expand all nonterminals
    tree = expand_tree(tree, grammar, max_symbols)
    if disp:
        print(repr(all_terminals(tree)))
        display_tree(tree)
    if log:
        print(tree)

    # Return the string
    return all_terminals(tree)


# In[257]:


from Grammars import URL_GRAMMAR


# \todo{We have trouble with expansions into empty strings - they are not visualized properly, and ignored by `allterminals()`}

# In[258]:


expanded_tree = expand_tree(init_tree(), URL_GRAMMAR, max_symbols=5)
print(repr(all_terminals(expanded_tree)))
print(expanded_tree)
display_tree(expanded_tree)


# In[259]:


trials = 100
xs = []
ys = []
for i in range(trials):
    with Timer() as t:
        s = grammar_tree_fuzzer(EXPR_GRAMMAR, max_symbols=20)
    xs.append(len(s))
    ys.append(t.elapsed_time())
    print(i, end=" ")

average_time = sum(ys) / trials
print()
print("Average time:", average_time)


# In[260]:


# get_ipython().run_line_magic('matplotlib', 'inline') # only in notebook

import matplotlib.pyplot as plt
plt.scatter(xs, ys)
plt.title('Time required for generating an output');


# ## Lessons Learned
# 
# * _Lesson one_
# * _Lesson two_
# * _Lesson three_

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
# _Close the chapter with a few exercises such that people have things to do.  Use the Jupyter `Exercise2` nbextension to add solutions that can be interactively viewed or hidden.  (Alternatively, just copy the exercise and solution cells below with their metadata.)  We will set up things such that solutions do not appear in the PDF and HTML formats._

# ### Exercise 1
# 
# Speed up things by memoizing.

# In[261]:


# cache the function calls. We only cache a given call based on the
# indicated argument number per function.
def memoize(argnum):
    def fn_wrap(function):
        memo = {}
        def wrapper(*args):
            if args[argnum] in memo: return memo[args[argnum]]
            rv = function(*args)
            memo[args[argnum]] = rv
            return rv
        return wrapper
    return fn_wrap


# _Solution for the exercise_

# ### Exercise 2
# 
# Speed up things by tracking which children still can be expanded.

# _Solution for the exercise_

# ### Exercise 3
# 
# Introduce a parameter `min_symbols` that would keep on expanding with _maximum_ cost until `min_symbols` is reached.

# In[262]:


def expand_max_expansions(node, grammar):
    (symbol, children) = node
    # print("Expanding " + repr(symbol))
    assert children is None

    # Fetch the possible expansions from grammar...
    expansions = grammar[symbol]

    possible_children_with_cost = [(expansion_to_children(expansion),
                                    min_expansions(expansion, grammar, {symbol}))
                                  for expansion in expansions]

    max_cost = max(cost for (child, cost) in possible_children_with_cost)
    children_with_max_cost = [child for (child, child_cost) in possible_children_with_cost
                              if child_cost == max_cost]

    children = random.choice(children_with_max_cost)

    # Return with a new list
    return (symbol, children)


# In[263]:


def expand_tree_minmax(tree, grammar, min_symbols=0, max_symbols=10, disp=False, log=False):
    
    def _expand_tree_once(tree, grammar, expand_node, disp, log):
        tree = expand_tree_once(tree, grammar, expand_node)
        if disp:
            display_tree(tree)
            print(possible_expansions(tree), "possible expansion(s) left")
        if log:
            print(tree)
        return tree

    if disp or log:
        print("Stage 0: Expanding until we reach", max_symbols, "unexpanded symbols")

    while 0 < possible_expansions(tree) < min_symbols:
        tree = _expand_tree_once(tree, grammar, expand_max_expansions, disp, log)
    
    if disp or log:
        print("Stage 1: Expanding until we reach", max_symbols, "unexpanded symbols")

    while 0 < possible_expansions(tree) < max_symbols:
        tree = _expand_tree_once(tree, grammar, expand_random_node, disp, log)

    if disp or log:
        print("Stage 2: Keep on expanding using shortest expansions only")

    while any_possible_expansions(tree):
        tree = _expand_tree_once(tree, grammar, expand_min_expansions, disp, log)
        
    assert possible_expansions(tree) == 0

    return tree


# In[264]:


expanded_tree = expand_tree_minmax(init_tree(), EXPR_GRAMMAR, min_symbols=10, max_symbols=10)
print(repr(all_terminals(expanded_tree)))
display_tree(expanded_tree)


# ### Exercise 4
# 
# Introduce Purdom's approach first expanding yet uncovered expansions \cite{purdom1972} as discussed in [the "Grammars" chapter](Grammars.ipynb).

# _Solution for the exercise_
