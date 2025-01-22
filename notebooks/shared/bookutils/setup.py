#!/usr/bin/env python
# Special setup code for fuzzingbook and debuggingbook notebooks

# We set a fixed seed for all notebooks and examples, such that creation
# is more predictable.
# Interacting with a notebook (in particular executing cells again and again)
# will still yield new results every time.

FIXED_SEED = 2001

import random
random.seed(FIXED_SEED)


# We disable automatic garbage collection for notebooks.
# As of Python 3.12, automatic gc in iPython may invoke a method
# _clean_thread_parent_frames(), interfering with tracing.

import gc
gc.disable()
