# Define the contents of this file as a package
__all__ = ["PrettyTable", "YouTubeVideo",
           "print_file", "HTML",
           "unicode_escape", "terminal_escape", "extract_class_definition"]


# Setup loader such that workbooks can be imported directly
try:
    import IPython
    have_ipython = True
except:
    have_ipython = False

if have_ipython:
    from . import import_notebooks

# Set fixed seed
from . import set_fixed_seed
set_fixed_seed.set_fixed_seed()


# Check for rich output
try:
    _rich_output = get_ipython().__class__.__name__
except NameError:
    _rich_output = False

def rich_output():
    return _rich_output


# Wrapper for YouTubeVideo
if have_ipython:
    import IPython.display
    class YouTubeVideo(IPython.display.YouTubeVideo):
        def __init__(self, video_id, **kwargs):
            super().__init__(video_id, width=640, height=360, **kwargs)
else:
    # Placeholder for imports
    class YouTubeVideo(object):
        def __init__(self, video_id, **kwargs):
            pass



# Checking for inheritance conflicts

# Multiple inheritance is a tricky thing.  If you have two classes $A'$ and $A''$ which both inherit from $A$, the same method $m()$ of $A$ may be overloaded in both $A'$ and $A''$.  If one now inherits from _both_ $A'$ and $A''$, and calls $m()$, which of the $m()$ implementations should be called?  Python "resolves" this conflict by simply invoking the one $m()$ method in the class one inherits from first.
# To avoid such conflicts, one can check whether the order in which one inherits makes a difference.  So try this method to compare the attributes with each other; if they refer to different code, you have to resolve the conflict.

from inspect import getattr_static, getsource

def inheritance_conflicts(c1, c2):
    """Return attributes defined differently in classes c1 and c2"""
    class c1c2(c1, c2):
        pass

    class c2c1(c2, c1):
        pass

    return [attr for attr in dir(c1c2) if getattr_static(
        c1c2, attr) != getattr_static(c2c1, attr)]


# Given a class, extract the final definitions of all methods defined so far.

def extract_class_definition(cls, log=False):
    eldest = [c for c in cls.mro()
                if c.__name__ == cls.__name__ and
                   cls.__name__ not in {i.__name__ for i in c.__bases__}]
    n_parents = sum([[j.__name__ for j in i.__bases__] for i in eldest], [])
    s_parents = '(%s)' % ', '.join(set(n_parents)) if n_parents else ''
    buf = ["class %s%s:" % (cls.__name__, s_parents)]
    seen = set()
    i = 0
    for curcls in cls.mro():
        i += 1
        if log: print('Parent: %d' % i, curcls.__name__)
        if curcls.__name__ != cls.__name__: continue
        for fn_name in dir(curcls):
            if log: print('\t:', fn_name)
            if fn_name in seen: continue
            if fn_name == '__new__':
                continue
            fn = curcls.__dict__.get(fn_name)
            if fn is None:
                continue
            if ('function' in str(type(fn))):
                seen.add(fn_name)
                buf.append(getsource(fn))
    return '\n'.join(buf)

# Printing files with syntax highlighting
def print_file(filename, lexer=None):
    content = open(filename, "rb").read().decode('utf-8')
    print_content(content, filename, lexer)

def print_content(content, filename=None, lexer=None):
    from pygments import highlight, lexers, formatters
    from pygments.lexers import get_lexer_for_filename, guess_lexer

    if rich_output():
        if lexer is None:
            if filename is None:
                lexer = guess_lexer(content)
            else:
                lexer = get_lexer_for_filename(filename)

        colorful_content = highlight(content, lexer, formatters.TerminalFormatter())
        print(colorful_content, end="")
    else:
        print(content, end="")


# Escaping unicode characters into ASCII for user-facing strings
def unicode_escape(s, error="backslashreplace"):
    def ascii_chr(byte):
        if 0 <= byte <= 127:
            return chr(byte)
        return r"\x%02x" % byte

    bytes = s.encode('utf-8', error)
    return "".join(map(ascii_chr, bytes))

# Same, but escaping unicode only if output is not a terminal
def terminal_escape(s):
    if rich_output():
        return s
    return unicode_escape(s)


# HTML() behaves like IPython.core.display.HTML(); but if png is True or the environment
# variable RENDER_HTML is set, it converts the HTML into a PNG image.
# This is useful for producing derived formats without HTML support (LaTeX/PDF, Word, ...)

import os
firefox = None

def HTML(data=None, url=None, filename=None, png=False, headless=True, zoom=2.0):
    if not png and not 'RENDER_HTML' in os.environ:
        # Standard behavior
        import IPython.core.display
        return IPython.core.display.HTML(data=data, url=url, filename=filename)

    # Import only as needed; avoids unnecessary dependencies
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
    from IPython.core.display import Image
    import tempfile

    # Get a webdriver
    global firefox
    if firefox is None:
        options = Options()
        options.headless = headless
        profile = FirefoxProfile()
        profile.set_preference("layout.css.devPixelsPerPx", repr(zoom))
        firefox = webdriver.Firefox(firefox_profile=profile, options=options)

    # Create a URL argument
    if data is not None:
        has_html = data.find('<html')
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.html') as fp:
            if has_html:
                fp.write(data.encode('utf8'))
            else:
                fp.write(('<html>' + data + '</html>').encode('utf8'))
            fp.flush()
            return HTML(filename=fp.name, png=True)

    if filename is not None:
        return HTML(url='file://' + filename, png=True)

    assert url is not None

    # Render URL as PNG
    firefox.get(url)
    return Image(firefox.get_screenshot_as_png())

import atexit
@atexit.register
def quit_webdriver():
    if firefox is not None:
        firefox.quit()
