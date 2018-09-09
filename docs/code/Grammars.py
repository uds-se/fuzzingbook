
# coding: utf-8

# # Fuzzing with Grammars
# 
# In the chapter on ["Mutation-Based Fuzzing"](Mutation_Fuzzing.ipynb), we have seen how to use extra hints – such as sample input files – to speed up test generation.  In this chapter, we take this idea one step further, by providing a _specification_ of the legal inputs to a program.  These _grammars_ allow for very effective and efficient testing, as we will see in this chapter.

# **Prerequisites**
# 
# * You should know how basic fuzzing works, e.g. from the [Chapter introducing fuzzing](Basic_Fuzzing.ipynb).
# * Knowledge on [mutation-based fuzzing](Mutation_Fuzzing.ipynb) and [coverage](Coverage.ipynb) is _not_ required yet, but still recommended.

# ## Input Languages
# 
# All possible behaviors of a program can be triggered by its input.  "Input" here can be a wide range of possible sources: We are talking about data read from files or over the network, data input by the user, or data acquired from interaction with other resources.  The set of all these inputs determines how the program will behave – including its failures.  When testing, it is thus very helpful to think about possible input sources, how to get them under control, and _how to systematically test them_.
# 
# For the sake of simplicity, we will assume for now that the program has only one source of inputs; this is the same assumption we have been using in the previous chapters, too.  The set of valid inputs to a program is called a _language_.  Languages range from the simple to the complex: the CSV language denotes the set of valid comma-separated inputs, whereas the Python language denotes the set of valid Python programs.  We commonly separate data languages and programming languages, although any program can also be treated as input data (say, to a compiler).  The [Wikipedia page on file formats](https://en.wikipedia.org/wiki/List_of_file_formats) lists more than 1,000 different file formats, each of which is its own language.

# ## Grammars

# ### Rules and Expansions
# 
# To formally specify input languages, _grammars_ are among the most popular (and best understood) formalisms.  A grammar consists of a _start symbol_ and a set of _rules_ which indicate how the start symbol (and other symbols) can be expanded.  As an example, consider the following grammar, denoting a sequence of two digits:
# 
# ```grammar
# <start> ::= <digit><digit>
# <digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# ```
# 
# To read such a grammar, start with the starting symbol (`<start>`).  A rule `<A> ::= <B>` means that the symbol on the left side (`<A>`) can be replaced by the string on the right side (`<B>`).  In the above grammar, `<start>` would be replaced by `<digit><digit>`.
# 
# In this string again, `<digit>` would be replaced by the string on the right side of the `<digit>` rule.  The special operator `|` denotes _alternatives_, meaning that any of the digits can be chosen for an expansion.  Each `<digit>` thus would be expanded into one of the given digits, eventually yielding a string between `00` and `99`.  There are no further expansions for `0` to `9`, so we are all set.
# 
# The interesting thing about grammars is that they can be _recursive_. That is, expansions can make use of symbols expanded earlier – which would then be expanded again.  As an example, consider a grammar that describes integers:
# 
# ```grammar
# <start>  ::= <integer>
# <integer> ::= <digit> | <digit><integer>
# <digit>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# ```
# 
# Here, a `<integer>` is either a single digit, or a digit followed by another integer.  The number `1234` thus would be represented as a single digit `1`, followed by the integer `234`, which in turn is a digit `2`, followed by the integer `34`.
# 
# If we wanted to express that an integer can be preceded by a sign (`+` or `-`), we would write the grammar as
# 
# ```grammar
# <start>   ::= <number>
# <number>  ::= <integer> | +<integer> | -<integer>
# <integer> ::= <digit> | <digit><integer>
# <digit>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# ```
# 
# These rules formally define the language: Anything that can be derived from the start symbol is part of the language; anything that cannot is not.

