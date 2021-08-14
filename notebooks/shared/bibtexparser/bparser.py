#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original source: github.com/okfn/bibserver
# Authors:
# markmacgillivray
# Etienne Posthumus (epoz)
# Francois Boulogne <fboulogne at april dot org>

import sys
import io
import logging

from bibtexparser.bibdatabase import (BibDatabase, BibDataString, as_text,
                                      BibDataStringExpression, STANDARD_TYPES)
from bibtexparser.bibtexexpression import BibtexExpression

logger = logging.getLogger(__name__)

__all__ = ['BibTexParser']


if sys.version_info >= (3, 0):
    ustr = str
else:
    ustr = unicode


def parse(data, *args, **kwargs):
    parser = BibTexParser(*args, **kwargs)
    return parser.parse(data)


class BibTexParser(object):
    """
    A parser for reading BibTeX bibliographic data files.

    Example::

        from bibtexparser.bparser import BibTexParser

        bibtex_str = ...

        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        parser.homogenize_fields = False
        parser.common_strings = False
        bib_database = bibtexparser.loads(bibtex_str, parser)

    :param customization: function or None (default)
        Customization to apply to parsed entries.
    :param ignore_nonstandard_types: bool (default True)
        If True ignores non-standard bibtex entry types.
    :param homogenize_fields: bool (default False)
        Common field name replacements (as set in alt_dict attribute).
    :param interpolate_strings: bool (default True)
        If True, replace bibtex string by their value, else uses
        BibDataString objects.
    :param common_strings: book (default False)
        Include common string definitions (e.g. month abbreviations) to
        the bibtex file.
    """

    def __new__(cls, data=None, **args):
        """
        To catch the old API structure in which creating the parser would
        immediately parse and return data.
        """

        if data is None:
            return super(BibTexParser, cls).__new__(cls)
        else:
            # For backwards compatibility: if data is given, parse
            # and return the `BibDatabase` object instead of the parser.
            return parse(data, **args)

    def __init__(self, data=None,
                 customization=None,
                 ignore_nonstandard_types=True,
                 homogenize_fields=False,
                 interpolate_strings=True,
                 common_strings=False):
        """
        Creates a parser for rading BibTeX files

        :return: parser
        :rtype: `BibTexParser`
        """
        self.bib_database = BibDatabase()

        #: Load common strings such as months abbreviation
        #: Default: `False`.
        self.common_strings = common_strings
        if self.common_strings:
            self.bib_database.load_common_strings()

        #: Callback function to process BibTeX entries after parsing,
        #: for example to create a list from a string with multiple values.
        #: By default all BibTeX values are treated as simple strings.
        #: Default: `None`.
        self.customization = customization

        #: Ignore non-standard BibTeX types (`book`, `article`, etc).
        #: Default: `True`.
        self.ignore_nonstandard_types = ignore_nonstandard_types

        #: Sanitize BibTeX field names, for example change `url` to `link` etc.
        #: Field names are always converted to lowercase names.
        #: Default: `False`.
        self.homogenize_fields = homogenize_fields

        #: Interpolate Bibtex Strings or keep the structure
        self.interpolate_strings = interpolate_strings

        # On some sample data files, the character encoding detection simply
        # hangs We are going to default to utf8, and mandate it.
        self.encoding = 'utf8'

        # pre-defined set of key changes
        self.alt_dict = {
            'keyw': u'keyword',
            'keywords': u'keyword',
            'authors': u'author',
            'editors': u'editor',
            'urls': u'url',
            'link': u'url',
            'links': u'url',
            'subjects': u'subject'
        }

        # Setup the parser expression
        self._init_expressions()

    def parse(self, bibtex_str, partial=False):
        """Parse a BibTeX string into an object

        :param bibtex_str: BibTeX string
        :type: str or unicode
        :param partial: If True, print errors only on parsing failures.
        If False, an exception is raised.
        :type: boolean
        :return: bibliographic database
        :rtype: BibDatabase
        """
        bibtex_file_obj = self._bibtex_file_obj(bibtex_str)
        try:
            self._expr.parseFile(bibtex_file_obj)
        except self._expr.ParseException as exc:
            logger.error("Could not parse properly, starting at %s", exc.line)
            if not partial:
                raise exc
        return self.bib_database

    def parse_file(self, file, partial=False):
        """Parse a BibTeX file into an object

        :param file: BibTeX file or file-like object
        :type: file
        :param partial: If True, print errors only on parsing failures.
        If False, an exception is raised.
        :type: boolean
        :return: bibliographic database
        :rtype: BibDatabase
        """
        return self.parse(file.read(), partial=partial)

    def _init_expressions(self):
        """
        Defines all parser expressions used internally.
        """
        self._expr = BibtexExpression()

        # Handle string as BibDataString object
        self._expr.set_string_name_parse_action(
            lambda s, l, t:
                BibDataString(self.bib_database, t[0]))
        if self.interpolate_strings:
            maybe_interpolate = lambda expr: as_text(expr)
        else:
            maybe_interpolate = lambda expr: expr
        self._expr.set_string_expression_parse_action(
            lambda s, l, t:
                maybe_interpolate(
                    BibDataStringExpression.expression_if_needed(t)))

        # Add notice to logger
        self._expr.add_log_function(logger.debug)

        # Set actions
        self._expr.entry.addParseAction(
            lambda s, l, t: self._add_entry(
                t.get('EntryType'), t.get('Key'), t.get('Fields'))
            )
        self._expr.implicit_comment.addParseAction(
            lambda s, l, t: self._add_comment(t[0])
            )
        self._expr.explicit_comment.addParseAction(
            lambda s, l, t: self._add_comment(t[0])
            )
        self._expr.preamble_decl.addParseAction(
            lambda s, l, t: self._add_preamble(t[0])
            )
        self._expr.string_def.addParseAction(
            lambda s, l, t: self._add_string(t['StringName'].name,
                                             t['StringValue'])
            )

    def _bibtex_file_obj(self, bibtex_str):
        # Some files have Byte-order marks inserted at the start
        byte = b'\xef\xbb\xbf'
        if isinstance(bibtex_str, ustr):
            byte = ustr(byte, self.encoding, 'ignore')
            if bibtex_str[0] == byte:
                bibtex_str = bibtex_str[1:]
        else:
            if bibtex_str[:3] == byte:
                bibtex_str = bibtex_str[3:]
            bibtex_str = bibtex_str.decode(encoding=self.encoding)
        return io.StringIO(bibtex_str)

    def _clean_val(self, val):
        """ Clean instring before adding to dictionary

        :param val: a value
        :type val: string
        :returns: string -- value
        """
        if not val or val == "{}":
            return ''
        return val

    def _clean_key(self, key):
        """ Lowercase a key and return as unicode.

        :param key: a key
        :type key: string
        :returns: (unicode) string -- value
        """
        key = key.lower()
        if not isinstance(key, ustr):
            return ustr(key, 'utf-8')
        else:
            return key

    def _clean_field_key(self, key):
        """ Clean a bibtex field key and homogenize alternative forms.

        :param key: a key
        :type key: string
        :returns: string -- value
        """
        key = self._clean_key(key)
        if self.homogenize_fields:
            if key in list(self.alt_dict.keys()):
                key = self.alt_dict[key]
        return key

    def _add_entry(self, entry_type, entry_id, fields):
        """ Adds a parsed entry.
        Includes checking type and fields, cleaning, applying customizations.

        :param entry_type: the entry type
        :type entry_type: string
        :param entry_id: the entry bibid
        :type entry_id: string
        :param fields: the fields and values
        :type fields: dictionary
        :returns: string -- value
        """
        d = {}
        entry_type = self._clean_key(entry_type)
        if self.ignore_nonstandard_types and entry_type not in STANDARD_TYPES:
            logger.warning('Entry type %s not standard. Not considered.',
                           entry_type)
            return
        for key in fields:
            d[self._clean_field_key(key)] = self._clean_val(fields[key])
        d['ENTRYTYPE'] = entry_type
        d['ID'] = entry_id
        if self.customization is not None:
            # apply any customizations to the record object then return it
            logger.debug('Apply customizations and return dict')
            d = self.customization(d)
        self.bib_database.entries.append(d)

    def _add_comment(self, comment):
        """
        Stores a comment in the list of comment.

        :param comment: the parsed comment
        :type comment: string
        """
        logger.debug('Store comment in list of comments: ' +
                     comment.__repr__())
        self.bib_database.comments.append(comment)

    def _add_string(self, string_key, string):
        """
        Stores a new string in the string dictionary.

        :param string_key: the string key
        :type string_key: string
        :param string: the string value
        :type string: string
        """
        if string_key in self.bib_database.strings:
            logger.warning('Overwritting existing string for key: %s.',
                           string_key)
        logger.debug(u'Store string: {} -> {}'.format(string_key, string))
        self.bib_database.strings[string_key] = self._clean_val(string)

    def _add_preamble(self, preamble):
        """
        Stores a preamble.

        :param preamble: the parsed preamble
        :type preamble: string
        """
        logger.debug('Store preamble in list of preambles')
        self.bib_database.preambles.append(preamble)
