# Define the contents of this file as a package
__all__ = ["PrettyTable", "YouTubeVideo"]

# Setup loader such that workbooks can be imported directly
from . import import_notebooks

# Set fixed seed
from . import set_fixed_seed
set_fixed_seed.set_fixed_seed()

# Wrapper for YouTubeVideo
import IPython.display

class YouTubeVideo(IPython.display.YouTubeVideo):
    def __init__(self, video_id, **kwargs):
        super().__init__(video_id, width=640, height=360, **kwargs)