# ### Arithmetic Expressions
# 
# Let us expand our grammar to cover full _arithmetic expressions_ – a poster child example for a grammar.  We see that an expression (`<expr>`) is either a sum, or a difference, or a term; a term is either a product or a division, or a factor; and a factor is either a number or a parenthesized expression.  Amost all rules can have recursion, and thus allow arbitrary complex expressions such as `(1 + 2) * (3.4 / 5.6 - 789)`.
# 
# ```grammar
# <start>   ::= <expr>
# <expr>    ::= <expr> + <term> | <expr> - <term> | <term>
# <term>    ::= <term> * <factor> | <term> / <factor> | <factor>
# <factor>  ::= +<factor> | -<factor> | (<expr>) | <integer> | <integer>.<integer>
# <integer> ::= <digit> | <digit><integer>
# <digit>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# ```
# 
# In such a grammar, if we start with `<start>` and then expand one symbol after another, randomly choosing alternatives, we can quickly produce one valid arithmetic expression after another.  Such _grammar fuzzing_ is highly effective as it comes to produce complex inputs, and this is what we will implement in this chapter.

# ## Representing Grammars in Python
# 
# Our first step in building a grammar fuzzer is to find an appropriate format for grammars.  To make the writing of grammars as simple as possible, we use a mostly format that is mostly based on strings.  Our grammars in Python takes the format of a _mapping_ between symbol names and expansions, where expansions are _lists_ of alternatives.  A one-rule grammar for digits thus takes the form

# In[1]:


# import fuzzingbook_utils # only in notebook


# In[2]:


DIGIT_GRAMMAR = {
    "<start>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}


# whereas the full grammar for arithmetic expressions looks like this:

# In[3]:


EXPR_GRAMMAR = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<term> + <term>", "<term> - <term>", "<term>"],

    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>"],

    "<factor>":
        ["+<factor>", "-<factor>", "(<expr>)", "<integer>", "<integer>.<integer>"],

    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}


# In the grammar, we can access any rule by its symbol...

# In[4]:


EXPR_GRAMMAR["<digit>"]


# ....and we can check whether a symbol is in the grammar:

# In[5]:


"<identifier>" in EXPR_GRAMMAR


# ## Hatching Grammars
# 
# Since grammars are represented as strings, it is fairly easy to introduce errors.  So let us introduce a helper function that checks a grammar for consistency.
# 
# Frst, this handy `nonterminals()` function gets us the list of nonterminals in an expansion.  

# In[6]:


import re

# As a symbol, we can have anything between <...> except spaces.
RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')


# In[7]:


def nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples, 
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_NONTERMINAL, expansion)


# In[8]:


assert nonterminals("<term> * <factor>") == ["<term>", "<factor>"]
assert nonterminals("<digit><integer>") == ["<digit>", "<integer>"]
assert nonterminals("1 < 3 > 2") == []
assert nonterminals("1 <3> 2") == ["<3>"]
assert nonterminals("1 + 2") == []
assert nonterminals(("<1>", {'option': 'value'})) == ["<1>"]


# Likewise, `is_nonterminal()` checks whether some symbol is a nonterminal:

# In[9]:


def is_nonterminal(s):
    return re.match(RE_NONTERMINAL, s)


# In[10]:


assert is_nonterminal("<abc>")
assert not is_nonterminal("+")


# The helper function `is_valid_grammar()` iterates over a grammar to check whether all used symbols are defined, and vice versa, which is very useful for debugging.  You don't have to dwelve into details here, but as always, it is important to get the input data straight before we make use of it.

# In[11]:


import sys


# In[12]:


START_SYMBOL = "<start>"


# In[13]:


def is_valid_grammar(grammar, start_symbol=START_SYMBOL):
    used_nonterminals = set([start_symbol])
    defined_nonterminals = set()

    for defined_nonterminal in grammar:
        defined_nonterminals.add(defined_nonterminal)
        expansions = grammar[defined_nonterminal]
        if not isinstance(expansions, list):
            print(repr(defined_nonterminal) + ": expansion is not a list", file=sys.stderr)
            return False
        if len(expansions) == 0:
            print(repr(defined_nonterminal) + ": expansion list empty", file=sys.stderr)
            return False

        for expansion in expansions:
            if isinstance(expansion, tuple):
                expansion = expansion[0]
            if not isinstance(expansion, str):
                print(repr(defined_nonterminal) + ": " + repr(expansion) + ": not a string", file=sys.stderr)
                return False

            for used_nonterminal in nonterminals(expansion):
                used_nonterminals.add(used_nonterminal)

    for unused_nonterminal in defined_nonterminals - used_nonterminals:
        print(repr(unused_nonterminal) + ": defined, but not used", file=sys.stderr)
    for undefined_nonterminal in used_nonterminals - defined_nonterminals:
        print(repr(undefined_nonterminal) + ": used, but not defined", file=sys.stderr)

    return used_nonterminals == defined_nonterminals


