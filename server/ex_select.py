"""Example"""

from __future__ import absolute_import
from __future__ import print_function

import select
import socket
import queue


def server_routine(address):
    """Server routine"""

    # create
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    # set reuse
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind(address)

    server.listen(10)

    # to read
    inputs = [server]
    # to write
    outputs = []
    message_queues = {}

    while inputs:
        print("server waiting")

        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout=20)

        if not (readable or writable or exceptional):
            print("timeout")
            break

        for s in readable:
            if s is server:
                # accept connection
                connection, client_address = s.accept()
                print("accept", client_address)
                connection.setblocking(False)
                inputs.append(connection)
                message_queues[connection] = queue.Queue()
            else:
                # read connection
                data = s.recv(1024)
                if data:
                    print("receive", data, "from", s.getpeername())
                    message_queues[s].put(data)
                    # add output for response
                    if s not in outputs:
                        outputs.append(s)
                else:
                    # close connection
                    print("close", s.getpeername())
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    # message queue
                    del message_queues[s]

        for s in writable:
            try:
                next_message = message_queues[s].get_nowait()
            except queue.Empty:
                print(s.getpeername(), "queue empty")
                outputs.remove(s)
            else:
                print("send", next_message, "to", s.getpeername())
                s.send(next_message)

        for s in exceptional:
            print("exception on", s.getpeername())
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


def client_routine(address):
    messages = ["This is the message",
                "It will be sent",
                "in parts"]
    print("connect to server")

    socks = []
    for i in range(10):
        socks.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    for s in socks:
        s.connect(address)

    count = 0
    for message in messages:
        for s in socks:
            count += 1
            data = message + " ver " + str(count)
            print("%s send %s" % (s.getpeername(), data))
            s.send(data)
        for s in socks:
            data = s.recv(1024)
            print("%s receive %s" % (s.getpeername(), data))
            if not data:
                print("close", s.getpeername())
                s.close()







if __name__ == "__main__":
    server_address = ('localhost', 5000)

