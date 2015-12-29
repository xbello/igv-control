"""Provide access through command line to IGV controlling."""
import socket


def check_igv():
    """Return True if a copy of IGV is reachable."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("", 60151))
    s.settimeout(5)

    response = ""
    try:
        s.sendall(bytes("echo", "ascii"))
        response = str(s.recv(1024), "ascii")
    finally:
        s.close()

    if response == "echo":
        return True
    return False


def goto(position):
    """Return "True" if IGV answered "OK" to a goto command."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("", 60151))
    s.settimeout(1)

    response = ""
    try:
        s.sendall(bytes("goto {}".format(position), "ascii"))
        response = str(s.recv(1024), "ascii")
    finally:
        s.close()

    if response.startswith("OK"):
        return True
    return False


def load(filepath):
    """Return "True" if IGV answered "OK" to a load command."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("", 60151))
    s.settimeout(1)

    response = ""
    try:
        s.sendall(bytes("load {}".format(filepath), "ascii"))
        response = str(s.recv(1024), "ascii")
    finally:
        s.close()

    if response.startswith("OK"):
        return True
    return False
