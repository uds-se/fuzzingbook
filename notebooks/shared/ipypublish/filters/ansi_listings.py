"""Filters for processing ANSI colors within Jinja templates."""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

import re

from nbconvert.filters.latex import escape_latex

__all__ = [
    'ansi2listings',
]

_ANSI_RE = re.compile('\x1b\\[(.*?)([@-~])')

_ANSI_COLORS = (
    'ansi-black',
    'ansi-red',
    'ansi-green',
    'ansi-yellow',
    'ansi-blue',
    'ansi-magenta',
    'ansi-cyan',
    'ansi-white',
    'ansi-black-intense',
    'ansi-red-intense',
    'ansi-green-intense',
    'ansi-yellow-intense',
    'ansi-blue-intense',
    'ansi-magenta-intense',
    'ansi-cyan-intense',
    'ansi-white-intense',
)


def ansi2listings(text, escapechar='%'):
    """
    Convert ANSI colors to LaTeX colors.

    Parameters
    ----------
    text : unicode
        Text containing ANSI colors to convert to LaTeX
    escapechar: str
        escape character

    Examples
    --------
    >>> print(ansi2listings('\x1b[32mFolder\x1b[0m(\"subdir1\")'))
    %\\textcolor{ansi-green}{Folder}%("subdir1")

    >>> print(ansi2listings('\x1b[1;32mFolder\x1b[0m(\"subdir1\")'))
    %\\textcolor{ansi-green-intense}{\\textbf{Folder}}%("subdir1")

    >>> print(ansi2listings('\x1b[38;2;10;10;10mFolder\x1b[0m(\"subdir1\")'))
    %\\def\\tcRGB{\\textcolor[RGB]}\\expandafter\\tcRGB\\expandafter{\\detokenize{10,10,10}}{Folder}%("subdir1")

    """
    return _ansi2anything(text, _latexconverter, escapechar)


def _latexconverter(fg, bg, bold, escapechar):
    """
    Return start and end markup given foreground/background/bold.

    """
    if (fg, bg, bold) == (None, None, False):
        return '', ''

    starttag, endtag = '', ''

    if isinstance(fg, int):
        starttag += r'\textcolor{' + _ANSI_COLORS[fg] + '}{'
        endtag = '}' + endtag
    elif fg:
        # See http://tex.stackexchange.com/a/291102/13684
        starttag += r'\def\tcRGB{\textcolor[RGB]}\expandafter'
        starttag += r'\tcRGB\expandafter{\detokenize{%s,%s,%s}}{' % fg
        endtag = '}' + endtag

    if isinstance(bg, int):
        starttag += r'\setlength{\fboxsep}{0pt}\colorbox{'
        starttag += _ANSI_COLORS[bg] + '}{'
        endtag = r'\strut}' + endtag
    elif bg:
        starttag += r'\setlength{\fboxsep}{0pt}'
        # See http://tex.stackexchange.com/a/291102/13684
        starttag += r'\def\cbRGB{\colorbox[RGB]}\expandafter'
        starttag += r'\cbRGB\expandafter{\detokenize{%s,%s,%s}}{' % bg
        endtag = r'\strut}' + endtag

    if bold:
        starttag += r'\textbf{'
        endtag = '}' + endtag

    starttag = escapechar + starttag
    endtag += escapechar

    return starttag, endtag


def _ansi2anything(text, converter, escapechar):
    r"""
    Convert ANSI colors to HTML or LaTeX.

    See https://en.wikipedia.org/wiki/ANSI_escape_code

    Accepts codes like '\x1b[32m' (red) and '\x1b[1;32m' (bold, red).
    The codes 1 (bold) and 5 (blinking) are selecting a bold font, code
    0 and an empty code ('\x1b[m') reset colors and bold-ness.
    Unlike in most terminals, "bold" doesn't change the color.
    The codes 21 and 22 deselect "bold", the codes 39 and 49 deselect
    the foreground and background color, respectively.
    The codes 38 and 48 select the "extended" set of foreground and
    background colors, respectively.

    Non-color escape sequences (not ending with 'm') are filtered out.

    Ideally, this should have the same behavior as the function
    fixConsole() in notebook/notebook/static/base/js/utils.js.

    """
    fg, bg = None, None
    bold = False
    numbers = []
    out = []

    while text:
        m = _ANSI_RE.search(text)
        if m:
            if m.group(2) == 'm':
                try:
                    numbers = [int(n) if n else 0
                               for n in m.group(1).split(';')]
                except ValueError:
                    pass  # Invalid color specification
            else:
                pass  # Not a color code
            chunk, text = text[:m.start()], text[m.end():]
        else:
            chunk, text = text, ''

        if chunk:
            if bold and fg in range(8):
                fg += 8
            starttag, endtag = converter(fg, bg, bold, escapechar)
            out.append(starttag)
            if starttag.startswith(escapechar) and endtag.endswith(escapechar):
                chunk = escape_latex(chunk)
            out.append(chunk)
            out.append(endtag)

        while numbers:
            n = numbers.pop(0)
            if n == 0:
                fg = bg = None
                bold = False
            elif n in (1, 5):
                bold = True
            elif n in (21, 22):
                bold = False
            elif 30 <= n <= 37:
                fg = n - 30
            elif n == 38:
                try:
                    fg = _get_extended_color(numbers)
                except ValueError:
                    numbers.clear()
            elif n == 39:
                fg = None
            elif 40 <= n <= 47:
                bg = n - 40
            elif n == 48:
                try:
                    bg = _get_extended_color(numbers)
                except ValueError:
                    numbers.clear()
            elif n == 49:
                bg = None
            elif 90 <= n <= 97:
                fg = n - 90 + 8
            elif 100 <= n <= 107:
                bg = n - 100 + 8
            else:
                pass  # Unknown codes are ignored
    return ''.join(out)


def _get_extended_color(numbers):
    n = numbers.pop(0)
    if n == 2 and len(numbers) >= 3:
        # 24-bit RGB
        r = numbers.pop(0)
        g = numbers.pop(0)
        b = numbers.pop(0)
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError()
    elif n == 5 and len(numbers) >= 1:
        # 256 colors
        idx = numbers.pop(0)
        if idx < 0:
            raise ValueError()
        elif idx < 16:
            # 16 default terminal colors
            return idx
        elif idx < 232:
            # 6x6x6 color cube, see http://stackoverflow.com/a/27165165/500098
            r = (idx - 16) // 36
            r = 55 + r * 40 if r > 0 else 0
            g = ((idx - 16) % 36) // 6
            g = 55 + g * 40 if g > 0 else 0
            b = (idx - 16) % 6
            b = 55 + b * 40 if b > 0 else 0
        elif idx < 256:
            # grayscale, see http://stackoverflow.com/a/27165165/500098
            r = g = b = (idx - 232) * 10 + 8
        else:
            raise ValueError()
    else:
        raise ValueError()
    return r, g, b
