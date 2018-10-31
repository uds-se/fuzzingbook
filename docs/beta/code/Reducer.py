#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Reducer.html
# Last change: 2018-10-25 14:38:14+02:00
#
#
# Copyright (c) 2018 Saarland University, CISPA, authors, and contributors
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




# ## Why Reducing?

if __name__ == "__main__":
    print('\n## Why Reducing?')




import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from Fuzzer import RandomFuzzer, Runner
else:
    from .Fuzzer import RandomFuzzer, Runner


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
    input_without_first_and_third_quarter = failing_input[quarter_length:quarter_length * 2] + failing_input[quarter_length * 3:]
    mystery.run(input_without_first_and_third_quarter)


if __name__ == "__main__":
    input_without_first_and_fourth_quarter = failing_input[quarter_length:quarter_length * 3]
    mystery.run(input_without_first_and_fourth_quarter)


class Reducer(object):
    def __init__(self, runner, log=False):
        """Attach reducer to the given `runner`"""
        self.runner = runner
        self.log = log
        self.reset()

    def reset(self):
        self.tests = 0

    def test(self, inp):
        result, outcome = self.runner.run(inp)
        self.tests += 1
        if self.log:
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
        assert self.test(inp) == Runner.FAIL

        n = 2     # Initial granularity
        while len(inp) >= 2:
            start = 0
            subset_length = len(inp) / n
            some_complement_is_failing = False

            while start < len(inp):
                complement = inp[:int(start)] + inp[int(start + subset_length):]

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
    dd_reducer = DeltaDebuggingReducer(mystery, log=True)
    dd_reducer.reduce(failing_input)


# ## Grammar-Based Input Reduction

if __name__ == "__main__":
    print('\n## Grammar-Based Input Reduction')




if __package__ is None or __package__ == "":
    from Parser import PEGParser, parse
else:
    from .Parser import PEGParser, parse


if __package__ is None or __package__ == "":
    from GrammarFuzzer import all_terminals, expansion_to_children
else:
    from .GrammarFuzzer import all_terminals, expansion_to_children


if __name__ == "__main__":
    # For logging the queue
    def queue_to_string(q):
        return "[" + ", ".join([all_terminals(tree) for tree in q]) + "]"


if __name__ == "__main__":
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])


if __name__ == "__main__":
    queue_to_string([derivation_tree, derivation_tree])


if __package__ is None or __package__ == "":
    from Grammars import START_SYMBOL
else:
    from .Grammars import START_SYMBOL


class GrammarReducer(Reducer):
    def __init__(self, runner, grammar, start_symbol=START_SYMBOL, log=False):
        super().__init__(runner, log=log)
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.parser = PEGParser(grammar, start_symbol)

class GrammarReducer(GrammarReducer):
    def derivation_reductions(self, tree):
        (symbol, children) = tree
        if len(children) == 0:
            return []  # Terminal symbol

        print("Trying alternative expansions for " + symbol)

        # Possible expansions for this symbol
        expansions = self.grammar[symbol]
        print("Expansions: " + repr(expansions))

        alternatives = \
            [expansion_to_children(expansion) for expansion in expansions]

        reductions = []
        for alternative in alternatives:

            if len(alternative) > len(children):
                continue  # New alternative has more children

            match = True
            new_children_reductions = []
            # print("Trying alternative expansion " + queue_to_string(alternative))
            for alt_child in alternative:
                (alt_symbol, _) = alt_child
                child_reductions = subtrees_with_symbol(alt_symbol, tree)
                if len(child_reductions) == 0:
                    # Child not found; cannot apply rule
                    match = False
                    break

                # print("Found alternatives " + queue_to_string(child_reductions))
                new_children_reductions.append(child_reductions)

            if not match:
                continue  # Try next alternative

            # Go through the possible combinations
            for new_children in possible_combinations(new_children_reductions):
                new_tree = (symbol, new_children)

                if number_of_nodes(new_tree) >= number_of_nodes(tree):
                    continue  # No reduction

                reductions.append(new_tree)

        # Apply this recursively
        if children is not None:
            for i in range(0, len(children)):
                child = children[i]
                child_reductions = self.derivation_reductions(child)
                for reduced_child in child_reductions:
                    new_children = (children[:i] + 
                            [reduced_child] +
                            children[i + 1:])
                    reductions.append((symbol, new_children))

        # Filter duplicates
        unique_reductions = []
        for r in reductions:
            if r not in unique_reductions:
                unique_reductions.append(r)
        reductions = unique_reductions

        if len(reductions) > 0:
            # We have a new expansion
            print("Can reduce " + symbol + " " + all_terminals(tree) + \
                 " to reduced subtrees " + queue_to_string(reductions))

        return reductions

