#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "The Fuzzing Book".
# Web site: https://www.fuzzingbook.org/html/Reducer.html
# Last change: 2020-01-21 11:03:52+01:00
#
#!/
# Copyright (c) 2018-2020 CISPA, Saarland University, authors, and contributors
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


# # Reducing Failure-Inducing Inputs

if __name__ == "__main__":
    print('# Reducing Failure-Inducing Inputs')




# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




# ## Why Reducing?

if __name__ == "__main__":
    print('\n## Why Reducing?')




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


if __package__ is None or __package__ == "":
    from Fuzzer import RandomFuzzer, Runner
else:
    from .Fuzzer import RandomFuzzer, Runner


import re

class MysteryRunner(Runner):
    def run(self, inp):
        x = inp.find(chr(0o17 + 0o31))
        y = inp.find(chr(0o27 + 0o22))
        if x >= 0 and y >= 0 and x < y:
            return (inp, Runner.FAIL)
        else:
            return (inp, Runner.PASS)

if __name__ == "__main__":
    mystery = MysteryRunner()
    random_fuzzer = RandomFuzzer()
    while True:
        inp = random_fuzzer.fuzz()
        result, outcome = mystery.run(inp)
        if outcome == mystery.FAIL:
            break


if __name__ == "__main__":
    failing_input = result
    failing_input


# ## Manual Input Reduction

if __name__ == "__main__":
    print('\n## Manual Input Reduction')




if __name__ == "__main__":
    failing_input


if __name__ == "__main__":
    half_length = len(failing_input) // 2   # // is integer division
    first_half = failing_input[:half_length]
    mystery.run(first_half)


if __name__ == "__main__":
    second_half = failing_input[half_length:]
    mystery.run(second_half)


# ## Delta Debugging

if __name__ == "__main__":
    print('\n## Delta Debugging')




if __name__ == "__main__":
    quarter_length = len(failing_input) // 4
    input_without_first_quarter = failing_input[quarter_length:]
    mystery.run(input_without_first_quarter)


if __name__ == "__main__":
    input_without_first_and_second_quarter = failing_input[quarter_length * 2:]
    mystery.run(input_without_first_and_second_quarter)


if __name__ == "__main__":
    second_half


if __name__ == "__main__":
    input_without_first_and_second_quarter


if __name__ == "__main__":
    input_without_first_and_third_quarter = failing_input[quarter_length:
                                                          quarter_length * 2] + failing_input[quarter_length * 3:]
    mystery.run(input_without_first_and_third_quarter)


if __name__ == "__main__":
    input_without_first_and_fourth_quarter = failing_input[quarter_length:quarter_length * 3]
    mystery.run(input_without_first_and_fourth_quarter)


class Reducer(object):
    def __init__(self, runner, log_test=False):
        """Attach reducer to the given `runner`"""
        self.runner = runner
        self.log_test = log_test
        self.reset()

    def reset(self):
        self.tests = 0

    def test(self, inp):
        result, outcome = self.runner.run(inp)
        self.tests += 1
        if self.log_test:
            print("Test #%d" % self.tests, repr(inp), repr(len(inp)), outcome)
        return outcome

    def reduce(self, inp):
        self.reset()
        # Default: Don't reduce
        return inp

class CachingReducer(Reducer):
    def reset(self):
        super().reset()
        self.cache = {}

    def test(self, inp):
        if inp in self.cache:
            return self.cache[inp]

        outcome = super().test(inp)
        self.cache[inp] = outcome
        return outcome

class DeltaDebuggingReducer(CachingReducer):
    def reduce(self, inp):
        self.reset()
        assert self.test(inp) != Runner.PASS

        n = 2     # Initial granularity
        while len(inp) >= 2:
            start = 0
            subset_length = len(inp) / n
            some_complement_is_failing = False

            while start < len(inp):
                complement = inp[:int(start)] + \
                    inp[int(start + subset_length):]

                if self.test(complement) == Runner.FAIL:
                    inp = complement
                    n = max(n - 1, 2)
                    some_complement_is_failing = True
                    break

                start += subset_length

            if not some_complement_is_failing:
                if n == len(inp):
                    break
                n = min(n * 2, len(inp))

        return inp

