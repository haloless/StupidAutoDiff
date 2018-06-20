"""
Test using httpd-tools

ab -n 10000 -c 10 "http://localhost:5000/"

"""


import sys
import os.path
import traceback

import socket
import selectors
import urllib.parse

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, CGIHTTPRequestHandler
from http.server import _url_collapse_path

import fnmatch


class PyWebServer(object):
    """Server"""

    def __init__(self, host: str, port: int, handler_factory):
        """Create server"""
        self.server_host = host
        self.server_port = port
        self.request_handler_factory = handler_factory

        # self.server_selector = selectors.DefaultSelector()
        self.server_socket = socket.socket()

    @property
    def server_address(self):
        return self.server_host, self.server_port

    @property
    def server_name(self):
        return socket.getfqdn(self.server_host)

    def serve(self):
        """Run server loop"""
        with selectors.DefaultSelector() as sel, self.server_socket as sock:
            # setup
            print(sel)

            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # sock.setblocking(False)
            sock.bind(self.server_address)
            sock.listen(20)
            print(sock)

            # register
            sel.register(sock, selectors.EVENT_READ)

            # enter loop
            while True:
                events = sel.select(timeout=1.0)
                if events:
                    self._handle_request()

    def _handle_request(self):
        """Internal method for handling request"""
        try:
            client_conn, client_addr = self.server_socket.accept()
        except OSError:
            return

        try:
            self.process_request(client_conn, client_addr)
        except Exception as e:
            self.handle_error(client_conn, client_addr, e)
        finally:
            self.shutdown_request(client_conn)

    def process_request(self, client_conn: socket.socket, client_addr):
        self.request_handler_factory(client_conn, client_addr, self)

    def shutdown_request(self, client_conn: socket.socket):
        """Force explicit shutdown"""
        try:
            client_conn.shutdown(socket.SHUT_WR)
        except OSError:
            pass
        client_conn.close()

    def handle_error(self, client_conn: socket.socket, client_addr, e: Exception=None):
        print('Exception for ', client_conn, client_addr, file=sys.stderr)
        if e:
            print(e)

        # print traceback
        traceback.print_exc()


class PyRequestHandler(CGIHTTPRequestHandler):
    """Request handler
    """

    allowed_patterns = ['/', '/*.html', '/*.css', '/overwatch.ico',
                        '/state.py', '/post.py', '/zip.py', ]

    forbidden_patterns = ['//*.py', ]

    cgi_paths = ['/state.py', '/post.py', '/zip.py', ]

    def is_cgi(self):
        """Test if in CGI paths"""
        collapsed_path = _url_collapse_path(self.path)
        dir_sep = collapsed_path.find('/', 1)
        head, tail = collapsed_path[:dir_sep], collapsed_path[dir_sep + 1:]

        res = urllib.parse.urlparse(self.path)
        # print(res)

        for cgi_path in self.cgi_paths:
            if res.path == cgi_path:
                self.cgi_info = head, tail
                return True
        return False
        # return CGIHTTPRequestHandler.is_cgi(self)

    def is_allowed(self):
        """Test"""
        res = urllib.parse.urlparse(self.path)

        for pat in self.allowed_patterns:
            if fnmatch.fnmatch(res.path, pat):
                return True
        return False

    def is_forbidden(self):
        collapsed_path = _url_collapse_path(self.path)
        # dir_sep = collapsed_path.find('/', 1)
        # head, tail = collapsed_path[:dir_sep], collapsed_path[dir_sep + 1:]
        # if collapsed_path in self.forbidden_patterns:
        #     return True
        for pat in self.forbidden_patterns:
            if fnmatch.fnmatch(collapsed_path, pat):
                return True
        return False

    def send_head(self):
        # if self.is_cgi():
        #     return self.run_cgi()
        # elif self.is_forbidden():
        #     self.send_error(HTTPStatus.FORBIDDEN, "Forbidden")
        #     return None
        # else:
        #     return SimpleHTTPRequestHandler.send_head(self)
        if self.is_allowed():
            return super(PyRequestHandler, self).send_head()
        else:
            self.send_error(HTTPStatus.FORBIDDEN, "Not allowed")
            return None


    # def __init__(self, client_conn: socket.socket, client_addr, server=None):
    #     self.client_conn = client_conn
    #     self.client_addr = client_addr
    #     self.server = server
    #
    #     self.rfile = self.client_conn.makefile('rb', buffering=-1)
    #     self.wfile = self.client_conn.makefile('wb')
    #
    #     try:
    #         self.handle()
    #     finally:
    #         self.finish()
    #
    # def handle(self): pass
    #
    # def finish(self):
    #     if not self.wfile.closed:
    #         try:
    #             self.wfile.flush()
    #         except socket.error:
    #             pass
    #     self.rfile.close()
    #     self.wfile.close()


if __name__ == '__main__':
    server = PyWebServer('localhost', 5000, PyRequestHandler)
    # server = PyWebServer('0.0.0.0', 5000, PyRequestHandler)
    print(server.server_address)
    server.serve()


