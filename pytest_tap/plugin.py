# Copyright (c) 2018, Matt Layman

try:
    from cStringIO import StringIO
except ImportError:  # pragma: no cover
    from io import StringIO
import sys

from py.io import TerminalWriter
import pytest
from tap.formatter import format_as_diagnostics
from tap.tracker import Tracker

from pytest_tap.i18n import _

import yaml

# Because of how pytest hooks work, there is not much choice
# except to use module level state. Ugh.
tracker = Tracker()


def pytest_addoption(parser):
    """Include all the command line options."""
    group = parser.getgroup('terminal reporting', 'reporting', after='general')
    group.addoption(
        '--tap-stream', default=False, action='store_true', help=_(
            'Stream TAP output instead of the default test runner output.'))
    group.addoption(
        '--tap-files', default=False, action='store_true', help=_(
            'Store all TAP test results into individual files per test case.'))
    group.addoption(
        '--tap-combined', default=False, action='store_true', help=_(
            'Store all TAP test results into a combined output file.'))
    group.addoption('--tap-outdir', metavar='path', help=_(
        'An optional output directory to write TAP files to. '
        'If the directory does not exist, it will be created.'))


@pytest.mark.trylast
def pytest_configure(config):
    """Set all the options before the test run."""
    tracker.outdir = config.option.tap_outdir
    tracker.combined = config.option.tap_combined
    if config.option.tap_stream:
        reporter = config.pluginmanager.getplugin('terminalreporter')
        if reporter:
            config.pluginmanager.unregister(reporter)
        tracker.streaming = True
        tracker.stream = sys.stdout
        # A common pytest pattern is to use test functions without classes.
        # The header looks really dumb for that pattern because it puts
        # out a lot of line noise since every function gets its own header.
        # Disable it automatically for streaming.
        tracker.header = False


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    report = yield  # get makereport outcome
    yaml_text_block = _get_yaml_from_pytest_mark(item)
    if call.when == 'call':
        report.result.tap_yaml_block = yaml_text_block


def pytest_runtest_logreport(report):
    """Add a test result to the tracker."""
    if not (
        (report.when == 'setup' and report.outcome == 'skipped') or
        report.when == 'call'
    ):
        return
    description = str(report.location[0]) + '::' + str(report.location[2])
    testcase = report.location[0]
    if report.outcome == 'passed':
        tracker.add_ok(testcase, description, directive=report.tap_yaml_block)
    elif report.outcome == 'failed':
        diagnostics = _make_as_diagnostics(report)
        tracker.add_not_ok(testcase, description, diagnostics=diagnostics, directive=report.tap_yaml_block)
    elif report.outcome == 'skipped':
        if type(report.longrepr) is tuple:
            reason = report.longrepr[2].split(':', 1)[1].strip()
        else:
            reason = report.wasxfail
        tracker.add_skip(testcase, description, reason)


def _make_as_diagnostics(report):
    """Format a report as TAP diagnostic output."""
    out = StringIO()
    tw = TerminalWriter(file=out)
    report.toterminal(tw)
    lines = out.getvalue().splitlines(True)
    return format_as_diagnostics(lines)


def pytest_unconfigure(config):
    """Dump the results."""
    if (
        config.option.tap_stream or
        config.option.tap_files or
        config.option.tap_combined
    ):
        tracker.generate_tap_reports()


def _get_yaml_from_pytest_mark(item):
    testids_mark = item.get_closest_marker('TESTIDS')
    if testids_mark is None:
        return ''
    else:
        return _get_yaml_as_text(testids_mark)


def _get_yaml_as_text(pytest_mark):
    testids_mark_arg_no = len(pytest_mark.args)
    if testids_mark_arg_no > 1:
        raise TypeError(
            'Incorrect number of arguments passed to @pytest.mark.TESTIDS expected 1 and received {}'.format(
                testids_mark_arg_no))
    else:
        yaml_object = yaml.load(pytest_mark.args[0])
        yaml_text_block = '\n---\n' + yaml.dump(yaml_object, default_flow_style=False) + '...'
        indented_yaml_text_block = '\n   '.join(yaml_text_block.split('\n'))
        return indented_yaml_text_block


# def tap_yaml(tap_yaml_text):
#     """Parse a YAML string decorator to a text block and add to test outcome"""
#     def tap_yaml_decorator(test_method):
#         def wrapper(self, arg2):
#             test_method(self, arg2)
#             tap_yaml_block = _create_yaml_text_block(tap_yaml_text)
#             self._outcome.result.tap_yaml_block = tap_yaml_block
#         return wrapper
#     return tap_yaml_decorator

# def _create_yaml_text_block(tap_yaml_text):
#     yaml_object = yaml.load(tap_yaml_text)
#     yaml_text_block = '\n---\n' + yaml.dump(yaml_object, default_flow_style=False) + '...'
#     indented_yaml_text_block = '\n   '.join(yaml_text_block.split('\n'))
#     return indented_yaml_text_block
