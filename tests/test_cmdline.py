"""Tests for the command line interface."""
import os
from unittest import mock, TestCase

import cmdline


def _fake_input(*args):
    return "fake/path"


class TestMain(TestCase):
    @mock.patch("helpers.Variants")
    def test_main_launches_commandline(self, variants_mock):
        args = mock.Mock()
        args.gui = False
        sample_path = os.path.join(os.path.dirname(__file__),
                                   "files", "example.tab")
        args.variants = sample_path

        cmdline.main(args)

        variants_mock.assert_called_with(sample_path)

    @mock.patch("helpers.Variants")
    @mock.patch("builtins.input")
    def test_main_launches_commandline_without_variants(self,
                                                        input_mock,
                                                        variants_mock):
        args = mock.Mock()
        args.gui = False
        args.variants = False

        input_mock.return_value = "fake/path"

        cmdline.main(args)

        variants_mock.assert_called_with("fake/path")
