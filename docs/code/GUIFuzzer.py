#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Testing Graphical User Interfaces" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/GUIFuzzer.html
# Last change: 2022-01-25 22:48:41+01:00
#
# Copyright (c) 2021 CISPA Helmholtz Center for Information Security
# Copyright (c) 2018-2020 Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r'''
The Fuzzing Book - Testing Graphical User Interfaces

This file can be _executed_ as a script, running all experiments:

    $ python GUIFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.GUIFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/GUIFuzzer.html

This chapter demonstrates how to programmatically interact with user interfaces, using Selenium on Web browsers.  It provides an experimental  `GUICoverageFuzzer` class that automatically explores a user interface by systematically interacting with all available user interface elements.

The function `start_webdriver()` starts a headless Web browser in the background and returns a _GUI driver_ as handle for further communication.

>>> gui_driver = start_webdriver()

We let the browser open the URL of the server we want to investigate (in this case, the vulnerable server from [the chapter on Web fuzzing](WebFuzzer.ipynb)) and obtain a screen shot.

>>> gui_driver.get(httpd_url)
>>> Image(gui_driver.get_screenshot_as_png())
The `GUICoverageFuzzer` class explores the user interface and builds a _grammar_ that encodes all states as well as the user interactions required to move from one state to the next.  It is paired with a `GUIRunner` which interacts with the GUI driver.

>>> gui_fuzzer = GUICoverageFuzzer(gui_driver)
>>> gui_runner = GUIRunner(gui_driver)

The `explore_all()` method extracts all states and all transitions from a Web user interface.

>>> gui_fuzzer.explore_all(gui_runner)

The grammar embeds a finite state automation and is best visualized as such.

>>> fsm_diagram(gui_fuzzer.grammar)
The GUI Fuzzer `fuzz()` method produces sequences of interactions that follow paths through the finite state machine.  Since `GUICoverageFuzzer` is derived from `CoverageFuzzer` (see the [chapter on coverage-based grammar fuzzing](GrammarCoverageFuzzer.ipynb)), it automatically covers (a) as many transitions between states as well as (b) as many form elements as possible.  In our case, the first set of actions explores the transition via the "order form" link; the second set then goes until the "" state.

>>> gui_driver.get(httpd_url)
>>> actions = gui_fuzzer.fuzz()
>>> print(actions)
click('terms and conditions')
click('order form')
check('terms', False)
fill('email', 'S@qy')
fill('name', 'x')
fill('zip', '6')
fill('city', 'Cf')
submit('submit')
click('order form')
check('terms', False)
fill('email', 'L@U')
fill('name', 'G')
fill('zip', '5')
fill('city', 'w')
submit('submit')



These actions can be fed into the GUI runner, which will execute them on the given GUI driver.

>>> gui_driver.get(httpd_url)
>>> result, outcome = gui_runner.run(actions)
>>> Image(gui_driver.get_screenshot_as_png())
Further invocations of `fuzz()` will further cover the model – for instance, exploring the terms and conditions.

Internally, `GUIFuzzer` and `GUICoverageFuzzer` use a subclass `GUIGrammarMiner` which implements the analysis of the GUI and all its states. Subclassing `GUIGrammarMiner` allows to extend the interpretation of GUIs; the `GUIFuzzer` constructor allows to pass a miner via the `miner` keyword parameter.

A tool like `GUICoverageFuzzer` will provide "deep" exploration of user interfaces, even filling out forms to explore what is behind them. Keep in mind, though, that `GUICoverageFuzzer` is experimental: It only supports a subset of HTML form and link features, and does not take JavaScript into account.

For more details, source, and documentation, see
"The Fuzzing Book - Testing Graphical User Interfaces"
at https://www.fuzzingbook.org/html/GUIFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Testing Graphical User Interfaces
# =================================

if __name__ == '__main__':
    print('# Testing Graphical User Interfaces')



if __name__ == '__main__':
    from .bookutils import YouTubeVideo
    YouTubeVideo('cjqxi8NCC28')

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## Automated GUI Interaction
## -------------------------

if __name__ == '__main__':
    print('\n## Automated GUI Interaction')



### Our Web Server, Again

if __name__ == '__main__':
    print('\n### Our Web Server, Again')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

from typing import Set, FrozenSet, List, Optional, Tuple, Any

import os
import sys

if __name__ == '__main__':
    if 'CI' in os.environ:
        # Can't run this in our continuous environment,
        # since it can't run a headless Web browser
        sys.exit(0)

from .WebFuzzer import init_db, start_httpd, webbrowser, print_httpd_messages
from .WebFuzzer import print_url, ORDERS_DB

import html

if __name__ == '__main__':
    db = init_db()

if __name__ == '__main__':
    httpd_process, httpd_url = start_httpd()
    print_url(httpd_url)

if __name__ == '__main__':
    from IPython.display import display, Image

from .bookutils import HTML, rich_output

if __name__ == '__main__':
    HTML(webbrowser(httpd_url))

