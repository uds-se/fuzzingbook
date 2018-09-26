#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/GrammarCoverageFuzzer.html
# Last change: 2018-09-26 17:16:40+02:00
#
# This material is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International License
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)


# # Grammar Coverage
# 
# In this chapter, we explore how to systematically cover elements of a grammar, as well as element combinations.  \todo{Work in progress.}

if __name__ == "__main__":
    print('# Grammar Coverage')




# **Prerequisites**
# 
# * You should have read the [chapter on grammars](Grammars.ipynb).
# * You should have read the [chapter on efficient grammar fuzzing](GrammarFuzzer.ipynb).

# ## Covering Grammar Elements
# 
# [Producing inputs from grammars](GrammarFuzzer.ipynb) gives all possible expansions of a rule the same likelihood.  For producing a comprehensive test suite, however, it makes more sense to maximize _variety_ – for instance, by avoiding repeating the same expansions over and over again.  To achieve this, we can track the _coverage_ of individual expansions: If we have seen some expansion already, we can prefer other possible expansions in the future.  The idea of ensuring that each expansion in the grammar is used at least once goes back to Paul Purdom \cite{purdom1972}.
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

if __name__ == "__main__":
    print('\n## Covering Grammar Elements')




# import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from Grammars import DIGIT_GRAMMAR, EXPR_GRAMMAR, CGI_GRAMMAR, URL_GRAMMAR, START_SYMBOL
else:
    from .Grammars import DIGIT_GRAMMAR, EXPR_GRAMMAR, CGI_GRAMMAR, URL_GRAMMAR, START_SYMBOL


if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer, all_terminals, nonterminals, display_tree
else:
    from .GrammarFuzzer import GrammarFuzzer, all_terminals, nonterminals, display_tree


import random

class GrammarCoverageFuzzer(GrammarFuzzer):
    def __init__(self, *args, **kwargs):
        # invoke superclass __init__(), passing all arguments
        super().__init__(*args, **kwargs)
        self.reset_coverage()

    def reset_coverage(self):
        self.covered_expansions = set()

    def expansion_coverage(self):
        return self.covered_expansions


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR)
    f.fuzz()


class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def expansion_key(self, symbol, children):
        """Convert (symbol, children) into a key.  `children` can be an expansion string or a derivation tree."""
        if not isinstance(children, str):
            children = all_terminals((symbol, children))
        return symbol + " -> " + children

    def max_expansion_coverage(self):
        """Return set of all expansions in a grammar"""
        expansions = set()
        for nonterminal in self.grammar:
            for expansion in self.grammar[nonterminal]:
                expansions.add(self.expansion_key(nonterminal, expansion))
        return expansions

if __name__ == "__main__":
    f = GrammarCoverageFuzzer(DIGIT_GRAMMAR)
    f.max_expansion_coverage()


class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def choose_node_expansion(self, node, possible_children):
        # Prefer uncovered expansions
        (symbol, children) = node
        uncovered_children = [(i, c) for (i, c) in enumerate(possible_children)
                              if self.expansion_key(symbol, c) not in self.covered_expansions]

        # print("Uncovered:", uncovered_children)

        if len(uncovered_children) == 0:
            # All expansions covered - use superclass method
            if self.log:
                print("All", symbol, "alternatives covered")

            return super().choose_node_expansion(node, possible_children)

        # select a random expansion
        index = random.randrange(len(uncovered_children))
        (new_children_index, new_children) = uncovered_children[index]

        # Save the expansion as covered
        key = self.expansion_key(symbol, new_children)
        assert key not in self.covered_expansions

        if self.log:
            print("Now covered:", key)
        self.covered_expansions.add(key)

        return new_children_index


# By returning the set of expansions covered so far, we can invoke the fuzzer multiple times, each time adding to the grammar coverage.  With the `DIGIT_GRAMMAR` grammar, for instance, this lets the grammar produce one digit after the other:

if __name__ == "__main__":
    f = GrammarCoverageFuzzer(DIGIT_GRAMMAR, log=True)
    f.fuzz()


if __name__ == "__main__":
    f.fuzz()


if __name__ == "__main__":
    f.fuzz()


if __name__ == "__main__":
    f.covered_expansions


