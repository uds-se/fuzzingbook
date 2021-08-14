#!/usr/bin/env python

# We set a fixed seed for all notebooks and examples,
# such that creation is more predictable.

# Interacting with a notebook (in particular executing cells again and again)
# will still yield new results every time.

import random

def set_fixed_seed(seed: int = 2001) -> None:
    # print("Setting fixed seed to", seed)
    random.seed(seed)