### Remote Control with Selenium

if __name__ == '__main__':
    print('\n### Remote Control with Selenium')



from selenium import webdriver

BROWSER = 'firefox'

import shutil

if __name__ == '__main__':
    if BROWSER == 'firefox':
        assert shutil.which('geckodriver') is not None, \
            "Please install 'geckodriver' executable " \
            "from https://github.com/mozilla/geckodriver/releases"

HEADLESS = True

def start_webdriver(browser=BROWSER, headless=HEADLESS, zoom=1.4):
    if browser == 'firefox':
        options = webdriver.FirefoxOptions()
    if browser == 'chrome':
        options = webdriver.ChromeOptions()

    if headless and browser == 'chrome':
        options.add_argument('headless')
    else:
        options.headless = headless

    # Start the browser, and obtain a _web driver_ object such that we can interact with it.
    if browser == 'firefox':
        # For firefox, set a higher resolution for our screenshots
        profile = webdriver.firefox.firefox_profile.FirefoxProfile()
        profile.set_preference("layout.css.devPixelsPerPx", repr(zoom))
        gui_driver = webdriver.Firefox(firefox_profile=profile, options=options)

        # We set the window size such that it fits our order form exactly;
        # this is useful for not wasting too much space when taking screen shots.
        gui_driver.set_window_size(700, 300)

    elif browser == 'chrome':
        gui_driver = webdriver.Chrome(options=options)
        gui_driver.set_window_size(700, 210 if headless else 340)

    return gui_driver

if __name__ == '__main__':
    gui_driver = start_webdriver(browser=BROWSER, headless=HEADLESS)

if __name__ == '__main__':
    gui_driver.get(httpd_url)

if __name__ == '__main__':
    print_httpd_messages()

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

### Filling out Forms

if __name__ == '__main__':
    print('\n### Filling out Forms')



if __name__ == '__main__':
    name = gui_driver.find_element_by_name("name")

if __name__ == '__main__':
    name.send_keys("Jane Doe")

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    email = gui_driver.find_element_by_name("email")
    email.send_keys("j.doe@example.com")

if __name__ == '__main__':
    city = gui_driver.find_element_by_name('city')
    city.send_keys("Seattle")

if __name__ == '__main__':
    zip = gui_driver.find_element_by_name('zip')
    zip.send_keys("98104")

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    terms = gui_driver.find_element_by_name('terms')
    terms.click()

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    submit = gui_driver.find_element_by_name('submit')
    submit.click()

if __name__ == '__main__':
    print_httpd_messages()

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

### Navigating

if __name__ == '__main__':
    print('\n### Navigating')



if __name__ == '__main__':
    gui_driver.back()

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    links = gui_driver.find_elements_by_tag_name("a")

if __name__ == '__main__':
    links[0].get_attribute('href')

if __name__ == '__main__':
    links[0].click()

if __name__ == '__main__':
    print_httpd_messages()

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    gui_driver.back()

if __name__ == '__main__':
    print_httpd_messages()

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

### Writing Test Cases

if __name__ == '__main__':
    print('\n### Writing Test Cases')



def test_successful_order(driver, url):
    name = "Walter White"
    email = "white@jpwynne.edu"
    city = "Albuquerque"
    zip_code = "87101"

    driver.get(url)
    driver.find_element_by_name("name").send_keys(name)
    driver.find_element_by_name("email").send_keys(email)
    driver.find_element_by_name('city').send_keys(city)
    driver.find_element_by_name('zip').send_keys(zip_code)
    driver.find_element_by_name('terms').click()
    driver.find_element_by_name('submit').click()

    title = driver.find_element_by_id('title')
    assert title is not None
    assert title.text.find("Thank you") >= 0

    confirmation = driver.find_element_by_id("confirmation")
    assert confirmation is not None

    assert confirmation.text.find(name) >= 0
    assert confirmation.text.find(email) >= 0
    assert confirmation.text.find(city) >= 0
    assert confirmation.text.find(zip_code) >= 0

    return True

if __name__ == '__main__':
    test_successful_order(gui_driver, httpd_url)

## Retrieving User Interface Actions
## ---------------------------------

if __name__ == '__main__':
    print('\n## Retrieving User Interface Actions')



### User Interface Elements

if __name__ == '__main__':
    print('\n### User Interface Elements')



if __name__ == '__main__':
    gui_driver.get(httpd_url)

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    ui_elements = gui_driver.find_elements_by_tag_name("input")

if __name__ == '__main__':
    for element in ui_elements:
        print("Name: %-10s | Type: %-10s | Text: %s" %
              (element.get_attribute('name'),
               element.get_attribute('type'),
               element.text))

if __name__ == '__main__':
    ui_elements = gui_driver.find_elements_by_tag_name("a")

if __name__ == '__main__':
    for element in ui_elements:
        print("Name: %-10s | Type: %-10s | Text: %s" %
              (element.get_attribute('name'),
               element.get_attribute('type'),
               element.text))

