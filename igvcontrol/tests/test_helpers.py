"""Tests for the helper classes."""
import os
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver
import threading
from unittest import TestCase

from igvcontrol import helpers


class TCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """Return the same it receives."""
        data = self.request.recv(1024)
        try:
            data = str(data, 'ascii')
        except TypeError:
            pass

        responses = {"echo": "echo",
                     "goto": "OK",
                     "load": "OK",
                     "": "ERROR"}

        response_text = responses.get(data.split()[0] if data else "")
        try:
            response_text = bytes("{}".format(response_text), 'ascii')
        except TypeError:
            pass

        self.request.sendall(response_text)


class TCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class TestCmd(TestCase):
    def setUp(self):
        try:
            super().setUp()
        except TypeError:
            super(TestCmd, self).setUp()
        self.igv_server = TCPServer(("localhost", 60151), TCPRequestHandler)

        server_thread = threading.Thread(target=self.igv_server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        self.igv_client = helpers.IGV()

    def tearDown(self):
        self.igv_server.shutdown()
        self.igv_server.server_close()
        try:
            super().tearDown()
        except TypeError:
            super(TestCmd, self).tearDown()

    def test_can_IGV_client_as_object(self):
        self.assertTrue(isinstance(self.igv_client, helpers.IGV))

    def test_we_can_send_multiple_commands(self):
        self.assertTrue(self.igv_client.check_igv())
        self.assertTrue(self.igv_client.goto("chr1:12345"))

    def test_check_igv_is_running(self):
        self.assertTrue(self.igv_client.check_igv())

    def test_we_can_send_goto_signal(self):
        self.assertTrue(self.igv_client.goto("chr1:123456"))

    def test_we_can_send_load_signal(self):
        self.assertTrue(self.igv_client.load("path/to/file.bam"))

    def test_we_can_send_through_command_method(self):
        self.assertEqual(self.igv_client.command("echo"), "echo")


class TestVCFandTAB(TestCase):
    def setUp(self):
        try:
            super().setUp()
        except TypeError:
            super(TestVCFandTAB, self).setUp()
        self.vcf_file = os.path.join(os.path.dirname(__file__),
                                     "files/example-4.0.vcf")
        self.tab_file = os.path.join(os.path.dirname(__file__),
                                     "files/example.tab")
        self.tab_file_noheader = os.path.join(os.path.dirname(__file__),
                                              "files/example_noheader.tab")

        self.variants_vcf = helpers.Variants(self.vcf_file)
        self.variants_tab = helpers.Variants(self.tab_file)
        self.variants_tab_noh = helpers.Variants(self.tab_file_noheader)

    def test_can_load_vcf_file(self):
        self.assertTrue(self.variants_vcf.loadvcf())
        self.assertFalse(self.variants_tab.loadvcf())

        self.assertEqual(len([_ for _ in self.variants_vcf]), 5)

    def test_can_load_tab_file(self):
        self.assertFalse(self.variants_vcf.loadtab())
        self.assertTrue(self.variants_tab.loadtab())

        self.assertEqual(len([_ for _ in self.variants_tab]), 3)

    def test_tab_generator(self):
        self.assertEqual(
            len([_ for _ in self.variants_tab.tab_generator()]), 3)
        self.assertEqual(
            len([_ for _ in self.variants_tab_noh.tab_generator()]), 3)

    def test_generate_chrompos_pairs_from_vcf_and_tab(self):
        self.assertEqual([("chr20", "14370"),
                          ("chr20", "17330"),
                          ("chr20", "1110696"),
                          ("chr20", "1230237"),
                          ("chr20", "1234567")],
                         [_ for _ in self.variants_vcf])
        self.assertEqual([("chr1", "7571115"),
                          ("chr1", "7572645"),
                          ("chr1", "7573472")],
                         [_ for _ in self.variants_tab])


class TestXLSandODF(TestCase):
    def setUp(self):
        try:
            super().setUp()
        except TypeError:
            super(TestXLSandODF, self).setUp()
        self.xls_file = os.path.join(os.path.dirname(__file__),
                                     "files/example.xls")
        self.xlsx_file = os.path.join(os.path.dirname(__file__),
                                      "files/example.xlsx")

        self.variants_xls = helpers.Variants(self.xls_file)
        self.variants_xlsx = helpers.Variants(self.xlsx_file)

    def test_can_load_xls_file(self):
        self.assertTrue(self.variants_xls.loadxls())

        self.assertEqual(len([_ for _ in self.variants_xls]), 3)

    def test_can_load_xlsx_file(self):
        self.assertTrue(self.variants_xlsx.loadxls())

        self.assertEqual(len([_ for _ in self.variants_xlsx]), 3)

    def test_generate_chrompos_pairs_from_xls(self):
        self.assertEqual([("chr1", "7571115"),
                          ("chr1", "7572645"),
                          ("chr1", "7573472")],
                         [_ for _ in self.variants_xls])

    def test_generate_chrompos_pairs_from_xlsx(self):
        self.assertEqual([("chr1", "7571115"),
                          ("chr1", "7572645"),
                          ("chr1", "7573472")],
                         [_ for _ in self.variants_xlsx])
