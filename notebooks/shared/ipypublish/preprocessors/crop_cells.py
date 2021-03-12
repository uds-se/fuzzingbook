import logging

import traitlets as traits
from nbconvert.preprocessors import Preprocessor


class CropCells(Preprocessor):
    """A preprocessor to crop the notebook cells from <start> to <end>"""

    start = traits.Integer(0, help="first cell of notebook to be converted").tag(config=True)
    end = traits.Integer(-1, help="last cell of notebook to be converted").tag(config=True)

    def preprocess(self, nb, resources):
        logging.info('preprocessing notebook: cropping cells {0} to {1}'.format(self.start, self.end))
        nb.cells = nb.cells[self.start:self.end]
        return nb, resources