### User Interface Actions

if __name__ == '__main__':
    print('\n### User Interface Actions')



### Retrieving Actions

if __name__ == '__main__':
    print('\n### Retrieving Actions')



class GUIGrammarMiner:
    """Retrieve a grammar of possible GUI interaction sequences"""

    def __init__(self, driver, stay_on_host: bool = True) -> None:
        """Constructor.
        `driver` - a web driver as produced by Selenium.
        `stay_on_host` - if True (default), no not follow links to other hosts.
        """
        self.driver = driver
        self.stay_on_host = stay_on_host
        self.grammar: Grammar = {}

#### Excursion: Implementing Retrieving Actions

if __name__ == '__main__':
    print('\n#### Excursion: Implementing Retrieving Actions')



class GUIGrammarMiner(GUIGrammarMiner):
    def mine_state_actions(self) -> FrozenSet[str]:
        """Return a set of all possible actions on the current Web site.
        Can be overloaded in subclasses."""
        return frozenset(self.mine_input_element_actions()
                         | self.mine_button_element_actions()
                         | self.mine_a_element_actions())

    def mine_input_element_actions(self) -> Set[str]:
        return set()  # to be defined later

    def mine_button_element_actions(self) -> Set[str]:
        return set()  # to be defined later

    def mine_a_element_actions(self) -> Set[str]:
        return set()  # to be defined later

##### Input Element Actions

if __name__ == '__main__':
    print('\n##### Input Element Actions')



from selenium.common.exceptions import StaleElementReferenceException

class GUIGrammarMiner(GUIGrammarMiner):
    def mine_input_element_actions(self) -> Set[str]:
        """Determine all input actions on the current Web page"""

        actions = set()

        for elem in self.driver.find_elements_by_tag_name("input"):
            try:
                input_type = elem.get_attribute("type")
                input_name = elem.get_attribute("name")
                if input_name is None:
                    input_name = elem.text

                if input_type in ["checkbox", "radio"]:
                    actions.add("check('%s', <boolean>)" % html.escape(input_name))
                elif input_type in ["text", "number", "email", "password"]:
                    actions.add("fill('%s', '<%s>')" % (html.escape(input_name), html.escape(input_type)))
                elif input_type in ["button", "submit"]:
                    actions.add("submit('%s')" % html.escape(input_name))
                elif input_type in ["hidden"]:
                    pass
                else:
                    # TODO: Handle more types here
                    actions.add("fill('%s', <%s>)" % (html.escape(input_name), html.escape(input_type)))
            except StaleElementReferenceException:
                pass

        return actions

if __name__ == '__main__':
    gui_grammar_miner = GUIGrammarMiner(gui_driver)
    gui_grammar_miner.mine_input_element_actions()

##### Button Element Actions

if __name__ == '__main__':
    print('\n##### Button Element Actions')



class GUIGrammarMiner(GUIGrammarMiner):
    def mine_button_element_actions(self) -> Set[str]:
        """Determine all button actions on the current Web page"""

        actions = set()

        for elem in self.driver.find_elements_by_tag_name("button"):
            try:
                button_type = elem.get_attribute("type")
                button_name = elem.get_attribute("name")
                if button_name is None:
                    button_name = elem.text
                if button_type == "submit":
                    actions.add("submit('%s')" % html.escape(button_name))
                elif button_type != "reset":
                    actions.add("click('%s')" % html.escape(button_name))
            except StaleElementReferenceException:
                pass

        return actions

if __name__ == '__main__':
    gui_grammar_miner = GUIGrammarMiner(gui_driver)
    gui_grammar_miner.mine_button_element_actions()

##### Link Element Actions

if __name__ == '__main__':
    print('\n##### Link Element Actions')



from urllib.parse import urljoin, urlsplit

class GUIGrammarMiner(GUIGrammarMiner):
    def mine_a_element_actions(self) -> Set[str]:
        """Determine all link actions on the current Web page"""

        actions = set()

        for elem in self.driver.find_elements_by_tag_name("a"):
            try:
                a_href = elem.get_attribute("href")
                if a_href is not None:
                    if self.follow_link(a_href):
                        actions.add("click('%s')" % html.escape(elem.text))
                    else:
                        actions.add("ignore('%s')" % html.escape(elem.text))
            except StaleElementReferenceException:
                pass

        return actions

class GUIGrammarMiner(GUIGrammarMiner):
    def follow_link(self, link: str) -> bool:
        """Return True iff we are allowed to follow the `link` URL"""

        if not self.stay_on_host:
            return True

        current_url = self.driver.current_url
        target_url = urljoin(current_url, link)
        return urlsplit(current_url).hostname == urlsplit(target_url).hostname

if __name__ == '__main__':
    gui_grammar_miner = GUIGrammarMiner(gui_driver)

if __name__ == '__main__':
    gui_grammar_miner.follow_link("ftp://foo.bar/")

