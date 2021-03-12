import logging
import os

import traitlets as traits
from nbconvert.preprocessors import Preprocessor


class LatexDocLinks(Preprocessor):
    """ a preprocessor to resolve file paths in the ipub metadata section

    retrieve external file paths from metadata,
    resolve where they are, if the path is relative
    make sure that the link points to a single folder
    add 'external_file_paths' and 'bibliopath' (if present) to resources

    """

    metapath = traits.Unicode('', help="the path to the meta data").tag(config=True)
    filesfolder = traits.Unicode('', help="the folder to point towards").tag(config=True)

    def resolve_path(self, fpath, filepath):
        """resolve a relative path, w.r.t. another filepath """
        if not os.path.isabs(fpath):
            fpath = os.path.join(os.path.dirname(str(filepath)), fpath)
            fpath = os.path.abspath(fpath)
        return fpath

    def preprocess(self, nb, resources):

        logging.info('resolving external file paths' +
                     ' in ipub metadata to: {}'.format(self.metapath))
        external_files = []
        if hasattr(nb.metadata, 'ipub'):

            # if hasattr(nb.metadata.ipub, 'files'):
            #     mfiles = []
            #     for fpath in nb.metadata.ipub.files:
            #         fpath = self.resolve_path(fpath, self.metapath)
            #         if not os.path.exists(fpath):
            #             logging.warning('file in metadata does not exist'
            #                             ': {}'.format(fpath))
            #         else:
            #             external_files.append(fpath)
            #         mfiles.append(os.path.join(self.filesfolder, os.path.basename(fpath)))
            #
            #     nb.metadata.ipub.files = mfiles

            if hasattr(nb.metadata.ipub, 'bibliography'):
                bib = nb.metadata.ipub.bibliography
                bib = self.resolve_path(bib, self.metapath)
                if not os.path.exists(bib):
                    logging.warning('bib in metadata does not exist'
                                    ': {}'.format(bib))
                else:
                    external_files.append(bib)
                    resources['bibliopath'] = bib

                nb.metadata.ipub.bibliography = os.path.join(self.filesfolder,
                                                             os.path.basename(bib))

            if hasattr(nb.metadata.ipub, 'titlepage'):
                if hasattr(nb.metadata.ipub.titlepage, 'logo'):
                    logo = nb.metadata.ipub.titlepage.logo
                    logo = self.resolve_path(logo, self.metapath)
                    if not os.path.exists(logo):
                        logging.warning('logo in metadata does not exist'
                                        ': {}'.format(logo))
                    else:
                        external_files.append(logo)

                    nb.metadata.ipub.titlepage.logo = os.path.join(self.filesfolder,
                                                                   os.path.basename(logo))
        resources.setdefault("external_file_paths", [])
        resources['external_file_paths'] += external_files

        return nb, resources