if __name__ == "__main__":
    dd_reducer = DeltaDebuggingReducer(mystery, log_test=True)
    dd_reducer.reduce(failing_input)


# ## Grammar-Based Input Reduction

if __name__ == "__main__":
    print('\n## Grammar-Based Input Reduction')




# ### Lexical Reduction vs. Syntactic Rules

if __name__ == "__main__":
    print('\n### Lexical Reduction vs. Syntactic Rules')




if __name__ == "__main__":
    expr_input = "1 + (2 * 3)"
    dd_reducer = DeltaDebuggingReducer(mystery, log_test=True)
    dd_reducer.reduce(expr_input)


if __package__ is None or __package__ == "":
    from Grammars import EXPR_GRAMMAR
else:
    from .Grammars import EXPR_GRAMMAR


if __package__ is None or __package__ == "":
    from Parser import EarleyParser  # minor dependency
else:
    from .Parser import EarleyParser  # minor dependency


class EvalMysteryRunner(MysteryRunner):
    def __init__(self):
        self.parser = EarleyParser(EXPR_GRAMMAR)

    def run(self, inp):
        try:
            tree, *_ = self.parser.parse(inp)
        except SyntaxError as exc:
            return (inp, Runner.UNRESOLVED)

        return super().run(inp)

if __name__ == "__main__":
    eval_mystery = EvalMysteryRunner()


if __name__ == "__main__":
    dd_reducer = DeltaDebuggingReducer(eval_mystery, log_test=True)
    dd_reducer.reduce(expr_input)


# ### A Grammmar-Based Reduction Approach

if __name__ == "__main__":
    print('\n### A Grammmar-Based Reduction Approach')




if __package__ is None or __package__ == "":
    from GrammarFuzzer import all_terminals, expansion_to_children, display_tree
else:
    from .GrammarFuzzer import all_terminals, expansion_to_children, display_tree


if __name__ == "__main__":
    derivation_tree, *_ = EarleyParser(EXPR_GRAMMAR).parse(expr_input)
    display_tree(derivation_tree)


# ### Simplifying by Replacing Subtrees

if __name__ == "__main__":
    print('\n### Simplifying by Replacing Subtrees')




import copy

if __name__ == "__main__":
    new_derivation_tree = copy.deepcopy(derivation_tree)
    # We really should have some query language
    sub_expr_tree = new_derivation_tree[1][0][1][2]
    display_tree(sub_expr_tree)


if __name__ == "__main__":
    new_derivation_tree[1][0] = sub_expr_tree
    display_tree(new_derivation_tree)


if __name__ == "__main__":
    all_terminals(new_derivation_tree)


# ### Simplifying by Alternative Expansions

if __name__ == "__main__":
    print('\n### Simplifying by Alternative Expansions')




if __name__ == "__main__":
    term_tree = new_derivation_tree[1][0][1][0][1][0][1][1][1][0]
    display_tree(term_tree)


if __name__ == "__main__":
    shorter_term_tree = term_tree[1][2]
    display_tree(shorter_term_tree)


if __name__ == "__main__":
    new_derivation_tree[1][0][1][0][1][0][1][1][1][0] = shorter_term_tree
    display_tree(new_derivation_tree)


if __name__ == "__main__":
    all_terminals(new_derivation_tree)


# ### A Class for Reducing with Grammars

if __name__ == "__main__":
    print('\n### A Class for Reducing with Grammars')