if __name__ == '__main__':
    gui_grammar_miner.follow_link("https://127.0.0.1/")

if __name__ == '__main__':
    gui_grammar_miner = GUIGrammarMiner(gui_driver)
    gui_grammar_miner.mine_a_element_actions()

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    gui_grammar_miner = GUIGrammarMiner(gui_driver)
    gui_grammar_miner.mine_state_actions()

## Models for User Interfaces
## --------------------------

if __name__ == '__main__':
    print('\n## Models for User Interfaces')



### User Interfaces as Finite State Machines

if __name__ == '__main__':
    print('\n### User Interfaces as Finite State Machines')



from graphviz import Digraph

from .GrammarFuzzer import dot_escape

if __name__ == '__main__':
    dot = Digraph(comment="Finite State Machine")
    dot.node(dot_escape('<start>'))
    dot.edge(dot_escape('<start>'),
             dot_escape('<Order Form>'))
    dot.edge(dot_escape('<Order Form>'),
             dot_escape('<Terms and Conditions>'), "click('Terms and conditions')")
    dot.edge(dot_escape('<Order Form>'),
             dot_escape('<Thank You>'), r"fill(...)\lsubmit('submit')")
    dot.edge(dot_escape('<Terms and Conditions>'),
             dot_escape('<Order Form>'), "click('order form')")
    dot.edge(dot_escape('<Thank You>'),
             dot_escape('<Order Form>'), "click('order form')")
    display(dot)

### State Machines as Grammars

if __name__ == '__main__':
    print('\n### State Machines as Grammars')



### Retrieving State Grammars

if __name__ == '__main__':
    print('\n### Retrieving State Grammars')



#### Excursion: Implementing Extracting State Grammars

if __name__ == '__main__':
    print('\n#### Excursion: Implementing Extracting State Grammars')



from .Grammars import new_symbol

from .Grammars import nonterminals, START_SYMBOL
from .Grammars import extend_grammar, unreachable_nonterminals, crange, srange
from .Grammars import syntax_diagram, is_valid_grammar, Grammar

class GUIGrammarMiner(GUIGrammarMiner):
    START_STATE = "<state>"
    UNEXPLORED_STATE = "<unexplored>"
    FINAL_STATE = "<end>"

    GUI_GRAMMAR: Grammar = ({
        START_SYMBOL: [START_STATE],
        UNEXPLORED_STATE: [""],
        FINAL_STATE: [""],

        "<text>": ["<string>"],
        "<string>": ["<character>", "<string><character>"],
        "<character>": ["<letter>", "<digit>", "<special>"],
        "<letter>": crange('a', 'z') + crange('A', 'Z'),

        "<number>": ["<digits>"],
        "<digits>": ["<digit>", "<digits><digit>"],
        "<digit>": crange('0', '9'),

        "<special>": srange(". !"),

        "<email>": ["<letters>@<letters>"],
        "<letters>": ["<letter>", "<letters><letter>"],

        "<boolean>": ["True", "False"],

        # Use a fixed password in case we need to repeat it
        "<password>": ["abcABC.123"],

        "<hidden>": ["<string>"],
    })

if __name__ == '__main__':
    syntax_diagram(GUIGrammarMiner.GUI_GRAMMAR)

class GUIGrammarMiner(GUIGrammarMiner):
    def new_state_symbol(self, grammar: Grammar) -> str:
        """Return a new symbol for some state in `grammar`"""
        return new_symbol(grammar, self.START_STATE)

    def mine_state_grammar(self, grammar: Grammar = {},
                           state_symbol: str = None) -> Grammar:
        """Return a state grammar for the actions on the current Web site.
        Can be overloaded in subclasses."""

        grammar = extend_grammar(self.GUI_GRAMMAR, grammar)  # type: ignore

        if state_symbol is None:
            state_symbol = self.new_state_symbol(grammar)
            grammar[state_symbol] = []

        alternatives = []
        form = ""
        submit = None

        for action in self.mine_state_actions():
            if action.startswith("submit"):
                submit = action

            elif action.startswith("click"):
                link_target = self.new_state_symbol(grammar)
                grammar[link_target] = [self.UNEXPLORED_STATE]
                alternatives.append(action + '\n' + link_target)

            elif action.startswith("ignore"):
                pass

            else:  # fill(), check() actions
                if len(form) > 0:
                    form += '\n'
                form += action

        if submit is not None:
            if len(form) > 0:
                form += '\n'
            form += submit

        if len(form) > 0:
            form_target = self.new_state_symbol(grammar)
            grammar[form_target] = [self.UNEXPLORED_STATE]
            alternatives.append(form + '\n' + form_target)

        alternatives += [self.FINAL_STATE]

        grammar[state_symbol] = alternatives  # type: ignore

        # Remove unused parts
        for nonterminal in unreachable_nonterminals(grammar):
            del grammar[nonterminal]

        assert is_valid_grammar(grammar)

        return grammar

from collections import deque

