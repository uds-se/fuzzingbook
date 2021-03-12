#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License:


import logging
from bibtexparser.bibdatabase import (BibDatabase, COMMON_STRINGS,
                                      BibDataString,
                                      BibDataStringExpression)


logger = logging.getLogger(__name__)

__all__ = ['BibTexWriter']


def to_bibtex(parsed):
    """
    Convenience function for backwards compatibility.
    """
    return BibTexWriter().write(parsed)


def _str_or_expr_to_bibtex(e):
    if isinstance(e, BibDataStringExpression):
        return ' # '.join([_str_or_expr_to_bibtex(s) for s in e.expr])
    elif isinstance(e, BibDataString):
        return e.name
    else:
        return '{' + e + '}'


class BibTexWriter(object):
    """
    Writer to convert a :class:`BibDatabase` object to a string or file formatted as a BibTeX file.

    Example::

        from bibtexparser.bwriter import BibTexWriter

        bib_database = ...

        writer = BibTexWriter()
        writer.contents = ['comments', 'entries']
        writer.indent = '  '
        writer.order_entries_by = ('ENTRYTYPE', 'author', 'year')
        bibtex_str = bibtexparser.dumps(bib_database, writer)

    """

    _valid_contents = ['entries', 'comments', 'preambles', 'strings']

    def __init__(self, write_common_strings=False):
        #: List of BibTeX elements to write, valid values are `entries`, `comments`, `preambles`, `strings`.
        self.contents = ['comments', 'preambles', 'strings', 'entries']
        #: Character(s) for indenting BibTeX field-value pairs. Default: single space.
        self.indent = ' '
        #: Align values. Determines the maximal number of characters used in any fieldname and aligns all values
        #    according to that by filling up with single spaces. Default: False
        self.align_values = False
        #: Characters(s) for separating BibTeX entries. Default: new line.
        self.entry_separator = '\n'
        #: Tuple of fields for ordering BibTeX entries. Set to `None` to disable sorting. Default: BibTeX key `('ID', )`.
        self.order_entries_by = ('ID', )
        #: Tuple of fields for display order in a single BibTeX entry. Fields not listed here will be displayed
        #: alphabetically at the end. Set to '[]' for alphabetical order. Default: '[]'
        self.display_order = []
        #: BibTeX syntax allows comma first syntax
        #: (common in functional languages), use this to enable
        #: comma first syntax as the bwritter output
        self.comma_first = False
        #: internal variable used if self.align_values = True
        self._max_field_width = 0
        #: Whether common strings are written
        self.common_strings = write_common_strings

    def write(self, bib_database):
        """
        Converts a bibliographic database to a BibTeX-formatted string.

        :param bib_database: bibliographic database to be converted to a BibTeX string
        :type bib_database: BibDatabase
        :return: BibTeX-formatted string
        :rtype: str or unicode
        """
        bibtex = ''
        for content in self.contents:
            try:
                # Add each element set (entries, comments)
                bibtex += getattr(self, '_' + content + '_to_bibtex')(bib_database)
            except AttributeError:
                logger.warning("BibTeX item '{}' does not exist and will not be written. Valid items are {}."
                               .format(content, self._valid_contents))
        return bibtex

    def _entries_to_bibtex(self, bib_database):
        bibtex = ''
        if self.order_entries_by:
            # TODO: allow sort field does not exist for entry
            entries = sorted(bib_database.entries, key=lambda x: BibDatabase.entry_sort_key(x, self.order_entries_by))
        else:
            entries = bib_database.entries

        if self.align_values:
            # determine maximum field width to be used
            widths = [max(map(len, entry.keys())) for entry in entries]
            self._max_field_width = max(widths)

        for entry in entries:
            bibtex += self._entry_to_bibtex(entry)
        return bibtex

    def _entry_to_bibtex(self, entry):
        bibtex = ''
        # Write BibTeX key
        bibtex += '@' + entry['ENTRYTYPE'] + '{' + entry['ID']

        # create display_order of fields for this entry
        # first those keys which are both in self.display_order and in entry.keys
        display_order = [i for i in self.display_order if i in entry]
        # then all the other fields sorted alphabetically
        display_order += [i for i in sorted(entry) if i not in self.display_order]
        if self.comma_first:
            field_fmt = u"\n{indent}, {field:<{field_max_w}} = {value}"
        else:
            field_fmt = u",\n{indent}{field:<{field_max_w}} = {value}"
        # Write field = value lines
        for field in [i for i in display_order if i not in ['ENTRYTYPE', 'ID']]:
            try:
                bibtex += field_fmt.format(
                    indent=self.indent,
                    field=field,
                    field_max_w=self._max_field_width,
                    value=_str_or_expr_to_bibtex(entry[field]))
            except TypeError:
                raise TypeError(u"The field %s in entry %s must be a string"
                                % (field, entry['ID']))
        bibtex += "\n}\n" + self.entry_separator
        return bibtex

    def _comments_to_bibtex(self, bib_database):
        return ''.join(['@comment{{{0}}}\n{1}'.format(comment, self.entry_separator)
                        for comment in bib_database.comments])

    def _preambles_to_bibtex(self, bib_database):
        return ''.join(['@preamble{{"{0}"}}\n{1}'.format(preamble, self.entry_separator)
                        for preamble in bib_database.preambles])

    def _strings_to_bibtex(self, bib_database):
        return ''.join([
            u'@string{{{name} = {value}}}\n{sep}'.format(
                name=name,
                value=_str_or_expr_to_bibtex(value),
                sep=self.entry_separator)
            for name, value in bib_database.strings.items()
            if (self.common_strings or
                name not in COMMON_STRINGS or  # user defined string
                value != COMMON_STRINGS[name]  # string has been updated
                )])