# At the end, all expansions are covered:

if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


# Let us now create some more expressions:

if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR)
    for i in range(10):
        print(f.fuzz())


# Again, all expansions are covered:

if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


# ## Grammar Coverage and Code Coverage

if __name__ == "__main__":
    print('\n## Grammar Coverage and Code Coverage')




if __name__ == "__main__":
    f = GrammarCoverageFuzzer(CGI_GRAMMAR)


if __name__ == "__main__":
    for i in range(10):
        print(f.fuzz())


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


# ## Deep Foresight
# 
# Our naive way of selecting expansions is not sufficient; we need to favor expansions that may be covered, but _lead to uncovered ones_.

if __name__ == "__main__":
    print('\n## Deep Foresight')




class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def _max_symbol_expansion_coverage(
            self, symbol, max_depth, cov, symbols_seen):
        """Return set of all expansions in a grammar starting with `symbol`"""
        if max_depth > 0:
            symbols_seen.add(symbol)
            for expansion in self.grammar[symbol]:
                key = self.expansion_key(symbol, expansion)
                if key not in cov:
                    cov.add(key)
                    for s in nonterminals(expansion):
                        if s not in symbols_seen:
                            new_cov, new_symbols_seen = self._max_symbol_expansion_coverage(s, max_depth - 1,
                                                                                            cov, symbols_seen)
                            cov |= new_cov
                            symbols_seen |= new_symbols_seen

        return (cov, symbols_seen)

    def max_symbol_expansion_coverage(self, symbol, max_depth=float('inf')):
        cov, symbols_seen = self._max_symbol_expansion_coverage(
            symbol, max_depth, set(), set())
        return cov


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR)
    f.max_symbol_expansion_coverage('<integer>')


if __name__ == "__main__":
    f.max_symbol_expansion_coverage('<digit>')


if __name__ == "__main__":
    assert f.max_expansion_coverage() == f.max_symbol_expansion_coverage(START_SYMBOL)


class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def _new_child_coverage(self, children, max_depth):
        new_cov = set()
        for (c_symbol, _) in children:
            if c_symbol in self.grammar:
                new_cov |= self.max_symbol_expansion_coverage(
                    c_symbol, max_depth)
        return new_cov

    def new_child_coverage(self, symbol, children, max_depth):
        new_cov = self._new_child_coverage(children, max_depth)
        for c in children:
            new_cov.add(self.expansion_key(symbol, children))
        new_cov -= self.expansion_coverage()
        return new_cov


class GrammarCoverageFuzzer(GrammarCoverageFuzzer):
    def choose_node_expansion(self, node, possible_children):
        # Prefer uncovered expansions
        (symbol, children) = node
        # print("Possible children:", possible_children)

        # Find maximum depth at which we discover uncovered nodes
        for max_depth in range(len(self.grammar)):
            new_coverages = [
                self.new_child_coverage(
                    symbol, c, max_depth) for c in possible_children]
            max_new_coverage = max(len(new_coverage)
                                   for new_coverage in new_coverages)
            if max_new_coverage > 0:
                break

        if max_new_coverage == 0:
            # All expansions covered - use superclass method
            if self.log:
                print("All", symbol, "alternatives covered")
            return super().choose_node_expansion(node, possible_children)

        if self.log:
            print("New coverages at depth", max_depth)
            for i in range(len(possible_children)):
                print(i,
                      possible_children[i],
                      new_coverages[i],
                      len(new_coverages[i]))

        children_with_max_new_coverage = [(i, c) for (i, c) in enumerate(possible_children)
                                          if len(new_coverages[i]) == max_new_coverage]
        if self.log:
            print("Children with max new coverage:",
                  [c for (i, c) in children_with_max_new_coverage])

        # select a random expansion
        new_children_index, new_children = random.choice(
            children_with_max_new_coverage)

        # Save the expansion as covered
        key = self.expansion_key(symbol, new_children)

        if self.log:
            print("Now covered:", key)
        self.covered_expansions.add(key)

        return new_children_index


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(EXPR_GRAMMAR, min_nonterminals=3)
    f.fuzz()