from .bookutils import unicode_escape

def fsm_diagram(grammar: Grammar, start_symbol: str = START_SYMBOL) -> Any:
    """Produce a FSM diagram for the state grammar `grammar`.
    `start_symbol` - the start symbol (default: START_SYMBOL)"""

    from graphviz import Digraph
    from IPython.display import display

    def left_align(label: str) -> str:
        """Render `label` as left-aligned in dot"""
        return dot_escape(label.replace('\n', r'\l')).replace(r'\\l', '\\l')

    dot = Digraph(comment="Grammar as Finite State Machine")

    symbols = deque([start_symbol])
    symbols_seen = set()

    while len(symbols) > 0:
        symbol = symbols.popleft()
        symbols_seen.add(symbol)
        dot.node(symbol, dot_escape(unicode_escape(symbol)))

        for expansion in grammar[symbol]:
            assert type(expansion) == str  # no opts() here

            nts = nonterminals(expansion)
            if len(nts) > 0:
                target_symbol = nts[-1]
                if target_symbol not in symbols_seen:
                    symbols.append(target_symbol)

                label = expansion.replace(target_symbol, '')
                dot.edge(symbol, target_symbol, left_align(unicode_escape(label)))

    return display(dot)

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    gui_grammar_miner = GUIGrammarMiner(gui_driver)
    state_grammar = gui_grammar_miner.mine_state_grammar()

if __name__ == '__main__':
    state_grammar

if __name__ == '__main__':
    fsm_diagram(state_grammar)

if __name__ == '__main__':
    state_grammar[GUIGrammarMiner.START_STATE]

if __name__ == '__main__':
    state_grammar['<state-1>']

if __name__ == '__main__':
    state_grammar['<state-2>']

if __name__ == '__main__':
    state_grammar['<unexplored>']

from .GrammarFuzzer import GrammarFuzzer

if __name__ == '__main__':
    gui_fuzzer = GrammarFuzzer(state_grammar)
    while True:
        action = gui_fuzzer.fuzz()
        if action.find('submit(') > 0:
            break
    print(action)

### Executing User Interface Actions

if __name__ == '__main__':
    print('\n### Executing User Interface Actions')



from .Fuzzer import Runner

class GUIRunner(Runner):
    """Execute the actions in a given action string"""

    def __init__(self, driver) -> None:
        """Constructor. `driver` is a Selenium Web driver"""
        self.driver = driver

#### Excursion: Implementing Executing UI Actions

if __name__ == '__main__':
    print('\n#### Excursion: Implementing Executing UI Actions')



class GUIRunner(GUIRunner):
    def run(self, inp: str) -> Tuple[str, str]:
        """Execute the action string `inp` on the current Web site.
        Return a pair (`inp`, `outcome`)."""

        def fill(name, value):
            self.do_fill(html.unescape(name), html.unescape(value))

        def check(name, state):
            self.do_check(html.unescape(name), state)

        def submit(name):
            self.do_submit(html.unescape(name))

        def click(name):
            self.do_click(html.unescape(name))

        exec(inp, {'__builtins__': {}},
                  {
                      'fill': fill,
                      'check': check,
                      'submit': submit,
                      'click': click,
                  })

        return inp, self.PASS

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException

class GUIRunner(GUIRunner):
    def find_element(self, name: str) -> Any:
        """Search for an element named `name` on the current Web site.
        Matches can occur by name or by link text."""

        try:
            return self.driver.find_element_by_name(name)
        except NoSuchElementException:
            return self.driver.find_element_by_link_text(name)

from selenium.webdriver.support.ui import WebDriverWait

class GUIRunner(GUIRunner):
    # Delays (in seconds)
    DELAY_AFTER_FILL = 0.1
    DELAY_AFTER_CHECK = 0.1
    DELAY_AFTER_SUBMIT = 1
    DELAY_AFTER_CLICK = 1

class GUIRunner(GUIRunner):
    def do_fill(self, name: str, value: str) -> None:
        """Fill the text element `name` with `value`"""

        element = self.find_element(name)
        element.send_keys(value)
        WebDriverWait(self.driver, self.DELAY_AFTER_FILL)

class GUIRunner(GUIRunner):
    def do_check(self, name: str, state: bool) -> None:
        """Set the check element `name` to `state`"""

        element = self.find_element(name)
        if bool(state) != bool(element.is_selected()):
            element.click()
        WebDriverWait(self.driver, self.DELAY_AFTER_CHECK)

class GUIRunner(GUIRunner):
    def do_submit(self, name: str) -> None:
        """Click on the submit element `name`"""

        element = self.find_element(name)
        element.click()
        WebDriverWait(self.driver, self.DELAY_AFTER_SUBMIT)

class GUIRunner(GUIRunner):
    def do_click(self, name: str) -> None:
        """Click on the element `name`"""

        element = self.find_element(name)
        element.click()
        WebDriverWait(self.driver, self.DELAY_AFTER_CLICK)

