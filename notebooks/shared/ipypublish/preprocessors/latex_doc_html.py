import logging
import os

import traitlets as traits
from nbconvert.preprocessors import Preprocessor
from nbformat.notebooknode import NotebookNode


class LatexDocHTML(Preprocessor):
    r""" processing of ipub metatags, specific to html

    - import embedded html files
    - add refmap key to references for {label:reference name} lookup
      e.g. {"fig:test":"fig. 1"}
    - add caption_prefix tag for floats with correct numbering/name
      e.g. cell.metadata.ipub.figure.caption_prefix = "Figure 1: "

    """

    metapath = traits.Unicode('', help="the path to the meta data").tag(config=True)
    filesfolder = traits.Unicode('', help="the folder to point towards").tag(config=True)
    src_name = traits.Unicode('src', help="for embedding, if reveal js slides use data-src (for lazy loading)").tag(
        config=True)

    @traits.validate('src_name')
    def _valid_value(self, proposal):
        if proposal['value'] not in ['src', 'data-src']:
            raise traits.TraitError('src_name must be src or src or data-src')
        return proposal['value']

    def __init__(self, *args, **kwargs):
        super(LatexDocHTML, self).__init__(*args, **kwargs)

    def resolve_path(self, fpath, filepath):
        """resolve a relative path, w.r.t. another filepath """
        if not os.path.isabs(fpath):
            fpath = os.path.join(os.path.dirname(str(filepath)), fpath)
            fpath = os.path.abspath(fpath)
        return fpath

    def embed_html(self, cell, path):
        """ a new cell, based on embedded html file
        """
        logging.info('embedding html in notebook from: {}'.format(path))

        height = int(cell.metadata.ipub.embed_html.get('height', 0.5) * 100)
        width = int(cell.metadata.ipub.embed_html.get('width', 0.5) * 100)
        embed_code = """
        <iframe style="display:block; margin: 0 auto; height:{height}vh; width:{width}vw; overflow:auto; resize:both" {src}="{path}" frameborder="0" allowfullscreen></iframe>
        """.format(src=self.src_name, path=path, height=height, width=width)

        # add to the exising output or create a new one
        if cell.outputs:
            cell.outputs[0]["data"]["text/html"] = embed_code
        else:
            cell.outputs.append(NotebookNode({"data": {"text/html": embed_code},
                                              "execution_count": 0,
                                              "metadata": {},
                                              "output_type": "execute_result"}))

        return cell

    def preprocess(self, nb, resources):

        logging.info('processing notebook for html output' +
                     ' in ipub metadata to: {}'.format(self.metapath))

        final_cells = []
        float_count = dict([('figure', 0), ('table', 0), ('code', 0), ('text', 0), ('error', 0)])
        for i, cell in enumerate(nb.cells):
            if hasattr(cell.metadata, 'ipub'):
                if hasattr(cell.metadata.ipub, 'embed_html'):
                    if hasattr(cell.metadata.ipub.embed_html, 'filepath'):
                        paths = [cell.metadata.ipub.embed_html.filepath]
                        if hasattr(cell.metadata.ipub.embed_html, 'other_files'):
                            assert isinstance(cell.metadata.ipub.embed_html.other_files, list)
                            paths += cell.metadata.ipub.embed_html.other_files
                        for j, path in enumerate(paths):
                            fpath = self.resolve_path(path, self.metapath)
                            if not os.path.exists(fpath):
                                logging.warning('file in embed html metadata does not exist'
                                                ': {}'.format(fpath))
                            else:
                                resources.setdefault("external_file_paths", [])
                                resources['external_file_paths'].append(fpath)
                                if j == 0:
                                    self.embed_html(cell, os.path.join(self.filesfolder, os.path.basename(fpath)))

                    elif hasattr(cell.metadata.ipub.embed_html, 'url'):
                        self.embed_html(cell, cell.metadata.ipub.embed_html.url)
                    else:
                        logging.warning('cell {} has no filepath or url key in its metadata.embed_html'.format(i))

                for floattype, floatabbr in [('figure', 'fig.'), ('table', 'tbl.'), ('code', 'code'),
                                             ('text', 'text'), ('error', 'error')]:
                    if floattype in cell.metadata.ipub:
                        if floattype != 'code' and not cell.get("outputs", []):
                            continue
                        float_count[floattype] += 1
                        if not isinstance(cell.metadata.ipub[floattype], dict):
                            continue
                        cell.metadata.ipub[floattype]['caption_prefix'] = '<b>{0} {1}:</b> '.format(
                            floattype.capitalize(), float_count[floattype])
                        if 'label' in cell.metadata.ipub[floattype]:
                            resources.setdefault('refmap', {})[
                                cell.metadata.ipub[floattype]['label']] = '{0} {1}'.format(floatabbr,
                                                                                           float_count[floattype])

            final_cells.append(cell)
        nb.cells = final_cells

        return nb, resources
