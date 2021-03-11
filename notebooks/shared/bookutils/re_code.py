#!/usr/bin/env python

import re

# To avoid re-running notebook computations during import,
# we only import code cells that match this regular expression
# i.e. definitions of 
# * functions: `def func()`
# * classes: `class X:`
# * constants: `UPPERCASE_VARIABLES`
# * types: `TypeVariables`, and
# * imports: `import foo`
RE_CODE = re.compile(r"^(def |class |@|[A-Z][A-Za-z0-9_]+ [-+*/]?= |[A-Z][A-Za-z0-9_]+[.:]|import |from )")
