#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This code is part of "Generating Software Tests"
# (https://www.fuzzingbook.org/)
# It is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License,
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)


# # Fuzzing with Grammars
# 
# In the chapter on ["Mutation-Based Fuzzing"](MutationFuzzer.ipynb), we have seen how to use extra hints – such as sample input files – to speed up test generation.  In this chapter, we take this idea one step further, by providing a _specification_ of the legal inputs to a program.  These _grammars_ allow for very systematic and efficient test generation, in particular for complex input formats.

# **Prerequisites**
# 
# * You should know how basic fuzzing works, e.g. from the [Chapter introducing fuzzing](Fuzzer.ipynb).
# * Knowledge on [mutation-based fuzzing](MutationFuzzer.ipynb) and [coverage](Coverage.ipynb) is _not_ required yet, but still recommended.

# ## Input Languages
# 
# All possible behaviors of a program can be triggered by its input.  "Input" here can be a wide range of possible sources: We are talking about data read from files, from the environment, or over the network, data input by the user, or data acquired from interaction with other resources.  The set of all these inputs determines how the program will behave – including its failures.  When testing, it is thus very helpful to think about possible input sources, how to get them under control, and _how to systematically test them_.
# 
# For the sake of simplicity, we will assume for now that the program has only one source of inputs; this is the same assumption we have been using in the previous chapters, too.  The set of valid inputs to a program is called a _language_.  Languages range from the simple to the complex: the CSV language denotes the set of valid comma-separated inputs, whereas the Python language denotes the set of valid Python programs.  We commonly separate data languages and programming languages, although any program can also be treated as input data (say, to a compiler).  The [Wikipedia page on file formats](https://en.wikipedia.org/wiki/List_of_file_formats) lists more than 1,000 different file formats, each of which is its own language.

# To formally describe languages, the field of _formal languages_ has devised a number of _language specifications_ that describe a language.  _Regular expressions_, for instance, denote sets of strings: The regular expression `[a-z]*`, for instance, denotes a (possibly empty) sequence of lowercase letters.  _Automata theory_ connects these languages to automata that accept these inputs; _finite state machines_, for instance, can be used to specify the same language as regular expressions.

# Regular expressions are great for not-too-complex input formats, and the associated finite state machine have many properties that make them great for reasoning.  To specify more complex inputs, though, they quickly encounter limitations.  On the other hand of the language spectrum, we have _universal grammars_ that denote the language accepted by _Turing machines_.  A Turing machine can compute anything that can be computed; and with Python being a Turing-complete language, this means that we can also use a Python program $p$ to specify or even enumerate legal inputs.  But then, computer science theory also tells us that each such testing program has to be written specifically for the program to be tested, which is not the level of automation we want.

# ## Grammars
# 
# The middle ground between regular expressions and Turing machines is covered by _grammars_.  Grammars are among the most popular (and best understood) formalisms to formally specify input languages.  Using a grammar, one can express a wide range of the properties of an input language.  Grammars are particularly great for expressing the _syntactical structure_ of an input, and are the formalism of choice to express nested or recursive inputs.

# ### Rules and Expansions
# 
# A grammar consists of a _start symbol_ and a set of _rules_ which indicate how the start symbol (and other symbols) can be expanded.  As an example, consider the following grammar, denoting a sequence of two digits:
# 
# ```
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
# ```
# <start>  ::= <integer>
# <integer> ::= <digit> | <digit><integer>
# <digit>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# ```
# 
# Here, a `<integer>` is either a single digit, or a digit followed by another integer.  The number `1234` thus would be represented as a single digit `1`, followed by the integer `234`, which in turn is a digit `2`, followed by the integer `34`.
# 
# If we wanted to express that an integer can be preceded by a sign (`+` or `-`), we would write the grammar as
# 
# ```
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
# ```
# <start>   ::= <expr>
# <expr>    ::= <term> + <expr> | <term> - <expr> | <term>
# <term>    ::= <term> * <factor> | <term> / <factor> | <factor>
# <factor>  ::= +<factor> | -<factor> | (<expr>) | <integer> | <integer>.<integer>
# <integer> ::= <digit><integer> | <digit>
# <digit>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
# ```
# 
# In such a grammar, if we start with `<start>` and then expand one symbol after another, randomly choosing alternatives, we can quickly produce one valid arithmetic expression after another.  Such _grammar fuzzing_ is highly effective as it comes to produce complex inputs, and this is what we will implement in this chapter.

