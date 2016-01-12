"""Tests for the command line interface."""
import os
from unittest import mock, TestCase

import cmdline


def _fake_input(*args):
    return "fake/path"


class TestMain(TestCase):
    @mock.patch("cmdline.text_mode")
    @mock.patch("helpers.Variants")
    def test_main_launches_commandline(self, variants_mock, text_mode_mock):
        args = mock.Mock()
        args.gui = False
        sample_path = os.path.join(os.path.dirname(__file__),
                                   "files", "example.tab")
        args.variants = sample_path

        text_mode_mock.return_value = True
        cmdline.main(args)

        variants_mock.assert_called_with(sample_path)

    @mock.patch("cmdline.text_mode")
    @mock.patch("helpers.Variants")
    @mock.patch("builtins.input")
    def test_main_launches_commandline_without_variants(self,
                                                        input_mock,
                                                        variants_mock,
                                                        text_mode_mock):
        args = mock.Mock()
        args.gui = False
        args.variants = False

        input_mock.return_value = "fake/path"
        text_mode_mock.return_value = True

        cmdline.main(args)

        variants_mock.assert_called_with("fake/path")


class TestTextMode(TestCase):
    def setUp(self):
        super().setUp()
        self.variants = [("chr1", "123456"), ("chr2", "987654")]

    @mock.patch("helpers.IGV")
    def test_arrows_launch_commands(self, IGV_mock):
        igv_wrap = IGV_mock.return_value

        # IGV is disconected
        igv_wrap.check_igv.return_value = False
        with self.assertRaises(OSError):
            cmdline.text_mode(self.variants)
            # Check a socket to IGV has been instatiated
            self.assertTrue(igv_wrap.called)
            self.assertTrue(igv_wrap.check_igv.called)

    @mock.patch("cmdline.readchar")
    @mock.patch("helpers.IGV")
    def test_we_can_navigate_right(self, IGV_mock, readchar_mock):
        igv_wrap = IGV_mock.return_value
        # IGV is connected
        igv_wrap.check_igv.return_value = True

        # "Enter" the right arrow
        readchar_wrap = readchar_mock.return_value
        readchar_wrap.key.return_value = True
        readchar_wrap.key.RIGHT = "RIGHT"

        readchar_wrap.readkey.return_value = "RIGHT"

        self.assertEqual(cmdline.text_mode(self.variants), self.variants[0])
