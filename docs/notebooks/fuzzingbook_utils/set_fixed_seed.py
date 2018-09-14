#!/usr/bin/env python

# We set a fixed seed for all notebooks, such that creation is more predictable.
# This will only have an effect in notebooks, not the exported Python code.

# Interacting with a notebook (in particular executing things again and again)
# will still yield new results every time.

import random

def set_fixed_seed(seed=2001):
    # print("Setting fixed seed to", seed)
    random.seed(seed)