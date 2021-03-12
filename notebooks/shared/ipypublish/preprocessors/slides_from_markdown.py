import copy
import logging
import re

import traitlets as traits
from nbconvert.preprocessors import Preprocessor
from nbformat.notebooknode import NotebookNode


class FinalCells(object):
    """ a class that stores cells
    """

    def __init__(self, header_slide):
        self.cells = []
        if header_slide:
            self.horizontalbreak_after = 'horizontalbreak_after_plusvertical'
        else:
            self.horizontalbreak_after = 'horizontalbreak_after'

    def mkdcell(self, source, metadata, slidetype):
        meta = copy.deepcopy(metadata)
        meta.ipyslides = slidetype
        self.append(NotebookNode({"cell_type": "markdown",
                                  "source": '\n'.join(source),
                                  "metadata": meta}))

    def append(self, cell):
        last = self.last()
        if not last:
            pass
        elif cell.metadata.ipyslides == 'verticalbreak_after':
            pass  # last.metadata.ipyslides = 'verticalbreak_above'
        elif cell.metadata.ipyslides == self.horizontalbreak_after:
            # if last.metadata.ipyslides == 'before_header':
            #    last.metadata.ipyslides == 'between_headers'
            if not last.metadata.ipyslides == self.horizontalbreak_after:
                last.metadata.ipyslides = 'horizontalbreak_before'
            else:
                last.metadata.ipyslides = 'horizontalbreak_after_novertical'
        self.cells.append(cell)

    def first(self):
        for cell in self.cells:
            if cell.metadata.ipyslides not in ['skip', 'notes']:
                return cell
        return False

    def last(self):
        for cell in reversed(self.cells):
            if cell.metadata.ipyslides not in ['skip', 'notes']:
                return cell
        return False

    def finalize(self):
        if not self.first():
            return False
        if self.first().metadata.ipyslides == 'normal':
            self.first().metadata.ipyslides = 'first_cell'
        if self.last().metadata.ipyslides == 'normal':
            self.last().metadata.ipyslides = 'last_cell'
        return True


def is_header(line, max_level):
    """if max_level is 0 assumes all headers ok

    Examples
    --------
    >>> is_header("abc",0)
    False
    >>> is_header("#",0)
    False
    >>> is_header("# title",0)
    True
    >>> is_header("### title",3)
    True
    >>> is_header("### title",2)
    False

    """
    if max_level:
        return len(re.findall('^#{{1,{0}}} .+'.format(max_level), line)) > 0
    else:
        return len(re.findall('^#+ .+', line)) > 0


def header_level(line):
    """

    Examples
    --------
    >>> header_level('# title')
    1
    >>> header_level('### title')
    3
    """
    i = 0
    title = line + 'e'
    while title[0] == "#":
        i += 1
        title = title[1:]
    return i


def number_title(line, current_levels):
    """

    Examples
    --------
    >>> number_title("# title",[])
    ('# 1. title', [1])
    >>> number_title("## title",[])
    ('## 1.1. title', [1, 1])
    >>> number_title("# title",[1,1])
    ('# 2. title', [2])
    >>> number_title("## title",[2,1])
    ('## 2.2. title', [2, 2])
    >>> number_title("### title a#bc",[2])
    ('### 2.1.1. title a#bc', [2, 1, 1])
    >>> number_title("### title a#bc",[2,1,2,3])
    ('### 2.1.3. title a#bc', [2, 1, 3])
    """
    level = header_level(line)
    assert level > 0
    if len(current_levels) < level:
        while len(current_levels) < level:
            current_levels.append(1)
    else:
        current_levels = current_levels[:level]
        current_levels[-1] += 1
    hashes, title = line.split(' ', 1)
    numbers = '.'.join([str(i) for i in current_levels]) + '.'
    new = ' '.join([hashes, numbers, title])
    return new, current_levels