if __name__ == "__main__":
    f.max_expansion_coverage() - f.expansion_coverage()


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(CGI_GRAMMAR, min_nonterminals=5)
    for i in range(10):
        print(f.fuzz(), f.max_expansion_coverage() - f.expansion_coverage())


if __name__ == "__main__":
    f = GrammarCoverageFuzzer(URL_GRAMMAR, min_nonterminals=5)
    for i in range(10):
        print(f.fuzz(), f.max_expansion_coverage() - f.expansion_coverage())


# ## Combinatorial Coverage
# 
# Start with depth of 1, then increase depth

if __name__ == "__main__":
    print('\n## Combinatorial Coverage')




def flatten_tree(tree):
    """Return `tree` without grandchildren"""
    (symbol, children) = tree
    if children is None:
        return symbol
    new_children = [c for (c, _) in children]
    return (symbol, new_children)

def match_path(path, tree):
    def _match_path(path, tree):
        (symbol, children) = tree
        (path_symbol, path_children) = path
        if symbol != path_symbol:
            return False

        if path_children is not None and len(path_children) > 0:
            if len(children) > 1:
                # Multiple children given; must all match
                if len(children) != len(path_children):
                    return False
                return all(_match_path(
                    path_children[i], children[i]) for i in range(len(children)))
            # One child given; can match any
            return any(_match_path(path_children[0], c) for c in children)
        else:
            return True

    # print("Matching", path, "in", tree)
    matched = _match_path(path, tree)
    # print("Matched" if matched else "Did not match", path, "in", tree)
    return matched


if __name__ == "__main__":
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])
    display_tree(derivation_tree)



if __name__ == "__main__":
    path = ("<start>", None)

    assert match_path(path, derivation_tree)


if __name__ == "__main__":
    start_tree = ('<start>', [('4', [])])
    display_tree(start_tree)


if __name__ == "__main__":
    path = ('<start>', [('4', None)])

    assert match_path(start_tree, path)


def find_path(path, tree):
    def _find_path(path, tree):
        (symbol, children) = tree
        (path_symbol, path_children) = path
        if symbol == path_symbol:
            if len(path_children) == 1:
                # One child given: any can match
                if any(match_path(path_children[0], c) for c in children):
                    return True
            elif match_path(path, tree):
                # Multiple children given; must all match
                return True

        return any(_find_path(path, c) for c in children)

    # print("Searching", path, "in", tree)
    found = _find_path(path, tree)
    # print("Found" if found else "Did not find", path, "in", tree)
    return found

if __name__ == "__main__":
    path = ("<expr>", [(" + ", None)])

    assert find_path(path, derivation_tree)
    assert not match_path(path, derivation_tree)


class CombinatorialCoverageFuzzer(GrammarFuzzer):
    def __init__(self, *args, **kwargs):
        # invoke superclass __init__(), passing all arguments
        super().__init__(*args, **kwargs)
        self.reset_coverage()

    def reset_coverage(self):
        self._current_depth = 0
        self.covered_expansions = set()

    def expand_tree_once(self, tree):
        if self._current_depth == 0:
            self._current_tree = tree
        self._current_depth += 1
        tree = super().expand_tree_once(tree)
        self._current_depth -= 1
        return tree


if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)
    f.fuzz()


class CombinatorialCoverageFuzzer(CombinatorialCoverageFuzzer):
    def path_to_node(self, tree, node):
        (symbol, children) = tree
        if id(tree) == id(node):
            return node

        if children is None:
            return None

        for c in children:
            p = self.path_to_node(c, node)
            if p is not None:
                return (symbol, [p])

        return None


if __name__ == "__main__":
    derivation_tree = ("<start>",
                       [("<expr>",
                         [("<expr>", None),
                          (" + ", []),
                             ("<term>", None)]
                         )])
    display_tree(derivation_tree)



if __name__ == "__main__":
    node = derivation_tree[1][0][1][0]
    node


if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)
    path = f.path_to_node(derivation_tree, node)
    path


if __name__ == "__main__":
    display_tree(path)


class CombinatorialCoverageFuzzer(CombinatorialCoverageFuzzer):
    def subpath(self, path, height):
        def _subpath(path, height):
            # print(path, height)
            (symbol, children) = path
            if children is None or len(children) == 0:
                return (path, 0)

            subpath, subheight = _subpath(children[0], height)
            if subheight < height:
                return ((symbol, [subpath]), subheight + 1)
            else:
                return (subpath, subheight)

        subpath, subheight = _subpath(path, height)
        return subpath


