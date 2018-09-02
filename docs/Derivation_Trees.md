
_This notebook is a chapter of the book ["Generating Software Tests"](https://uds-se.github.io/fuzzingbook/Main.html)._ <br>
<a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Derivation_Trees.ipynb"><img style="float:right" src="https://mybinder.org/badge.svg" alt="Launch Binder (beta)"></a>
[Interactive version (beta)](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Derivation_Trees.ipynb) • 
[Download code](https://uds-se.github.io/fuzzingbook/code/Derivation_Trees.py) • 
[Table of contents](https://uds-se.github.io/fuzzingbook/Main.html) • 
[Change history](https://github.com/uds-se/fuzzingbook/commits/master/notebooks/Derivation_Trees.ipynb) • 
[Issues and comments](https://github.com/uds-se/fuzzingbook/issues) • 
[Main project page](https://github.com/uds-se/fuzzingbook/)
<hr>

# Fuzzing with Derivation Trees

In the chapter on ["Grammars"](Grammars.html), we have introduced the concept of _grammars_ that specify input formats and _producers_ that randomly generate a valid input from a grammar.  Our implementation was not very efficient, though.  In this chapter, we introduce _derivation trees_ that encode a (produced) string as a syntactic structure.  This allows for efficient production of inputs from grammars, as well as easy manipulation.

**Prerequisites**

* You should know how grammar-based fuzzing works, e.g. from the ["Grammars" chapter](Grammars.html).

## The Trouble with String Replacement

In our [previous chapter](Grammars.html), we had introduced a simple fuzzer that would produce a random string from a grammar, using string replacement.  With each iteration, this fuzzer would go search the string produced so far for symbols to expand.  How expensive is this in the long run?  Let us plot the time required for strings of different lengths.


```python
import fuzzingbook_utils
```


```python
from Grammars import simple_grammar_fuzzer, EXPR_GRAMMAR
```


```python
from Timer import Timer
```


```python
xs = []
ys = []
for i in range(100):
    with Timer() as t:
        s = simple_grammar_fuzzer(EXPR_GRAMMAR, max_symbols=15)
    xs.append(len(s))
    ys.append(t.elapsed_time())
    print(i, end=" ")
```

    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 


```python
%matplotlib inline

import matplotlib.pyplot as plt
plt.scatter(xs, ys)
plt.title('Time required for generating an output');
```


![png](Derivation_Trees_files/Derivation_Trees_8_0.png)


We see that the effort increases quadratically.

\todo{Discuss how we can have outputs that are 20,000 characters long}

## Derivation Trees

## Representing Derivation

e.g. `<expr> + <expr>`


```python
import re
import random
```


```python
from Grammars import START_SYMBOL, RE_SYMBOL, EXPR_GRAMMAR, symbols
```


```python
derivation_tree = ("<start>", 
        [("<expr>", 
          [("<expr>", None),
           (" + ", []),
           ("<expr>", None)]
         )])
```

Let's visualize this tree!


```python
from IPython.display import display
```


```python
from graphviz import Digraph
```


```python
import re
```


```python
def dot_escape(s):
    """Return s in a form suitable for dot"""
    # s = s.replace("\\", "\\\\")
    s = re.sub(r"([^a-zA-Z0-9 ])", r"\\\1", s)
    return s
```


```python
assert dot_escape("hello") == "hello"
assert dot_escape("<hello>, world") == "\\<hello\\>\\, world"
assert dot_escape("\\n") == "\\\\n"
```


```python
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
```


```python
display_tree(derivation_tree)
```


![svg](Derivation_Trees_files/Derivation_Trees_23_0.svg)


## Expanding a Node


```python
def init_tree(start_symbol=START_SYMBOL):
    return (start_symbol, None)
```


```python
def is_symbol(s):
    return re.match(RE_SYMBOL, s)
```


```python
assert is_symbol("<abc>")
assert not is_symbol("+")
```


```python
def expansion_to_children(expansion):
    # print("Converting " + repr(expansion))
    # strings contains all substrings -- both terminals and non-terminals such
    # that ''.join(strings) == expansion
    strings  = re.split(RE_SYMBOL, expansion)
    return [(s, None) if is_symbol(s) else (s, []) for s in strings if len(s) > 0]
```


```python
expansion_to_children("<term> + <expr>")
```




    [('<term>', None), (' + ', []), ('<expr>', None)]




```python
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
```


```python
example_node = ("<term>", None)
example_tree = expand_random_node(example_node, EXPR_GRAMMAR)
display_tree(example_tree)
```


![svg](Derivation_Trees_files/Derivation_Trees_31_0.svg)


## Expanding a Tree


```python
def possible_expansions(tree):
    (symbol, children) = tree
    if children is None:
        return 1

    number_of_expansions = sum(possible_expansions(c) for c in children)
    return number_of_expansions
```


```python
print(possible_expansions(example_tree))
```

    2



```python
def any_possible_expansions(tree):
    (symbol, children) = tree
    if children is None: return True

    return any(any_possible_expansions(c) for c in children)
```


```python
print(any_possible_expansions(example_tree))
```

    True



```python
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
```


```python
example_tree_expanded = expand_tree_once(example_tree, EXPR_GRAMMAR)
display_tree(example_tree_expanded)
```


![svg](Derivation_Trees_files/Derivation_Trees_38_0.svg)



```python
example_tree_expanded_twice = expand_tree_once(example_tree_expanded, EXPR_GRAMMAR)
display_tree(example_tree_expanded_twice)
```


![svg](Derivation_Trees_files/Derivation_Trees_39_0.svg)


## Closing the Expansion


```python
def symbol_min_cost(symbol, grammar, seen=set()):
    expansions = grammar[symbol]
    return min(min_expansions(e, grammar, seen | {symbol}) for e in expansions)
```


```python
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
```


```python
assert symbol_min_cost("<digit>", EXPR_GRAMMAR) == 1
```


```python
assert symbol_min_cost("<expr>", EXPR_GRAMMAR) == 5
```


```python
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
```

## All Together


```python
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
```


```python
expanded_tree = expand_tree(example_tree, EXPR_GRAMMAR, max_symbols=5, disp=False)
print("Final tree")
display_tree(expanded_tree)
```

    Final tree



![svg](Derivation_Trees_files/Derivation_Trees_48_1.svg)



```python
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
```


```python
all_terminals(expanded_tree)
```




    '4 * 1 * +2.09'




```python
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
```


```python
from Grammars import URL_GRAMMAR
```

\todo{We have trouble with expansions into empty strings - they are not visualized properly, and ignored by `allterminals()`}


```python
expanded_tree = expand_tree(init_tree(), URL_GRAMMAR, max_symbols=5)
print(repr(all_terminals(expanded_tree)))
print(expanded_tree)
display_tree(expanded_tree)
```

    'ftps://user:password@fuzzingbook.com:80<path><query>'
    ('<start>', [('<call>', [('<url>', [('<scheme>', [('ftps', [])]), ('://', []), ('<authority>', [('<userinfo>', [('user:password', [])]), ('@', []), ('<host>', [('fuzzingbook.com', [])]), (':', []), ('<port>', [('80', [])])]), ('<path>', []), ('<query>', [])])])])



![svg](Derivation_Trees_files/Derivation_Trees_54_1.svg)



```python
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
```

    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 
    Average time: 0.02638135053915903



```python
%matplotlib inline

import matplotlib.pyplot as plt
plt.scatter(xs, ys)
plt.title('Time required for generating an output');
```


![png](Derivation_Trees_files/Derivation_Trees_56_0.png)


## Lessons Learned

* _Lesson one_
* _Lesson two_
* _Lesson three_

## Next Steps

_Link to subsequent chapters (notebooks) here, as in:_

* [use _mutations_ on existing inputs to get more valid inputs](Mutation_Fuzzing.html)
* [use _grammars_ (i.e., a specification of the input format) to get even more valid inputs](Grammars.html)
* [reduce _failing inputs_ for efficient debugging](Reducing.html)


## Exercises

_Close the chapter with a few exercises such that people have things to do.  Use the Jupyter `Exercise2` nbextension to add solutions that can be interactively viewed or hidden.  (Alternatively, just copy the exercise and solution cells below with their metadata.)  We will set up things such that solutions do not appear in the PDF and HTML formats._

### Exercise 1

Speed up things by memoizing.


```python
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
```

_Solution for the exercise_

### Exercise 2

Speed up things by tracking which children still can be expanded.

_Solution for the exercise_

### Exercise 3

Introduce a parameter `min_symbols` that would keep on expanding with _maximum_ cost until `min_symbols` is reached.


```python
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
```


```python
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
```


```python
expanded_tree = expand_tree_minmax(init_tree(), EXPR_GRAMMAR, min_symbols=10, max_symbols=10)
print(repr(all_terminals(expanded_tree)))
display_tree(expanded_tree)
```

    '0 - 9 / 7 - 3 * 3 / +1 - 4 * 8 * (2) / (5)'



![svg](Derivation_Trees_files/Derivation_Trees_68_1.svg)


### Exercise 4

Introduce Purdom's approach first expanding yet uncovered expansions \cite{purdom1972} as discussed in [the "Grammars" chapter](Grammars.html).

_Solution for the exercise_

<hr>

<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">

_This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)._<br>