# ## Representing Grammars in Python
# 
# Our first step in building a grammar fuzzer is to find an appropriate format for grammars.  To make the writing of grammars as simple as possible, we use a mostly format that is mostly based on strings.  Our grammars in Python takes the format of a _mapping_ between symbol names and expansions, where expansions are _lists_ of alternatives.  A one-rule grammar for digits thus takes the form

# import fuzzingbook_utils

DIGIT_GRAMMAR = {
    "<start>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

# whereas the full grammar for arithmetic expressions looks like this:

EXPR_GRAMMAR = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<term> + <expr>", "<term> - <expr>", "<term>"],

    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>"],

    "<factor>":
        ["+<factor>",
         "-<factor>",
         "(<expr>)",
         "<integer>",
         "<integer>.<integer>"],

    "<integer>":
        ["<digit><integer>", "<digit>"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

# In the grammar, we can access any rule by its symbol...

if __name__ == "__main__":
    EXPR_GRAMMAR["<digit>"]


# ....and we can check whether a symbol is in the grammar:

if __name__ == "__main__":
    "<identifier>" in EXPR_GRAMMAR


# ## Some Definitions

# We assume that the canonical start symbol is `<start>`:

START_SYMBOL = "<start>"

# The handy `nonterminals()` function extracts the list of nonterminal symbols (i.e., anything between `<` and `>`) from an expansion.

import re

if __name__ == "__main__":
    # anything between <...> except spaces


RE_NONTERMINAL = re.compile(r'(<[^<> ]*>)')

def nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_NONTERMINAL, expansion)

if __name__ == "__main__":
    assert nonterminals("<term> * <factor>") == ["<term>", "<factor>"]
    assert nonterminals("<digit><integer>") == ["<digit>", "<integer>"]
    assert nonterminals("1 < 3 > 2") == []
    assert nonterminals("1 <3> 2") == ["<3>"]
    assert nonterminals("1 + 2") == []
    assert nonterminals(("<1>", {'option': 'value'})) == ["<1>"]


# Likewise, `is_nonterminal()` checks whether some symbol is a nonterminal:

def is_nonterminal(s):
    return re.match(RE_NONTERMINAL, s)

if __name__ == "__main__":
    assert is_nonterminal("<abc>")
    assert is_nonterminal("<symbol-1>")
    assert not is_nonterminal("+")


# ## A Simple Grammar Fuzzer
# 
# Let us now put the above grammars to use.   We will build a very simple grammar fuzzer that starts with a start symbol (`"<start>"`) and then keeps on expanding it.  To avoid expansion to infinite inputs, we place a limit (`max_symbols`) on the number of symbols.  Furthermore, to avoid being stuck in a situation where we cannot reduce the number of symbols any further, we also limit the total number of expansion steps.

import random

class ExpansionError(Exception):
    pass

def simple_grammar_fuzzer(grammar, start_symbol=START_SYMBOL,
                          max_nonterminals=10, max_expansion_trials=100, log=False):
    term = start_symbol
    expansion_trials = 0

    while len(nonterminals(term)) > 0:
        symbol_to_expand = random.choice(nonterminals(term))
        expansions = grammar[symbol_to_expand]
        expansion = random.choice(expansions)
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

if __name__ == "__main__":
    simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=3, log=True)


if __name__ == "__main__":
    for i in range(10):
        print(simple_grammar_fuzzer(grammar=EXPR_GRAMMAR, max_nonterminals=5))


# \todo{Discuss.}

# Note that this fuzzer is rather inefficient due to the large number of search and replace operations.  On the other hand, the implementation is straightforward and does the job.  For this chapter, we'll stick to it; in the [next chapter](GrammarFuzzer.ipynb), we'll show how to build a more efficient one.

# ## Some Grammars

# With grammars, we can easily specify the format for several of the examples we discussed earlier.  The above arithmetic expressions, for instance, can be directly sent into `bc` (or any other program that takes arithmetic expressions.  

