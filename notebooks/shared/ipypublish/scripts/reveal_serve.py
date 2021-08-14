""" serve HTML page """

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import logging
import os
import signal
import webbrowser

from tornado import web, ioloop, httpserver, log
from tornado.httpclient import AsyncHTTPClient
from traitlets import Bool, Unicode, Int
from traitlets.config.configurable import LoggingConfigurable


class ProxyHandler(web.RequestHandler):
    """handler the proxies requests from a local prefix to a CDN"""

    @web.asynchronous
    def get(self, prefix, url):
        """proxy a request to a CDN"""
        proxy_url = "/".join([self.settings['cdn'], url])
        client = self.settings['client']
        client.fetch(proxy_url, callback=self.finish_get)

    def finish_get(self, response):
        """finish the request"""
        # rethrow errors
        response.rethrow()

        for header in ["Content-Type", "Cache-Control", "Date", "Last-Modified", "Expires"]:
            if header in response.headers:
                self.set_header(header, response.headers[header])
        self.finish(response.body)


class RevealServer(LoggingConfigurable):
    """Post processor designed to serve files

    Proxies reveal.js requests to a CDN if no local reveal.js is present
    """

    open_in_browser = Bool(True,
                           help="""Should the browser be opened automatically?"""
                           ).tag(config=True)
    reveal_cdn = Unicode("https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.1.0",
                         help="""URL for reveal.js CDN."""
                         ).tag(config=True)
    reveal_prefix = Unicode("reveal.js", help="URL prefix for reveal.js").tag(config=True)
    ip = Unicode("127.0.0.1", help="The IP address to listen on.").tag(config=True)
    port = Int(8000, help="port for the server to listen on.").tag(config=True)

    def serve(self, input):
        """Serve the build directory with a webserver."""
        if not os.path.exists(input):
            logging.error('the html path does not exist: {}'.format(input))
            raise IOError('the html path does not exist: {}'.format(input))

        dirname, filename = os.path.split(input)

        handlers = [
            (r"/(.+)", web.StaticFileHandler, {'path': dirname}),
            (r"/", web.RedirectHandler, {"url": "/%s" % filename})
        ]

        if '://' in self.reveal_prefix or self.reveal_prefix.startswith("//"):
            # reveal specifically from CDN, nothing to do
            pass
        elif os.path.isdir(os.path.join(dirname, self.reveal_prefix)):
            # reveal prefix exists
            self.log.info("Serving local %s", self.reveal_prefix)
            logging.info("Serving local %s", self.reveal_prefix)
        else:
            self.log.info("Redirecting %s requests to %s", self.reveal_prefix, self.reveal_cdn)
            logging.info("Redirecting %s requests to %s", self.reveal_prefix, self.reveal_cdn)
            handlers.insert(0, (r"/(%s)/(.*)" % self.reveal_prefix, ProxyHandler))

        app = web.Application(handlers,
                              cdn=self.reveal_cdn,
                              client=AsyncHTTPClient(),
                              )

        # hook up tornado logging to our logger
        log.app_log = self.log

        http_server = httpserver.HTTPServer(app)

        # find an available port
        port_attempts = list(range(10))
        for port_attempt in port_attempts:
            try:
                url = "http://%s:%i/%s" % (self.ip, self.port, filename)
                logging.info("Attempting to serve at %s" % url)
                http_server.listen(self.port, address=self.ip)
                break
            except IOError:
                self.port += 1
        if port_attempt == port_attempts[-1]:
            logging.error('no port available to launch slides on, try closing some slideshows')
            raise IOError('no port available to launch slides on, try closing some slideshows')

        logging.info("Serving your slides at %s" % url)
        logging.info("Use Control-C to stop this server")

        # don't let people press ctrl-z, which leaves port open
        def handler(signum, frame):
            logging.info('Control-Z pressed, but ignored, use Control-C!')

        signal.signal(signal.SIGTSTP, handler)

        if self.open_in_browser:
            webbrowser.open(url, new=2)
        try:
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            # ioloop.IOLoop.instance().stop() #dosen't look like this is necessary
            logging.info("\nInterrupted")
