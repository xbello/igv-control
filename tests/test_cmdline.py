"""Tests for the command line interface."""
import os
from unittest import mock, TestCase

import cmdline


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

        self.fail("Continue testing here")