class GrammarReducer(CachingReducer):
    def __init__(self, runner, parser, log_test=False, log_reduce=False):
        super().__init__(runner, log_test=log_test)
        self.parser = parser
        self.grammar = parser.grammar()
        self.start_symbol = parser.start_symbol()
        self.log_reduce = log_reduce
        self.try_all_combinations = False

# ### A Few Helpers

if __name__ == "__main__":
    print('\n### A Few Helpers')




def tree_list_to_string(q):
    return "[" + ", ".join([all_terminals(tree) for tree in q]) + "]"

if __name__ == "__main__":
    tree_list_to_string([derivation_tree, derivation_tree])


def possible_combinations(list_of_lists):
    if len(list_of_lists) == 0:
        return []

    ret = []
    for e in list_of_lists[0]:
        if len(list_of_lists) == 1:
            ret.append([e])
        else:
            for c in possible_combinations(list_of_lists[1:]):
                new_combo = [e] + c
                ret.append(new_combo)
    return ret

if __name__ == "__main__":
    possible_combinations([[1, 2], ['a', 'b']])


def number_of_nodes(tree):
    (symbol, children) = tree
    return 1 + sum([number_of_nodes(c) for c in children])

if __name__ == "__main__":
    number_of_nodes(derivation_tree)


def max_height(tree):
    (symbol, children) = tree
    if len(children) == 0:
        return 1
    return 1 + max([max_height(c) for c in children])

if __name__ == "__main__":
    max_height(derivation_tree)


# ### Simplification Strategies

if __name__ == "__main__":
    print('\n### Simplification Strategies')




# #### Finding Subtrees

if __name__ == "__main__":
    print('\n#### Finding Subtrees')




class GrammarReducer(GrammarReducer):
    def subtrees_with_symbol(self, tree, symbol, depth=-1, ignore_root=True):
        # Find all subtrees in TREE whose root is SYMBOL.
        # If IGNORE_ROOT is true, ignore the root note of TREE.

        ret = []
        (child_symbol, children) = tree
        if depth <= 0 and not ignore_root and child_symbol == symbol:
            ret.append(tree)

        # Search across all children
        if depth != 0 and children is not None:
            for c in children:
                ret += self.subtrees_with_symbol(c,
                                                 symbol,
                                                 depth=depth - 1,
                                                 ignore_root=False)

        return ret

if __name__ == "__main__":
    grammar_reducer = GrammarReducer(
        mystery,
        EarleyParser(EXPR_GRAMMAR),
        log_reduce=True)


if __name__ == "__main__":
    all_terminals(derivation_tree)


if __name__ == "__main__":
    [all_terminals(t) for t in grammar_reducer.subtrees_with_symbol(
        derivation_tree, "<term>")]


# #### Alternate Expansions

if __name__ == "__main__":
    print('\n#### Alternate Expansions')




class GrammarReducer(GrammarReducer):
    def alternate_reductions(self, tree, symbol, depth=-1):
        reductions = []

        expansions = self.grammar.get(symbol, [])
        expansions.sort(
            key=lambda expansion: len(
                expansion_to_children(expansion)))

        for expansion in expansions:
            expansion_children = expansion_to_children(expansion)

            match = True
            new_children_reductions = []
            for (alt_symbol, _) in expansion_children:
                child_reductions = self.subtrees_with_symbol(
                    tree, alt_symbol, depth=depth)
                if len(child_reductions) == 0:
                    match = False   # Child not found; cannot apply rule
                    break

                new_children_reductions.append(child_reductions)

            if not match:
                continue  # Try next alternative

            # Use the first suitable combination
            for new_children in possible_combinations(new_children_reductions):
                new_tree = (symbol, new_children)
                if number_of_nodes(new_tree) < number_of_nodes(tree):
                    reductions.append(new_tree)
                    if not self.try_all_combinations:
                        break

        # Sort by number of nodes
        reductions.sort(key=number_of_nodes)

        return reductions

if __name__ == "__main__":
    grammar_reducer = GrammarReducer(
        mystery,
        EarleyParser(EXPR_GRAMMAR),
        log_reduce=True)


