# Copyright (c) 2017, Matt Layman

try:
    from unittest import mock
except ImportError:
    import mock
import tempfile
import unittest

from tap.tracker import Tracker

from pytest_tap import plugin


class TestPlugin(unittest.TestCase):

    def setUp(self):
        """The pytest plugin uses module scope so a fresh tracker
        must be installed each time."""
        # When running this suite with pytest, save and restore the tracker.
        self._tracker = plugin.tracker
        plugin.tracker = Tracker()

    def tearDown(self):
        plugin.tracker = self._tracker

    def _make_config(self):
        config = mock.Mock()
        config.option.tap_stream = False
        config.option.tap_files = False
        config.option.tap_outdir = None
        config.option.tap_combined = False
        return config

    def test_includes_options(self):
        group = mock.Mock()
        parser = mock.Mock()
        parser.getgroup.return_value = group
        plugin.pytest_addoption(parser)
        self.assertEqual(group.addoption.call_count, 4)

    def test_tracker_stream_set(self):
        config = self._make_config()
        config.option.tap_stream = True
        plugin.pytest_configure(config)
        self.assertTrue(plugin.tracker.streaming)
        self.assertFalse(plugin.tracker.header)

    def test_tracker_outdir_set(self):
        outdir = tempfile.mkdtemp()
        config = self._make_config()
        config.option.tap_outdir = outdir
        plugin.pytest_configure(config)
        self.assertEqual(plugin.tracker.outdir, outdir)

    def test_tracker_combined_set(self):
        config = self._make_config()
        config.option.tap_combined = True
        plugin.pytest_configure(config)
        self.assertTrue(plugin.tracker.combined)

    def test_track_when_call_report(self):
        """Only the call reports are tracked."""
        plugin.tracker = mock.Mock()
        report = mock.Mock(when='setup', outcome='passed')
        plugin.pytest_runtest_logreport(report)
        self.assertFalse(plugin.tracker.add_ok.called)

    def test_tracks_ok(self):
        plugin.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        report = mock.Mock(when='call', outcome='passed', location=location)
        plugin.pytest_runtest_logreport(report)
        plugin.tracker.add_ok.assert_called_once_with(
                'test_file.py', 'test_file.py::TestFake.test_me')

    def test_tracks_not_ok(self):
        plugin.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        report = mock.Mock(when='call', outcome='failed', location=location)
        plugin.pytest_runtest_logreport(report)
        plugin.tracker.add_not_ok.assert_called_once_with(
            'test_file.py', 'test_file.py::TestFake.test_me', diagnostics='')

    def test_tracks_skip(self):
        plugin.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        longrepr = ('', '', 'Skipped: a reason')
        report = mock.Mock(
            when='setup', outcome='skipped', location=location,
            longrepr=longrepr)
        plugin.pytest_runtest_logreport(report)
        plugin.tracker.add_skip.assert_called_once_with(
            'test_file.py', 'test_file.py::TestFake.test_me', 'a reason')

    def test_tracks_xfail(self):
        plugin.tracker = mock.Mock()
        location = ('test_file.py', 1, 'TestFake.test_me')
        report = mock.Mock(
            when='call', outcome='skipped', location=location, wasxfail='')
        plugin.pytest_runtest_logreport(report)
        plugin.tracker.add_skip.assert_called_once_with(
            'test_file.py', 'test_file.py::TestFake.test_me', '')

    def test_generates_reports_for_stream(self):
        config = self._make_config()
        config.option.tap_stream = True
        plugin.tracker = mock.Mock()
        plugin.pytest_unconfigure(config)
        plugin.tracker.generate_tap_reports.assert_called_once_with()

    def test_generates_reports_for_files(self):
        config = self._make_config()
        config.option.tap_files = True
        plugin.tracker = mock.Mock()
        plugin.pytest_unconfigure(config)
        plugin.tracker.generate_tap_reports.assert_called_once_with()

    def test_generates_reports_for_combined(self):
        config = self._make_config()
        config.option.tap_combined = True
        plugin.tracker = mock.Mock()
        plugin.pytest_unconfigure(config)
        plugin.tracker.generate_tap_reports.assert_called_once_with()

    def test_skips_reporting_with_no_output_option(self):
        config = self._make_config()
        plugin.tracker = mock.Mock()
        plugin.pytest_unconfigure(config)
        self.assertFalse(plugin.tracker.generate_tap_reports.called)

    def test_path_pytest(self):
        plugin.tracker = mock.Mock()
        location = ('tests/test_file.py', 1, 'TestFake.test_me')
        report = mock.Mock(when='call', outcome='passed', location=location)
        plugin.pytest_runtest_logreport(report)
        plugin.tracker.add_ok.assert_called_once_with(
                'tests/test_file.py', 'tests/test_file.py::TestFake.test_me')
