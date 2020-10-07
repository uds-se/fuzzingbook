# Backwards Compatibility module

print(f"Warning: module '{__name__}' is deprecated. Use 'bookutils' instead.")

if __package__ is None or __package__ == "":
    from bookutils import *
else:
    from .bookutils import *
