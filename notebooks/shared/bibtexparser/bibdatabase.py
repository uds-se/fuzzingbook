from collections import OrderedDict
import sys


if sys.version_info.major == 2:
    TEXT_TYPE = unicode
else:
    TEXT_TYPE = str


STANDARD_TYPES = set([
    'article',
    'book',
    'booklet',
    'conference',
    'inbook',
    'incollection',
    'inproceedings',
    'manual',
    'mastersthesis',
    'misc',
    'phdthesis',
    'proceedings',
    'techreport',
    'unpublished'])
COMMON_STRINGS = OrderedDict([
    ('jan', 'January'),
    ('feb', 'February'),
    ('mar', 'March'),
    ('apr', 'April'),
    ('may', 'May'),
    ('jun', 'June'),
    ('jul', 'July'),
    ('aug', 'August'),
    ('sep', 'September'),
    ('oct', 'October'),
    ('nov', 'November'),
    ('dec', 'December'),
    ])


class UndefinedString(KeyError):
    pass


class BibDatabase(object):
    """
    Bibliographic database object that follows the data structure of a BibTeX file.
    """

    def __init__(self):
        #: List of BibTeX entries, for example `@book{...}`, `@article{...}`, etc. Each entry is a simple dict with
        #: BibTeX field-value pairs, for example `'author': 'Bird, R.B. and Armstrong, R.C. and Hassager, O.'` Each
        #: entry will always have the following dict keys (in addition to other BibTeX fields):
        #:
        #: * `ID` (BibTeX key)
        #: * `ENTRYTYPE` (entry type in lowercase, e.g. `book`, `article` etc.)
        self.entries = []
        self._entries_dict = {}
        #: List of BibTeX comment (`@comment{...}`) blocks.
        self.comments = []
        #: OrderedDict of BibTeX string definitions (`@string{...}`). In order of definition.
        self.strings = OrderedDict()  # Not sure if order is import, keep order just in case
        #: List of BibTeX preamble (`@preamble{...}`) blocks.
        self.preambles = []

    def load_common_strings(self):
        self.strings.update(COMMON_STRINGS)

    def get_entry_list(self):
        """Get a list of bibtex entries.

        :returns: BibTeX entries
        :rtype: list
        .. deprecated:: 0.5.6
           Use :attr:`entries` instead.
        """
        return self.entries

    @staticmethod
    def entry_sort_key(entry, fields):
        result = []
        for field in fields:
            result.append(TEXT_TYPE(entry.get(field, '')).lower())  # Sorting always as string
        return tuple(result)

    def get_entry_dict(self):
        """Return a dictionary of BibTeX entries.
        The dict key is the BibTeX entry key
        """
        # If the hash has never been made, make it
        if not self._entries_dict:
            for entry in self.entries:
                self._entries_dict[entry['ID']] = entry
        return self._entries_dict

    entries_dict = property(get_entry_dict)

    def expand_string(self, name):
        try:
            return BibDataStringExpression.expand_if_expression(
                self.strings[name])
        except KeyError:
            raise(UndefinedString(name))


class BibDataString(object):
    """
    Represents a bibtex string.

    This object enables maintaining string expressions as list of strings
    and BibDataString. Can be interpolated from Bibdatabase.
    """

    def __init__(self, bibdatabase, name):
        self._bibdatabase = bibdatabase
        self.name = name.lower()

    def __eq__(self, other):
        return isinstance(other, BibDataString) and self.name == other.name

    def __repr__(self):
        return "BibDataString({})".format(self.name.__repr__())

    def get_value(self):
        """
        Query value from string name.

        :returns: string
        """
        return self._bibdatabase.expand_string(self.name)

    def get_dependencies(self, known_dependencies=set()):
        """Recursively tracks strings on which the expression depends.

        :param kown_dependencies: dependencies to ignore
        """
        raise NotImplementedError

    @staticmethod
    def expand_string(string_or_bibdatastring):
        """
        Eventually replaces a bibdatastring by its value.

        :param string_or_bibdatastring: the parsed token
        :type string_expr: string or BibDataString
        :returns: string
        """
        if isinstance(string_or_bibdatastring, BibDataString):
            return string_or_bibdatastring.get_value()
        else:
            return string_or_bibdatastring


class BibDataStringExpression(object):
    """
    Represents a bibtex string expression.

    String expressions are sequences of regular strings and bibtex strings.
    This object enables maintaining string expressions as list of strings.
    The expression are represented as lists of regular strings and
    BibDataStrings. They can be interpolated from Bibdatabase.

    BibDataStringExpression(e)

    :param e: list of strings and BibDataStrings
    """

    def __init__(self, expression):
        self.expr = expression

    def __eq__(self, other):
        return isinstance(other, BibDataStringExpression) and self.expr == other.expr

    def __repr__(self):
        return "BibDataStringExpression({})".format(self.expr.__repr__())

    def get_value(self):
        """
        Replaces bibdatastrings by their values in the expression.

        :returns: string
        """
        return ''.join([BibDataString.expand_string(s) for s in self.expr])

    def apply_on_strings(self, fun):
        """
        Maps a function on strings in expression, keeping unchanged
        BibDataStrings.

        :param fun: function from strings to strings
        """
        self.expr = [s if isinstance(s, BibDataString) else fun(s)
                     for s in self.expr]

    @staticmethod
    def expand_if_expression(string_or_expression):
        """
        Eventually replaces a BibDataStringExpression by its value.

        :param string_or_expression: the object to expand
        :type string_expr: string or BibDataStringExpression
        :returns: string
        """
        if isinstance(string_or_expression, BibDataStringExpression):
            return string_or_expression.get_value()
        else:
            return string_or_expression

    @staticmethod
    def expression_if_needed(tokens):
        """Build expression only if tokens are not a regular value.
        """
        if len(tokens) == 1 and not isinstance(tokens[0], BibDataString):
            return tokens[0]
        else:
            return BibDataStringExpression(tokens)


def as_text(text_string_or_expression):
    if isinstance(text_string_or_expression,
                  (BibDataString, BibDataStringExpression)):
        return text_string_or_expression.get_value()
    else:
        return TEXT_TYPE(text_string_or_expression)