# ### A CGI Grammar
# 
# Let us create some more grammars.  Here's one for `cgi_decode()`:

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
        ["0", "1", "2", "3", "4", "5", "6", "7",
            "8", "9", "a", "b", "c", "d", "e", "f"],

    "<other>":  # Actually, could be _all_ letters
        ["0", "1", "2", "3", "4", "5", "a", "b", "c", "d", "e", "-", "_"],
}

# In contrast to [basic fuzzing](Fuzzer.ipynb) or [mutation-based fuzzing](MutationFuzzer.ipynb), the grammar quickly produces all sorts of combinations:

if __name__ == "__main__":
    for i in range(10):
        print(simple_grammar_fuzzer(grammar=CGI_GRAMMAR, max_nonterminals=10))


# ### A URL Grammar

# The same properties we have seen for CGI input also hold for more complex inputs.  Let us use a grammar to produce a large number of valid URLs:

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

# Again, within milliseconds, we can produce plenty of valid inputs.

if __name__ == "__main__":
    for i in range(10):
        print(simple_grammar_fuzzer(grammar=URL_GRAMMAR, max_nonterminals=10))


# ## Grammars as Mutation Seeds
# 
# One very useful property of grammars is that they produce mostly valid inputs.  From a syntactical standpoint, the inputs are actually _always_ valid, as they satisfy the constraints of the given grammar.  (Of course, one needs a valid grammar in the first place.)  However, there are also _semantical_ properties that cannot be easily expressed in a grammar.  If, say, for a URL, the port range is supposed to be between 1024 and 2048, this is hard to write in a grammar.  If one has to satisfy more complex constraints, one quickly reaches the limits of what a grammar can express.

# One way around this is to attach constraints to grammars, as we will discuss [later in this book](ConstraintFuzzer.ipynb).  Another possibility is to put together the strengths of grammar-based fuzzing and [mutation-based fuzzing](MutationFuzzer.ipynb).  The idea is to use the grammar-generated inputs as _seeds_ for further mutation-based fuzzing.  This way, we can explore not only _valid_ inputs, but also check out the _boundaries_ between valid and invalid inputs – and, by the way, also again errors due to invalid inputs.

# To use our generated inputs as seeds, we can feed them directly into the mutation fuzzers introduced earlier:

from MutationFuzzer import MutationFuzzer

if __name__ == "__main__":
    number_of_seeds = 10
    seeds = [
        simple_grammar_fuzzer(
            grammar=URL_GRAMMAR,
            max_nonterminals=10) for i in range(number_of_seeds)]
    seeds


if __name__ == "__main__":
    m = MutationFuzzer(seeds)


if __name__ == "__main__":
    for i in range(20):
        print(m.fuzz())


# While the first 10 `fuzz()` calls return the seeded inputs (as designed), the later ones again create arbitrary mutations.  Using `MutationCoverageFuzzer` instead of `MutationFuzzer`, we could again have our search guided by coverage – and thus bring together the best of multiple worlds.

# ## Hatching Grammars
# 
# We close the chapter with a few functions that help us check and write grammars.

# ### Checking Grammars for Consistency
# 
# Since grammars are represented as strings, it is fairly easy to introduce errors.  So let us introduce a helper function that checks a grammar for consistency.

# The helper function `is_valid_grammar()` iterates over a grammar to check whether all used symbols are defined, and vice versa, which is very useful for debugging.  You don't have to delve into details here, but as always, it is important to get the input data straight before we make use of it.

import sys

def is_valid_grammar(grammar, start_symbol=START_SYMBOL):
    used_nonterminals = set([start_symbol])
    defined_nonterminals = set()

    for defined_nonterminal in grammar:
        defined_nonterminals.add(defined_nonterminal)
        expansions = grammar[defined_nonterminal]
        if not isinstance(expansions, list):
            print(repr(defined_nonterminal) + ": expansion is not a list",
                  file=sys.stderr)
            return False
        if len(expansions) == 0:
            print(repr(defined_nonterminal) + ": expansion list empty",
                  file=sys.stderr)
            return False

        for expansion in expansions:
            if isinstance(expansion, tuple):
                expansion = expansion[0]
            if not isinstance(expansion, str):
                print(repr(defined_nonterminal) + ": "
                      + repr(expansion) + ": not a string",
                      file=sys.stderr)
                return False

            for used_nonterminal in nonterminals(expansion):
                used_nonterminals.add(used_nonterminal)

    for unused_nonterminal in defined_nonterminals - used_nonterminals:
        print(repr(unused_nonterminal) + ": defined, but not used",
              file=sys.stderr)
    for undefined_nonterminal in used_nonterminals - defined_nonterminals:
        print(repr(undefined_nonterminal) + ": used, but not defined",
              file=sys.stderr)

    return used_nonterminals == defined_nonterminals

