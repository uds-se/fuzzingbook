#!/usr/bin/env python

# We set a fixed seed for all notebooks and examples,
# such that creation is more predictable.

# Interacting with a notebook (in particular executing cells again and again)
# will still yield new results every time.

FIXED_SEED = 2001

import random
random.seed(FIXED_SEED)