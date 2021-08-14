#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A set of functions useful for customizing bibtex fields.
You can find inspiration from these functions to design yours.
Each of them takes a record and return the modified record.
"""

import re
import logging

from builtins import str

from bibtexparser.latexenc import latex_to_unicode, string_to_latex, protect_uppercase

logger = logging.getLogger(__name__)

__all__ = ['splitname', 'getnames', 'author', 'editor', 'journal', 'keyword',
           'link', 'page_double_hyphen', 'doi', 'type', 'convert_to_unicode',
           'homogenize_latex_encoding', 'add_plaintext_fields']


class InvalidName(ValueError):
    """Exception raised by :py:func:`customization.splitname` when an invalid name is input.

    """
    pass


def splitname(name, strict_mode=True):
    """
    Break a name into its constituent parts: First, von, Last, and Jr.

    :param string name: a string containing a single name
    :param Boolean strict_mode: whether to use strict mode
    :returns: dictionary of constituent parts
    :raises `customization.InvalidName`: If an invalid name is given and
                                         ``strict_mode = True``.

    In BibTeX, a name can be represented in any of three forms:
        * First von Last
        * von Last, First
        * von Last, Jr, First

    This function attempts to split a given name into its four parts. The
    returned dictionary has keys of ``first``, ``last``, ``von`` and ``jr``.
    Each value is a list of the words making up that part; this may be an empty
    list.  If the input has no non-whitespace characters, a blank dictionary is
    returned.

    It is capable of detecting some errors with the input name. If the
    ``strict_mode`` parameter is ``True``, which is the default, this results in
    a :class:`customization.InvalidName` exception being raised. If it is
    ``False``, the function continues, working around the error as best it can.
    The errors that can be detected are listed below along with the handling
    for non-strict mode:

        * Name finishes with a trailing comma: delete the comma
        * Too many parts (e.g., von Last, Jr, First, Error): merge extra parts
          into First
        * Unterminated opening brace: add closing brace to end of input
        * Unmatched closing brace: add opening brace at start of word

    """
    # Useful references:
    # http://maverick.inria.fr/~Xavier.Decoret/resources/xdkbibtex/bibtex_summary.html#names
    # http://tug.ctan.org/info/bibtex/tamethebeast/ttb_en.pdf

    # Whitespace characters that can separate words.
    whitespace = set(' ~\r\n\t')

    # We'll iterate over the input once, dividing it into a list of words for
    # each comma-separated section. We'll also calculate the case of each word
    # as we work.
    sections = [[]]      # Sections of the name.
    cases = [[]]         # 1 = uppercase, 0 = lowercase, -1 = caseless.
    word = []            # Current word.
    case = -1            # Case of the current word.
    level = 0            # Current brace level.
    bracestart = False   # Will the next character be the first within a brace?
    controlseq = True    # Are we currently processing a control sequence?
    specialchar = None   # Are we currently processing a special character?

    # Using an iterator allows us to deal with escapes in a simple manner.
    nameiter = iter(name)
    for char in nameiter:
        # An escape.
        if char == '\\':
            escaped = next(nameiter)

            # BibTeX doesn't allow whitespace escaping. Copy the slash and fall
            # through to the normal case to handle the whitespace.
            if escaped in whitespace:
                word.append(char)
                char = escaped

            else:
                # Is this the first character in a brace?
                if bracestart:
                    bracestart = False
                    controlseq = escaped.isalpha()
                    specialchar = True

                # Can we use it to determine the case?
                elif (case == -1) and escaped.isalpha():
                    if escaped.isupper():
                        case = 1
                    else:
                        case = 0

                # Copy the escape to the current word and go to the next
                # character in the input.
                word.append(char)
                word.append(escaped)
                continue

        # Start of a braced expression.
        if char == '{':
            level += 1
            word.append(char)
            bracestart = True
            controlseq = False
            specialchar = False
            continue

        # All the below cases imply this (and don't test its previous value).
        bracestart = False

        # End of a braced expression.
        if char == '}':
            # Check and reduce the level.
            if level:
                level -= 1
            else:
                if strict_mode:
                    raise InvalidName("Unmatched closing brace in name {{{0}}}.".format(name))
                word.insert(0, '{')

            # Update the state, append the character, and move on.
            controlseq = False
            specialchar = False
            word.append(char)
            continue

        # Inside a braced expression.
        if level:
            # Is this the end of a control sequence?
            if controlseq:
                if not char.isalpha():
                    controlseq = False

            # If it's a special character, can we use it for a case?
            elif specialchar:
                if (case == -1) and char.isalpha():
                    if char.isupper():
                        case = 1
                    else:
                        case = 0

            # Append the character and move on.
            word.append(char)
            continue

        # End of a word.
        # NB. we know we're not in a brace here due to the previous case.
        if char == ',' or char in whitespace:
            # Don't add empty words due to repeated whitespace.
            if word:
                sections[-1].append(''.join(word))
                word = []
                cases[-1].append(case)
                case = -1
                controlseq = False
                specialchar = False

            # End of a section.
            if char == ',':
                if len(sections) < 3:
                    sections.append([])
                    cases.append([])
                elif strict_mode:
                    raise InvalidName("Too many commas in the name {{{0}}}.".format(name))
            continue

        # Regular character.
        word.append(char)
        if (case == -1) and char.isalpha():
            if char.isupper():
                case = 1
            else:
                case = 0

    # Unterminated brace?
    if level:
        if strict_mode:
            raise InvalidName("Unterminated opening brace in the name {{{0}}}.".format(name))
        while level:
            word.append('}')
            level -= 1

    # Handle the final word.
    if word:
        sections[-1].append(''.join(word))
        cases[-1].append(case)

    # Get rid of trailing sections.
    if not sections[-1]:
        # Trailing comma?
        if (len(sections) > 1) and strict_mode:
            raise InvalidName("Trailing comma at end of name {{{0}}}.".format(name))
        sections.pop(-1)
        cases.pop(-1)

    # No non-whitespace input.
    if not sections or not any(bool(section) for section in sections):
        return {}

    # Initialise the output dictionary.
    parts = {'first': [], 'last': [], 'von': [], 'jr': []}

    # Form 1: "First von Last"
    if len(sections) == 1:
        p0 = sections[0]

        # One word only: last cannot be empty.
        if len(p0) == 1:
            parts['last'] = p0

        # Two words: must be first and last.
        elif len(p0) == 2:
            parts['first'] = p0[:1]
            parts['last'] = p0[1:]

        # Need to use the cases to figure it out.
        else:
            cases = cases[0]

            # First is the longest sequence of words starting with uppercase
            # that is not the whole string. von is then the longest sequence
            # whose last word starts with lowercase that is not the whole
            # string. Last is the rest. NB., this means last cannot be empty.

            # At least one lowercase letter.
            if 0 in cases:
                # Index from end of list of first and last lowercase word.
                firstl = cases.index(0) - len(cases)
                lastl = -cases[::-1].index(0) - 1
                if lastl == -1:
                    lastl -= 1      # Cannot consume the rest of the string.

                # Pull the parts out.
                parts['first'] = p0[:firstl]
                parts['von'] = p0[firstl:lastl+1]
                parts['last'] = p0[lastl+1:]

            # No lowercase: last is the last word, first is everything else.
            else:
                parts['first'] = p0[:-1]
                parts['last'] = p0[-1:]

    # Form 2 ("von Last, First") or 3 ("von Last, jr, First")
    else:
        # As long as there is content in the first name partition, use it as-is.
        first = sections[-1]
        if first and first[0]:
            parts['first'] = first

        # And again with the jr part.
        if len(sections) == 3:
            jr = sections[-2]
            if jr and jr[0]:
                parts['jr'] = jr

        # Last name cannot be empty; if there is only one word in the first
        # partition, we have to use it for the last name.
        last = sections[0]
        if len(last) == 1:
            parts['last'] = last

        # Have to look at the cases to figure it out.
        else:
            lcases = cases[0]

            # At least one lowercase: von is the longest sequence of whitespace
            # separated words whose last word does not start with an uppercase
            # word, and last is the rest.
            if 0 in lcases:
                split = len(lcases) - lcases[::-1].index(0)
                if split == len(lcases):
                    split = 0            # Last cannot be empty.
                parts['von'] = sections[0][:split]
                parts['last'] = sections[0][split:]

            # All uppercase => all last.
            else:
                parts['last'] = sections[0]

    # Done.
    return parts


def getnames(names):
    """Convert people names as surname, firstnames
    or surname, initials.

    :param names: a list of names
    :type names: list
    :returns: list -- Correctly formated names

    .. Note::

    This function is known to be too simple to handle properly
    the complex rules. We would like to enhance this in forthcoming releases.
    """
    tidynames = []
    for namestring in names:
        namestring = namestring.strip()
        if len(namestring) < 1:
            continue
        if ',' in namestring:
            namesplit = namestring.split(',', 1)
            last = namesplit[0].strip()
            firsts = [i.strip() for i in namesplit[1].split()]
        else:
            namesplit = namestring.split()
            last = namesplit.pop()
            firsts = [i.replace('.', '. ').strip() for i in namesplit]
        if last in ['jnr', 'jr', 'junior']:
            last = firsts.pop()
        for item in firsts:
            if item in ['ben', 'van', 'der', 'de', 'la', 'le']:
                last = firsts.pop() + ' ' + last
        tidynames.append(last + ", " + ' '.join(firsts))
    return tidynames


def author(record):
    """
    Split author field into a list of "Name, Surname".

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.

    """
    if "author" in record:
        if record["author"]:
            record["author"] = getnames([i.strip() for i in record["author"].replace('\n', ' ').split(" and ")])
        else:
            del record["author"]
    return record


def editor(record):
    """
    Turn the editor field into a dict composed of the original editor name
    and a editor id (without coma or blank).

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.

    """
    if "editor" in record:
        if record["editor"]:
            record["editor"] = getnames([i.strip() for i in record["editor"].replace('\n', ' ').split(" and ")])
            # convert editor to object
            record["editor"] = [{"name": i, "ID": i.replace(',', '').replace(' ', '').replace('.', '')} for i in record["editor"]]
        else:
            del record["editor"]
    return record


def page_double_hyphen(record):
    """
    Separate pages by a double hyphen (--).

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.

    """
    if "pages" in record:
        # hyphen, non-breaking hyphen, en dash, em dash, hyphen-minus, minus sign
        separators = [u'‐', u'‑', u'–', u'—', u'-', u'−']
        for separator in separators:
            if separator in record["pages"]:
                p = [i.strip().strip(separator) for i in record["pages"].split(separator)]
                record["pages"] = p[0] + '--' + p[-1]
    return record


def type(record):
    """
    Put the type into lower case.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.

    """
    if "type" in record:
        record["type"] = record["type"].lower()
    return record


def journal(record):
    """
    Turn the journal field into a dict composed of the original journal name
    and a journal id (without coma or blank).

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.

    """
    if "journal" in record:
        # switch journal to object
        if record["journal"]:
            record["journal"] = {"name": record["journal"], "ID": record["journal"].replace(',', '').replace(' ', '').replace('.', '')}

    return record


def keyword(record, sep=',|;'):
    """
    Split keyword field into a list.

    :param record: the record.
    :type record: dict
    :param sep: pattern used for the splitting regexp.
    :type record: string, optional
    :returns: dict -- the modified record.

    """
    if "keyword" in record:
        record["keyword"] = [i.strip() for i in re.split(sep, record["keyword"].replace('\n', ''))]

    return record


def link(record):
    """

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.

    """
    if "link" in record:
        links = [i.strip().replace("  ", " ") for i in record["link"].split('\n')]
        record['link'] = []
        for link in links:
            parts = link.split(" ")
            linkobj = {"url": parts[0]}
            if len(parts) > 1:
                linkobj["anchor"] = parts[1]
            if len(parts) > 2:
                linkobj["format"] = parts[2]
            if len(linkobj["url"]) > 0:
                record["link"].append(linkobj)

    return record


def doi(record):
    """

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.

    """
    if 'doi' in record:
        if 'link' not in record:
            record['link'] = []
        nodoi = True
        for item in record['link']:
            if 'doi' in item:
                nodoi = False
        if nodoi:
            link = record['doi']
            if link.startswith('10'):
                link = 'http://dx.doi.org/' + link
            record['link'].append({"url": link, "anchor": "doi"})
    return record


def convert_to_unicode(record):
    """
    Convert accent from latex to unicode style.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    for val in record:
        if isinstance(record[val], list):
            record[val] = [
                latex_to_unicode(x) for x in record[val]
            ]
        elif isinstance(record[val], dict):
            record[val] = {
                k: latex_to_unicode(v) for k, v in record[val].items()
            }
        else:
            record[val] = latex_to_unicode(record[val])
    return record


