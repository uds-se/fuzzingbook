#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/LangFuzzer.html
# Last change: 2019-04-02 22:28:20+13:00
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


# # Fuzzing with Input Fragments

if __name__ == "__main__":
    print('# Fuzzing with Input Fragments')




if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


if __package__ is None or __package__ == "":
    from Parser import PEGParser
else:
    from .Parser import PEGParser

if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer
else:
    from .GrammarFuzzer import GrammarFuzzer


# ## Recombining Parsed Inputs

if __name__ == "__main__":
    print('\n## Recombining Parsed Inputs')




# ### A Grammar-based Mutational Fuzzer

if __name__ == "__main__":
    print('\n### A Grammar-based Mutational Fuzzer')




import string

if __package__ is None or __package__ == "":
    from Grammars import crange, syntax_diagram
else:
    from .Grammars import crange, syntax_diagram


VAR_GRAMMAR = {
    '<start>': ['<statements>'],
    '<statements>': ['<statement>;<statements>', '<statement>'],
    '<statement>': ['<assignment>'],
    '<assignment>': ['<identifier>=<expr>'],
    '<identifier>': ['<word>'],
    '<word>': ['<alpha><word>', '<alpha>'],
    '<alpha>': list(string.ascii_letters),
    '<expr>': ['<term>+<expr>', '<term>-<expr>', '<term>'],
    '<term>': ['<factor>*<term>', '<factor>/<term>', '<factor>'],
    '<factor>':
    ['+<factor>', '-<factor>', '(<expr>)', '<identifier>', '<number>'],
    '<number>': ['<integer>.<integer>', '<integer>'],
    '<integer>': ['<digit><integer>', '<digit>'],
    '<digit>': crange('0', '9')
}

if __name__ == "__main__":
    syntax_diagram(VAR_GRAMMAR)


if __name__ == "__main__":
    mystring = 'va=10;vb=20'


def hl_predicate(_d, _n, symbol, _a): return symbol in {
    '<number>', '<identifier>'}

if __package__ is None or __package__ == "":
    from Parser import PEGParser, highlight_node
else:
    from .Parser import PEGParser, highlight_node

if __package__ is None or __package__ == "":
    from GrammarFuzzer import display_tree
else:
    from .GrammarFuzzer import display_tree


if __name__ == "__main__":
    parser = PEGParser(VAR_GRAMMAR)
    for tree in parser.parse(mystring):
        display_tree(tree, node_attr=highlight_node(hl_predicate))


VAR_TOKENS = {'<number>', '<identifier>'}

if __name__ == "__main__":
    mystring = 'avar=1.3;bvar=avar-3*(4+300)'
    parser = PEGParser(VAR_GRAMMAR, tokens=VAR_TOKENS)
    for tree in parser.parse(mystring):
        display_tree(tree, node_attr=highlight_node(hl_predicate))


if __name__ == "__main__":
    mystrings = [
        'abc=12+(3+3.3)',
        'a=1;b=2;c=a+b',
        'avar=1.3;bvar=avar-3*(4+300)',
        'a=1.3;b=a-1*(4+3+(2/a))',
        'a=10;b=20;c=34;d=-b+(b*b-4*a*c)/(2*a)',
        'x=10;y=20;z=(x+y)*(x-y)',
        'x=23;y=51;z=x*x-y*y',
    ]


if __package__ is None or __package__ == "":
    from Fuzzer import Fuzzer
else:
    from .Fuzzer import Fuzzer


class LangFuzzer(Fuzzer):
    def __init__(self, parser):
        self.parser = parser
        self.fragments = {k: [] for k in self.parser.cgrammar}

    def traverse_tree(self, node):
        counter = 1
        nodes = {}

        def helper(node, id):
            nonlocal counter
            name, children = node
            new_children = []
            nodes[id] = node
            for child in children:
                counter += 1
                new_children.append(helper(child, counter))
            return name, new_children, id

        return helper(node, counter), nodes

    def fragment(self, strings):
        self.trees = []
        for string in strings:
            for tree in self.parser.parse(string):
                tree, nodes = self.traverse_tree(tree)
                self.trees.append((tree, nodes))
                for node in nodes:
                    symbol = nodes[node][0]
                    if symbol in self.fragments:
                        self.fragments[symbol].append(nodes[node])
        return self.fragments

if __name__ == "__main__":
    lf = LangFuzzer(PEGParser(VAR_GRAMMAR, tokens=VAR_TOKENS))
    fragments = lf.fragment(mystrings)
    for key in fragments:
        print("%s: %d" % (key, len(fragments[key])))


import random

class LangFuzzer(LangFuzzer):
    def __init__(self, parser, strings):
        self.parser = parser
        self.fragments = {k: [] for k in self.parser.cgrammar}
        self.fragment(strings)

# #### Candidate

if __name__ == "__main__":
    print('\n#### Candidate')




class LangFuzzer(LangFuzzer):
    def candidate(self):
        tree, nodes = random.choice(self.trees)
        interesting_nodes = [
            n for n in nodes if nodes[n][0] in self.fragments
            and len(self.fragments[nodes[n][0]]) > 1
        ]
        node = random.choice(interesting_nodes)
        return tree, node

