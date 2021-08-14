#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Fuzzing with Generators" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/GeneratorGrammarFuzzer.html
# Last change: 2021-06-04 14:56:27+02:00
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
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

r'''
The Fuzzing Book - Fuzzing with Generators

This file can be _executed_ as a script, running all experiments:

    $ python GeneratorGrammarFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.GeneratorGrammarFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/GeneratorGrammarFuzzer.html

This chapter introduces the ability to attach _functions_ to individual production rules:

* A `pre` function is executed _before_ the expansion takes place.  Its result (typically a string) can _replace_ the actual expansion.
* A `post` function is executed _after_ the expansion has taken place.  If it returns a string, the string replaces the expansion; it it returns `False`, it triggers a new expansion.

Both functions can return `None` to not interfere with grammar production at all.

To attach a function `F` to an individual expansion `S` in a grammar, replace `S` with a pair

(S, opts(pre=F))   # Set a function to be executed before expansion

or
(S, opts(post=F))  # Set a function to be executed after expansion


Here is an example, To take an area code from a list that is given programmatically, we can write:

>>> from Grammars import US_PHONE_GRAMMAR, extend_grammar, opts
>>> def pick_area_code():
>>>     return random.choice(['555', '554', '553'])
>>> PICKED_US_PHONE_GRAMMAR = extend_grammar(US_PHONE_GRAMMAR,
>>> {
>>>     "": [("", opts(pre=pick_area_code))]
>>> })

A `GeneratorGrammarFuzzer` will extract and interpret these options.  Here is an example:

>>> picked_us_phone_fuzzer = GeneratorGrammarFuzzer(PICKED_US_PHONE_GRAMMAR)
>>> [picked_us_phone_fuzzer.fuzz() for i in range(5)]
['(553)200-6118',
 '(553)889-0205',
 '(555)317-0936',
 '(553)455-2577',
 '(553)263-8511']

As you can see, the area codes now all stem from `pick_area_code()`.  Such definitions allow to closely tie program code (such as `pick_area_code()`) to grammars.

The `PGGCFuzzer` class incorporates all features from [the `GrammarFuzzer` class](GrammarFuzzer.ipynb) and its [coverage-based](GrammarCoverageFuzzer.ipynb), [probabilistic-based](ProbabilisticGrammarFuzzer.ipynb), and [generator-based](GeneratorGrammarFuzzer.ipynb) derivatives.


For more details, source, and documentation, see
"The Fuzzing Book - Fuzzing with Generators"
at https://www.fuzzingbook.org/html/GeneratorGrammarFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Fuzzing with Generators
# =======================

if __name__ == '__main__':
    print('# Fuzzing with Generators')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Example: Test a Credit Card System
## ----------------------------------

if __name__ == '__main__':
    print('\n## Example: Test a Credit Card System')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from .Grammars import EXPR_GRAMMAR, is_valid_grammar, is_nonterminal, extend_grammar
from .Grammars import opts, exp_opt, exp_string, crange

CHARGE_GRAMMAR = {
    "<start>": ["Charge <amount> to my credit card <credit-card-number>"],
    "<amount>": ["$<float>"],
    "<float>": ["<integer>.<digit><digit>"],
    "<integer>": ["<digit>", "<integer><digit>"],
    "<digit>": crange('0', '9'),

    "<credit-card-number>": ["<digits>"],
    "<digits>": ["<digit-block><digit-block><digit-block><digit-block>"],
    "<digit-block>": ["<digit><digit><digit><digit>"],
}

assert is_valid_grammar(CHARGE_GRAMMAR)

from .GrammarFuzzer import GrammarFuzzer, all_terminals, display_tree

if __name__ == '__main__':
    g = GrammarFuzzer(CHARGE_GRAMMAR)
    [g.fuzz() for i in range(5)]

## Attaching Functions to Expansions
## ---------------------------------

if __name__ == '__main__':
    print('\n## Attaching Functions to Expansions')



### Functions Called Before Expansion

if __name__ == '__main__':
    print('\n### Functions Called Before Expansion')



import random

def high_charge():
    return random.randint(10000000, 90000000) / 100.0

CHARGE_GRAMMAR.update({
    "<float>": [("<integer>.<digit><digit>", opts(pre=high_charge))],
})

def apply_twice(function, x):
    return function(function(x))

if __name__ == '__main__':
    apply_twice(lambda x: x * x, 2)

CHARGE_GRAMMAR.update({
    "<float>": [("<integer>.<digit><digit>",
                 opts(pre=lambda: random.randint(10000000, 90000000) / 100.0))]
})

### Functions Called After Expansion

if __name__ == '__main__':
    print('\n### Functions Called After Expansion')



CHARGE_GRAMMAR.update({
    "<credit-card-number>": [("<digits>", opts(post=lambda digits: check_credit_card(digits)))]
})

CHARGE_GRAMMAR.update({
    "<credit-card-number>": [("<digits>", opts(post=lambda digits: fix_credit_card(digits)))]
})

def luhn_checksum(s):
    """Compute Luhn's check digit over a string of digits"""
    LUHN_ODD_LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7,
                       9)  # sum_of_digits (index * 2)

    evens = sum(int(p) for p in s[-1::-2])
    odds = sum(LUHN_ODD_LOOKUP[int(p)] for p in s[-2::-2])
    return (evens + odds) % 10

def valid_luhn_checksum(s):
    """Check whether the last digit is Luhn's checksum over the earlier digits"""
    return luhn_checksum(s[:-1]) == int(s[-1])

def fix_luhn_checksum(s):
    """Return the given string of digits, with a fixed check digit"""
    return s[:-1] + repr(luhn_checksum(s[:-1]))

if __name__ == '__main__':
    luhn_checksum("123")

if __name__ == '__main__':
    fix_luhn_checksum("123x")

if __name__ == '__main__':
    check_credit_card = valid_luhn_checksum
    fix_credit_card = fix_luhn_checksum

    fix_credit_card("1234567890123456")

## A Class for Integrating Constraints
## -----------------------------------

if __name__ == '__main__':
    print('\n## A Class for Integrating Constraints')



if __name__ == '__main__':
    g = GrammarFuzzer(CHARGE_GRAMMAR)
    g.fuzz()

class GeneratorGrammarFuzzer(GrammarFuzzer):
    def supported_opts(self):
        return super().supported_opts() | {"pre", "post", "order"}

def exp_pre_expansion_function(expansion):
    """Return the specified pre-expansion function, or None if unspecified"""
    return exp_opt(expansion, 'pre')

def exp_post_expansion_function(expansion):
    """Return the specified post-expansion function, or None if unspecified"""
    return exp_opt(expansion, 'post')

## Generating Elements before Expansion
## ------------------------------------

if __name__ == '__main__':
    print('\n## Generating Elements before Expansion')



import inspect

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def process_chosen_children(self, children, expansion):
        function = exp_pre_expansion_function(expansion)
        if function is None:
            return children

        assert callable(function)
        if inspect.isgeneratorfunction(function):
            # See "generators", below
            result = self.run_generator(expansion, function)
        else:
            result = function()

        if self.log:
            print(repr(function) + "()", "=", repr(result))
        return self.apply_result(result, children)

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def apply_result(self, result, children):
        if isinstance(result, str):
            children = [(result, [])]
        elif isinstance(result, list):
            symbol_indexes = [i for i, c in enumerate(
                children) if is_nonterminal(c[0])]

            for index, value in enumerate(result):
                if value is not None:
                    child_index = symbol_indexes[index]
                    if not isinstance(value, str):
                        value = repr(value)
                    if self.log:
                        print(
                            "Replacing", all_terminals(
                                children[child_index]), "by", value)

                    # children[child_index] = (value, [])
                    child_symbol, _ = children[child_index]
                    children[child_index] = (child_symbol, [(value, [])])
        elif result is None:
            pass
        elif isinstance(result, bool):
            pass
        else:
            if self.log:
                print("Replacing", "".join(
                    [all_terminals(c) for c in children]), "by", result)

            children = [(repr(result), [])]

        return children

### Example: Numeric Ranges

if __name__ == '__main__':
    print('\n### Example: Numeric Ranges')



if __name__ == '__main__':
    charge_fuzzer = GeneratorGrammarFuzzer(CHARGE_GRAMMAR)
    charge_fuzzer.fuzz()

if __name__ == '__main__':
    amount_fuzzer = GeneratorGrammarFuzzer(
        CHARGE_GRAMMAR, start_symbol="<amount>", log=True)
    amount_fuzzer.fuzz()

### Example: More Numeric Ranges

if __name__ == '__main__':
    print('\n### Example: More Numeric Ranges')



if __name__ == '__main__':
    expr_100_200_grammar = extend_grammar(EXPR_GRAMMAR,
                                          {
                                              "<factor>": [
                                                  "+<factor>", "-<factor>", "(<expr>)",

                                                  # Generate only the integer part with a function;
                                                  # the fractional part comes from
                                                  # the grammar
                                                  ("<integer>.<integer>", opts(
                                                      pre=lambda: [random.randint(100, 200), None])),

                                                  # Generate the entire integer
                                                  # from the function
                                                  ("<integer>", opts(
                                                      pre=lambda: random.randint(100, 200))),
                                              ],
                                          }
                                          )

if __name__ == '__main__':
    expr_100_200_fuzzer = GeneratorGrammarFuzzer(expr_100_200_grammar)
    expr_100_200_fuzzer.fuzz()

### Support for Python Generators

if __name__ == '__main__':
    print('\n### Support for Python Generators')



def iterate():
    t = 0
    while True:
        t = t + 1
        yield t

if __name__ == '__main__':
    for i in iterate():
        if i > 10:
            break
        print(i, end=" ")

if __name__ == '__main__':
    iterate_grammar = extend_grammar(EXPR_GRAMMAR,
                                     {
                                         "<factor>": [
                                             "+<factor>", "-<factor>", "(<expr>)",
                                             # "<integer>.<integer>",

                                             # Generate one integer after another
                                             # from the function
                                             ("<integer>", opts(pre=iterate)),
                                         ],
                                     })

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def fuzz_tree(self):
        self.reset_generators()
        return super().fuzz_tree()

    def reset_generators(self):
        self.generators = {}

    def run_generator(self, expansion, function):
        key = repr((expansion, function))
        if key not in self.generators:
            self.generators[key] = function()
        generator = self.generators[key]
        return next(generator)

if __name__ == '__main__':
    iterate_fuzzer = GeneratorGrammarFuzzer(iterate_grammar)
    iterate_fuzzer.fuzz()

if __name__ == '__main__':
    iterate_grammar = extend_grammar(EXPR_GRAMMAR,
                                     {
                                         "<factor>": [
                                             "+<factor>", "-<factor>", "(<expr>)",
                                             ("<integer>", opts(pre=range(1, 1000))),
                                         ],
                                     })

if __name__ == '__main__':
    iterate_grammar = extend_grammar(EXPR_GRAMMAR,
                                     {
                                         "<factor>": [
                                             "+<factor>", "-<factor>", "(<expr>)",
                                             ("<integer>", opts(
                                                 pre=(x for x in range(1, 1000)))),
                                         ],
                                     })

## Checking and Repairing Elements after Expansion
## -----------------------------------------------

if __name__ == '__main__':
    print('\n## Checking and Repairing Elements after Expansion')



class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def fuzz_tree(self):
        while True:
            tree = super().fuzz_tree()
            (symbol, children) = tree
            result, new_children = self.run_post_functions(tree)
            if not isinstance(result, bool) or result:
                return (symbol, new_children)
            self.restart_expansion()

    def restart_expansion(self):
        # To be overloaded in subclasses
        self.reset_generators()

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    # Return True iff all constraints of grammar are satisfied in TREE
    def run_post_functions(self, tree, depth=float("inf")):
        symbol, children = tree
        if children == []:
            return True, children  # Terminal symbol

        try:
            expansion = self.find_expansion(tree)
        except KeyError:
            # Expansion (no longer) found - ignore
            return True, children

        result = True
        function = exp_post_expansion_function(expansion)
        if function is not None:
            result = self.eval_function(tree, function)
            if isinstance(result, bool) and not result:
                if self.log:
                    print(
                        all_terminals(tree),
                        "did not satisfy",
                        symbol,
                        "constraint")
                return False, children

            children = self.apply_result(result, children)

        if depth > 0:
            for c in children:
                result, _ = self.run_post_functions(c, depth - 1)
                if isinstance(result, bool) and not result:
                    return False, children

        return result, children

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def find_expansion(self, tree):
        symbol, children = tree

        applied_expansion = \
            "".join([child_symbol for child_symbol, _ in children])

        for expansion in self.grammar[symbol]:
            if exp_string(expansion) == applied_expansion:
                return expansion

        raise KeyError(
            symbol +
            ": did not find expansion " +
            repr(applied_expansion))

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def eval_function(self, tree, function):
        symbol, children = tree

        assert callable(function)

        args = []
        for (symbol, exp) in children:
            if exp != [] and exp is not None:
                symbol_value = all_terminals((symbol, exp))
                args.append(symbol_value)

        result = function(*args)
        if self.log:
            print(repr(function) + repr(tuple(args)), "=", repr(result))

        return result

### Example: Negative Expressions

if __name__ == '__main__':
    print('\n### Example: Negative Expressions')



from .ExpectError import ExpectError

def eval_with_exception(s):
    # Use "mute=True" to suppress all messages
    with ExpectError(print_traceback=False):
        return eval(s)
    return False

if __name__ == '__main__':
    negative_expr_grammar = extend_grammar(EXPR_GRAMMAR,
                                           {
                                               "<start>": [("<expr>", opts(post=lambda s: eval_with_exception(s) < 0))]
                                           }
                                           )

    assert is_valid_grammar(negative_expr_grammar)

if __name__ == '__main__':
    negative_expr_fuzzer = GeneratorGrammarFuzzer(negative_expr_grammar)
    expr = negative_expr_fuzzer.fuzz()
    expr

if __name__ == '__main__':
    eval(expr)

### Example: Matching XML Tags

if __name__ == '__main__':
    print('\n### Example: Matching XML Tags')



from .bookutils import HTML

if __name__ == '__main__':
    HTML("<strong>A bold text</strong>")

XML_GRAMMAR = {
    "<start>": ["<xml-tree>"],
    "<xml-tree>": ["<<id>><xml-content></<id>>"],
    "<xml-content>": ["Text", "<xml-tree>"],
    "<id>": ["<letter>", "<id><letter>"],
    "<letter>": crange('a', 'z')
}

assert is_valid_grammar(XML_GRAMMAR)

if __name__ == '__main__':
    xml_fuzzer = GrammarFuzzer(XML_GRAMMAR)
    xml_fuzzer.fuzz()

XML_GRAMMAR.update({
    "<xml-tree>": [("<<id>><xml-content></<id>>",
                    opts(post=lambda id1, content, id2: [None, None, id1])
                    )]
})

assert is_valid_grammar(XML_GRAMMAR)

if __name__ == '__main__':
    xml_fuzzer = GeneratorGrammarFuzzer(XML_GRAMMAR)
    xml_fuzzer.fuzz()

### Example: Checksums

if __name__ == '__main__':
    print('\n### Example: Checksums')



if __name__ == '__main__':
    credit_card_fuzzer = GeneratorGrammarFuzzer(
        CHARGE_GRAMMAR, start_symbol="<credit-card-number>")
    credit_card_number = credit_card_fuzzer.fuzz()
    credit_card_number

if __name__ == '__main__':
    assert valid_luhn_checksum(credit_card_number)

if __name__ == '__main__':
    charge_fuzzer = GeneratorGrammarFuzzer(CHARGE_GRAMMAR)
    charge_fuzzer.fuzz()

## Local Checking and Repairing
## ----------------------------

if __name__ == '__main__':
    print('\n## Local Checking and Repairing')



if __name__ == '__main__':
    binary_expr_grammar = extend_grammar(EXPR_GRAMMAR,
                                         {
                                             "<integer>": [("<digit><integer>", opts(post=lambda digit, _: digit in ["0", "1"])),
                                                           ("<digit>", opts(post=lambda digit: digit in ["0", "1"]))]
                                         }
                                         )

    assert is_valid_grammar(binary_expr_grammar)

if __name__ == '__main__':
    binary_expr_fuzzer = GeneratorGrammarFuzzer(binary_expr_grammar)
    binary_expr_fuzzer.fuzz()

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def expand_tree_once(self, tree):
        # Apply inherited method.  This also calls `expand_tree_once()` on all
        # subtrees.
        new_tree = super().expand_tree_once(tree)

        (symbol, children) = new_tree
        if all([exp_post_expansion_function(expansion)
                is None for expansion in self.grammar[symbol]]):
            # No constraints for this symbol
            return new_tree

        if self.any_possible_expansions(tree):
            # Still expanding
            return new_tree

        return self.run_post_functions_locally(new_tree)

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def run_post_functions_locally(self, new_tree):
        symbol, _ = new_tree

        result, children = self.run_post_functions(new_tree, depth=0)
        if not isinstance(result, bool) or result:
            # No constraints, or constraint satisfied
            # children = self.apply_result(result, children)
            new_tree = (symbol, children)
            return new_tree

        # Replace tree by unexpanded symbol and try again
        if self.log:
            print(
                all_terminals(new_tree),
                "did not satisfy",
                symbol,
                "constraint")

        if self.replacement_attempts_counter > 0:
            if self.log:
                print("Trying another expansion")
            self.replacement_attempts_counter -= 1
            return (symbol, None)

        if self.log:
            print("Starting from scratch")
        raise RestartExpansionException

class RestartExpansionException(Exception):
    pass

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def __init__(self, grammar, replacement_attempts=10, **kwargs):
        super().__init__(grammar, **kwargs)
        self.replacement_attempts = replacement_attempts

    def restart_expansion(self):
        super().restart_expansion()
        self.replacement_attempts_counter = self.replacement_attempts

    def fuzz_tree(self):
        self.replacement_attempts_counter = self.replacement_attempts
        while True:
            try:
                # This is fuzz_tree() as defined above
                tree = super().fuzz_tree()
                return tree
            except RestartExpansionException:
                self.restart_expansion()

if __name__ == '__main__':
    binary_expr_fuzzer = GeneratorGrammarFuzzer(
        binary_expr_grammar, replacement_attempts=100)
    binary_expr_fuzzer.fuzz()

## Definitions and Uses
## --------------------

if __name__ == '__main__':
    print('\n## Definitions and Uses')



from .LangFuzzer import VAR_GRAMMAR  # minor dependency

if __name__ == '__main__':
    g = GrammarFuzzer(VAR_GRAMMAR)
    for i in range(10):
        print(g.fuzz())

SYMBOL_TABLE = set()

def define_id(id):
    SYMBOL_TABLE.add(id)

def use_id():
    if len(SYMBOL_TABLE) == 0:
        return False

    id = random.choice(list(SYMBOL_TABLE))
    return id

def clear_symbol_table():
    global SYMBOL_TABLE
    SYMBOL_TABLE = set()

CONSTRAINED_VAR_GRAMMAR = extend_grammar(VAR_GRAMMAR)

CONSTRAINED_VAR_GRAMMAR = extend_grammar(CONSTRAINED_VAR_GRAMMAR, {
    "<assignment>": [("<identifier>=<expr>",
                      opts(post=lambda id, expr: define_id(id)))]
})

CONSTRAINED_VAR_GRAMMAR = extend_grammar(CONSTRAINED_VAR_GRAMMAR, {
    "<factor>": ['+<factor>', '-<factor>', '(<expr>)',
                 ("<identifier>", opts(post=lambda _: use_id())),
                 '<number>']
})

CONSTRAINED_VAR_GRAMMAR = extend_grammar(CONSTRAINED_VAR_GRAMMAR, {
    "<start>": [("<statements>", opts(pre=clear_symbol_table))]
})

if __name__ == '__main__':
    assert is_valid_grammar(CONSTRAINED_VAR_GRAMMAR)

if __name__ == '__main__':
    var_grammar_fuzzer = GeneratorGrammarFuzzer(CONSTRAINED_VAR_GRAMMAR)
    for i in range(10):
        print(var_grammar_fuzzer.fuzz())

## Ordering Expansions
## -------------------

if __name__ == '__main__':
    print('\n## Ordering Expansions')



if __name__ == '__main__':
    var_grammar_fuzzer = GeneratorGrammarFuzzer(CONSTRAINED_VAR_GRAMMAR)
    with ExpectError():
        for i in range(100):
            s = var_grammar_fuzzer.fuzz()
            try:
                exec(s, {}, {})
            except SyntaxError:
                continue
            except ZeroDivisionError:
                continue
    print(s)

CONSTRAINED_VAR_GRAMMAR = extend_grammar(CONSTRAINED_VAR_GRAMMAR, {
    "<statements>": [("<statement>;<statements>", opts(order=[1, 2])),
                     "<statement>"]
})

CONSTRAINED_VAR_GRAMMAR = extend_grammar(CONSTRAINED_VAR_GRAMMAR, {
    "<assignment>": [("<identifier>=<expr>", opts(post=lambda id, expr: define_id(id),
                                                  order=[2, 1]))],
})

def exp_order(expansion):
    """Return the specified expansion ordering, or None if unspecified"""
    return exp_opt(expansion, 'order')

class GeneratorGrammarFuzzer(GeneratorGrammarFuzzer):
    def choose_tree_expansion(self, tree, expandable_children):
        """Return index of subtree in `children` to be selected for expansion.  Defaults to random."""
        (symbol, tree_children) = tree
        if len(expandable_children) == 1:
            # No choice
            return super().choose_tree_expansion(tree, expandable_children)

        expansion = self.find_expansion(tree)
        given_order = exp_order(expansion)
        if given_order is None:
            # No order specified
            return super().choose_tree_expansion(tree, expandable_children)

        nonterminal_children = [c for c in tree_children if c[1] != []]
        assert len(nonterminal_children) == len(given_order), \
            "Order must have one element for each nonterminal"

        # Find expandable child with lowest ordering
        min_given_order = None
        j = 0
        for k, expandable_child in enumerate(expandable_children):
            while j < len(
                    nonterminal_children) and expandable_child != nonterminal_children[j]:
                j += 1
            assert j < len(nonterminal_children), "Expandable child not found"
            if self.log:
                print("Expandable child #%d %s has order %d" %
                      (k, expandable_child[0], given_order[j]))

            if min_given_order is None or given_order[j] < min_given_order:
                min_given_order = k

        assert min_given_order is not None

        if self.log:
            print("Returning expandable child #%d %s" %
                  (min_given_order, expandable_children[min_given_order][0]))

        return min_given_order

if __name__ == '__main__':
    var_grammar_fuzzer = GeneratorGrammarFuzzer(CONSTRAINED_VAR_GRAMMAR)
    for i in range(100):
        s = var_grammar_fuzzer.fuzz()
        if i < 10:
            print(s)
        try:
            exec(s, {}, {})
        except SyntaxError:
            continue
        except ZeroDivisionError:
            continue

## All Together
## ------------

if __name__ == '__main__':
    print('\n## All Together')



### Generators and Probabilistic Fuzzing

if __name__ == '__main__':
    print('\n### Generators and Probabilistic Fuzzing')



from .ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer  # minor dependency

from .bookutils import inheritance_conflicts

if __name__ == '__main__':
    inheritance_conflicts(ProbabilisticGrammarFuzzer, GeneratorGrammarFuzzer)

class ProbabilisticGeneratorGrammarFuzzer(GeneratorGrammarFuzzer,
                                          ProbabilisticGrammarFuzzer):
    def supported_opts(self):
        return (super(GeneratorGrammarFuzzer, self).supported_opts() |
                super(ProbabilisticGrammarFuzzer, self).supported_opts())

    def __init__(self, grammar, replacement_attempts=10, **kwargs):
        super(
            GeneratorGrammarFuzzer,
            self).__init__(
            grammar,
            replacement_attempts)
        super(ProbabilisticGrammarFuzzer, self).__init__(grammar, **kwargs)

CONSTRAINED_VAR_GRAMMAR.update({
    '<word>': [('<alpha><word>', opts(prob=0.9)),
               '<alpha>'],
})

if __name__ == '__main__':
    pgg_fuzzer = ProbabilisticGeneratorGrammarFuzzer(CONSTRAINED_VAR_GRAMMAR)
    pgg_fuzzer.supported_opts()

if __name__ == '__main__':
    pgg_fuzzer.fuzz()

# Generators and Grammar Coverage
# ===============================

if __name__ == '__main__':
    print('\n# Generators and Grammar Coverage')



from .ProbabilisticGrammarFuzzer import ProbabilisticGrammarCoverageFuzzer  # minor dependency

from .GrammarCoverageFuzzer import GrammarCoverageFuzzer  # minor dependency

if __name__ == '__main__':
    inheritance_conflicts(
        ProbabilisticGrammarCoverageFuzzer,
        GeneratorGrammarFuzzer)

class ProbabilisticGeneratorGrammarCoverageFuzzer(GeneratorGrammarFuzzer,
                                                  ProbabilisticGrammarCoverageFuzzer):
    def supported_opts(self):
        return (super(GeneratorGrammarFuzzer, self).supported_opts() |
                super(ProbabilisticGrammarCoverageFuzzer, self).supported_opts())

    def __init__(self, grammar, replacement_attempts=10, **kwargs):
        super(
            GeneratorGrammarFuzzer,
            self).__init__(
            grammar,
            replacement_attempts)
        super(
            ProbabilisticGrammarCoverageFuzzer,
            self).__init__(
            grammar,
            **kwargs)

import copy

class ProbabilisticGeneratorGrammarCoverageFuzzer(
        ProbabilisticGeneratorGrammarCoverageFuzzer):
    def fuzz_tree(self):
        self.orig_covered_expansions = copy.deepcopy(self.covered_expansions)
        tree = super().fuzz_tree()
        self.covered_expansions = self.orig_covered_expansions
        self.add_tree_coverage(tree)
        return tree

    def add_tree_coverage(self, tree):
        (symbol, children) = tree
        if len(children) > 0:
            flat_children = [(child_symbol, None)
                             for (child_symbol, _) in children]
            self.add_coverage(symbol, flat_children)
            for c in children:
                self.add_tree_coverage(c)

class ProbabilisticGeneratorGrammarCoverageFuzzer(
        ProbabilisticGeneratorGrammarCoverageFuzzer):
    def restart_expansion(self):
        super().restart_expansion()
        self.covered_expansions = self.orig_covered_expansions

if __name__ == '__main__':
    pggc_fuzzer = ProbabilisticGeneratorGrammarCoverageFuzzer(
        CONSTRAINED_VAR_GRAMMAR)
    pggc_fuzzer.fuzz()

if __name__ == '__main__':
    pggc_fuzzer.expansion_coverage()

if __name__ == '__main__':
    [pggc_fuzzer.fuzz() for i in range(10)]

PGGCFuzzer = ProbabilisticGeneratorGrammarCoverageFuzzer

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



from .Grammars import US_PHONE_GRAMMAR, extend_grammar, opts

def pick_area_code():
    return random.choice(['555', '554', '553'])

PICKED_US_PHONE_GRAMMAR = extend_grammar(US_PHONE_GRAMMAR,
{
    "<area>": [("<lead-digit><digit><digit>", opts(pre=pick_area_code))]
})

if __name__ == '__main__':
    picked_us_phone_fuzzer = GeneratorGrammarFuzzer(PICKED_US_PHONE_GRAMMAR)
    [picked_us_phone_fuzzer.fuzz() for i in range(5)]

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Tree Processing

if __name__ == '__main__':
    print('\n### Exercise 1: Tree Processing')



### Exercise 2: Attribute Grammars

if __name__ == '__main__':
    print('\n### Exercise 2: Attribute Grammars')



ATTR_GRAMMAR = {
    "<clause>": [("<xml-open>Text<xml-close>", opts(post=lambda x1, x2: [None, x1.name]))],
    "<xml-open>": [("<<tag>>", opts(post=lambda tag: opts(name=random_name())))],
    "<xml-close>": ["</<tag>>"]
}
