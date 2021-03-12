import glob
import imp
import inspect
import logging
import os
import uuid
import warnings

# py 2/3 compatibility
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
try:
    from importlib.machinery import SourceFileLoader
    from types import ModuleType


    def load_source(modname, fname):
        loader = SourceFileLoader(modname, fname)
        mod = ModuleType(loader.name)
        loader.exec_module(mod)
        return mod
except ImportError as err:
    load_source = lambda modname, fname: imp.load_source(modname, fname)

from ipypublish import export_plugins


def _get_module_path(module):
    """return a directory path to a module"""
    return pathlib.Path(os.path.dirname(os.path.abspath(inspect.getfile(module))))


def _get_modules(path):
    """ get modules from a directory

    Properties
    ----------
    path : str or path-like

    Returns
    -------
    modules : list of modules
    load_errors: list of str

    Examples
    --------
    >>> from jsonextended.utils import MockPath
    >>> mod1 = MockPath('mod1.py', is_file=True,
    ... content="name='modname1'")
    >>> dir = MockPath(structure=[mod1])
    >>> modules, errors = _get_modules(dir)
    >>> errors
    []
    >>> list(modules.keys())
    ['mod1']
    >>> modules['mod1'].name
    'modname1'

    """
    # get potential plugin python files
    if hasattr(path, 'glob'):
        pypaths = path.glob('*.py')
    else:
        pypaths = glob.glob(os.path.join(path, '*.py'))

    modules = {}
    load_errors = []
    for pypath in pypaths:
        # use uuid to ensure no conflicts in name space
        mod_name = str(uuid.uuid4())
        try:
            if hasattr(pypath, 'resolve'):
                # Make the path absolute, resolving any symlinks
                pypath = pypath.resolve()

            with warnings.catch_warnings(record=True) as w:
                warnings.filterwarnings("ignore", category=ImportWarning)

                # for MockPaths
                if hasattr(pypath, 'maketemp'):
                    with pypath.maketemp() as fpath:
                        module = load_source(mod_name, str(fpath))
                    pypath = pypath.name
                else:
                    module = load_source(mod_name, str(pypath))
            modules[os.path.splitext(os.path.basename(str(pypath)))[0]] = module
        except Exception as err:
            load_errors.append((str(pypath), 'Load Error: {}'.format(err)))
            continue

    return modules, load_errors


_plugins_dict = {}


def add_directory(path):
    """ add a directory of export plugin modules to the existing dict

    plugins must have: oformat, template and config attributes and a doc string

    Properties
    ----------
    path : str or path-like

    """
    modules, load_errors = _get_modules(path)
    for mod_name, mod in modules.items():
        try:
            descript = getattr(mod, '__doc__')
            oformat = getattr(mod, 'oformat')
            template = getattr(mod, 'template')
            config = getattr(mod, 'config')
        except AttributeError:
            continue
        _plugins_dict[mod_name] = {'descript': descript,
                                   'oformat': oformat,
                                   'template': template,
                                   'config': config}
    return load_errors


logging.debug('loading builtin plugins')

load_errors = add_directory(_get_module_path(export_plugins))
if load_errors:
    raise IOError(
        'errors in builtin plugins loading: {}'.format('\n'.join(['{0}: {1}'.format(a, b) for a, b in load_errors])))


def get():
    """ return export plugins
    """
    return _plugins_dict.copy()
