import sys

import pytest
from tap.formatter import format_as_diagnostics
from tap.tracker import Tracker

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
        help="Stream TAP output instead of the default test runner output.",
    )
    group.addoption(
        "--tap-files",
        default=False,
        action="store_true",
        help="Store all TAP test results into individual files per test case.",
    )
    group.addoption(
        "--tap-combined",
        default=False,
        action="store_true",
        help="Store all TAP test results into a combined output file.",
    )
    group.addoption(
        "--tap-outdir",
        metavar="path",
        help=(
            "An optional output directory to write TAP files to. "
            "If the directory does not exist, it will be created."
        ),
    )


@pytest.mark.trylast
def pytest_configure(config):
    """Set all the options before the test run."""
    # The help printing uses the terminalreporter,
    # which is unregistered by the streaming mode.
    if config.option.help:
        return

    global ENABLED
    ENABLED = (
        config.option.tap_stream
        or config.option.tap_combined
        or config.option.tap_files
    )

    tracker.outdir = config.option.tap_outdir
    tracker.combined = config.option.tap_combined
    if config.option.tap_stream:
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
    option = session.config.option
    if ENABLED and (option.tap_stream or option.tap_combined):
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
        reason = ""
        # pytest adds an ugly "reason: " for expectedFailure
        # even though the standard library doesn't accept a reason for that decorator.
        # Ignore the "reason: " from pytest.
        if report.wasxfail and report.wasxfail != "reason: ":
            reason = ": {}".format(report.wasxfail)

        if report.skipped:
            directive = "TODO expected failure{}".format(reason)
            tracker.add_not_ok(testcase, description, directive=directive)
        elif report.passed:
            directive = "TODO unexpected success{}".format(reason)
            tracker.add_ok(testcase, description, directive=directive)
    elif report.passed:
        tracker.add_ok(testcase, description)
    elif report.failed:
        diagnostics = _make_as_diagnostics(report)

        # pytest treats an unexpected success from unitest.expectedFailure as a failure.
        # To match up with TAPTestResult and the TAP spec, treat the pass
        # as an ok with a todo directive instead.
        if isinstance(report.longrepr, str) and "Unexpected success" in report.longrepr:
            tracker.add_ok(testcase, description, directive="TODO unexpected success")
            return

        # A strict xfail that passes (i.e., XPASS) should be marked as a failure.
        # The only indicator that strict xfail occurred for XPASS is to check longrepr.
        if isinstance(report.longrepr, str) and "[XPASS(strict)]" in report.longrepr:
            tracker.add_not_ok(
                testcase,
                description,
                directive="unexpected success: {}".format(report.longrepr),
            )
            return

        tracker.add_not_ok(testcase, description, diagnostics=diagnostics)
    elif report.skipped:
        reason = report.longrepr[2].split(":", 1)[1].strip()
        tracker.add_skip(testcase, description, reason)


def _make_as_diagnostics(report):
    """Format a report as TAP diagnostic output."""
    lines = report.longreprtext.splitlines(keepends=True)
    return format_as_diagnostics(lines)


def pytest_unconfigure(config):
    """Dump the results."""
    if ENABLED:
        tracker.generate_tap_reports()
