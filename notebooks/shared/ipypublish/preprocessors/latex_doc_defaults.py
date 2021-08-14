import logging

import traitlets as traits
from nbconvert.preprocessors import Preprocessor
from nbformat.notebooknode import NotebookNode


def flatten(d, key_as_tuple=True, sep='.'):
    """ get nested dict as {key:val,...}, where key is tuple/string of all nested keys

    Parameters
    ----------
    d : dict
    key_as_tuple : bool
        whether keys are list of nested keys or delimited string of nested keys
    sep : str
        if key_as_tuple=False, delimiter for keys

    Examples
    --------

    >>> from pprint import pprint

    >>> d = {1:{"a":"A"},2:{"b":"B"}}
    >>> pprint(flatten(d))
    {(1, 'a'): 'A', (2, 'b'): 'B'}

    >>> d = {1:{"a":"A"},2:{"b":"B"}}
    >>> pprint(flatten(d,key_as_tuple=False))
    {'1.a': 'A', '2.b': 'B'}

    """

    def expand(key, value):
        if isinstance(value, dict):
            if key_as_tuple:
                return [(key + k, v) for k, v in flatten(value, key_as_tuple).items()]
            else:
                return [(str(key) + sep + k, v) for k, v in flatten(value, key_as_tuple).items()]
        else:
            return [(key, value)]

    if key_as_tuple:
        items = [item for k, v in d.items() for item in expand((k,), v)]
    else:
        items = [item for k, v in d.items() for item in expand(k, v)]

    return dict(items)


class MetaDefaults(Preprocessor):
    """ a preprocessor which enters default metadata tags
    into all cell metadata, without overriding any currently set

    """

    nb_defaults = traits.Dict(default_value={}, help='dict of notebook level defaults').tag(config=True)
    cell_defaults = traits.Dict(default_value={}, help='dict of cell level defaults').tag(config=True)
    overwrite = traits.Bool(False, help="whether existing values should be overwritten").tag(config=True)

    def preprocess(self, nb, resources):

        logging.info('adding ipub defaults to notebook')

        for keys, val in flatten(self.nb_defaults).items():
            dct = nb.metadata
            for key in keys[:-1]:
                if key not in dct:
                    dct[key] = NotebookNode({})
                dct = dct[key]
            if keys[-1] not in dct:
                dct[keys[-1]] = val
            elif self.overwrite:
                dct[keys[-1]] = val

        for cell in nb.cells:
            for keys, val in flatten(self.cell_defaults).items():
                dct = cell.metadata
                for key in keys[:-1]:
                    if key not in dct:
                        dct[key] = NotebookNode({})
                    dct = dct[key]
                if keys[-1] not in dct:
                    dct[keys[-1]] = val
                elif self.overwrite:
                    dct[keys[-1]] = val

        return nb, resources