# Our grammars defined above pass the test:

if __name__ == "__main__":
    assert is_valid_grammar(EXPR_GRAMMAR)
    assert is_valid_grammar(CGI_GRAMMAR)
    assert is_valid_grammar(URL_GRAMMAR)


# These ones do not, though:

if __name__ == "__main__":
    assert not is_valid_grammar({"<start>": ["<x>"], "<y>": ["1"]})


if __name__ == "__main__":
    assert not is_valid_grammar({"<start>": "123"})


if __name__ == "__main__":
    assert not is_valid_grammar({"<start>": []})


if __name__ == "__main__":
    assert not is_valid_grammar({"<start>": [1, 2, 3]})


# ### Grammar Shortcuts
# 
# Formally, our grammars come in so-called [Backus-Naur form](https://en.wikipedia.org/wiki/Backus–Naur_form), or BNF for short.  To use grammars efficiently, let us introduce a few _syntactical shortcuts_ that allow for simpler specification of frequently occurring items:
# 
# * The form `<symbol>?` indicates that `<symbol>` is optional – that is, it can occur 0 or 1 times.
# * The form `<symbol>+` indicates that `<symbol>` can occur 1 or more times repeatedly.
# * The form `<symbol>*` indicates that `<symbol>` can occur 0 or more times.  (In other words, it is an optional repetition.)
# 
# To make matters even more interesting, we would like to use _parentheses_ with the above shortcuts.  Thus, `(<foo><bar>)?` indicates that the sequence of `<foo>` and `<bar>` is optional.  The combination of parentheses and operators results in a so-called 

# Using such operators, we can define the expression grammar in a slightly simpler way.  Consider how signs are optional, and how integers can be expressed as sequences of digits.

