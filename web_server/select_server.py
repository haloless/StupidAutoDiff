
import sys
import selectors
import socket
if sys.version_info[0] == 3:
    from http.server import HTTPServer


class AbstractHandler(object):
    def __init__(self,
                 request: socket.socket,
                 client_address,
                 server: "AbstractServer"):
        self.client_conn = request
        self.client_address = client_address
        self.server = server

        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def finish(self):
        pass

    def handle(self):
        pass


class AbstractHandlerFactory(object):
    def create(self, client_socket: socket.socket, client_address, server: "AbstractServer") -> AbstractHandler:
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        return self.create(*args, **kwargs)


class AbstractServer(object):
    """Abstract server"""

    def __init__(self, address: str, port: int, handler_factory: AbstractHandlerFactory):
        self.address = address
        self.port = port
        self.handler_factory = handler_factory

    def serve(self):
        """Run server loop"""
        with selectors.DefaultSelector() as sel:
            print(sel)
            with socket.socket() as sock:
                sock.bind((self.address, self.port))
                sock.listen(10)
                sock.setblocking(False)
                print(sock)

                sel.register(sock, selectors.EVENT_READ)

                while True:
                    ready = sel.select()
                    if ready:
                        # self.handle_request_nonblock()
                        client_socket, client_address = sock.accept()
                        if self.verify_request(client_socket, client_address):
                            try:
                                self.process_request(client_socket, client_address)
                            except Exception:
                                self.shutdown_request(client_socket)
                                raise
                        else:
                            self.shutdown_request(client_socket)

                    self.serve_actions()

    def serve_actions(self):
        pass

    def handle_request_nonblock(self):
        pass

    def verify_request(self, request, client_address):
        return True

    def process_request(self, request, client_address):
        self.finish_request(request, client_address)
        self.shutdown_request(request)

    def finish_request(self, request: socket.socket, client_address):
        self.handler_factory.create(request, client_address, self)

    def shutdown_request(self, request: socket.socket):
        """Explicitly shutdown client socket"""
        request.shutdown(socket.SHUT_WR)
        self.close_request(request)

    def close_request(self, request: socket.socket):
        request.close()

# sel = selectors.DefaultSelector()
# print(sel)
#
#
# def accept(sock: socket.socket, mask):
#     conn, addr = sock.accept()
#     print('accepted', conn, 'from', addr)
#     conn.setblocking(False)
#     sel.register(conn, selectors.EVENT_READ, read)
#
#
# def read(conn: socket.socket, mask):
#     data = conn.recv(1024)
#     if data:
#         print('echo', repr(data), 'to', conn)
#         conn.send(data)
#     else:
#         print('close', conn)
#         sel.unregister(conn)
#         conn.close()
#
#
# sock = socket.socket()
# sock.bind(('localhost', 5000))
# sock.listen(100)
# sock.setblocking(False)
# sel.register(sock, selectors.EVENT_READ, accept)
#
# while True:
#     events = sel.select()
#     for key, mask in events:
#         callback = key.data
#         callback(key.fileobj, mask)

if __name__ == '__main__':
    print()

