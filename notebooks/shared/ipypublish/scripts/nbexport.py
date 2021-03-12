#!/usr/bin/env python
import logging

import nbconvert
from jinja2 import DictLoader
from traitlets.config import Config


def export_notebook(nb, format, config, template):
    """ exports a notebook in a particular format

    Parameters
    ----------
    nb: nbformat.notebooknode.NotebookNode
    format: str
        the nbconvert exporter class prefix ('Latex', 'HTML',...)
    config : dict
        configuration for the nbconvert exporter
    template : str
        the Jinja template for the conversion

    Returns
    -------
    export: tuple
        (body, resources)
    extension: str
        the file extension of the exported format (e.g. .tex)

    """
    jinja_template = DictLoader({'my_template': template})
    c = Config()
    for key, val in config.items():
        # TODO should probably not use exec, need to think of another way
        exec('c.{0} = val'.format(key)) in globals(), locals()

    if not hasattr(nbconvert, format + 'Exporter'):
        logging.error('the export format is not recognised: {}'.format(format))
        raise ValueError('the export format is not recognised: {}'.format(format))

    class MyExporter(getattr(nbconvert, format + 'Exporter')):
        """override the default template"""
        template_file = 'my_template'

    logging.info('running nbconvert')
    exporter = MyExporter(
        config=c,
        extra_loaders=[jinja_template])

    return exporter.from_notebook_node(nb), exporter.file_extension