if __name__ == "__main__":
    all_terminals(derivation_tree)


if __name__ == "__main__":
    grammar_reducer.try_all_combinations = True
    print([all_terminals(t)
           for t in grammar_reducer.alternate_reductions(derivation_tree, "<term>")])


if __name__ == "__main__":
    grammar_reducer.try_all_combinations = False
    [all_terminals(t) for t in grammar_reducer.alternate_reductions(
        derivation_tree, "<term>")]


# #### Both Strategies Together

if __name__ == "__main__":
    print('\n#### Both Strategies Together')




class GrammarReducer(GrammarReducer):
    def symbol_reductions(self, tree, symbol, depth=-1):
        """Find all expansion alternatives for the given symbol"""
        reductions = (self.subtrees_with_symbol(tree, symbol, depth=depth)
                      + self.alternate_reductions(tree, symbol, depth=depth))

        # Filter duplicates
        unique_reductions = []
        for r in reductions:
            if r not in unique_reductions:
                unique_reductions.append(r)

        return unique_reductions

if __name__ == "__main__":
    grammar_reducer = GrammarReducer(
        mystery,
        EarleyParser(EXPR_GRAMMAR),
        log_reduce=True)


if __name__ == "__main__":
    all_terminals(derivation_tree)


if __name__ == "__main__":
    reductions = grammar_reducer.symbol_reductions(derivation_tree, "<expr>")
    tree_list_to_string([r for r in reductions])


if __name__ == "__main__":
    reductions = grammar_reducer.symbol_reductions(derivation_tree, "<term>")
    tree_list_to_string([r for r in reductions])


# ### The Reduction Strategy

if __name__ == "__main__":
    print('\n### The Reduction Strategy')




class GrammarReducer(GrammarReducer):
    def reduce_subtree(self, tree, subtree, depth=-1):
        symbol, children = subtree
        if len(children) == 0:
            return False

        if self.log_reduce:
            print("Reducing", all_terminals(subtree), "with depth", depth)

        reduced = False
        while True:
            reduced_child = False
            for i, child in enumerate(children):
                (child_symbol, _) = child
                for reduction in self.symbol_reductions(
                        child, child_symbol, depth):
                    if number_of_nodes(reduction) >= number_of_nodes(child):
                        continue

                    # Try this reduction
                    if self.log_reduce:
                        print(
                            "Replacing",
                            all_terminals(
                                children[i]),
                            "by",
                            all_terminals(reduction))
                    children[i] = reduction
                    if self.test(all_terminals(tree)) == Runner.FAIL:
                        # Success
                        if self.log_reduce:
                            print("New tree:", all_terminals(tree))
                        reduced = reduced_child = True
                        break
                    else:
                        # Didn't work out - restore
                        children[i] = child

            if not reduced_child:
                if self.log_reduce:
                    print("Tried all alternatives for", all_terminals(subtree))
                break

        # Run recursively
        for c in children:
            if self.reduce_subtree(tree, c, depth):
                reduced = True

        return reduced

class GrammarReducer(GrammarReducer):
    def reduce_tree(self, tree):
        return self.reduce_subtree(tree, tree)

class GrammarReducer(GrammarReducer):
    def parse(self, inp):
        tree, *_ = self.parser.parse(inp)
        if self.log_reduce:
            print(all_terminals(tree))
        return tree

class GrammarReducer(GrammarReducer):
    def reduce(self, inp):
        tree = self.parse(inp)
        self.reduce_tree(tree)
        return all_terminals(tree)

if __name__ == "__main__":
    expr_input


if __name__ == "__main__":
    grammar_reducer = GrammarReducer(
        eval_mystery,
        EarleyParser(EXPR_GRAMMAR),
        log_test=True)
    grammar_reducer.reduce(expr_input)


# ### A Depth-Oriented Strategy

