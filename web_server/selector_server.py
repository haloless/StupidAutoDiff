
import sys

import socket
import selectors


def _register(sel: selectors.BaseSelector,
              sock: socket.socket,
              mask,
              func,
              data=None):
    """Register in selector"""
    sel.register(sock, mask, (func, data))


def _unregister(sel: selectors.BaseSelector,
                sock: socket.socket):
    """Unregister in selector"""
    sel.unregister(sock)


class Server(object):
    """Server using Selector"""

    def __init__(self):
        self._sock = socket.socket()
        self._sel = selectors.DefaultSelector()

    def serve(self):
        with self._sel as sel, self._sock as sock:
            # setup socket
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setblocking(0)
            sock.bind(('localhost', 5000))
            sock.listen(100)
            print(sock)

            # accept selector
            _register(sel, sock, selectors.EVENT_READ, self._accept)
            print(sel)

            while True:
                ready = sel.select(timeout=1.0)
                for key, event in ready:
                    func, data = key.data
                    if data:
                        func(**data)
                    else:
                        func()

    def _accept(self):
        try:
            conn, addr = self._sock.accept()
            conn.setblocking(0)
            _register(self._sel, conn, selectors.EVENT_READ,
                      self._read, {'conn': conn, 'addr': addr})
        except OSError:
            conn.close()
            raise

    def _read(self, conn: socket.socket, addr):
        _unregister(self._sel, conn)

        try:
            buf = conn.recv(4096)
            # print("Read data:", str(buf))
            _register(self._sel, conn, selectors.EVENT_WRITE,
                      self._write, {'conn': conn, 'addr': addr})
        except OSError:
            conn.close()
            raise

    def _write(self, conn: socket.socket, addr):
        _unregister(self._sel, conn)

        try:
            conn.send(b'HTTP 1.0 200 OK\r\n\r\nHello world')
        finally:
            conn.close()


if __name__ == '__main__':
    s = Server()
    s.serve()