class GrammarReducer(GrammarReducer):
    def reductions(self, tree):
        return self.derivation_reductions(tree)

class GrammarReducer(GrammarReducer):
    # Reduce with respect to a given test
    def reduce_tree(self, tree):
        # Find possible reductions
        smallest_tree = tree
        tree_reductions = self.reductions(tree)
        print("Alternatives: " + queue_to_string(tree_reductions))

        while len(tree_reductions) > 0:
            t = tree_reductions[0]
            tree_reductions = tree_reductions[1:]
            s = all_terminals(t)
            if self.test(s) == Runner.FAIL:
                # Found new smallest tree; try to reduce that one further
                smallest_tree = t
                tree_reductions = self.reductions(t)
                tree_reductions.sort(key = lambda tree: -number_of_nodes(tree))
                print("New smallest tree: " + all_terminals(smallest_tree))

        return smallest_tree

class GrammarReducer(GrammarReducer):
    def parse(self, inp):
        cursor, tree = self.parser.unify_key(self.start_symbol, inp) # TODO: Have "Parser" base class
        print(all_terminals(tree))
        return tree

    def reduce(self, inp):
        tree = self.parse(inp)
        smallest_tree = self.reduce_tree(tree)
        return all_terminals(smallest_tree)

if __name__ == "__main__":
    # Find all subtrees in TREE whose root is SEARCH_SYMBOL.
    # If IGNORE_ROOT is true, ignore the root note of TREE.
    def subtrees_with_symbol(search_symbol, tree, ignore_root = True):
        ret = []
        (symbol, children) = tree
        if not ignore_root and symbol == search_symbol:
            ret.append(tree)

        # Search across all children
        if children is not None:
            for c in children:
                ret += subtrees_with_symbol(search_symbol, c, False)
        return ret


if __name__ == "__main__":
    # convert a list [[X1, X2], [Y1, Y2], ...] 
    # into [X1, Y1], [X1, Y2], [X2, Y1], [X2, Y2], ...
    def possible_combinations(list_of_lists):
        if len(list_of_lists) == 0:
            return []

        # print(list_of_lists)

        ret = []
        for e in list_of_lists[0]:
            if len(list_of_lists) == 1:
                ret.append([e])
            else:
                for c in possible_combinations(list_of_lists[1:]):
                    new_combo = [e] + c
                    # print("New combo: ", repr(new_combo))
                    ret.append(new_combo)
        return ret


if __name__ == "__main__":
    # Return the number of nodes
    def number_of_nodes(tree):
        (symbol, children) = tree
        n = 1
        for c in children:
            n += number_of_nodes(c)
        return n


if __package__ is None or __package__ == "":
    from Grammars import EXPR_GRAMMAR
else:
    from .Grammars import EXPR_GRAMMAR


if __name__ == "__main__":
    inp = "1 + (2 * 3)"
    grammar_reducer = GrammarReducer(mystery, EXPR_GRAMMAR)
    grammar_reducer.reduce(inp)


# ## _Section 4_

if __name__ == "__main__":
    print('\n## _Section 4_')




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




# ### Exercise 1: _Title_

if __name__ == "__main__":
    print('\n### Exercise 1: _Title_')




if __name__ == "__main__":
    # Some code that is part of the exercise
    pass


if __name__ == "__main__":
    # Some code for the solution
    2 + 2


# ### Exercise 2: _Title_

if __name__ == "__main__":
    print('\n### Exercise 2: _Title_')



