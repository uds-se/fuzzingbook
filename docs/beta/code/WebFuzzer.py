#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/WebFuzzer.html
# Last change: 2018-11-19 09:30:28+01:00
#
#
# Copyright (c) 2018 Saarland University, CISPA, authors, and contributors
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


# # Web GUI Fuzzing

if __name__ == "__main__":
    print('# Web GUI Fuzzing')




# ## A Web User Interface

if __name__ == "__main__":
    print('\n## A Web User Interface')




import fuzzingbook_utils

from IPython.core.display import HTML, display

if __name__ == "__main__":
    fuzzingbook_swag = {
        "tshirt": "One FuzzingBook T-Shirt",
        "drill": "One FuzzingBook Rotary Hammer",
        "lockset": "One FuzzingBook Lock Set"
    }


if __name__ == "__main__":
    html_order_form = """
    <form action="/order" style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
      <h3>Fuzzingbook Swag Order Form</h3>
      Yes! Please send me at your earliest convenience
      <select name="item">
      """
    for item in fuzzingbook_swag:
        html_order_form += '<option value="{item}">{name}</option>'.format(item=item, name=fuzzingbook_swag[item])
    html_order_form += """
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
      <input type="checkbox" name="tandc"><label for="tandc">I have read the <a href="/">terms and conditions</a></label><br>
      <button>Place order</button>
    </form>
    """


if __name__ == "__main__":
    HTML(html_order_form)


if __name__ == "__main__":
    html_order_received = """
    <div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
      <h3>Thank you for your Order!</h3>
      We will send <strong>{item_name}</strong> to {name} in {city}, {zip}<br>
      A confirmation mail will be sent to {email}.
    </div>
    """


if __name__ == "__main__":
    HTML(html_order_received.format(item_name="One FuzzingBook Rotary Hammer", 
                                    name="Jane Doe", 
                                    email="doe@example.com",
                                    city="Seattle",
                                    zip="98104"))


from multiprocessing import Process

from http.server import HTTPServer, BaseHTTPRequestHandler, HTTPStatus

import urllib.parse

import html

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        print("HEAD " + self.path)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
            
    def do_GET(self):
        print("GET " + self.path)
        if self.path == "/":
            self.send_order_form()
        elif self.path.startswith("/order"):
            self.send_order_received()
        else:
            self.send_response(HTTPStatus.NOT_FOUND, "Not found")

class MyHTTPRequestHandler(MyHTTPRequestHandler):
    def send_order_form(self):
        self.send_response(HTTPStatus.OK, "Place your order")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_order_form.encode("utf8"))

if __package__ is None or __package__ == "":
    from Coverage import cgi_decode
else:
    from .Coverage import cgi_decode


class MyHTTPRequestHandler(MyHTTPRequestHandler):
    def send_order_received(self):
        self.send_response(HTTPStatus.OK, "Order received")
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # self.path is sth like "/order?item=foo&name=bar"
        # Note: this fails to decode non-ASCII characters properly
        query_string = urllib.parse.urlparse(self.path).query
        
        # fields is { 'item': ['tshirt'], 'name': ['Jane Doe'], ...}
        fields = urllib.parse.parse_qs(query_string, keep_blank_values=True)

        values = {}
        html_values = {}
        for key in fields:
            values[key] = urllib.parse.unquote(html.unescape(fields[key][0]))
            html_values[key] = html.escape(urllib.parse.unquote(values[key]))
            
        values["item_name"] = fuzzingbook_swag[values["item"]]
        html_values["item_name"] = html.escape(values["item_name"])
        
        confirmation = html_order_received.format(**html_values)
        self.wfile.write(confirmation.encode("utf8"))

class MyHTTPRequestHandler(MyHTTPRequestHandler):
    def not_found(self):
        self.send_response(HTTPStatus.NOT_FOUND, "Not found")

def run_httpd():
    localhost = "127.0.0.1"
    for port in range(8800, 9000):
        httpd_address = (localhost, port)
        # httpd_url = "http://" + httpd_address[0] + ":" + repr(httpd_address[1]) + "/"
        
        try:
            httpd = HTTPServer(httpd_address, MyHTTPRequestHandler)
            break
        except OSError:
            continue
    
    print("Running on port", port)
    with open("httpd_port.txt", "w") as f:
        f.write(repr(port))
    httpd.serve_forever()    

if __name__ == "__main__":
    http_process = Process(target=run_httpd)
    http_process.start()


import time

if __name__ == "__main__":
    time.sleep(1)
    with open("httpd_port.txt") as f:
        httpd_port = int(f.read())

        # Better yet: https://stackoverflow.com/questions/2311510/getting-a-machines-external-ip-address-with-python

    httpd_port


import urllib.request
import socket

def httpd_url(ip, port):
    return "http://" + ip + ":" + repr(port) + "/"

if __name__ == "__main__":
    local_ip = "127.0.0.1"

    # Get external IP (needed if running on a remote server)
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

    # Get hostname
    hostname_ip = socket.gethostname()

    for ip in [external_ip, hostname_ip, local_ip]:
        try:
            response = urllib.request.urlopen(httpd_url(ip, httpd_port))
            break
        except urllib.request.URLError:
            response = None

    if response is not None:
        httpd_ip = ip


if __name__ == "__main__":
    HTML('<a href="' + httpd_url(httpd_ip, httpd_port) + '">' + httpd_url(httpd_ip, httpd_port) + "</a>")


if __name__ == "__main__":
    HTML('<iframe src="' + httpd_url(httpd_ip, httpd_port) + '" width="100%" height="220">')


if __package__ is None or __package__ == "":
    from Carver import webbrowser
else:
    from .Carver import webbrowser


if __name__ == "__main__":
    contents = webbrowser(httpd_url(httpd_ip, httpd_port))


if __name__ == "__main__":
    HTML(contents)


if __name__ == "__main__":
    HTML(webbrowser(httpd_url(httpd_ip, httpd_port) + "order?item=tshirt&name=Jane+Doe&email=doe%40example.com&city=Seattle&zip=98104"))


if __package__ is None or __package__ == "":
    from Grammars import crange, is_valid_grammar
else:
    from .Grammars import crange, is_valid_grammar


ORDER_GRAMMAR = {
    "<start>": [ "<order>" ],
    "<order>": [ "order?item=<item>&name=<name>&email=<email>&city=<city>&zip=<zip>" ],
    "<item>": [ "tshirt", "drill", "lockset" ],
    "<name>": [ "Jane Doe", "John Smith" ],
    "<email>": [ "foo@example.com"],
    "<city>": [ "Seattle", "New York"],
    "<zip>": [ "<digit>" * 5 ],
    "<digit>": crange('0', '9')
}
assert is_valid_grammar(ORDER_GRAMMAR)

BAD_ORDER_GRAMMAR = {
    "<name>": [ "Robert'; drop table students; --"],  # https://xkcd.com/327/
    "<city>": [ "Mötley Crüe" ],
}
...

if __name__ == "__main__":
    time.sleep(5)
    http_process.terminate()


import os

if __name__ == "__main__":
    os.remove("httpd_port.txt")


# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Background

if __name__ == "__main__":
    print('\n## Background')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1: _Title_

if __name__ == "__main__":
    print('\n### Exercise 1: _Title_')




if __name__ == "__main__":
    # Some code that is part of the exercise
    pass


if __name__ == "__main__":
    # Some code for the solution
    2 + 2


# ### Exercise 2: _Title_

if __name__ == "__main__":
    print('\n### Exercise 2: _Title_')



