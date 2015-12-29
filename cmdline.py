"""Provide access through command line to IGV controlling."""
import socket


class SocketManager():

    """A Context Manager to deal with Sockets."""

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.settimeout(1)

        return self.socket

    def __exit__(self, *exc_info):
        self.socket.close()


class IGV():

    """IGV wrapper to control the program through a socket."""
    def __init__(self, host="", port=60151):
        self.host = host
        self.port = port

    def check_igv(self):
        """Return True if a copy of IGV is reachable."""

        response = ""
        with SocketManager(self.host, self.port) as s:
            s.sendall(bytes("echo", "ascii"))
            response = str(s.recv(1024), "ascii")

        if response == "echo":
            return True
        return False

    def command(self, command):
        pass

    def goto(self, position):
        """Return "True" if IGV answered "OK" to a goto command."""

        response = ""
        with SocketManager(self.host, self.port) as s:
            s.sendall(bytes("goto {}".format(position), "ascii"))
            response = str(s.recv(1024), "ascii")

        if response.startswith("OK"):
            return True
        return False

    def load(self, filepath):
        """Return "True" if IGV answered "OK" to a load command."""

        response = ""
        with SocketManager(self.host, self.port) as s:
            s.sendall(bytes("load {}".format(filepath), "ascii"))
            response = str(s.recv(1024), "ascii")

        if response.startswith("OK"):
            return True
        return False
