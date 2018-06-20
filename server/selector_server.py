
from http.server import HTTPServer

import socket
import selectors


class WebServer(object):
    """Server"""

    def __init__(self, address: str, port: int, handler_factory):
        """Create server"""
        self.server_address = address
        self.server_port = port
        self.request_handler_factory = handler_factory

        self.server_selector = selectors.DefaultSelector()
        self.server_socket = socket.socket()

    def serve(self):
        """Run server loop"""
        with self.server_selector as sel, self.server_socket as sock:
            # setup
            print(sel)

            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setblocking(False)
            sock.bind((self.server_address, self.server_port))
            sock.listen(100)
            print(sock)

            # sel.register(sock.fileno(), selectors.EVENT_READ)
            self._register(sock, selectors.EVENT_READ, self._accept)

            # enter loop
            while True:
                events = sel.select(timeout=1.0)
                for key, mask in events:
                    func, data = key.data
                    if data:
                        func(**data)
                    else:
                        func()

    def _accept(self):
        client_socket, client_address = self.server_socket.accept()
        client_socket.setblocking(False)
        self._register(client_socket, selectors.EVENT_READ, self._read, {'conn': client_socket})

    def _read(self, conn: socket.socket):
        self._unregister(conn)
        try:
            conn.recv(1024)
        except:
            conn.close()
            raise
        else:
            self._register(conn, selectors.EVENT_WRITE, self._write, {'conn': conn})

    def _write(self, conn: socket.socket):
        self._unregister(conn)
        try:
            conn.send(b'HTTP 1.0 200 OK\r\n\r\nHelloWorld')
        finally:
            conn.close()

    def _register(self, fileobj, events, action, data=None):
        self.server_selector.register(fileobj, events, (action, data))

    def _unregister(self, fileobj):
        self.server_selector.unregister(fileobj)


if __name__ == '__main__':
    server = WebServer('localhost', 5000, None)
    server.serve()