if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)
    f.subpath(path, height=0)


if __name__ == "__main__":
    f.subpath(path, height=1)


if __name__ == "__main__":
    f.subpath(('<start>', [('<expr>', [('<expr>', None)])]), height=0)


class CombinatorialCoverageFuzzer(CombinatorialCoverageFuzzer):
    def append_to_path(self, path, new_children):
        (symbol, children) = path
        if children is None or len(children) == 0:
            return (symbol, new_children)
        else:
            assert len(children) == 1
            return (symbol, [self.append_to_path(children[0], new_children)])

if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)
    new_children = [("<term>", None)]


if __name__ == "__main__":
    new_path = f.append_to_path(path, new_children)
    display_tree(new_path)


class CombinatorialCoverageFuzzer(CombinatorialCoverageFuzzer):
    def expansion_key(self, path):
        return repr(path)

    def choose_node_expansion(self, node, possible_children):
        (symbol, children) = node

        path_to_node = self.path_to_node(self._current_tree, node)
        # print(path_to_node)

        for path_height in range(0, len(path_to_node)):
            possible_indexes = []
            subpath = self.subpath(path_to_node, height=path_height)

            if self.log:
                print(
                    "Choosing from subpaths of height",
                    path_height,
                    ":",
                    subpath)

            for i in range(len(possible_children)):
                expansion_path = self.append_to_path(
                    subpath, possible_children[i])
                key = self.expansion_key(expansion_path)
                if key not in self.covered_expansions:
                    # print(key, "not seen before")
                    possible_indexes.append(i)

            if len(possible_indexes) > 0:
                index = random.choice(possible_indexes)
                expansion_path = self.append_to_path(
                    subpath, possible_children[index])
                key = self.expansion_key(expansion_path)
                assert key not in self.covered_expansions
                self.covered_expansions.add(key)
                return index

        if self.log:
            print("All combinations covered")
        return super().choose_node_expansion(node, possible_children)


if __name__ == "__main__":
    f = CombinatorialCoverageFuzzer(EXPR_GRAMMAR)

    for i in range(10):
        before = len(f.covered_expansions)
        s = f.fuzz()
        after = len(f.covered_expansions)
        print(s, "  #", after - before, "new")


if __name__ == "__main__":
    f.covered_expansions


# ## Advanced Grammar Coverage Metrics
# 
# \todo{Expand.}

if __name__ == "__main__":
    print('\n## Advanced Grammar Coverage Metrics')




# ## Lessons Learned
# 
# * _Lesson one_
# * _Lesson two_
# * _Lesson three_

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps
# 
# _Link to subsequent chapters (notebooks) here, as in:_
# 
# * [use _mutations_ on existing inputs to get more valid inputs](MutationFuzzer.ipynb)
# * [use _grammars_ (i.e., a specification of the input format) to get even more valid inputs](Grammars.ipynb)
# * [reduce _failing inputs_ for efficient debugging](Reducing.ipynb)
# 

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Exercises
# 
# Close the chapter with a few exercises such that people have things to do.  In Jupyter Notebook, use the `exercise2` nbextension to add solutions that can be interactively viewed or hidden:
# 
# * Mark the _last_ cell of the exercise (this should be a _text_ cell) as well as _all_ cells of the solution.  (Use the `rubberband` nbextension and use Shift+Drag to mark multiple cells.)
# * Click on the `solution` button at the top.
# 
# (Alternatively, just copy the exercise and solution cells below with their metadata.)

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1
# 
# _Text of the exercise_

if __name__ == "__main__":
    print('\n### Exercise 1')




if __name__ == "__main__":
    # Some code that is part of the exercise
    pass


# _Some more text for the exercise_

# _Some text for the solution_

if __name__ == "__main__":
    # Some code for the solution
    2 + 2


# _Some more text for the solution_

# ### Exercise 2
# 
# _Text of the exercise_

if __name__ == "__main__":
    print('\n### Exercise 2')




# _Solution for the exercise_
