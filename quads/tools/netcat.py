#!/usr/bin/python3

import socket


class Netcat:
    """ Python 'netcat like' module """

    def __init__(self, ip, port=22):
        self.ip = ip
        self.port = port
        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    def health_check(self, timeout=15):
        try:
            self.socket.settimeout(timeout)
            self.connect()
        except (
            socket.timeout,
            TimeoutError,
            ConnectionResetError,
            ConnectionRefusedError,
        ):
            return False
        return True

    def read(self, length=1024):
        """ Read 1024 bytes off the socket """
        return self.socket.recv(length)

    def read_until(self, data):
        """ Read data into the buffer until we have data """
        while data not in self.buff:
            self.buff += self.socket.recv(1024)

        pos = self.buff.find(data)
        return_val = self.buff[: pos + len(data)]
        self.buff = self.buff[pos + len(data) :]

        return return_val

    def write(self, data):
        self.socket.send(data)

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def close(self):
        self.socket.close()
