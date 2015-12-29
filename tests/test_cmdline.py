"""Tests for the command line interface."""
import socketserver
import threading
from unittest import TestCase

import cmdline


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """Return the same it receives."""
        data = str(self.request.recv(1024), 'ascii')
        if data == "echo":
            response = bytes("{}".format(data), 'ascii')
        elif data.startswith("goto"):
            response = bytes("OK\n", 'ascii')

        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class TestCmd(TestCase):
    def setUp(self):
        super().setUp()
        self.igv = ThreadedTCPServer(("", 60151), ThreadedTCPRequestHandler)

        server_thread = threading.Thread(target=self.igv.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def tearDown(self):
        self.igv.shutdown()
        self.igv.server_close()
        super().tearDown()

    def test_check_igv_is_running(self):
        self.assertTrue(cmdline.check_igv())

    def test_igv_receives_goto_signal(self):
        self.assertTrue(cmdline.goto("chr1:123456"))