if __name__ == "__main__":
    random.seed(1)
    lf = LangFuzzer(PEGParser(VAR_GRAMMAR, tokens=VAR_TOKENS), mystrings)
    tree, node = lf.candidate()


def hl_predicate(_d, nid, _s, _a): return nid in {node}

if __name__ == "__main__":
    display_tree(tree, node_attr=highlight_node(hl_predicate))


# #### Generate New Tree

if __name__ == "__main__":
    print('\n#### Generate New Tree')




class LangFuzzer(LangFuzzer):
    def generate_new_tree(self, node, choice):
        name, children, id = node
        if id == choice:
            return random.choice(self.fragments[name])
        else:
            return (name, [self.generate_new_tree(c, choice)
                           for c in children])

if __name__ == "__main__":
    random.seed(1)
    lf = LangFuzzer(PEGParser(VAR_GRAMMAR, tokens=VAR_TOKENS), mystrings)
    tree, node = lf.candidate()


def hl_predicate(_d, nid, _s, _a): return nid in {node}

if __package__ is None or __package__ == "":
    from GrammarFuzzer import tree_to_string
else:
    from .GrammarFuzzer import tree_to_string


if __name__ == "__main__":
    new_tree = lf.generate_new_tree(tree, node)
    for s in [tree_to_string(i) for i in [tree, new_tree]]:
        print(s)
    display_tree(new_tree, node_attr=highlight_node(hl_predicate))


# #### Fuzz

if __name__ == "__main__":
    print('\n#### Fuzz')




class LangFuzzer(LangFuzzer):
    def fuzz(self):
        tree, node = self.candidate()
        modified = self.generate_new_tree(tree, node)
        return tree_to_string(modified)

if __name__ == "__main__":
    lf = LangFuzzer(PEGParser(VAR_GRAMMAR, tokens=VAR_TOKENS), mystrings)
    for i in range(10):
        print(lf.fuzz())


if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


if __name__ == "__main__":
    trials = 100

    lf = LangFuzzer(PEGParser(VAR_GRAMMAR, tokens=VAR_TOKENS), mystrings)
    valid = []
    time = 0
    for i in range(trials):
        with Timer() as t:
            s = lf.fuzz()
            try:
                exec(s, {}, {})
                valid.append((s, t.elapsed_time()))
            except:
                pass
            time += t.elapsed_time()
    print("%d valid strings, that is LangFuzzer generated %f%% valid entries" %
          (len(valid), len(valid) * 100.0 / trials))
    print("Total time of %f seconds" % time)


if __name__ == "__main__":
    gf = GrammarFuzzer(VAR_GRAMMAR)
    valid = []
    time = 0
    for i in range(trials):
        with Timer() as t:
            s = gf.fuzz()
            try:
                exec(s, {}, {})
                valid.append(s)
            except:
                pass
            time += t.elapsed_time()
    print("%d valid strings, that is GrammarFuzzer generated %f%% valid entries" %
          (len(valid), len(valid) * 100.0 / trials))
    print("Total time of %f seconds" % time)


# ## Grammar-Based Mutation

if __name__ == "__main__":
    print('\n## Grammar-Based Mutation')




if __package__ is None or __package__ == "":
    from Grammars import EXPR_GRAMMAR
else:
    from .Grammars import EXPR_GRAMMAR

if __package__ is None or __package__ == "":
    from GrammarFuzzer import display_tree
else:
    from .GrammarFuzzer import display_tree

if __package__ is None or __package__ == "":
    from Parser import EarleyParser
else:
    from .Parser import EarleyParser


if __name__ == "__main__":
    parser = EarleyParser(EXPR_GRAMMAR)
    tree,*_ = parser.parse("1 + 2 * 3")
    display_tree(tree)


def mutate_tree(tree, grammar):
    pass

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




# ### Exercise 1: A Different LangFuzzer

if __name__ == "__main__":
    print('\n### Exercise 1: A Different LangFuzzer')




class LangFuzzer2(LangFuzzer):
    def __init__(self, parser, strings):
        super().__init__(parser, strings)
        self.gfuzz = GrammarFuzzer(parser.grammar())

    def check_diversity(self, pool):
        return len(pool) > 10

    def candidate(self):
        tree, nodes = random.choice(self.trees)
        interesting_nodes = [
            n for n in nodes if nodes[n][0] in self.fragments
            and nodes[n][0] is not self.parser.start_symbol()
            and len(self.fragments[nodes[n][0]]) > 0
        ]
        node = random.choice(interesting_nodes)
        return tree, node

    def generate_new_tree(self, node, choice):
        name, children, id = node
        if id == choice:
            pool = self.fragments[name]
            if self.check_diversity(pool):
                return random.choice(self.fragments[name])
            else:
                return None
        else:
            return (name,
                    [self.generate_new_tree(c, choice) for c in children])

    def fuzz(self):
        tree, node = self.candidate()
        tree_with_a_hole = self.generate_new_tree(tree, node)
        modified = self.gfuzz.expand_tree(tree_with_a_hole)
        return tree_to_string(modified)

if __name__ == "__main__":
    parser = EarleyParser(VAR_GRAMMAR, tokens=VAR_TOKENS)
    lf = LangFuzzer2(parser, mystrings)
    for i in range(100):
        print(lf.fuzz())

