#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/404.html
# Last change: 2018-09-26 13:58:11+02:00
#
# This material is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International License
# (https://creativecommons.org/licenses/by-nc-sa/4.0/)


# # Oh no!  We are not ready yet!
# 
# We're sorry - this page does not exist (yet).  

if __name__ == "__main__":
    print('# Oh no!  We are not ready yet!')




# ## Finding Content
# 
# Most likely, you have been looking for material that is not yet written or not yet published.  Go to the [home page](__SITE_HTML__) or choose from this list of chapters:
# 
# <ol>
#                <__ALL_CHAPTERS_MENU__>
# </ol>

if __name__ == "__main__":
    print('\n## Finding Content')




# If you think this is an error, please [report an issue](__GITHUB_HTML__/issues/).

# ## Getting Informed About New Content
# 
# New chapters are coming out every week.  To get notified when a new chapter (or this one) comes out, <a href="https://twitter.com/FuzzingBook?ref_src=twsrc%5Etfw" data-show-count="false">follow us on Twitter</a>.
# 
# <a class="twitter-timeline" data-width="500" data-chrome="noheader nofooter noborders transparent" data-link-color="#A93226" data-align="center" href="https://twitter.com/FuzzingBook?ref_src=twsrc%5Etfw">News from @FuzzingBook</a> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

if __name__ == "__main__":
    print('\n## Getting Informed About New Content')




# ## Error Details

if __name__ == "__main__":
    print('\n## Error Details')




# import fuzzingbook_utils

class FourOhFourError(Exception):
    def __init__(self, value="404 - Page not Found"):
        self.value = value

    def __str__(self):
        return repr(self.value)

from ExpectError import ExpectError

with ExpectError():
    raise FourOhFourError