#### End of Excursion

if __name__ == '__main__':
    print('\n#### End of Excursion')



if __name__ == '__main__':
    gui_driver.get(httpd_url)

if __name__ == '__main__':
    gui_runner = GUIRunner(gui_driver)

if __name__ == '__main__':
    gui_runner.run("fill('name', 'Walter White')")

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    gui_runner.run("submit('submit')")

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    gui_driver.get(httpd_url)

if __name__ == '__main__':
    gui_fuzzer = GrammarFuzzer(state_grammar)

if __name__ == '__main__':
    while True:
        action = gui_fuzzer.fuzz()
        if action.find('submit(') > 0:
            break

if __name__ == '__main__':
    print(action)

if __name__ == '__main__':
    gui_runner.run(action)

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

## Exploring User Interfaces
## -------------------------

if __name__ == '__main__':
    print('\n## Exploring User Interfaces')



### Excursion: Implementing GUIFuzzer

if __name__ == '__main__':
    print('\n### Excursion: Implementing GUIFuzzer')



from .Grammars import is_nonterminal

from .GrammarFuzzer import GrammarFuzzer

class GUIFuzzer(GrammarFuzzer):
    """A fuzzer for GUIs, using Selenium."""

    def __init__(self, driver, *,
                 miner: Optional[GUIGrammarMiner] = None,
                 stay_on_host: bool = True,
                 log_gui_exploration: bool = False,
                 disp_gui_exploration: bool = False,
                 **kwargs) -> None:
        """Constructor.
        `driver` - the Selenium driver to use.
        `miner` - the miner to use (default: `GUIGrammarMiner(driver)`)
        `stay_on_host` - if True (default), do not explore external links.
        `log_gui_exploration` - if set, print out exploration steps.
        `disp_gui_exploration` - if set, display screenshot of current Web page
            as well as FSM diagrams during exploration.
        Other keyword arguments are passed to the `GrammarFuzzer` superclass.
        """

        self.driver = driver

        if miner is None:
            miner = GUIGrammarMiner(driver)

        self.miner = miner
        self.stay_on_host = True
        self.log_gui_exploration = log_gui_exploration
        self.disp_gui_exploration = disp_gui_exploration
        self.initial_url = driver.current_url

        self.states_seen = {}  # Maps states to symbols
        self.state_symbol = self.miner.START_STATE
        self.state: FrozenSet[str] = self.miner.mine_state_actions()
        self.states_seen[self.state] = self.state_symbol

        grammar = self.miner.mine_state_grammar()
        super().__init__(grammar, **kwargs)

if __name__ == '__main__':
    gui_driver.get(httpd_url)

if __name__ == '__main__':
    gui_fuzzer = GUIFuzzer(gui_driver)
    gui_fuzzer.state_symbol

if __name__ == '__main__':
    gui_fuzzer.state

if __name__ == '__main__':
    gui_fuzzer.states_seen[gui_fuzzer.state]

class GUIFuzzer(GUIFuzzer):
    def restart(self) -> None:
        """Get back to original URL"""

        self.driver.get(self.initial_url)
        self.state = frozenset(self.miner.START_STATE)

if __name__ == '__main__':
    while True:
        action = gui_fuzzer.fuzz()
        if action.find('click(') >= 0:
            break

from .GrammarFuzzer import display_tree, DerivationTree

if __name__ == '__main__':
    tree = gui_fuzzer.derivation_tree
    display_tree(tree)

class GUIFuzzer(GUIFuzzer):
    def fsm_path(self, tree: DerivationTree) -> List[str]:
        """Return sequence of state symbols."""

        (node, children) = tree
        if node == self.miner.UNEXPLORED_STATE:
            return []
        elif children is None or len(children) == 0:
            return [node]
        else:
            return [node] + self.fsm_path(children[-1])

if __name__ == '__main__':
    gui_fuzzer = GUIFuzzer(gui_driver)
    gui_fuzzer.fsm_path(tree)

class GUIFuzzer(GUIFuzzer):
    def fsm_last_state_symbol(self, tree: DerivationTree) -> str:
        """Return current (expected) state symbol"""

        for state in reversed(self.fsm_path(tree)):
            if is_nonterminal(state):
                return state

        assert False

if __name__ == '__main__':
    gui_fuzzer = GUIFuzzer(gui_driver)
    gui_fuzzer.fsm_last_state_symbol(tree)

class GUIFuzzer(GUIFuzzer):
    def run(self, runner: GUIRunner) -> Tuple[str, str]:  # type: ignore
        """Run the fuzzer on the given GUIRunner `runner`."""
        assert isinstance(runner, GUIRunner)

        self.restart()
        action = self.fuzz()
        self.state_symbol = self.fsm_last_state_symbol(self.derivation_tree)

        if self.log_gui_exploration:
            print("Action", action.strip(), "->", self.state_symbol)

        result, outcome = runner.run(action)

        if self.state_symbol != self.miner.FINAL_STATE:
            self.update_state()

        return self.state_symbol, outcome

