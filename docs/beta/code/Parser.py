#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Parser.html
# Last change: 2018-10-06 17:39:04+02:00
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


# # Parsing and Recombining Inputs

if __name__ == "__main__":
    print('# Parsing and Recombining Inputs')




# import fuzzingbook_utils

if __package__ is None or __package__ == "":
    from Grammars import EXPR_GRAMMAR, START_SYMBOL
else:
    from .Grammars import EXPR_GRAMMAR, START_SYMBOL


if __package__ is None or __package__ == "":
    from GrammarFuzzer import display_tree
else:
    from .GrammarFuzzer import display_tree


import functools
import re

RE_NONTERMINAL = re.compile(r'(<[a-zA-Z_]*>)')

class PEGParser:
    def __init__(self, grammar):
        def split(rule): return tuple(s for s in re.split(RE_NONTERMINAL, rule) if s)
        self.grammar = {k:[split(l) for l in rules] for k,rules in grammar.items()}

    def literal_match(self, part, text, cursor):
        return (cursor + len(part), (part, [])) if text[cursor:].startswith(part) else (cursor, None)

    # memoize repeated calls.
    @functools.lru_cache(maxsize=None)
    def unify_key(self, key, text, cursor=0):
        rules = self.grammar[key]
        # make a generator for matching rules. We dont want a list because
        # we want to be lazy and evaluate only until the first matching
        rets = (self.unify_line(rule, text, cursor) for rule in rules)
        # return the first non null (matching) rule's cursor and res
        cursor, res = next((ret for ret in rets if ret[1] is not None), (cursor, None))
        return (cursor, (key, res) if res is not None else None)

    def unify_line(self, parts, text, cursor):
        def is_symbol(v): return v[0] == '<'

        results = []
        for part in parts:
            # get the matcher function
            matcher = (self.unify_key if is_symbol(part) else self.literal_match)
            # compute the cursor, and the result from it.
            cursor, res = matcher(part, text, cursor)
            if res is None: return (cursor, None)
            results.append(res)
        return cursor, results

def parse(text, grammar, start_symbol=START_SYMBOL):
    def readall(fn): return ''.join([f for f in open(fn, 'r')]).strip()

    result = PEGParser(grammar).unify_key(start_symbol, text)
    return result

if __name__ == "__main__":
    cursor, tree = parse("1 + 2 * 3", EXPR_GRAMMAR)
    display_tree(tree)


# ## _Section 4_

if __name__ == "__main__":
    print('\n## _Section 4_')




# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1

if __name__ == "__main__":
    print('\n### Exercise 1')




if __name__ == "__main__":
    # Some code that is part of the exercise
    pass


if __name__ == "__main__":
    # Some code for the solution
    2 + 2


# ### Exercise 2

if __name__ == "__main__":
    print('\n### Exercise 2')



