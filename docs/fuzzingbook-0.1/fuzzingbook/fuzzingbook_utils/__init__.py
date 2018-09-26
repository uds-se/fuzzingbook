# Define the contents of this file as a package
__all__ = ["PrettyTable"]

# Setup loader such that workbooks can be imported directly
from . import import_notebooks

# Set fixed seed
from . import set_fixed_seed
set_fixed_seed.set_fixed_seed()