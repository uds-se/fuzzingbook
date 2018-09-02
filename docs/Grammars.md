
_This notebook is a chapter of the book ["Generating Software Tests"](https://uds-se.github.io/fuzzingbook/Main.html)._ <br>
<a href="https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Grammars.ipynb"><img style="float:right" src="https://mybinder.org/badge.svg" alt="Launch Binder (beta)"></a>
[Interactive version (beta)](https://mybinder.org/v2/gh/uds-se/fuzzingbook/master?filepath=notebooks/Grammars.ipynb) • 
[Download code](https://uds-se.github.io/fuzzingbook/code/Grammars.py) • 
[Table of contents](https://uds-se.github.io/fuzzingbook/Main.html) • 
[Change history](https://github.com/uds-se/fuzzingbook/commits/master/notebooks/Grammars.ipynb) • 
[Issues and comments](https://github.com/uds-se/fuzzingbook/issues) • 
[Main project page](https://github.com/uds-se/fuzzingbook/)
<hr>

# Fuzzing with Grammars

In the chapter on ["Mutation-Based Fuzzing"](Mutation_Fuzzing.html), we have seen how to use extra hints – such as sample input files – to speed up test generation.  In this chapter, we take this idea one step further, by providing a _specification_ of the legal inputs to a program.  These _grammars_ allow for very effective and efficient testing, as we will see in this chapter.

**Prerequisites**

* You should know how basic fuzzing works, e.g. from the [Chapter introducing fuzzing](Basic_Fuzzing.html).
* Knowledge on [mutation-based fuzzing](Mutation_Fuzzing.html) and [coverage](Coverage.html) is _not_ required yet, but still recommended.

## Input Languages

All possible behaviors of a program can be triggered by its input.  "Input" here can be a wide range of possible sources: We are talking about data read from files or over the network, data input by the user, or data acquired from interaction with other resources.  The set of all these inputs determines how the program will behave – including its failures.  When testing, it is thus very helpful to think about possible input sources, how to get them under control, and _how to systematically test them_.

For the sake of simplicity, we will assume for now that the program has only one source of inputs; this is the same assumption we have been using in the previous chapters, too.  The set of valid inputs to a program is called a _language_.  Languages range from the simple to the complex: the CSV language denotes the set of valid comma-separated inputs, whereas the Python language denotes the set of valid Python programs.  We commonly separate data languages and programming languages, although any program can also be treated as input data (say, to a compiler).  The [Wikipedia page on file formats](https://en.wikipedia.org/wiki/List_of_file_formats) lists more than 1,000 different file formats, each of which is its own language.

## Grammars

### Rules and Expansions

To formally specify input languages, _grammars_ are among the most popular (and best understood) formalisms.  A grammar consists of a _start symbol_ and a set of _rules_ which indicate how the start symbol (and other symbols) can be expanded.  As an example, consider the following grammar, denoting a sequence of two digits:

```grammar
<start> ::= <digit><digit>
<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

To read such a grammar, start with the starting symbol (`<start>`).  A rule `<A> ::= <B>` means that the symbol on the left side (`<A>`) can be replaced by the string on the right side (`<B>`).  In the above grammar, `<start>` would be replaced by `<digit><digit>`.

In this string again, `<digit>` would be replaced by the string on the right side of the `<digit>` rule.  The special operator `|` denotes _alternatives_, meaning that any of the digits can be chosen for an expansion.  Each `<digit>` thus would be expanded into one of the given digits, eventually yielding a string between `00` and `99`.  There are no further expansions for `0` to `9`, so we are all set.

The interesting thing about grammars is that they can be _recursive_. That is, expansions can make use of symbols expanded earlier – which would then be expanded again.  As an example, consider a grammar that describes integers:

```grammar
<start>  ::= <integer>
<integer> ::= <digit> | <digit><integer>
<digit>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

Here, a `<integer>` is either a single digit, or a digit followed by another integer.  The number `1234` thus would be represented as a single digit `1`, followed by the integer `234`, which in turn is a digit `2`, followed by the integer `34`.

If we wanted to express that an integer can be preceded by a sign (`+` or `-`), we would write the grammar as

```grammar
<start>   ::= <number>
<number>  ::= <integer> | +<integer> | -<integer>
<integer> ::= <digit> | <digit><integer>
<digit>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

These rules formally define the language: Anything that can be derived from the start symbol is part of the language; anything that cannot is not.

### Arithmetic Expressions

Let us expand our grammar to cover full _arithmetic expressions_ – a poster child example for a grammar.  We see that an expression (`<expr>`) is either a sum, or a difference, or a term; a term is either a product or a division, or a factor; and a factor is either a number or a parenthesized expression.  Amost all rules can have recursion, and thus allow arbitrary complex expressions such as `(1 + 2) * (3.4 / 5.6 - 789)`.

```grammar
<start>   ::= <expr>
<expr>    ::= <expr> + <term> | <expr> - <term> | <term>
<term>    ::= <term> * <factor> | <term> / <factor> | <factor>
<factor>  ::= +<factor> | -<factor> | (<expr>) | <integer> | <integer>.<integer>
<integer> ::= <digit> | <digit><integer>
<digit>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

In such a grammar, if we start with `<start>` and then expand one symbol after another, randomly choosing alternatives, we can quickly produce one valid arithmetic expression after another.  Such _grammar fuzzing_ is highly effective as it comes to produce complex inputs, and this is what we will implement in this chapter.

## Representing Grammars in Python

Our first step in building a grammar fuzzer is to find an appropriate format for grammars.  To make the writing of grammars as simple as possible, we use a mostly format that is mostly based on strings.  Our grammars in Python takes the format of a _mapping_ between symbol names and expansions, where expansions are _lists_ of alternatives.  A one-rule grammar for digits thus takes the form


```python
import fuzzingbook_utils
```


```python
DIGIT_GRAMMAR = {
    "<start>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}
```

whereas the full grammar for arithmetic expressions looks like this:


```python
EXPR_GRAMMAR = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<expr> + <term>", "<expr> - <term>", "<term>"],

    "<term>":
        ["<term> * <factor>", "<term> / <factor>", "<factor>"],

    "<factor>":
        ["+<factor>", "-<factor>", "(<expr>)", "<integer>", "<integer>.<integer>"],

    "<integer>":
        ["<integer><digit>", "<digit>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}
```

In the grammar, we can access any rule by its symbol...


```python
EXPR_GRAMMAR["<digit>"]
```




    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']



....and we can check whether a symbol is in the grammar:


```python
"<identifier>" in EXPR_GRAMMAR
```




    False



## Hatching Grammars

Since grammars are represented as strings, it is fairly easy to introduce errors.  So let us introduce a helper function that checks a grammar for consistency.

Frst, this handy `nonterminals()` function gets us the list of nonterminals in an expansion.  


```python
import re

# As a symbol, we can have anything between <...> except spaces.
RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')
```


```python
def nonterminals(expansion):
    return re.findall(RE_NONTERMINAL, expansion)
```


```python
assert nonterminals("<term> * <factor>") == ["<term>", "<factor>"]
assert nonterminals("<digit><integer>") == ["<digit>", "<integer>"]
assert nonterminals("1 < 3 > 2") == []
assert nonterminals("1 <3> 2") == ["<3>"]
assert nonterminals("1 + 2") == []
```

Likewise, `is_nonterminal()` checks whether some symbol is a nonterminal:


```python
def is_nonterminal(s):
    return re.match(RE_NONTERMINAL, s)
```


```python
assert is_nonterminal("<abc>")
assert not is_nonterminal("+")
```

The helper function `is_valid_grammar()` iterates over a grammar to check whether all used symbols are defined, and vice versa, which is very useful for debugging.  You don't have to dwelve into details here, but as always, it is important to get the input data straight before we make use of it.


```python
import sys
```


```python
START_SYMBOL = "<start>"
```


```python
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
```

Our expression grammar passes the test:


```python
assert is_valid_grammar(EXPR_GRAMMAR)
```

But these ones don't:


```python
assert not is_valid_grammar({"<start>": ["<x>"], "<y>": ["1"]})
```

    '<y>': defined, but not used
    '<x>': used, but not defined



```python
assert not is_valid_grammar({"<start>": "123"})
```

    '<start>': expansion is not a list



```python
assert not is_valid_grammar({"<start>": []})
```

    '<start>': expansion list empty



```python
assert not is_valid_grammar({"<start>": [1, 2, 3]})
```

    '<start>': 1: not a string


## A Simple Grammar Fuzzer

Let us now put the above grammars to use.   We will build a very simple grammar fuzzer that starts with a start symbol (`"<start>"`) and then keeps on expanding it.  To avoid expansion to infinite inputs, we place a limit (`max_symbols`) on the number of symbols.  Furthermore, to avoid being stuck in a sitution where we cannot reduce the number of symbols any further, we also limit the total number of expansion steps.


```python
import random
```


```python
class ExpansionError(Exception):
    pass
```


```python
def simple_grammar_fuzzer(grammar, start_symbol=START_SYMBOL, max_nonterminals=10, max_expansion_trials=100, log=False):
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
```

Let us see how this simple grammar fuzzer obtains an arithmetic expression from the start symbol:


```python
simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=3, log=True)
```

    <start> -> <expr>                        <expr>
    <expr> -> <term>                         <term>
    <term> -> <term> / <factor>              <term> / <factor>
    <factor> -> +<factor>                    <term> / +<factor>
    <term> -> <factor>                       <factor> / +<factor>
    <factor> -> <integer>                    <integer> / +<factor>
    <factor> -> -<factor>                    <integer> / +-<factor>
    <factor> -> -<factor>                    <integer> / +--<factor>
    <factor> -> +<factor>                    <integer> / +--+<factor>
    <factor> -> +<factor>                    <integer> / +--++<factor>
    <factor> -> (<expr>)                     <integer> / +--++(<expr>)
    <integer> -> <digit>                     <digit> / +--++(<expr>)
    <digit> -> 1                             1 / +--++(<expr>)
    <expr> -> <expr> + <term>                1 / +--++(<expr> + <term>)
    <expr> -> <term>                         1 / +--++(<term> + <term>)
    <term> -> <factor>                       1 / +--++(<factor> + <term>)
    <factor> -> -<factor>                    1 / +--++(-<factor> + <term>)
    <term> -> <factor>                       1 / +--++(-<factor> + <factor>)
    <factor> -> (<expr>)                     1 / +--++(-(<expr>) + <factor>)
    <factor> -> (<expr>)                     1 / +--++(-(<expr>) + (<expr>))
    <expr> -> <term>                         1 / +--++(-(<term>) + (<expr>))
    <expr> -> <term>                         1 / +--++(-(<term>) + (<term>))
    <term> -> <factor>                       1 / +--++(-(<factor>) + (<term>))
    <factor> -> +<factor>                    1 / +--++(-(+<factor>) + (<term>))
    <term> -> <factor>                       1 / +--++(-(+<factor>) + (<factor>))
    <factor> -> <integer>                    1 / +--++(-(+<integer>) + (<factor>))
    <factor> -> -<factor>                    1 / +--++(-(+<integer>) + (-<factor>))
    <factor> -> <integer>                    1 / +--++(-(+<integer>) + (-<integer>))
    <integer> -> <digit>                     1 / +--++(-(+<digit>) + (-<integer>))
    <integer> -> <digit>                     1 / +--++(-(+<digit>) + (-<digit>))
    <digit> -> 3                             1 / +--++(-(+3) + (-<digit>))
    <digit> -> 1                             1 / +--++(-(+3) + (-1))





    '1 / +--++(-(+3) + (-1))'




```python
for i in range(10):
    print(simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=5))
```

    -+39 * +--(--+-1 - +-(((-+(+-0.1 * -16))) + +((2))) * -7 - +--(+7.46 / 5) / -+-0.4) / 5 * 9
    +5 + +08.4 * -++9.93
    (--++(((2 - -(4 - -++2 / -(+(-+-+(9))) / -(--4) + 4 - 5 + +-++-8 + --((-4 + +((5 - +-++--(-(+4) * (768 - (1 + 2)) * -21))) * (7) * +(-7) * 3 * -(3.1)))))))) + (+-9) * (((+8))) - (-+-+42 - 8)
    +--82 * +(1) * 2 / +4
    (+-+((+-(0)) * --+-((+(8)) / (-+-(1) - +--4 / --+(+86.32) * ---0.1 + +-3)))) - +-+(+---982) / (---2) + 2 - 3956
    209
    ++3 - 3 - --(6) / (+(3 - +4) * +4) - -(6.0 / ---1.3 / +1)
    68.57
    1 - -(+3 - -(-+7 + --+(9))) + -+----+7 / -(-0 - ((((3 + +(+--9 / (-+6) / -10 * (((+(--7) / (--+328 / 1) - -----+6.7) + (+6)))) / -(+0)))) - (-6) - 7 * -(-8)))
    7.4


\todo{Discuss.}

Note that this fuzzer is rather inefficient due to the large number of search and replace operations.  On the other hand, the implementation is straight-forward and does the job.  For this chapter, we'll stick to it; in the [next chapter](Derivation_Trees.html), we'll show how to build a more efficient one.

## Some Grammars

With grammars, we can easily specify the format for several of the examples we discussed earlier.  The above arithmetic expressions, for instance, can be directly sent into `bc` (or any other program that takes arithmetic expressions.  

Let us create some more grammars.  Here's one for `cgi_decode()`:


```python
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
```


```python
for i in range(10):
    print(simple_grammar_fuzzer(grammar=CGI_GRAMMAR, max_nonterminals=10))
```

    d
    +
    %da
    50
    ++c%f44
    5
    %e7-+
    1
    +++
    a


Or a URL grammar:


```python
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
```


```python
for i in range(10):
    print(simple_grammar_fuzzer(grammar=URL_GRAMMAR, max_nonterminals=10))
```

    https://user:password@www.google.com/def
    ftps://fuzzingbook.com:8080?abc=def
    ftps://user:password@fuzzingbook.com/
    ftps://cispa.saarland:61/
    ftp://user:password@cispa.saarland/
    http://user:password@fuzzingbook.com:0/x37?x44=abc
    https://fuzzingbook.com/
    http://www.google.com/
    https://cispa.saarland:3/def?x72=06&x30=def&def=x60&abc=abc
    ftp://www.google.com:8080/?def=3&abc=abc&x26=64&abc=9&x08=def


## A More Efficient Algorithm

While simple and straight-forward, our grammar production algorithm suffers from two problems:

1. *It is inefficient*.  With each iteration, this fuzzer would go search the string produced so far for symbols to expand.  This becomes inefficient as the production string grows.

2. *It is hard to control.*  Even while limiting the number of symbols, it is still possible to obtain very long strings.

Both problems can be easily illustrated by plotting the time required for strings of different lengths.


```python
from Timer import Timer
```


```python
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
```

    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 
    Average time: 0.28545589194080095



```python
%matplotlib inline

import matplotlib.pyplot as plt
plt.scatter(xs, ys)
plt.title('Time required for generating an output');
```


![png](Grammars_files/Grammars_53_0.png)


We see that (1) the effort increases quadratically over time, and (2) we can easily produce outputs that are tens of thousands of characters long.

## Derivation Trees

To both obtain a more efficient algorithm _and_ exercise better control over expansions, we will use a special representation for the strings that our grammar produces.  The general idea is to use a _tree_ structure that will be subsequently expanded – a so-called _derivation tree_.

The expansion process with derivation trees is illustrated in the following steps.  We use `dot` as a drawing program; you don't need to look at the code, just at its results.  We start with a single node as root of the tree.


```python
from graphviz import Digraph
```


```python
dot = Digraph("root")
dot.attr('node', shape='plain')
dot.node(r"\<start\>")
dot
```




![svg](Grammars_files/Grammars_57_0.svg)



We then traverse the tree, searching for a symbol to expand, and add a new edge from the symbol to its expansion.


```python
dot.edge(r"\<start\>", r"\<expr\>")
dot
```




![svg](Grammars_files/Grammars_59_0.svg)



To construct the actually produced string from the derivation tree, we traverse the tree in order and collect the symbols at the leaves of the tree.  In the case above, we obtain the string `<expr>`.

To further expand the tree, we choose a symbol to expand, and add a new edge from the symbol to its expansion.  This would get us the string `<expr> + <term>`.


```python
dot.edge(r"\<expr\>", r"\<expr\> ")
dot.edge(r"\<expr\>", r"+")
dot.edge(r"\<expr\>", r"\<term\>")
dot
```




![svg](Grammars_files/Grammars_61_0.svg)



We repeat the process until there are no symbols left to expand:


```python
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
```




![svg](Grammars_files/Grammars_63_0.svg)



We now have a representation for the string `2 + 2`.  In contrast to the string alone, though, the derivation tree records the entire structure (and production history) of the produced string.  It also allows for simple comparison and manipulation – say, replacing one subtree (substructure) against another.

## Representing Derivation Trees

To represent a derivation tree in Python, we use the following format.  A node is a pair

```python
(SYMBOL_NAME, CHILDREN)
```

where `SYMBOL_NAME` is a string representing the node (i.e. `<start>` or `+`) and `CHILDREN` is a list of children nodes.

`CHILDREN` can take some special values:

1. `None` as a placeholder for future expansion.  This means that the node is a _nonterminal symbol_ that should be expanded further.
2. `[]` (i.e., the empty list) to indicate _no_ children.  This means that the node is a _terminal symbol_ that can no longer be expanded.

Let us take a very simple derivation tree, representing the intermediate step `<expr> + <term>`, above.


```python
derivation_tree = ("<start>", 
        [("<expr>", 
          [("<expr>", None),
           (" + ", []),
           ("<term>", None)]
         )])
```

Let's visualize this tree!  Again, we use the `dot` drawing program, but now do this algorithmically, traversing the above structure; as with the above visualizations, only the result counts.


```python
from IPython.display import display
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
                nonlocal counter  # Assign each node a unique identifier
                counter += 1
                child_id = counter
                dot.edge(repr(id), repr(child_id))
                traverse_tree(dot, child, child_id)

    dot = Digraph(comment="Derivation Tree")
    dot.attr('node', shape='plain')
    traverse_tree(dot, derivation_tree)
    display(dot)
```

This is what our tree visualizes into:


```python
display_tree(derivation_tree)
```


![svg](Grammars_files/Grammars_74_0.svg)


To turn the tree into a string, the following function comes in handy:


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
all_terminals(derivation_tree)
```




    '<expr> + <term>'



## Expanding a Node

Let us now develop an algorithm that takes a tree with unexpanded symbols (say, `derivation_tree`, above), and expands all these symbols onbe after the other.  First, let us define a helper function that constructs a tree with just the start symbol:


```python
def init_tree(start_symbol=START_SYMBOL):
    return (start_symbol, None)
```


```python
display_tree(init_tree())
```


![svg](Grammars_files/Grammars_81_0.svg)


Next, we will need a helper function that takes an expansion string and converts it into a list of derivation trees:


```python
def expansion_to_children(expansion):
    # print("Converting " + repr(expansion))
    # strings contains all substrings -- both terminals and non-terminals such
    # that ''.join(strings) == expansion
    if expansion == "":  # Special case: empty expansion
        return [("", [])]
    strings  = re.split(RE_NONTERMINAL, expansion)
    return [(s, None) if is_nonterminal(s) else (s, []) for s in strings if len(s) > 0]
```


```python
expansion_to_children("<term> + <expr>")
```




    [('<term>', None), (' + ', []), ('<expr>', None)]



The case of an empty expansion needs special treatment:


```python
expansion_to_children("")
```




    [('', [])]



With this, we can now take some unexpanded node in the tree, choose a random expansion, and return the new tree


```python
def expand_node_randomly(node, grammar):
    (symbol, children) = node
    assert children is None

    # Fetch the possible expansions from grammar...
    expansions = grammar[symbol]

    possible_children = [expansion_to_children(expansion) for expansion in expansions]

    # TODO: Consider preferring children not expanded yet,
    # and other forms of grammar coverage (or code coverage)
    children = random.choice(possible_children)

    # Return with new children
    return (symbol, children)
```


```python
print("Before:")
tree = ("<term>", None)
display_tree(tree)

print("After:")
tree = expand_node_randomly(tree, EXPR_GRAMMAR)
display_tree(tree)
```

    Before:



![svg](Grammars_files/Grammars_89_1.svg)


    After:



![svg](Grammars_files/Grammars_89_3.svg)


## Expanding a Tree

Let us now apply the above node expansion to some node in the tree.  To this end, we first need to search the tree for unexpanded nodes.  `possible_expansions()` counts how many unexpanded symbols there are in a tree:


```python
def possible_expansions(tree):
    (symbol, children) = tree
    if children is None:
        return 1

    number_of_expansions = sum(possible_expansions(c) for c in children)
    return number_of_expansions
```


```python
print(possible_expansions(derivation_tree))
```

    2


`any_possible_expansions()` returns True if the tree has any unexpanded nodes.


```python
def any_possible_expansions(tree):
    (symbol, children) = tree
    if children is None: return True

    return any(any_possible_expansions(c) for c in children)
```


```python
print(any_possible_expansions(derivation_tree))
```

    True


Here comes `expand_tree_once()`, the core method of our tree expansion algorithm.  It first checks whether it is currently being applied on a nonterminal symbol without expansion; if so, it invokes `expand_node_randomly()` on it as above.  (With the `expand_node` parameter, we can actually select the function to use for expansion.)

If the node is already expanded (i.e. has children), it checks the subset of children which still have unexpanded symbols; ranomly selects one of them, and applies itself recursively on that child.

The `expand_tree_once()` function replaces the child _in place_, meaning that it actually mutates the tree being passed as an argument rather than returning a new tree.  This in-place mutation is what makes this function particularly efficient.


```python
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
    children[child_to_be_expanded] = expand_tree_once_randomly(children[child_to_be_expanded], grammar, expand_node)

    return tree
```

Let's put it to use, expanding our derivation tree from above twice.


```python
derivation_tree = ("<start>", 
        [("<expr>", 
          [("<expr>", None),
           (" + ", []),
           ("<term>", None)]
         )])
display_tree(derivation_tree)
```


![svg](Grammars_files/Grammars_99_0.svg)



```python
derivation_tree = expand_tree_once_randomly(derivation_tree, EXPR_GRAMMAR)
display_tree(derivation_tree)
```


![svg](Grammars_files/Grammars_100_0.svg)



```python
derivation_tree = expand_tree_once_randomly(derivation_tree, EXPR_GRAMMAR)
display_tree(derivation_tree)
```


![svg](Grammars_files/Grammars_101_0.svg)


We see that which each step, one more symbol is expanded.  Now all it takes is to apply this again and again, expanding the tree further and further.

## Closing the Expansion

With `expand_tree_once()`, we can keep on expanding the tree – but how do we actually stop?  The key idea here, introduced by Luke in \cite{Luke2000}, is that after inflating the derivation tree to some maximum size, we _only want to apply expansions that increase the size of the tree by a minimum_.  For `<factor>`, for instance, we would prefer an expansion into `<integer>`, as this will not introduce further recursion (and potential size inflation); for `<integer>`, likewise, an expansion into `<digit>` is preferred, as it will less increase tree size than `<digit><integer>`.

To identify the _cost_ of expanding a symbol, we introduce two functions that mutually rely on each other.  First, `symbol_min_cost()` returns the minimum cost of all expansions of a symbol, using `expansion_min_cost()` to compute the cost for each expansion.


```python
def symbol_min_cost(symbol, grammar, seen=set()):
    expansions = grammar[symbol]
    return min(expansion_min_cost(e, grammar, seen | {symbol}) for e in expansions)
```

The function `expansion_min_cost()` returns the sum of all expansions in `expansions`.  If a nonterminal is encountered again during traversal, the cost of the expansion is $\infty$, as this indicates (potential infinite) recursion.


```python
def expansion_min_cost(expansion, grammar, seen=set()):
    syms = nonterminals(expansion)
    if len(syms) == 0:
        return 1  # no symbol

    if any(s in seen for s in syms):
        return float('inf')

    # the value of a expansion is the sum of all expandable variables inside + 1
    return sum(symbol_min_cost(s, grammar, seen) for s in syms) + 1
```

Here's two examples: The minimum cost of expanding a digit is 1, since we have to choose between one of its expansions.


```python
assert symbol_min_cost("<digit>", EXPR_GRAMMAR) == 1
```

The minimum number of expansions when expanding `<expr>`, though, is five, as this is the minimum number of expansions required.  (`<expr>` → `<term>` → `<factor>` → `<integer>` → `<digit>` → 1)


```python
assert symbol_min_cost("<expr>", EXPR_GRAMMAR) == 5
```

Here's now a variant of `expand_node_randomly()` that takes the above cost into account.  It determines the minimum cost `min_cost` across all children and then uses the child with the minimum cost.  If multiple children all have the same minimum cost, it chooses randomly between these.


```python
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
```

We can now apply this function to close the expansion of our derivation tree, using `expand_tree_once()` with the above `expand_node_min_cost()` as expansion function.


```python
display_tree(derivation_tree)

while any_possible_expansions(derivation_tree):
    derivation_tree = expand_tree_once_randomly(derivation_tree, EXPR_GRAMMAR, expand_node=expand_node_min_cost)
    display_tree(derivation_tree)
```


![svg](Grammars_files/Grammars_114_0.svg)



![svg](Grammars_files/Grammars_114_1.svg)



![svg](Grammars_files/Grammars_114_2.svg)



![svg](Grammars_files/Grammars_114_3.svg)



![svg](Grammars_files/Grammars_114_4.svg)



![svg](Grammars_files/Grammars_114_5.svg)



![svg](Grammars_files/Grammars_114_6.svg)



![svg](Grammars_files/Grammars_114_7.svg)



![svg](Grammars_files/Grammars_114_8.svg)



![svg](Grammars_files/Grammars_114_9.svg)



![svg](Grammars_files/Grammars_114_10.svg)



![svg](Grammars_files/Grammars_114_11.svg)



![svg](Grammars_files/Grammars_114_12.svg)



![svg](Grammars_files/Grammars_114_13.svg)



![svg](Grammars_files/Grammars_114_14.svg)



![svg](Grammars_files/Grammars_114_15.svg)



![svg](Grammars_files/Grammars_114_16.svg)



![svg](Grammars_files/Grammars_114_17.svg)


We see that in each step, `expand_node_min_cost()` chooses an expansion that does not increase the number of symbols, evantually closing all open expansions.

## All Together

We can now put both phases together in a single function `expand_tree` that will expand a tree first with `expand_node_randomly()` until a limit of `max_nonterminals` possible expansions is reached, and then use `expand_node_min_cost()` to close the remaining expansions as quickly as possible.


```python
def expand_tree(tree, grammar, max_nonterminals=10, expand_tree_once=expand_tree_once_randomly, disp=False, log=False):
    
    def _expand_tree_once(tree, grammar, expand_node, disp, log):
        tree = expand_tree_once(tree, grammar, expand_node)
        if disp:
            display_tree(tree)
            print(possible_expansions(tree), "possible expansion(s) left")
        if log:
            print(tree)
        return tree

    if disp or log:
        print("Stage 1: Expanding until we reach", max_nonterminals, "unexpanded symbols")

    while 0 < possible_expansions(tree) < max_nonterminals:
        tree = _expand_tree_once(tree, grammar, expand_node_randomly, disp, log)

    if disp or log:
        print("Stage 2: Keep on expanding using shortest expansions only")

    while any_possible_expansions(tree):
        tree = _expand_tree_once(tree, grammar, expand_node_min_cost, disp, log)
        
    assert possible_expansions(tree) == 0

    return tree
```


```python
derivation_tree = ("<start>", 
        [("<expr>", 
          [("<expr>", None),
           (" + ", []),
           ("<term>", None)]
         )])

derivation_tree = expand_tree(derivation_tree, EXPR_GRAMMAR, max_nonterminals=5, disp=False)
print("Final tree")
display_tree(derivation_tree)
```

    Final tree



![svg](Grammars_files/Grammars_118_1.svg)



```python
all_terminals(derivation_tree)
```




    '9 + 3 * 7 / 0.1'



Based on this, we can now create a function `grammar_fuzzer()` that – like `simple_grammar_fuzzer()` – simply takes a grammar and produces a string from it, no longer exposing the complexity of derivation trees:


```python
def grammar_fuzzer(grammar, max_nonterminals=10, start_symbol=START_SYMBOL, expand_tree_once=expand_tree_once_randomly, 
                   disp=False, log=False):
    # Create an initial derivation tree
    tree = init_tree(start_symbol)
    # print(tree)

    # Expand all nonterminals
    tree = expand_tree(tree, grammar, max_nonterminals, expand_tree_once)
    if disp:
        print(repr(all_terminals(tree)))
        display_tree(tree)
    if log:
        print(tree)

    # Return the string
    return all_terminals(tree)
```

We can now apply this on all our defined grammars (and visualize the derivation tree along)


```python
grammar_fuzzer(EXPR_GRAMMAR, disp=True)
```

    '460.7 / -0.7538 / +(2 * (8) / -9.391)'



![svg](Grammars_files/Grammars_123_1.svg)





    '460.7 / -0.7538 / +(2 * (8) / -9.391)'




```python
grammar_fuzzer(URL_GRAMMAR, disp=True)
```

    'ftps://user:password@cispa.saarland/?x01=abc'



![svg](Grammars_files/Grammars_124_1.svg)





    'ftps://user:password@cispa.saarland/?x01=abc'




```python
grammar_fuzzer(CGI_GRAMMAR, disp=True)
```

    '0'



![svg](Grammars_files/Grammars_125_1.svg)





    '0'



How do we stack up against `simple_grammar_fuzzer()`?


```python
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
```

    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 
    Average time: 0.03342591954016825



```python
%matplotlib inline

import matplotlib.pyplot as plt
plt.scatter(xs, ys)
plt.title('Time required for generating an output');
```


![png](Grammars_files/Grammars_128_0.png)


Our test generation is much faster, but also our inputs are much smaller.  \todo{(Actually, parts of the time gain may be due to the faster time.)}  We see that with derivation trees, we can get much better control over grammar production.

## Grammar Coverage

At this point, when we produce from grammars, all possible expansions get the same likelihood.  For producing a comprehensive test suite, however, it makes more sense to maximize _variety_ – for instance, by avoiding repeating the same expansions over and over again.  To achieve this, we can track the _coverage_ of individual expansions: If we have seen some expansion already, we can prefer other possible expansions in the future.  The idea of ensuring that each expansion in the grammar is used at least once goes back to Paul Purdom \cite{purdom1972}.

As an example, consider the grammar

```grammar
<start> ::= <digit><digit>
<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
```

Let us assume we have already produced a `0` in the first expansion of `<digit>`.  As it comes to expand the next digit, we would mark the `0` expansion as already covered, and choose one of the yet uncovered alternatives.  Only when we have covered all alternatives would we go back and consider expansions covered before.

This concept of coverage is very easy to implement.


```python
covered_expansions = set()

# TODO: Have two functions that hook into choosing children and choosing nodes.
```

By returning the set of expansions covered so far, we can invoke the fuzzer multiple times, each time adding to the grammar coverage.  With the `DIGIT_EXPR` grammar, for instance, this lets the grammar produce one digit after the other:


```python
grammar_fuzzer(DIGIT_GRAMMAR)
```




    '1'



At the end, all expansions are covered:


```python
covered_expansions
```




    set()



Let us now create some more expressions:


```python
# covered_expansions = set()
# for i in range(10):
#     term, covered_expansions = \
#         grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=3, covered_expansions=covered_expansions)
#     print(term)
```

Again, all expansions are covered:


```python
covered_expansions
```




    set()



## Alternatives to Grammars

To formally describe languages, the field of _formal languages_ has devised a number of _language specifications_ that describe a language.  _Regular expressions_, for instance, denote sets of strings: The regular expression `[a-z]*`, for instance, denotes a (possibly empty) sequence of lowercase letters.  _Automata theory_ connects these languages to automata that accept these inputs; _finite state machines_, for instance, can be used to specify the same language as regular expressions.

Regular expressions are great for not-too-complex input formats, and the associated finite state machine have many properties that make them great for reasoning.  To specify more complex inputs, though, they quickly encounter limitations.  On the other hand of the language spectrum, we have _universal grammars_ that denote the language accepted by _Turing machines_.  A Turing machine can compute anything that can be computed; and with Python being a Turing-complete language, this means that we can also use a Python program $p$ to specify or even enumerate legal inputs.  But then, computer science theory also tells us that each such testing program has to be written specifically for the program to be tested, which is not the level of automation we want.



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

### Exercise 4

Introduce Purdom's approach first expanding yet uncovered expansions \cite{purdom1972} as discussed in [the "Grammars" chapter](Grammars.html).

_Solution for the exercise_

<hr>

<img style="float:right" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" alt="Creative Commons License">

_This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)._<br>