def homogenize_latex_encoding(record):
    """
    Homogenize the latex enconding style for bibtex

    This function is experimental.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    # First, we convert everything to unicode
    record = convert_to_unicode(record)
    # And then, we fall back
    for val in record:
        if val not in ('ID',):
            logger.debug('Apply string_to_latex to: %s', val)
            record[val] = string_to_latex(record[val])
            if val == 'title':
                logger.debug('Protect uppercase in title')
                logger.debug('Before: %s', record[val])
                record[val] = protect_uppercase(record[val])
                logger.debug('After: %s', record[val])
    return record


def add_plaintext_fields(record):
    """
    For each field in the record, add a `plain_` field containing the
    plaintext, stripped from braces and similar. See
    https://github.com/sciunto-org/python-bibtexparser/issues/116.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    def _strip_string(string):
        for stripped in ['{', '}']:
            string = string.replace(stripped, "")
        return string

    for key in list(record.keys()):
        plain_key = "plain_{}".format(key)
        record[plain_key] = record[key]

        if isinstance(record[plain_key], str):
            record[plain_key] = _strip_string(record[plain_key])
        elif isinstance(record[plain_key], dict):
            record[plain_key] = {
                subkey: _strip_string(value)
                for subkey, value in record[plain_key].items()
            }
        elif isinstance(record[plain_key], list):
            record[plain_key] = [
                _strip_string(value)
                for value in record[plain_key]
            ]

    return record
