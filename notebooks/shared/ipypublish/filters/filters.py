def wrap_latex(input, max_length=75, **kwargs):
    if len(input) > max_length:
        # remove double dollars, as they don't allow word wrap
        if len(input) > 3:
            if input[0:2] == '$$' and input[-2:] == '$$':
                input = input[1:-1]
        # change \left( and \right) to \bigg( and \bigg), as they allow word wrap
        input = input.replace(r'\left(', r'\big(')
        input = input.replace(r'\right)', r'\big)')

    return input


def remove_dollars(input, **kwargs):
    """remove dollars from start/end of file"""
    while input.startswith('$'):
        input = input[1:]
    while input.endswith('$'):
        input = input[0:-1]
    return input


def first_para(input, **kwargs):
    r"""get only ttext before a \n (i.e. the fist paragraph)"""
    return input.split('\n')[0]


import re
from collections import OrderedDict


def _write_roman(num):
    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num > 0:
                roman_num(num)
            else:
                break

    return "".join([a for a in roman_num(num)])


def _repl(match):
    return _write_roman(int(match.group(0)))


def create_key(input, **kwargs):
    """create sanitized key string which only contains lowercase letters,
    (semi)colons as c, underscores as u and numbers as roman numerals
    in this way the keys with different input should mainly be unique

    >>> create_key('fig:A_10name56')
    'figcauxnamelvi'

    """
    input = re.compile(r"\d+").sub(_repl, input)
    input = input.replace(':', 'c')
    input = input.replace(';', 'c')
    input = input.replace('_', 'u')
    return re.sub('[^a-zA-Z]+', '', str(input)).lower()


def dict_to_kwds(dct, kwdstr):
    """ convert a dictionary to a string of keywords

    Parameters
    ----------
    dct : dict
    kwdstr: str
        additional keyword strings

    Examples
    --------
    >>> dict_to_kwds({"a":1,"c":3},'a=1,b=2')
    'a=1,c=3,b=2,'

    """
    string = ''
    for key in sorted(dct.keys()):
        string += '{0}={1},'.format(key, dct[key])
    for kwd in kwdstr.split(","):
        if not kwd.split('=')[0] + '=' in string:
            string += kwd + ','
    return string


def is_equation(text):
    text = text.strip()

    if any([text.startswith('\\begin{{{0}}}'.format(env)) and text.endswith('\\end{{{0}}}'.format(env)) for env in
            ['equation', 'split', 'equation*', 'align', 'align*', 'multline', 'multline*', 'gather', 'gather*']]):
        return True
    elif text.startswith('$') and text.endswith('$'):
        return True
    else:
        return False
