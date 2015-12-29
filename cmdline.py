"""Provide access through command line to IGV controlling."""
import socket


class IGV():

    """IGV wrapper to control the program through a socket."""

    def check_igv(self):
        """Return True if a copy of IGV is reachable."""

        self.open_socket()
        response = ""
        self.socket.sendall(bytes("echo", "ascii"))
        response = str(self.socket.recv(1024), "ascii")

        self.close()

        if response == "echo":
            return True
        return False

    def close(self):
        """Close the socket if it is open."""
        self.socket.close()

    def command(self, command):
        pass

    def goto(self, position):
        """Return "True" if IGV answered "OK" to a goto command."""
        response = ""

        self.open_socket()
        self.socket.sendall(bytes("goto {}".format(position), "ascii"))
        response = str(self.socket.recv(1024), "ascii")
        self.close()

        if response.startswith("OK"):
            return True
        return False

    def load(self, filepath):
        """Return "True" if IGV answered "OK" to a load command."""
        response = ""

        self.open_socket()
        self.socket.sendall(bytes("load {}".format(filepath), "ascii"))
        response = str(self.socket.recv(1024), "ascii")
        self.close()

        if response.startswith("OK"):
            return True
        return False

    def open_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("", 60151))
        self.socket.settimeout(1)