EXPR_GRAMMAR_EBNF = {
    "<start>":
        ["<expr>"],

    "<expr>":
        ["<term> + <expr>", "<term> - <expr>", "<term>"],

    "<term>":
        ["<factor> * <term>", "<factor> / <term>", "<factor>"],

    "<factor>":
        ["<sign>?<factor>", "(<expr>)", "<integer>(.<integer>)?"],

    "<sign>":
        ["+", "-"],

    "<integer>":
        ["<digit>+"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

assert is_valid_grammar(EXPR_GRAMMAR_EBNF)

# Our aim is to convert an extended grammar such as the one above into a regular BNF grammar.  This is done by four rules:
# 
# 1. An expression `(content)op`, where `op` is one of `?`, `+`, `*`, becomes `<new-symbol>op`, with a new rule `<new-symbol> ::= content`.
# 2. An expression `<symbol>?` becomes `<new-symbol>`, where `<new-symbol> ::= "" | <symbol>`.
# 3. An expression `<symbol>+` becomes `<new-symbol>`, where `<new-symbol> ::= <symbol> | <symbol><new-symbol>`.
# 4. An expression `<symbol>+` becomes `<new-symbol>`, where `<new-symbol> ::= "" | <symbol><new-symbol>`.

# Applying these rules on `"<integer>(.<integer>)?"`, for instance, yields `<integer><new-symbol>` with `<new-symbol> ::= "" | .<integer>`.

# Let us implement threse rules in three steps.

# #### Creating New Symbols
# 
# First, we need a mechanism to create new symbols.  This is fairly straightforward.

def new_symbol(grammar, symbol_name="<symbol>"):
    """Return a new symbol for `grammar` based on `symbol_name`"""
    count = 1
    while True:
        tentative_symbol_name = symbol_name[:-1] + "-" + repr(count) + ">"
        if tentative_symbol_name not in grammar:
            return tentative_symbol_name
        count += 1

if __name__ == "__main__":
    assert new_symbol(EXPR_GRAMMAR, '<expr>') == '<expr-1>'


# #### Expanding Parenthesized Expressions

# Next, we need a means to extract parenthesized expressions from our expansions and expand them according to the rules above.  Let's start with extracting expressions:

RE_PARENTHESIZED_EXPR = re.compile(r'\([^())]*\)[?+*]')

def parenthesized_expressions(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_PARENTHESIZED_EXPR, expansion)

if __name__ == "__main__":
    assert parenthesized_expressions("(<foo>)* (<foo><bar>)+ (+<foo>)? <integer>(.<integer>)?") == [
        '(<foo>)*', '(<foo><bar>)+', '(+<foo>)?', '(.<integer>)?']


# We can now use these to apply rule number 1, above, introducing new symbols for expressions in parentheses.

from copy import deepcopy

def convert_ebnf_parentheses(ebnf_grammar):
    """Convert a grammar in extended BNF to BNF"""
    grammar = deepcopy(ebnf_grammar)
    for nonterminal in ebnf_grammar:
        expansions = ebnf_grammar[nonterminal]

        for i in range(len(expansions)):
            expansion = expansions[i]

            while True:
                parenthesized_exprs = parenthesized_expressions(expansion)
                if len(parenthesized_exprs) == 0:
                    break

                for expr in parenthesized_exprs:
                    operator = expr[-1:]
                    contents = expr[1:-2]

                    new_sym = new_symbol(grammar)
                    expansion = grammar[nonterminal][i].replace(
                        expr, new_sym + operator, 1)
                    grammar[nonterminal][i] = expansion
                    grammar[new_sym] = [contents]

    return grammar

# This does the conversion as sketched above:

if __name__ == "__main__":
    convert_ebnf_parentheses({"<number>": ["<integer>(.<integer>)?"]})


# This even works for nested parenthesized expressions:

if __name__ == "__main__":
    convert_ebnf_parentheses({"<foo>": ["((<foo>)?)+"]})


# #### Expanding Operators
# 
# After expanding parenthesized expressions, we now need to take care of symbols followed by operators (`?`, `*`, `+`).  As with `convert_ebnf_parentheses()`, above, we first extract all symbols followed by an operator.

RE_EXTENDED_NONTERMINAL = re.compile(r'(<[^<> ]*>[?+*])')

def extended_nonterminals(expansion):
    # In later chapters, we allow expansions to be tuples,
    # with the expansion being the first element
    if isinstance(expansion, tuple):
        expansion = expansion[0]

    return re.findall(RE_EXTENDED_NONTERMINAL, expansion)

if __name__ == "__main__":
    assert extended_nonterminals(
        "<foo>* <bar>+ <elem>? <none>") == ['<foo>*', '<bar>+', '<elem>?']


# Our converter extracts the symbol and the operator, and adds new symbols according to the rules laid out above.

def convert_ebnf_operators(ebnf_grammar):
    """Convert a grammar in extended BNF to BNF"""
    grammar = deepcopy(ebnf_grammar)
    for nonterminal in ebnf_grammar:
        expansions = ebnf_grammar[nonterminal]

        for i in range(len(expansions)):
            expansion = expansions[i]
            extended_symbols = extended_nonterminals(expansion)

            for extended_symbol in extended_symbols:
                operator = extended_symbol[-1:]
                original_symbol = extended_symbol[:-1]

                new_sym = new_symbol(grammar, original_symbol)
                grammar[nonterminal][i] = grammar[nonterminal][i].replace(
                    extended_symbol, new_sym, 1)

                if operator == '?':
                    grammar[new_sym] = ["", original_symbol]
                elif operator == '*':
                    grammar[new_sym] = ["", original_symbol + new_sym]
                elif operator == '+':
                    grammar[new_sym] = [
                        original_symbol, original_symbol + new_sym]

    return grammar

if __name__ == "__main__":
    convert_ebnf_operators({"<integer>": ["<digit>+"]})


# #### All Together

# We can combine the two, first extending parentheses and then operators:

def convert_ebnf_grammar(ebnf_grammar):
    return convert_ebnf_operators(convert_ebnf_parentheses(ebnf_grammar))

if __name__ == "__main__":
    convert_ebnf_grammar({"<authority>": ["(<userinfo>@)?<host>(:<port>)?"]})


if __name__ == "__main__":
    expr_grammar = convert_ebnf_grammar(EXPR_GRAMMAR_EBNF)
    assert is_valid_grammar(expr_grammar)
    expr_grammar


# Success! We have nicely converted the EBNF grammar into BNF.

# We can repeat the same with our URL grammar:

URL_GRAMMAR_EBNF = {
    "<start>":
        ["<call>"],

    "<call>":
        ["<url>"],

    "<url>":
        ["<scheme>://<authority><path>?(?<params>)?"],

    "<scheme>":
        ["http", "https", "ftp", "ftps"],

    "<authority>":
        ["(<userinfo>@)?<host>(:<port>)?"],

    "<host>":  # Just a few
        ["cispa.saarland", "www.google.com", "fuzzingbook.com"],

    "<port>":
        ["80", "8080", "<digit>+"],

    "<digit>":
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],

    "<userinfo>":  # Just one
        ["user:password"],

    "<path>":  # Just a few
        ["/", "/<id>"],

    "<id>":  # Just a few
        ["abc", "def", "x<digit><digit>"],

    "<params>":
        ["<param>(&<params>)*"],

    "<param>":  # Just a few
        ["<id>=<id>", "<id>=<digit>*"],
}

if __name__ == "__main__":
    url_grammar = convert_ebnf_grammar(URL_GRAMMAR_EBNF)
    assert is_valid_grammar(url_grammar)
    url_grammar


# And we can still use the grammar for fuzzing:

if __name__ == "__main__":
    simple_grammar_fuzzer(grammar=url_grammar, max_nonterminals=5)


# With `is_valid_grammar()` and `convert_ebnf_grammar()`, we have two powerful tools that allow for checking grammars for consistency as well as making the writing of grammars easier.  We will use these again and again as it comes to working with grammars.

# ## Lessons Learned
# 
# * Grammars are powerful tools to express and produce syntactically valid inputs.
# * Inputs produced from grammars can be used as is, or used as seeds for mutation-based fuzzing.
# * Grammars can be extended with operators to make writing easier.

# ## Next Steps
# 
# As they make a great foundation for generating software tests, we use grammars again and again in this work – and they become especially valuable when we can _infer_ them automatically from a given domain, dropping the need to write them manually.  But before we get there, we first have to learn how to 
# 
# * [create an efficient grammar fuzzer](GrammarFuzzer.ipynb)

# ## Exercises
# 
# \todo{finish.}

# ### Exercise 1: A JSON Grammar
# 
# Take a look at the [JSON specification] and derive a grammar from it.  As with `URL_GRAMMAR` above, restrict yourself to a few representatives as it comes to strings.  Use `assert is_valid_grammar()`to ensure the grammar is valid.  Feed the grammar into `simple_grammar_fuzzer()` and assess the results.

# **Solution**.  \todo{To be added.}

# ### Exercise 2: Grammar Annotations
# 
# Python 3.7 and later allow the use of _annotations_ to attach Python snippets to arbitrary syntactic elements.  You can make use of such annotations to produce even nicer grammars, using `|` to separate alternatives:
# 
# ```python
# from __future__ import annotations
# 
# class expression_grammar:
#    start: "<expr>"
#    expr: "<term> + <expr>" | "<term> - <expr>"
#    term: "<factor> * <term>" | "<factor> / <term>" | "<factor>"
#    factor: "+<factor>" | "-<factor>" | "(<expr>)" | "<integer>" | "<integer>.<integer>"
#    integer: "<digit><integer>" | "<digit>"
#    digit: '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
# ```
# 
# The annotation can be accessed using the `__annotations__` attribute:
# 
# ```python
# print(expression_grammar.__annotations__)
# {'start': "'<expr>'", 'expr': "'<term> + <expr>' | '<term> - <expr>'", 
#  'term': "'<factor> * <term>' | '<factor> / <term>' | '<factor>'", 
#  ...}
# ```
# 
# Using Python 3.7 or later, write a converter that takes a grammar class using the above syntax and convert it to the "portable" format described in this chapter.

# **Solution**.  No solution yet :-)