class MarkdownSlides(Preprocessor):
    """ a preprocessor to setup the notebook as an ipyslideshow,
    according to a set of rules

    - markdown cells containaing # headers are broken into individual cells
    - any cells where ipub.ignore=True is set to 'skip'
    - any code cells with no other ipub tags are set to 'skip'
    - any header level >= column_level starts a new column
    - else, any header level >= row_level starts a new row
    - if max_cells is not 0, then breaks to a new row after <max_cells> cells

    """

    column_level = traits.Integer(1, min=0, help='maximum header level for new columns (0 indicates no maximum)').tag(
        config=True)
    row_level = traits.Integer(0, min=0, help='maximum header level for new rows (0 indicates no maximum)').tag(
        config=True)
    header_slide = traits.Bool(False, help='if True, make the first header in a column appear on its own slide').tag(
        config=True)
    max_cells = traits.Integer(0, min=0, help='maximum number of nb cells per slide (0 indicates no maximum)').tag(
        config=True)
    autonumbering = traits.Bool(False, help='append section numbering to titles, e.g. 1.1.1 Title').tag(config=True)

    def preprocess(self, nb, resources):

        logging.info('creating slides based on markdown and existing slide tags')
        latexdoc_tags = ['code', 'error', 'table', 'equation', 'figure', 'text']
        # break up titles
        cells_in_slide = 0
        header_levels = []
        final_cells = FinalCells(self.header_slide)
        for i, cell in enumerate(nb.cells):

            # Make sure every cell has an ipub meta tag
            cell.metadata.ipub = cell.metadata.get('ipub', NotebookNode())

            if cell.metadata.ipub.get('ignore', False):
                cell.metadata.ipyslides = 'skip'
                final_cells.append(cell)
                continue

            if cell.metadata.ipub.get('slide', False) == 'notes':
                cell.metadata.ipyslides = 'notes'
                final_cells.append(cell)
                continue

            if not cell.cell_type == "markdown":
                # TODO this doesn't test if the data is actually available to be output
                if not any([cell.metadata.ipub.get(typ, False) for typ in latexdoc_tags]):
                    cell.metadata.ipyslides = 'skip'
                    final_cells.append(cell)
                    continue

                if cells_in_slide > self.max_cells and self.max_cells:
                    cell.metadata.ipyslides = 'verticalbreak_after'
                    cells_in_slide = 1
                elif cell.metadata.ipub.get('slide', False) == 'new':
                    cell.metadata.ipyslides = 'verticalbreak_after'
                    cells_in_slide = 1
                else:
                    cell.metadata.ipyslides = 'normal'
                    cells_in_slide += 1
                final_cells.append(cell)
                continue

            nonheader_lines = []
            for line in cell.source.split('\n'):

                if is_header(line, 0) and self.autonumbering:
                    line, header_levels = number_title(line, header_levels[:])

                if is_header(line, self.column_level):
                    if nonheader_lines and cell.metadata.ipub.get('slide', False):
                        if (cells_in_slide > self.max_cells and self.max_cells) or cell.metadata.ipub.slide == 'new':
                            final_cells.mkdcell(nonheader_lines, cell.metadata, 'verticalbreak_after')
                            cells_in_slide = 1
                        else:
                            cells_in_slide += 1
                            final_cells.mkdcell(nonheader_lines, cell.metadata, 'normal')
                        current_lines = []

                    if self.header_slide:
                        final_cells.mkdcell([line], cell.metadata, 'horizontalbreak_after_plusvertical')
                    else:
                        final_cells.mkdcell([line], cell.metadata, 'horizontalbreak_after')
                    cells_in_slide = 1

                elif is_header(line, self.row_level):
                    if nonheader_lines and cell.metadata.ipub.get('slide', False):
                        if (cells_in_slide > self.max_cells and self.max_cells) or cell.metadata.ipub.slide == 'new':
                            final_cells.mkdcell(nonheader_lines, cell.metadata, 'verticalbreak_after')
                            cells_in_slide = 1
                        else:
                            cells_in_slide += 1
                            final_cells.mkdcell(nonheader_lines, cell.metadata, 'normal')
                        current_lines = []

                    final_cells.mkdcell([line], cell.metadata, 'verticalbreak_after')
                    cells_in_slide = 1
                else:
                    nonheader_lines.append(line)

            if nonheader_lines and cell.metadata.ipub.get('slide', False):
                if (cells_in_slide > self.max_cells and self.max_cells) or cell.metadata.ipub.slide == 'new':
                    final_cells.mkdcell(nonheader_lines, cell.metadata, 'verticalbreak_after')
                    cells_in_slide = 1
                else:
                    cells_in_slide += 1
                    final_cells.mkdcell(nonheader_lines, cell.metadata, 'normal')

        if not final_cells.finalize():
            logging.warning('no cells available for slideshow')
        nb.cells = final_cells.cells

        return nb, resources
