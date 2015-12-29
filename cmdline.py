"""Provide access through command line to IGV controlling."""
import socket


def check_igv():
    """Return True if a copy of IGV is reachable."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("", 60151))
    s.settimeout(5)

    try:
        s.sendall(bytes("echo", "ascii"))
        response = str(s.recv(1024), "ascii")
    finally:
        s.close()

    if response == "echo":
        return True
    return False
