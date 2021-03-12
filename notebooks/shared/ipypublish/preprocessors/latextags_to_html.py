import logging
import re
import string

import bibtexparser
import traitlets as traits
from nbconvert.preprocessors import Preprocessor

# python 3 to 2 compatibility
try:
    basestring
except NameError:
    basestring = str


class DefaultFormatter(string.Formatter):
    def __init__(self, default=''):
        self.default = default

    def get_value(self, key, args, kwds):
        if isinstance(key, basestring):
            return kwds.get(key, self.default.format(key))
        else:
            Formatter.get_value(key, args, kwds)


class LatexTagsToHTML(Preprocessor):
    r""" a preprocessor to find latex tags (like \cite{abc} or \todo[color]{stuff}) and:
    1. attempt to process them into a html friendly format
    2. remove them entirely if this is not possible

    for \ref or \cref,  attempts to use resources.refmap to map labels to reference names
    for labels not found in resources.refmap
    the reference name is '<name> <number>', where;
    - <name> is either ref of, if labelbycolon is True and the label has a colon, all text before the colon
    - <number> iterate by order of first appearance of a particular label

    NB: should be applied after LatexDocHTML, if you want resources.refmap to be available

    Examples
    --------
    >>> from nbformat import NotebookNode
    >>> from jsonextended.utils import MockPath

    >>> processor = LatexTagsToHTML()

    >>> bibfile = MockPath(is_file=True,content='''
    ... @article{bibkey,
    ... title = {the title},
    ... doi = {10.1134/S0018143916050209},
    ... author = {Surname, A. Name},
    ... date = {2016-09-01},
    ... }
    ... ''')
    >>> resources = NotebookNode({'bibliopath':bibfile, 'refmap':{"label":"label_name"}})

    >>> cell = NotebookNode({
    ... "cell_type":"markdown",
    ... "metadata":{},
    ... "source":"test"
    ... })
    >>> nb = NotebookNode({"cells":[cell]})
    >>> nb, _ = processor.preprocess(nb,resources)
    >>> print(nb.cells[0].source)
    test

    >>> cell.source = "\\unknown{test}"
    >>> nb, _ = processor.preprocess(nb,resources)
    >>> print(nb.cells[0].source)
    <BLANKLINE>

    >>> cell.source = "\\ref{label}\\unknown{test}"
    >>> nb, _ = processor.preprocess(nb,resources)
    >>> print(nb.cells[0].source)
    <a href="{id_home_prefix}label">label_name</a>

    >>> cell.source = "\\label{test}"
    >>> nb, _ = processor.preprocess(nb,resources)
    >>> print(nb.cells[0].source)
    <a id="test" class="anchor-link" name="#test">&#182;</a>

    >>> cell.source = "\\cite{bibkey}"
    >>> nb, _ = processor.preprocess(nb,resources)
    >>> print(nb.cells[0].source)
    [<a href="https://doi.org/10.1134/S0018143916050209">Surname <em>et al</em>, 2016.</a>]

    >>> cell.source = "\\begin{equation}x=a+b\\end{equation}"
    >>> nb, _ = processor.preprocess(nb,resources)
    >>> print(nb.cells[0].source)
    \begin{equation}x=a+b\end{equation}

    """

    regex = traits.Unicode(r"\\(?:[^a-zA-Z]|[a-zA-Z]+[*=']?)(?:\[.*?\])?{.*?}",
                           help="the regex to identify latex tags").tag(config=True)
    bibformat = traits.Unicode("{author}, {year}",
                               help=r"the format to output \cite{} tags found in the bibliography").tag(config=True)
    labelbycolon = traits.Bool(True,
                               help=r'create reference label based on text before colon, e.g. \ref{fig:example} -> fig 1').tag(
        config=True)

    def __init__(self, *args, **kwargs):
        # a dictionary to keep track of references, so they each get a different number
        self.refs = {}
        # bibliography references
        self.bibdatabase = {}
        super(LatexTagsToHTML, self).__init__(*args, **kwargs)

    @staticmethod
    def read_bibliography(path):
        """ read a bibliography

        """
        logging.info('reading bibliopath: {}'.format(path))
        bibdatabase = {}
        if hasattr(path,'open'):
            with path.open() as bibtex_file:
                bibdatabase = bibtexparser.load(bibtex_file).entries_dict
        else:
            with open(path) as bibtex_file:
                bibdatabase = bibtexparser.load(bibtex_file).entries_dict

        return bibdatabase

    def rreplace(self, source, target, replacement, replacements=1):
        """replace in string, from right-to-left"""
        return replacement.join(source.rsplit(target, replacements))

    def process_bib_entry(self, entry):
        """work out the best way to represent the bib entry """

        # abbreviate a list of authors
        if 'author' in entry:
            authors = re.split(", | and ", entry['author'])
            if len(authors) > 1:
                author = authors[0] + ' <em>et al</em>'
            else:
                author = authors[0]
            entry['author'] = author

            # split up date into year, month, day
        if 'date' in entry:
            date = entry['date'].split('-')
            if len(date) == 3:
                entry['year'] = date[0]
                entry['month'] = date[1]
                entry['day'] = date[2]
            else:
                entry['year'] = date[0]

        text = DefaultFormatter().format(self.bibformat, **entry)

        if 'doi' in entry:
            return r'<a href="https://doi.org/{doi}">{text}</a>'.format(doi=entry['doi'], text=text)
        elif 'url' in entry:
            return r'<a href="{url}">{text}</a>'.format(url=entry['url'], text=text)
        elif 'link' in entry:
            return r'<a href="{url}">{text}</a>'.format(url=entry['link'], text=text)
        else:
            return text

    def replace_reflabel(self, name, resources):
        """ find a suitable html replacement for a reference label

        the links are left with a format hook in them: {id_home_prefix},
        so that an nbconvert filter can later replace it
        this is particularly useful for slides, which require a prefix #/<slide_number><label>
        """
        if 'refmap' in resources:
            if name in resources['refmap']:
                return r'<a href="{{id_home_prefix}}{0}">{1}</a>'.format(name, resources['refmap'][name])

        if self.labelbycolon:
            ref_name = name.split(':')[0] if ':' in name else 'ref'
        else:
            ref_name = 'ref'
        if not ref_name in self.refs:
            self.refs[ref_name] = {}
        refs = self.refs[ref_name]
        if name in refs:
            id = refs[name]
        else:
            id = len(refs) + 1
            refs[name] = id
        return r'<a href="{{id_home_prefix}}{0}">{1}. {2}</a>'.format(name, ref_name, id)

    def convert(self, source, resources):
        """ convert a a string with tags in

        Example
        -------

        >>> source = r'''
        ... References to \\cref{fig:example}, \\cref{tbl:example}, \\cref{eqn:example_sympy} and \\cref{code:example_mpl}.
        ...
        ... Referencing multiple items: \\cref{fig:example,fig:example_h,fig:example_v}.
        ...
        ... An unknown latex tag.\\unknown{zelenyak_molecular_2016}
        ... '''
        >>> processor = LatexTagsToHTML()
        >>> print(processor.convert(source,{}))
        <BLANKLINE>
        References to <a href="{id_home_prefix}fig:example">fig. 1</a>, <a href="{id_home_prefix}tbl:example">tbl. 1</a>, <a href="{id_home_prefix}eqn:example_sympy">eqn. 1</a> and <a href="{id_home_prefix}code:example_mpl">code. 1</a>.
        <BLANKLINE>
        Referencing multiple items: <a href="{id_home_prefix}fig:example">fig. 1</a>, <a href="{id_home_prefix}fig:example_h">fig. 2</a> and <a href="{id_home_prefix}fig:example_v">fig. 3</a>.
        <BLANKLINE>
        An unknown latex tag.
        <BLANKLINE>

        """
        new = source
        in_equation = False
        labels = []
        for tag in re.findall(self.regex, source):

            if tag.startswith('\\label'):
                link = r'<a id="{label}" class="anchor-link" name="#{label}">&#182;</a>'.format(label=tag[7:-1])
                if in_equation:
                    labels.append(link)
                    new = new.replace(tag, '')
                else:
                    new = new.replace(tag, link)

            elif tag.startswith('\\ref'):
                names = tag[5:-1].split(',')
                html = []
                for name in names:
                    html.append(self.replace_reflabel(name, resources))
                new = new.replace(tag, self.rreplace(', '.join(html), ',', ' and'))

            elif tag.startswith('\\cref'):
                names = tag[6:-1].split(',')
                html = []
                for name in names:
                    html.append(self.replace_reflabel(name, resources))
                new = new.replace(tag, self.rreplace(', '.join(html), ',', ' and'))

            elif tag.startswith('\\cite'):
                names = tag[6:-1].split(',')
                html = []
                for name in names:
                    if name in self.bibdatabase:
                        html.append(self.process_bib_entry(self.bibdatabase[name]))
                    else:
                        html.append('Unresolved citation: {}.'.format(name))
                new = new.replace(tag, '[' + ', '.join(html) + ']')

            elif any([tag.startswith('\\begin{{{0}}}'.format(env)) for env in
                      ['equation', 'equation*', 'align', 'align*', 'multline', 'multline*', 'gather', 'gather*']]):
                in_equation = True
            elif any([tag.startswith('\\end{{{0}}}'.format(env)) for env in
                      ['equation', 'equation*', 'align', 'align*', 'multline', 'multline*', 'gather', 'gather*']]):
                new += ' '.join(labels)
                labels = []
                in_equation = False
            elif any([tag.startswith('\\begin{{{0}}}'.format(env)) for env in
                      ['split']]):
                pass
            elif any([tag.startswith('\\end{{{0}}}'.format(env)) for env in
                      ['split']]):
                pass
            else:
                # new = new.replace(tag, '')
                pass # -- AZ
        return new

    def preprocess(self, nb, resources):

        logging.info('converting latex tags to html')
        if 'bibliopath' in resources:
            self.bibdatabase = self.read_bibliography(resources['bibliopath'])
        else:
            self.bibdatabase = {}

        for cell in nb.cells:

            if "ipub" in cell['metadata']:
                for key in cell['metadata']["ipub"]:
                    if not isinstance(cell['metadata']["ipub"][key], dict):
                        continue
                    if "caption" in cell['metadata']["ipub"][key]:
                        text = cell['metadata']["ipub"][key]["caption"]
                        cell['metadata']["ipub"][key]["caption"] = self.convert(text, resources)

            if not cell['cell_type'] == "markdown":
                continue
            cell['source'] = self.convert(cell['source'], resources)

        resources['refslide'] = {}
        return nb, resources
