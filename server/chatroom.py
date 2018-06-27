"""use select"""

import sys
import time
import socket
import select
import logging
import queue
import threading


class ChatServer(object):

    TIMEOUT = 5

    def __init__(self, host, port, timeout, client_num):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._client_num = client_num
        self._buffer_size = 1024

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.settimeout(self._timeout)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((self._host, self._port))
        self.server.listen(self._client_num)

        # to select
        self.inputs = [self.server]
        self.outputs = []
        self.message_queues = {}
        self.client_info = {}

    def run(self):
        while True:
            rlist, wlist, xlist = select.select(self.inputs,
                                                self.outputs,
                                                self.inputs,
                                                self.TIMEOUT)

            if not (rlist or wlist or xlist):
                continue

            for s in rlist:  # read data
                if s is self.server:
                    self._accept_client(s)
                else:
                    self._read_client(s)

            for s in wlist:  # write data
                try:
                    next_msg = self.message_queues[s].get_nowait()
                except queue.Empty:
                    err_msg = "message queue empty"
                    self._rem_output(s)
                except Exception as e:
                    err_msg = "send data error: %s" % str(e)
                    logging.error(err_msg)
                    self._rem_output(s)
                else:
                    clients = [c for c in self.inputs if c is not self.server]
                    for c in clients:
                        if c is not s:
                            try:
                                c.sendall(bytes(next_msg, encoding='utf-8'))
                            except Exception as e:
                                err_msg = "send error: %s" % str(e)
                                logging.error(err_msg)
                                print("close: %s" % self.client_info[c])
                                self._clear(c)


            for s in xlist:  # error
                logging.error("Error: %s" % self.client_info[s])
                self._clear(s)



    def _accept_client(self, s):
        connection, client_address = s.accept()
        print("Connect: %s" % str(client_address))
        connection.setblocking(False)
        self.inputs.append(connection)
        self.client_info[connection] = str(client_address)
        self.message_queues[connection] = queue.Queue()

    def _read_client(self, s):
        data = s.recv(self._buffer_size)
        data = data.decode('utf-8')
        if data:
            data = "%s %s say: %s" % (time.strftime("%Y-%m-%d %H:%M:%S"),
                                      self.client_info[s],
                                      data)
            self.message_queues[s].put(data)
            # ensure in outputs
            self._add_output(s)
            print(data)
        else:
            print("Close: %s" % str(self.client_info[s]))
            self._rem_output(s)
            self.inputs.remove(s)
            s.close()
            del self.message_queues[s]
            del self.client_info[s]

    def _add_output(self, s):
        if s not in self.outputs:
            self.outputs.append(s)

    def _rem_output(self, s):
        if s in self.outputs:
            self.outputs.remove(s)

    def _clear(self, s):
        if s in self.inputs:
            self.inputs.remove(s)
            s.close()
        if s in self.outputs:
            self.outputs.remove(s)
        if s in self.message_queues:
            del self.message_queues[s]
        if s in self.client_info:
            del self.client_info[s]



class ChatClient(object):

    def __init__(self, host, port, timeout=1, reconnect=2):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._buffer_size = 1024
        self._flag = 1
        self.client = None
        self._lock = threading.Lock()

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, value):
        self._flag = value

    def _connect(self):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.setblocking(True)
        c.settimeout(self._timeout)
        c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        c.connect((self._host, self._port))
        return c

    def send_msg(self):
        if not self.client:
            return
        while True:
            time.sleep(0.1)
            bye = False
            try:
                data = sys.stdin.readline().strip()
            except KeyboardInterrupt as e:
                print(e)
                bye = True
            else:
                if data.lower() == "exit":
                    bye = True

            if bye:
                with self._lock:
                    self.flag = 0
                break

            self.client.sendall(bytes(data, encoding='utf-8'))
        return

    def recv_msg(self):
        if not self.client:
            return
        while True:
            data = None
            with self._lock:
                if not self.flag:
                    print("Bye")
                    break
            try:
                data = self.client.recv(self._buffer_size)
                data = data.decode('utf-8')
            except socket.timeout:
                # print('timeout')
                continue

            if data:
                print("%s" % data)

            time.sleep(0.1)
        return

    def run(self):
        self.client = self._connect()
        # send_proc = threading.Thread(target=self.send_msg)
        recv_proc = threading.Thread(target=self.recv_msg)
        # send_proc.start()
        recv_proc.start()
        # send_proc.join()
        self.send_msg()
        recv_proc.join()
        self.client.close()


def _main_server():
    s = ChatServer(host="localhost", port=5000, timeout=20, client_num=10)
    s.run()


def _main_client():
    c = ChatClient(host="localhost", port=5000)
    c.run()


if __name__ == "__main__":
    if sys.argv[1] == "server":
        _main_server()
    elif sys.argv[1] == "client":
        _main_client()