class GUIFuzzer(GUIFuzzer):
    def update_state(self) -> None:
        """Determine current state from current Web page"""

        if self.disp_gui_exploration:
            display(Image(self.driver.get_screenshot_as_png()))

        self.state = self.miner.mine_state_actions()
        if self.state not in self.states_seen:
            self.states_seen[self.state] = self.state_symbol
            self.update_new_state()
        else:
            self.update_existing_state()

class GUIFuzzer(GUIFuzzer):
    def set_grammar(self, new_grammar: Grammar) -> None:
        """Set grammar to `new_grammar`."""

        self.grammar = new_grammar

        if self.disp_gui_exploration and rich_output():
            display(fsm_diagram(self.grammar))

class GUIFuzzer(GUIFuzzer):
    def update_new_state(self) -> None:
        """Found new state; extend grammar accordingly"""

        if self.log_gui_exploration:
            print("In new state", unicode_escape(self.state_symbol),
                                  unicode_escape(repr(self.state)))

        state_grammar = self.miner.mine_state_grammar(grammar=self.grammar, 
                                                      state_symbol=self.state_symbol)
        del state_grammar[START_SYMBOL]
        del state_grammar[self.miner.START_STATE]
        self.set_grammar(extend_grammar(self.grammar, state_grammar))

    def update_existing_state(self) -> None:
        pass  # See below

from .Grammars import exp_string, exp_opts

def replace_symbol(grammar: Grammar, 
                   old_symbol: str, new_symbol: str) -> Grammar:
    """Return a grammar in which all occurrences of `old_symbol` are replaced by `new_symbol`"""

    new_grammar: Grammar = {}

    for symbol in grammar:
        new_expansions = []
        for expansion in grammar[symbol]:
            new_expansion_string = exp_string(expansion).replace(old_symbol, new_symbol)
            if len(exp_opts(expansion)) > 0:
                new_expansion = (new_expansion_string, exp_opts(expansion))
            else:
                new_expansion = new_expansion_string  # type: ignore
            new_expansions.append(new_expansion)

        new_grammar[symbol] = new_expansions  # type: ignore

    # Remove unused parts
    for nonterminal in unreachable_nonterminals(new_grammar):
        del new_grammar[nonterminal]

    return new_grammar

class GUIFuzzer(GUIFuzzer):
    def update_existing_state(self) -> None:
        """Update actions of existing state"""

        if self.log_gui_exploration:
            print("In existing state", self.states_seen[self.state])

        if self.state_symbol != self.states_seen[self.state]:
            if self.log_gui_exploration:
                print("Replacing expected state %s by %s" %
                      (self.state_symbol, self.states_seen[self.state]))

            new_grammar = replace_symbol(self.grammar, self.state_symbol, 
                                         self.states_seen[self.state])
            self.state_symbol = self.states_seen[self.state]
            self.set_grammar(new_grammar)

### End of Excursion

if __name__ == '__main__':
    print('\n### End of Excursion')



if __name__ == '__main__':
    gui_driver.get(httpd_url)

if __name__ == '__main__':
    gui_fuzzer = GUIFuzzer(gui_driver, log_gui_exploration=True, disp_gui_exploration=True)

if __name__ == '__main__':
    gui_fuzzer.run(gui_runner)

if __name__ == '__main__':
    gui_fuzzer.run(gui_runner)

if __name__ == '__main__':
    gui_fuzzer.run(gui_runner)

## Covering States
## ---------------

if __name__ == '__main__':
    print('\n## Covering States')



from .GrammarCoverageFuzzer import GrammarCoverageFuzzer

from .bookutils import inheritance_conflicts

if __name__ == '__main__':
    inheritance_conflicts(GUIFuzzer, GrammarCoverageFuzzer)

class GUICoverageFuzzer(GUIFuzzer, GrammarCoverageFuzzer):
    """Systematically explore all states of the current Web page"""

    def __init__(self, *args, **kwargs):
        """Constructor. All args are passed to the `GUIFuzzer` superclass."""
        GUIFuzzer.__init__(self, *args, **kwargs)
        self.reset_coverage()

class GUICoverageFuzzer(GUICoverageFuzzer):
    def explore_all(self, runner: GUIRunner, max_actions=100) -> None:
        """Explore all states of the GUI, up to `max_actions` (default 100)."""

        actions = 0
        while (self.miner.UNEXPLORED_STATE in self.grammar and 
               actions < max_actions):
            actions += 1
            if self.log_gui_exploration:
                print("Run #" + repr(actions))
            try:
                self.run(runner)
            except ElementClickInterceptedException:
                pass
            except ElementNotInteractableException:
                pass
            except NoSuchElementException:
                pass

if __name__ == '__main__':
    gui_driver.get(httpd_url)

if __name__ == '__main__':
    gui_fuzzer = GUICoverageFuzzer(gui_driver)

