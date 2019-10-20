# Copyright (c) 2019, Matt Layman

try:
    from cStringIO import StringIO
except ImportError:  # pragma: no cover
    from io import StringIO
import sys

from py.io import TerminalWriter
import pytest
import six
from tap.formatter import format_as_diagnostics
from tap.tracker import Tracker

from pytest_tap.i18n import _

# Because of how pytest hooks work, there is not much choice
# except to use module level state. Ugh.
tracker = Tracker()
ENABLED = False


def pytest_addoption(parser):
    """Include all the command line options."""
    group = parser.getgroup("terminal reporting", "reporting", after="general")
    group.addoption(
        "--tap-stream",
        default=False,
        action="store_true",
        help=_("Stream TAP output instead of the default test runner output."),
    )
    group.addoption(
        "--tap-files",
        default=False,
        action="store_true",
        help=_("Store all TAP test results into individual files per test case."),
    )
    group.addoption(
        "--tap-combined",
        default=False,
        action="store_true",
        help=_("Store all TAP test results into a combined output file."),
    )
    group.addoption(
        "--tap-outdir",
        metavar="path",
        help=_(
            "An optional output directory to write TAP files to. "
            "If the directory does not exist, it will be created."
        ),
    )


@pytest.mark.trylast
def pytest_configure(config):
    """Set all the options before the test run."""
    global ENABLED
    ENABLED = (
        config.getoption("tap_stream")
        or config.getoption("tap_combined")
        or config.getoption("tap_files")
    )

    tracker.outdir = config.getoption("tap_outdir")
    tracker.combined = config.getoption("tap_combined")
    if config.getoption("tap_stream"):
        reporter = config.pluginmanager.getplugin("terminalreporter")
        if reporter:
            config.pluginmanager.unregister(reporter)
        tracker.streaming = True
        tracker.stream = sys.stdout
        # A common pytest pattern is to use test functions without classes.
        # The header looks really dumb for that pattern because it puts
        # out a lot of line noise since every function gets its own header.
        # Disable it automatically for streaming.
        tracker.header = False


def pytest_runtestloop(session):
    """Output the plan line first."""
    if ENABLED:
        if session.config.getoption("tap_stream") or session.config.getoption(
            "tap_combined"
        ):
            tracker.set_plan(session.testscollected)


def pytest_runtest_logreport(report):
    """Add a test result to the tracker."""
    if not ENABLED:
        return

    is_trackable_result = (
        (report.when == "setup" and report.outcome == "skipped")
        or (report.when == "setup" and report.outcome == "failed")
        or report.when == "call"
    )
    if not is_trackable_result:
        return

    description = str(report.location[0]) + "::" + str(report.location[2])
    testcase = report.location[0]

    # Handle xfails first because they report in unusual ways.
    # Non-strict xfails will include `wasxfail` while strict xfails won't.
    if hasattr(report, "wasxfail"):
        directive = ""
        if report.skipped:
            directive = "TODO expected failure: {}".format(report.wasxfail)
        elif report.passed:
            directive = "TODO unexpected success: {}".format(report.wasxfail)

        tracker.add_ok(testcase, description, directive=directive)
    elif report.passed:
        tracker.add_ok(testcase, description)
    elif report.failed:
        diagnostics = _make_as_diagnostics(report)

        # strict xfail mode should include the todo directive.
        # The only indicator that strict xfail occurred for this report
        # is to check longrepr.
        directive = ""
        if (
            isinstance(report.longrepr, six.string_types)
            and "[XPASS(strict)]" in report.longrepr
        ):
            directive = "TODO"

        tracker.add_not_ok(
            testcase, description, directive=directive, diagnostics=diagnostics
        )
    elif report.skipped:
        reason = report.longrepr[2].split(":", 1)[1].strip()
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
    if ENABLED:
        tracker.generate_tap_reports()
