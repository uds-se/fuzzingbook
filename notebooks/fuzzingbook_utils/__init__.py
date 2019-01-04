# Define the contents of this file as a package
__all__ = ["PrettyTable", "YouTubeVideo", "print_file", "HTML"]


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