if __name__ == '__main__':
    gui_fuzzer.explore_all(gui_runner)

if __name__ == '__main__':
    fsm_diagram(gui_fuzzer.grammar)

if __name__ == '__main__':
    gui_fuzzer.covered_expansions

if __name__ == '__main__':
    gui_fuzzer.missing_expansion_coverage()

## Exploring Large Sites
## ---------------------

if __name__ == '__main__':
    print('\n## Exploring Large Sites')



if __name__ == '__main__':
    gui_driver.get("https://www.fuzzingbook.org/html/Fuzzer.html")

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    book_runner = GUIRunner(gui_driver)

if __name__ == '__main__':
    book_fuzzer = GUICoverageFuzzer(gui_driver, log_gui_exploration=True)  # , disp_gui_exploration=True)

ACTIONS = 5

if __name__ == '__main__':
    book_fuzzer.explore_all(book_runner, max_actions=ACTIONS)

if __name__ == '__main__':
    fsm_diagram(book_fuzzer.grammar)

if __name__ == '__main__':
    gui_driver.quit()

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



if __name__ == '__main__':
    gui_driver = start_webdriver()

if __name__ == '__main__':
    gui_driver.get(httpd_url)
    Image(gui_driver.get_screenshot_as_png())

if __name__ == '__main__':
    gui_fuzzer = GUICoverageFuzzer(gui_driver)

if __name__ == '__main__':
    gui_runner = GUIRunner(gui_driver)

if __name__ == '__main__':
    gui_fuzzer.explore_all(gui_runner)

if __name__ == '__main__':
    fsm_diagram(gui_fuzzer.grammar)

if __name__ == '__main__':
    gui_driver.get(httpd_url)
    actions = gui_fuzzer.fuzz()
    print(actions)

if __name__ == '__main__':
    gui_driver.get(httpd_url)
    result, outcome = gui_runner.run(actions)

if __name__ == '__main__':
    Image(gui_driver.get_screenshot_as_png())

from .ClassDiagram import display_class_hierarchy
from .Fuzzer import Fuzzer, Runner
from .Grammars import Grammar, Expansion
from .GrammarFuzzer import GrammarFuzzer, DerivationTree

if __name__ == '__main__':
    display_class_hierarchy([GUIFuzzer, GUICoverageFuzzer,
                             GUIRunner, GUIGrammarMiner],
                            public_methods=[
                                Fuzzer.__init__,
                                Fuzzer.fuzz,
                                Fuzzer.run,
                                Fuzzer.runs,
                                Runner.__init__,
                                Runner.run,
                                GUIRunner.__init__,
                                GUIRunner.run,
                                GrammarFuzzer.__init__,
                                GrammarFuzzer.fuzz,
                                GrammarFuzzer.fuzz_tree,
                                GUIFuzzer.__init__,
                                GUIFuzzer.restart,
                                GUIFuzzer.run,
                                GUIGrammarMiner.__init__,
                                GrammarCoverageFuzzer.__init__,
                                GUICoverageFuzzer.__init__,
                                GUICoverageFuzzer.explore_all,
                            ],
                            types={
                                'DerivationTree': DerivationTree,
                                'Expansion': Expansion,
                                'Grammar': Grammar
                            },
                            project='fuzzingbook')

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



if __name__ == '__main__':
    httpd_process.terminate()

if __name__ == '__main__':
    gui_driver.quit()

import os

if __name__ == '__main__':
    for temp_file in [ORDERS_DB, "geckodriver.log", "ghostdriver.log"]:
        if os.path.exists(temp_file):
            os.remove(temp_file)

## Next Steps
## ----------

if __name__ == '__main__':
    print('\n## Next Steps')



## Background
## ----------

if __name__ == '__main__':
    print('\n## Background')



## Exercises
## ---------

if __name__ == '__main__':
    print('\n## Exercises')



### Exercise 1: Stay in Local State

if __name__ == '__main__':
    print('\n### Exercise 1: Stay in Local State')



### Exercise 2: Going Back

if __name__ == '__main__':
    print('\n### Exercise 2: Going Back')



### Exercise 3: Avoiding Bad Form Values

if __name__ == '__main__':
    print('\n### Exercise 3: Avoiding Bad Form Values')



### Exercise 4: Saving Form Values

if __name__ == '__main__':
    print('\n### Exercise 4: Saving Form Values')



### Exercise 5: Same Names, Same States

if __name__ == '__main__':
    print('\n### Exercise 5: Same Names, Same States')



### Exercise 6: Combinatorial Coverage

if __name__ == '__main__':
    print('\n### Exercise 6: Combinatorial Coverage')



### Exercise 7: Implicit Delays

if __name__ == '__main__':
    print('\n### Exercise 7: Implicit Delays')



### Exercise 8: Oracles

if __name__ == '__main__':
    print('\n### Exercise 8: Oracles')



### Exercise 9: More UI Elements

if __name__ == '__main__':
    print('\n### Exercise 9: More UI Elements')