# Our expression grammar passes the test:

# In[14]:


assert is_valid_grammar(EXPR_GRAMMAR)


# But these ones don't:

# In[15]:


assert not is_valid_grammar({"<start>": ["<x>"], "<y>": ["1"]})


# In[16]:


assert not is_valid_grammar({"<start>": "123"})


# In[17]:


assert not is_valid_grammar({"<start>": []})


# In[18]:


assert not is_valid_grammar({"<start>": [1, 2, 3]})


# ## A Simple Grammar Fuzzer
# 
# Let us now put the above grammars to use.   We will build a very simple grammar fuzzer that starts with a start symbol (`"<start>"`) and then keeps on expanding it.  To avoid expansion to infinite inputs, we place a limit (`max_symbols`) on the number of symbols.  Furthermore, to avoid being stuck in a sitution where we cannot reduce the number of symbols any further, we also limit the total number of expansion steps.

# In[19]:


import random


# In[20]:


class ExpansionError(Exception):
    pass


# In[21]:


def simple_grammar_fuzzer(grammar, start_symbol=START_SYMBOL, 
                          max_nonterminals=10, max_expansion_trials=100,
                          log=False):
    term = start_symbol
    expansion_trials = 0

    while len(nonterminals(term)) > 0:
        symbol_to_expand = random.choice(nonterminals(term))
        expansion = random.choice(grammar[symbol_to_expand])
        new_term = term.replace(symbol_to_expand, expansion, 1)

        if len(nonterminals(new_term)) < max_nonterminals:
            term = new_term
            if log:
                print("%-40s" % (symbol_to_expand + " -> " + expansion), term)
            expansion_trials = 0
        else:
            expansion_trials += 1
            if expansion_trials >= max_expansion_trials:
                raise ExpansionError("Cannot expand " + repr(term))

    return term


# Let us see how this simple grammar fuzzer obtains an arithmetic expression from the start symbol:

# In[22]:


simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=3, log=True)


# In[23]:


for i in range(10):
    print(simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=5))


# \todo{Discuss.}

# Note that this fuzzer is rather inefficient due to the large number of search and replace operations.  On the other hand, the implementation is straight-forward and does the job.  For this chapter, we'll stick to it; in the [next chapter](Derivation_Trees.ipynb), we'll show how to build a more efficient one.

# ## Some Grammars

# With grammars, we can easily specify the format for several of the examples we discussed earlier.  The above arithmetic expressions, for instance, can be directly sent into `bc` (or any other program that takes arithmetic expressions.  
# 
# Let us create some more grammars.  Here's one for `cgi_decode()`:

# In[24]:


CGI_GRAMMAR = {
    "<start>":
        ["<string>"],

    "<string>":
        ["<letter>", "<letter><string>"],

    "<letter>":
        ["<plus>", "<percent>", "<other>"],

    "<plus>":
        ["+"],

    "<percent>":
        ["%<hexdigit><hexdigit>"],

    "<hexdigit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"],

    "<other>":  # Actually, could be _all_ letters
        ["0", "1", "2", "3", "4", "5", "a", "b", "c", "d", "e", "-", "_"],
}

assert is_valid_grammar(CGI_GRAMMAR)


# In[25]:


for i in range(10):
    print(simple_grammar_fuzzer(grammar=CGI_GRAMMAR, max_nonterminals=10))


# Or a URL grammar:

# In[26]:


