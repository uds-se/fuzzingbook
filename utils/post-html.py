#!/usr/bin/env python
# Fix HTML produced by nbpublish

import sys

contents = sys.stdin.read()
print(contents.replace("\n\n</pre>", "\n</pre>"), end="")
