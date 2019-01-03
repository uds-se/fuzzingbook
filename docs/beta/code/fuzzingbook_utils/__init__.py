# Define the contents of this file as a package
__all__ = ["PrettyTable", "YouTubeVideo", "print_file"]


# Setup loader such that workbooks can be imported directly
from . import import_notebooks


# Set fixed seed
from . import set_fixed_seed
set_fixed_seed.set_fixed_seed()


# Wrapper for YouTubeVideo
import IPython.display

class YouTubeVideo(IPython.display.YouTubeVideo):
    def __init__(self, video_id, **kwargs):
        super().__init__(video_id, width=640, height=360, **kwargs)


# Check for rich output
try:
    _rich_output = get_ipython().__class__.__name__
except NameError:
    _rich_output = False

def rich_output():
    return _rich_output

  
# Printing files with syntax highlighting
from pygments import highlight, lexers, formatters
from pygments.lexers import get_lexer_for_filename

def print_file(filename, lexer=None):
    contents = open(filename, "rb").read().decode('utf-8')
    if rich_output():
        if lexer is None:
            lexer = get_lexer_for_filename(filename)
        colorful_contents = highlight(contents, lexer, formatters.TerminalFormatter())
        print(colorful_contents, end="")
    else:
        print(contents, end="")