URL_GRAMMAR = {
    "<start>":
        ["<call>"],

    "<call>":
        ["<url>"],

    "<url>":
        ["<scheme>://<authority><path><query>"],

    "<scheme>":
        ["http", "https", "ftp", "ftps"],

    "<authority>":
        ["<host>", "<host>:<port>", "<userinfo>@<host>", "<userinfo>@<host>:<port>"],

    "<host>":  # Just a few
        ["cispa.saarland", "www.google.com", "fuzzingbook.com"],

    "<port>":
        ["80", "8080", "<nat>"],

    "<nat>":
        ["<digit>", "<digit><digit>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],

    "<userinfo>":  # Just one
        ["user:password"],

    "<path>":  # Just a few
        ["", "/", "/<id>"],

    "<id>":  # Just a few
        ["abc", "def", "x<digit><digit>"],

    "<query>":
        ["", "?<params>"],

    "<params>":
        ["<param>", "<param>&<params>"],

    "<param>":  # Just a few
        ["<id>=<id>", "<id>=<nat>"],
}

assert is_valid_grammar(URL_GRAMMAR)


# In[27]:


for i in range(10):
    print(simple_grammar_fuzzer(grammar=URL_GRAMMAR, max_nonterminals=10))


# ## A More Efficient Algorithm
# 
# While simple and straight-forward, our grammar production algorithm suffers from two problems:
# 
# 1. *It is inefficient*.  With each iteration, this fuzzer would go search the string produced so far for symbols to expand.  This becomes inefficient as the production string grows.
# 
# 2. *It is hard to control.*  Even while limiting the number of symbols, it is still possible to obtain very long strings.
# 
# Both problems can be easily illustrated by plotting the time required for strings of different lengths.

# In[28]:


from Timer import Timer


# In[29]:


trials = 100
xs = []
ys = []
for i in range(trials):
    with Timer() as t:
        s = simple_grammar_fuzzer(EXPR_GRAMMAR, max_nonterminals=15)
    xs.append(len(s))
    ys.append(t.elapsed_time())
    print(i, end=" ")
    
average_time = sum(ys) / trials
print()
print("Average time:", average_time)


# In[30]:


# get_ipython().run_line_magic('matplotlib', 'inline') # only in notebook

import matplotlib.pyplot as plt
plt.scatter(xs, ys)
plt.title('Time required for generating an output');


# We see that (1) the effort increases quadratically over time, and (2) we can easily produce outputs that are tens of thousands of characters long.

# ## Derivation Trees
# 
# To both obtain a more efficient algorithm _and_ exercise better control over expansions, we will use a special representation for the strings that our grammar produces.  The general idea is to use a _tree_ structure that will be subsequently expanded – a so-called _derivation tree_.
# 
# The expansion process with derivation trees is illustrated in the following steps.  We use `dot` as a drawing program; you don't need to look at the code, just at its results.  We start with a single node as root of the tree.

# In[31]:


from graphviz import Digraph


# In[32]:


dot = Digraph("root")
dot.attr('node', shape='plain')
dot.node(r"\<start\>")
dot


# We then traverse the tree, searching for a symbol to expand, and add a new edge from the symbol to its expansion.

# In[33]:


dot.edge(r"\<start\>", r"\<expr\>")
dot


# To construct the actually produced string from the derivation tree, we traverse the tree in order and collect the symbols at the leaves of the tree.  In the case above, we obtain the string `<expr>`.
# 
# To further expand the tree, we choose a symbol to expand, and add a new edge from the symbol to its expansion.  This would get us the string `<expr> + <term>`.

# In[34]:


dot.edge(r"\<expr\>", r"\<expr\> ")
dot.edge(r"\<expr\>", r"+")
dot.edge(r"\<expr\>", r"\<term\>")
dot


# We repeat the process until there are no symbols left to expand:

# In[35]:


dot.edge(r"\<expr\> ", r"\<term\> ")
dot.edge(r"\<term\> ", r"\<factor\> ")
dot.edge(r"\<factor\> ", r"\<integer\> ")
dot.edge(r"\<integer\> ", r"\<digit\> ")
dot.edge(r"\<digit\> ", r"2 ")

dot.edge(r"\<term\>", r"\<factor\>")
dot.edge(r"\<factor\>", r"\<integer\>")
dot.edge(r"\<integer\>", r"\<digit\>")
dot.edge(r"\<digit\>", r"2")
dot


# We now have a representation for the string `2 + 2`.  In contrast to the string alone, though, the derivation tree records the entire structure (and production history) of the produced string.  It also allows for simple comparison and manipulation – say, replacing one subtree (substructure) against another.

# ## Representing Derivation Trees
# 
# To represent a derivation tree in Python, we use the following format.  A node is a pair
# 
# ```python
# (SYMBOL_NAME, CHILDREN)
# ```
# 
# where `SYMBOL_NAME` is a string representing the node (i.e. `<start>` or `+`) and `CHILDREN` is a list of children nodes.
# 
# `CHILDREN` can take some special values:
# 
# 1. `None` as a placeholder for future expansion.  This means that the node is a _nonterminal symbol_ that should be expanded further.
# 2. `[]` (i.e., the empty list) to indicate _no_ children.  This means that the node is a _terminal symbol_ that can no longer be expanded.
# 
# Let us take a very simple derivation tree, representing the intermediate step `<expr> + <term>`, above.

# In[36]:


derivation_tree = ("<start>", 
        [("<expr>", 
          [("<expr>", None),
           (" + ", []),
           ("<term>", None)]
         )])


# Let's visualize this tree!  Again, we use the `dot` drawing program, but now do this algorithmically, traversing the above structure; as with the above visualizations, only the result counts.

# In[37]:


from IPython.display import display


# In[38]:


import re


# In[39]:


def dot_escape(s):
    """Return s in a form suitable for dot"""
    # s = s.replace("\\", "\\\\")
    s = re.sub(r"([^a-zA-Z0-9 ])", r"\\\1", s)
    return s


# In[40]:


assert dot_escape("hello") == "hello"
assert dot_escape("<hello>, world") == "\\<hello\\>\\, world"
assert dot_escape("\\n") == "\\\\n"


# In[41]:


def display_tree(derivation_tree):
    """Visualize a derivation tree as SVG using the graphviz/dot package."""
    
    counter = 0
    def traverse_tree(dot, tree, id=0):
        (symbol, children) = tree
        dot.node(repr(id), dot_escape(symbol))
        
        if children is not None:
            for child in children:
                nonlocal counter  # Assign each node a unique identifier
                counter += 1
                child_id = counter
                dot.edge(repr(id), repr(child_id))
                traverse_tree(dot, child, child_id)

    dot = Digraph(comment="Derivation Tree")
    dot.attr('node', shape='plain')
    traverse_tree(dot, derivation_tree)
    display(dot)


# This is what our tree visualizes into:

# In[42]:


display_tree(derivation_tree)


# To turn the tree into a string, the following function comes in handy:

# In[43]:


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


# In[44]:


all_terminals(derivation_tree)


# ## Expanding a Node

# Let us now develop an algorithm that takes a tree with unexpanded symbols (say, `derivation_tree`, above), and expands all these symbols onbe after the other.  First, let us define a helper function that constructs a tree with just the start symbol:

# In[45]:


def init_tree(start_symbol=START_SYMBOL):
    return (start_symbol, None)


# In[46]:


display_tree(init_tree())


# Next, we will need a helper function that takes an expansion string and converts it into a list of derivation trees:

# In[47]:


def expansion_to_children(expansion):
    # print("Converting " + repr(expansion))
    # strings contains all substrings -- both terminals and non-terminals such
    # that ''.join(strings) == expansion

    # See nonterminals(), above
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    if expansion == "":  # Special case: empty expansion
        return [("", [])]

    strings  = re.split(RE_NONTERMINAL, expansion)
    return [(s, None) if is_nonterminal(s) else (s, []) for s in strings if len(s) > 0]


# In[48]:


expansion_to_children("<term> + <expr>")


# The case of an empty expansion needs special treatment:

# In[49]:


expansion_to_children("")


# With this, we can now take some unexpanded node in the tree, choose a random expansion, and return the new tree.

# In[50]:


def expand_node_randomly(node, grammar):
    (symbol, children) = node
    assert children is None
    
    # print("Expanding", all_terminals(node), "randomly")

    # Fetch the possible expansions from grammar...
    expansions = grammar[symbol]
    possible_children = [expansion_to_children(expansion) for expansion in expansions]

    # ... and select a random expansion
    children = random.choice(possible_children)

    # Return with new children
    return (symbol, children)


# In[51]:


print("Before:")
tree = ("<term>", None)
display_tree(tree)

print("After:")
tree = expand_node_randomly(tree, EXPR_GRAMMAR)
display_tree(tree)


# ## Expanding a Tree
# 
# Let us now apply the above node expansion to some node in the tree.  To this end, we first need to search the tree for unexpanded nodes.  `possible_expansions()` counts how many unexpanded symbols there are in a tree:

# In[52]:


def possible_expansions(tree):
    (symbol, children) = tree
    if children is None:
        return 1

    number_of_expansions = sum(possible_expansions(c) for c in children)
    return number_of_expansions


# In[53]:


print(possible_expansions(derivation_tree))


# `any_possible_expansions()` returns True if the tree has any unexpanded nodes.

# In[54]:


def any_possible_expansions(tree):
    (symbol, children) = tree
    if children is None: return True

    return any(any_possible_expansions(c) for c in children)


# In[55]:


print(any_possible_expansions(derivation_tree))


# Here comes `expand_tree_once()`, the core method of our tree expansion algorithm.  It first checks whether it is currently being applied on a nonterminal symbol without expansion; if so, it invokes `expand_node_randomly()` on it as above.  (With the `expand_node` parameter, we can actually select the function to use for expansion.)
# 
# If the node is already expanded (i.e. has children), it checks the subset of children which still have unexpanded symbols; ranomly selects one of them, and applies itself recursively on that child.
# 
# The `expand_tree_once()` function replaces the child _in place_, meaning that it actually mutates the tree being passed as an argument rather than returning a new tree.  This in-place mutation is what makes this function particularly efficient.

# In[56]:


def expand_tree_once_randomly(tree, grammar, expand_node=expand_node_randomly):
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
    children[child_to_be_expanded] = expand_tree_once_randomly(children[child_to_be_expanded], 
                                                               grammar, expand_node=expand_node)

    return tree


# Let's put it to use, expanding our derivation tree from above twice.

# In[57]:


derivation_tree = ("<start>", 
        [("<expr>", 
          [("<expr>", None),
           (" + ", []),
           ("<term>", None)]
         )])
display_tree(derivation_tree)


# In[58]:


derivation_tree = expand_tree_once_randomly(derivation_tree, EXPR_GRAMMAR)
display_tree(derivation_tree)


# In[59]:


derivation_tree = expand_tree_once_randomly(derivation_tree, EXPR_GRAMMAR)
display_tree(derivation_tree)


# We see that which each step, one more symbol is expanded.  Now all it takes is to apply this again and again, expanding the tree further and further.

# ## Closing the Expansion
# 
# With `expand_tree_once()`, we can keep on expanding the tree – but how do we actually stop?  The key idea here, introduced by Luke in \cite{Luke2000}, is that after inflating the derivation tree to some maximum size, we _only want to apply expansions that increase the size of the tree by a minimum_.  For `<factor>`, for instance, we would prefer an expansion into `<integer>`, as this will not introduce further recursion (and potential size inflation); for `<integer>`, likewise, an expansion into `<digit>` is preferred, as it will less increase tree size than `<digit><integer>`.
# 
# To identify the _cost_ of expanding a symbol, we introduce two functions that mutually rely on each other.  First, `symbol_min_cost()` returns the minimum cost of all expansions of a symbol, using `expansion_min_cost()` to compute the cost for each expansion.

# In[60]:


def symbol_min_cost(symbol, grammar, seen=set()):
    expansions = grammar[symbol]
    return min(expansion_min_cost(e, grammar, seen | {symbol}) for e in expansions)


# The function `expansion_min_cost()` returns the sum of all expansions in `expansions`.  If a nonterminal is encountered again during traversal, the cost of the expansion is $\infty$, as this indicates (potential infinite) recursion.

# In[61]:


def expansion_min_cost(expansion, grammar, seen=set()):
    syms = nonterminals(expansion)
    if len(syms) == 0:
        return 1  # no symbol

    if any(s in seen for s in syms):
        return float('inf')

    # the value of a expansion is the sum of all expandable variables inside + 1
    return sum(symbol_min_cost(s, grammar, seen) for s in syms) + 1


# Here's two examples: The minimum cost of expanding a digit is 1, since we have to choose between one of its expansions.

# In[62]:


assert symbol_min_cost("<digit>", EXPR_GRAMMAR) == 1


# The minimum number of expansions when expanding `<expr>`, though, is five, as this is the minimum number of expansions required.  (`<expr>` → `<term>` → `<factor>` → `<integer>` → `<digit>` → 1)

# In[63]:


assert symbol_min_cost("<expr>", EXPR_GRAMMAR) == 5


# Here's now a variant of `expand_node_randomly()` that takes the above cost into account.  It determines the minimum cost `min_cost` across all children and then uses the child with the minimum cost.  If multiple children all have the same minimum cost, it chooses randomly between these.

# In[64]:


def expand_node_min_cost(node, grammar):
    (symbol, children) = node
    # print("Expanding " + repr(symbol))
    assert children is None

    # Fetch the possible expansions from grammar...
    expansions = grammar[symbol]

    possible_children_with_cost = [(expansion_to_children(expansion),
                                    expansion_min_cost(expansion, grammar, {symbol}))
                                  for expansion in expansions]

    min_cost = min(cost for (child, cost) in possible_children_with_cost)
    children_with_min_cost = [child for (child, child_cost) in possible_children_with_cost
                              if child_cost == min_cost]

    children = random.choice(children_with_min_cost)

    # Return with a new list
    return (symbol, children)


# We can now apply this function to close the expansion of our derivation tree, using `expand_tree_once()` with the above `expand_node_min_cost()` as expansion function.

# In[65]:


display_tree(derivation_tree)

while any_possible_expansions(derivation_tree):
    derivation_tree = expand_tree_once_randomly(derivation_tree, EXPR_GRAMMAR, 
                                                expand_node=expand_node_min_cost)
    display_tree(derivation_tree)


# We see that in each step, `expand_node_min_cost()` chooses an expansion that does not increase the number of symbols, evantually closing all open expansions.

# ## All Together
# 
# We can now put both phases together in a single function `expand_tree()` that will expand a tree first with `expand_node_randomly()` until a limit of `max_nonterminals` possible expansions is reached, and then use `expand_node_min_cost()` to close the remaining expansions as quickly as possible.

# In[66]:


def expand_tree(tree, grammar, max_nonterminals=10,
                expand_tree_once=expand_tree_once_randomly,
                expand_node=expand_node_randomly,
                disp=False, log=False):

    def _expand_tree_once(tree, grammar, expand_node, disp, log):
        tree = expand_tree_once(tree, grammar, expand_node=expand_node)
        if disp:
            display_tree(tree)
            print(possible_expansions(tree), "possible expansion(s) left")
        if log:
            print(tree)
        return tree

    if disp or log:
        print("Stage 1: Expanding until we reach", max_nonterminals, "unexpanded symbols")

    while 0 < possible_expansions(tree) < max_nonterminals:
        tree = _expand_tree_once(tree, grammar, expand_node, disp, log)

    if disp or log:
        print("Stage 2: Keep on expanding using shortest expansions only")

    while any_possible_expansions(tree):
        tree = _expand_tree_once(tree, grammar, expand_node_min_cost, disp, log)

    assert possible_expansions(tree) == 0

    return tree


# In[67]:


derivation_tree = ("<start>", 
        [("<expr>", 
          [("<expr>", None),
           (" + ", []),
           ("<term>", None)]
         )])

derivation_tree = expand_tree(derivation_tree, EXPR_GRAMMAR, max_nonterminals=5, disp=False)
print("Final tree")
display_tree(derivation_tree)


# In[68]:


all_terminals(derivation_tree)


# Based on this, we can now create a function `grammar_fuzzer()` that – like `simple_grammar_fuzzer()` – simply takes a grammar and produces a string from it, no longer exposing the complexity of derivation trees:

# In[69]:


def grammar_fuzzer(grammar, max_nonterminals=10, start_symbol=START_SYMBOL, 
                   expand_tree_once=expand_tree_once_randomly,
                   expand_node=expand_node_randomly,
                   disp=False, log=False):

    # Create an initial derivation tree
    tree = init_tree(start_symbol)
    # print(tree)

    # Expand all nonterminals
    tree = expand_tree(tree, grammar, max_nonterminals, 
                       expand_tree_once=expand_tree_once,
                       expand_node=expand_node)
    if disp:
        print(repr(all_terminals(tree)))
        display_tree(tree)
    if log:
        print(tree)

    # Return the string
    return all_terminals(tree)


# We can now apply this on all our defined grammars (and visualize the derivation tree along)

# In[70]:


grammar_fuzzer(EXPR_GRAMMAR, disp=True)


# In[71]:


grammar_fuzzer(URL_GRAMMAR, disp=True)


# In[72]:


grammar_fuzzer(CGI_GRAMMAR, disp=True)


# How do we stack up against `simple_grammar_fuzzer()`?

# In[73]:


trials = 100
xs = []
ys = []
for i in range(trials):
    with Timer() as t:
        s = grammar_fuzzer(EXPR_GRAMMAR, max_nonterminals=20)
    xs.append(len(s))
    ys.append(t.elapsed_time())
    print(i, end=" ")

average_time = sum(ys) / trials
print()
print("Average time:", average_time)


# In[74]:


# get_ipython().run_line_magic('matplotlib', 'inline') # only in notebook

import matplotlib.pyplot as plt
plt.scatter(xs, ys)
plt.title('Time required for generating an output');


# Our test generation is much faster, but also our inputs are much smaller.  \todo{(Actually, parts of the time gain may be due to the faster time.)}  We see that with derivation trees, we can get much better control over grammar production.

# ## Alternatives to Grammars
# 
# To formally describe languages, the field of _formal languages_ has devised a number of _language specifications_ that describe a language.  _Regular expressions_, for instance, denote sets of strings: The regular expression `[a-z]*`, for instance, denotes a (possibly empty) sequence of lowercase letters.  _Automata theory_ connects these languages to automata that accept these inputs; _finite state machines_, for instance, can be used to specify the same language as regular expressions.
# 
# Regular expressions are great for not-too-complex input formats, and the associated finite state machine have many properties that make them great for reasoning.  To specify more complex inputs, though, they quickly encounter limitations.  On the other hand of the language spectrum, we have _universal grammars_ that denote the language accepted by _Turing machines_.  A Turing machine can compute anything that can be computed; and with Python being a Turing-complete language, this means that we can also use a Python program $p$ to specify or even enumerate legal inputs.  But then, computer science theory also tells us that each such testing program has to be written specifically for the program to be tested, which is not the level of automation we want.
# 
# 

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

# In[75]:


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

# In[76]:


def expand_node_max_cost(node, grammar):
    (symbol, children) = node
    # print("Expanding " + repr(symbol))
    assert children is None

    # Fetch the possible expansions from grammar...
    expansions = grammar[symbol]

    possible_children_with_cost = [(expansion_to_children(expansion),
                                    expansion_min_cost(expansion, grammar, {symbol}))
                                  for expansion in expansions]

    min_cost = max(cost for (child, cost) in possible_children_with_cost)
    children_with_min_cost = [child for (child, child_cost) in possible_children_with_cost
                              if child_cost == min_cost]

    children = random.choice(children_with_min_cost)

    # Return with a new list
    return (symbol, children)


# In[77]:


def expand_tree_minmax(tree, grammar, min_nonterminals=10, max_nonterminals=10,
                expand_tree_once=expand_tree_once_randomly,
                expand_node=expand_node_randomly,
                disp=False, log=False):
    
    def _expand_tree_once(tree, grammar, expand_node, disp, log):
        tree = expand_tree_once(tree, grammar, expand_node)
        if disp:
            display_tree(tree)
            print(possible_expansions(tree), "possible expansion(s) left")
        if log:
            print(tree)
        return tree

    if disp or log:
        print("Stage 0: Expanding until we reach", max_nonterminals, "unexpanded nonterminals")

    while 0 < possible_expansions(tree) < min_nonterminals:
        tree = _expand_tree_once(tree, grammar, expand_node_max_cost, disp, log)
    
    if disp or log:
        print("Stage 1: Expanding until we reach", max_nonterminals, "unexpanded nonterminals")

    while 0 < possible_expansions(tree) < max_nonterminals:
        tree = _expand_tree_once(tree, grammar, expand_random_node, disp, log)

    if disp or log:
        print("Stage 2: Keep on expanding using shortest expansions only")

    while any_possible_expansions(tree):
        tree = _expand_tree_once(tree, grammar, expand_node_min_cost, disp, log)
        
    assert possible_expansions(tree) == 0

    return tree


# In[79]:


expanded_tree = expand_tree_minmax(init_tree(), EXPR_GRAMMAR, min_nonterminals=10, max_nonterminals=10)
print(repr(all_terminals(expanded_tree)))
display_tree(expanded_tree)


# ### Exercise 4
# 
# Introduce Purdom's approach first expanding yet uncovered expansions \cite{purdom1972} as discussed in [the "Grammars" chapter](Grammars.ipynb).

# _Solution for the exercise_