if __name__ == "__main__":
    print('\n### A Depth-Oriented Strategy')




if __name__ == "__main__":
    grammar_reducer = GrammarReducer(
        mystery,
        EarleyParser(EXPR_GRAMMAR),
        log_reduce=True)


if __name__ == "__main__":
    all_terminals(derivation_tree)


if __name__ == "__main__":
    display_tree(derivation_tree)


if __name__ == "__main__":
    [all_terminals(t) for t in grammar_reducer.subtrees_with_symbol(
        derivation_tree, "<term>", depth=1)]


if __name__ == "__main__":
    [all_terminals(t) for t in grammar_reducer.subtrees_with_symbol(
        derivation_tree, "<term>", depth=2)]


if __name__ == "__main__":
    [all_terminals(t) for t in grammar_reducer.subtrees_with_symbol(
        derivation_tree, "<term>", depth=3)]


class GrammarReducer(GrammarReducer):
    def reduce_tree(self, tree):
        depth = 0
        while depth < max_height(tree):
            reduced = self.reduce_subtree(tree, tree, depth)
            if reduced:
                depth = 0    # Start with new tree
            else:
                depth += 1   # Extend search for subtrees
        return tree        

if __name__ == "__main__":
    grammar_reducer = GrammarReducer(
        mystery,
        EarleyParser(EXPR_GRAMMAR),
        log_test=True)
    grammar_reducer.reduce(expr_input)


# ### Comparing Strategies

if __name__ == "__main__":
    print('\n### Comparing Strategies')




if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer
else:
    from .GrammarFuzzer import GrammarFuzzer


if __name__ == "__main__":
    long_expr_input = GrammarFuzzer(EXPR_GRAMMAR, min_nonterminals=100).fuzz()
    long_expr_input


if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


if __name__ == "__main__":
    grammar_reducer = GrammarReducer(eval_mystery, EarleyParser(EXPR_GRAMMAR))
    with Timer() as grammar_time:
        print(grammar_reducer.reduce(long_expr_input))


if __name__ == "__main__":
    grammar_reducer.tests


if __name__ == "__main__":
    grammar_time.elapsed_time()


if __name__ == "__main__":
    dd_reducer = DeltaDebuggingReducer(eval_mystery)
    with Timer() as dd_time:
        print(dd_reducer.reduce(long_expr_input))


if __name__ == "__main__":
    dd_reducer.tests


if __name__ == "__main__":
    dd_time.elapsed_time()


# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




if __name__ == "__main__":
    import os
    os.system("python -c 'x = 1 + 2 * 3 / 0'")


if __package__ is None or __package__ == "":
    from Fuzzer import ProgramRunner
else:
    from .Fuzzer import ProgramRunner


class ZeroDivisionRunner(ProgramRunner):
    """Make outcome 'FAIL' if ZeroDivisionError occurs"""
    def run(self, inp=""):
        result, outcome = super().run(inp)
        if result.stderr.find('ZeroDivisionError') >= 0:
            outcome = 'FAIL'
        return result, outcome

if __name__ == "__main__":
    python_input = "x = 1 + 2 * 3 / 0"
    python_runner = ZeroDivisionRunner("python")
    result, outcome = python_runner.run(python_input)
    outcome


if __name__ == "__main__":
    dd = DeltaDebuggingReducer(python_runner)
    dd.reduce(python_input)


# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Background

if __name__ == "__main__":
    print('\n## Background')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1: Mutation-Based Fuzzing with Reduction

if __name__ == "__main__":
    print('\n### Exercise 1: Mutation-Based Fuzzing with Reduction')




# ### Exercise 2: Reduction by Production

if __name__ == "__main__":
    print('\n### Exercise 2: Reduction by Production')




# ### Exercise 3: The Big Reduction Shoot-Out

if __name__ == "__main__":
    print('\n### Exercise 3: The Big Reduction Shoot-Out')



