from tap.tracker import ENABLE_VERSION_13


def test_stream(testdir, sample_test_file):
    """Results are streamed to stdout."""
    result = testdir.runpytest_subprocess("--tap-stream")

    result.stdout.fnmatch_lines(
        [
            "1..6",
            "ok 1 test_stream.py::test_ok",
            "not ok 2 test_stream.py::test_not_ok",
            "ok 3 test_stream.py::test_params[foo]",
            "ok 4 test_stream.py::test_params[bar]",
            "ok 5 test_stream.py::test_skipped # SKIP some reason",
            "not ok 6 test_stream.py::test_broken # TODO expected failure: a reason",
        ]
    )


def test_stream_simple_flag(testdir, sample_test_file):
    """Results are streamed to stdout when the shorter streaming flag."""
    result = testdir.runpytest_subprocess("--tap")

    result.stdout.fnmatch_lines(
        [
            "1..6",
            "ok 1 test_stream_simple_flag.py::test_ok",
            "not ok 2 test_stream_simple_flag.py::test_not_ok",
            "ok 3 test_stream_simple_flag.py::test_params[foo]",
            "ok 4 test_stream_simple_flag.py::test_params[bar]",
            "ok 5 test_stream_simple_flag.py::test_skipped # SKIP some reason",
            "not ok 6 test_stream_simple_flag.py::test_broken "
            "# TODO expected failure: a reason",
        ]
    )


def test_combined(testdir, sample_test_file):
    """Tests are combined into a single output file."""
    testdir.runpytest_subprocess("--tap-combined")

    testresults = testdir.tmpdir.join("testresults.tap")
    assert testresults.check()
    actual_results = [
        line.strip() for line in testresults.readlines() if not line.startswith("#")
    ]
    expected_results = [
        "1..6",
        "ok 1 test_combined.py::test_ok",
        "not ok 2 test_combined.py::test_not_ok",
        "ok 3 test_combined.py::test_params[foo]",
        "ok 4 test_combined.py::test_params[bar]",
        "ok 5 test_combined.py::test_skipped # SKIP some reason",
        "not ok 6 test_combined.py::test_broken # TODO expected failure: a reason",
    ]
    # If the dependencies for version 13 happen to be installed, tweak the output.
    if ENABLE_VERSION_13:
        expected_results.insert(0, "TAP version 13")
    assert actual_results == expected_results


def test_files(testdir, sample_test_file):
    """Tests are split into separate files."""
    testdir.makepyfile(
        test_other_file="""
        def test_other_ok():
            assert True
    """
    )

    testdir.runpytest_subprocess("--tap-files")

    sample_tap = testdir.tmpdir.join("test_files.py.tap")
    assert sample_tap.check()
    other_tap = testdir.tmpdir.join("test_other_file.py.tap")
    assert other_tap.check()


def test_outdir(testdir, sample_test_file):
    """Tests are put in the output directory."""
    testdir.runpytest_subprocess("--tap-outdir", "results", "--tap-combined")

    outdir = testdir.tmpdir.join("results")
    testresults = outdir.join("testresults.tap")
    assert testresults.check()


def test_logging(testdir, sample_test_file):
    """Test logs are added to TAP diagnostics."""
    result = testdir.runpytest_subprocess("--tap", "--tap-logging", "all")
    result.stdout.fnmatch_lines(
        [
            "# --- Captured Log ---",
            "*Running test_not_ok*",
            "# --- Captured Out ---",
            "# --- Captured Err ---",
        ]
    )


def test_log_passing_tests(testdir, sample_test_file):
    """Test logs are added to TAP diagnostics."""
    result = testdir.runpytest_subprocess(
        "--tap",
        "--tap-logging",
        "log",
        "--tap-log-passing-tests",
        "--log-level",
        "INFO",
    )
    result.stdout.fnmatch_lines(
        [
            "# --- Captured Log ---",
            "*Running test_ok*",
        ]
    )


def test_xfail_no_reason(testdir):
    """xfails output gracefully when no reason is provided."""
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.xfail(strict=False)
        def test_unexpected_success():
            assert True

        @pytest.mark.xfail(strict=False)
        def test_expected_failure():
            assert False
    """
    )
    result = testdir.runpytest_subprocess("--tap")

    result.stdout.fnmatch_lines(
        [
            "ok 1 test_xfail_no_reason.py::test_unexpected_success "
            "# TODO unexpected success",
            "not ok 2 test_xfail_no_reason.py::test_expected_failure "
            "# TODO expected failure",
        ]
    )


def test_xfail_nonstrict(testdir):
    """Non-strict xfails are treated as TODO directives."""
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.xfail(strict=False, reason='a reason')
        def test_unexpected_success():
            assert True

        @pytest.mark.xfail(strict=False, reason='a reason')
        def test_expected_failure():
            assert False
    """
    )
    result = testdir.runpytest_subprocess("--tap")

    result.stdout.fnmatch_lines(
        [
            "ok 1 test_xfail_nonstrict.py::test_unexpected_success "
            "# TODO unexpected success: a reason",
            "not ok 2 test_xfail_nonstrict.py::test_expected_failure "
            "# TODO expected failure: a reason",
        ]
    )


def test_xfail_strict(testdir):
    """xfail strict mode handles expected behavior."""
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.xfail(strict=True, reason='a reason')
        def test_unexpected_success():
            assert True

        @pytest.mark.xfail(strict=True, reason='a reason')
        def test_expected_failure():
            assert False
    """
    )
    result = testdir.runpytest_subprocess("--tap")

    result.stdout.fnmatch_lines(
        [
            "not ok 1 test_xfail_strict.py::test_unexpected_success "
            "# unexpected success: [XPASS(strict)] a reason",
            "not ok 2 test_xfail_strict.py::test_expected_failure "
            "# TODO expected failure: a reason",
        ]
    )


def test_unittest_expected_failure(testdir):
    """The plugin handles unittest's expectedFailure decorator behavior."""
    testdir.makepyfile(
        """
        import pytest
        import unittest

        class TestExpectedFailure(unittest.TestCase):
            @unittest.expectedFailure
            def test_when_failing(self):
                assert False

            @unittest.expectedFailure
            def test_when_passing(self):
                assert True
    """
    )
    result = testdir.runpytest_subprocess("--tap")

    expected = [
        "not ok 1 test_unittest_expected_failure.py::"
        "TestExpectedFailure.test_when_failing # TODO expected failure",
        "ok 2 test_unittest_expected_failure.py::"
        "TestExpectedFailure.test_when_passing # TODO unexpected success",
    ]
    result.stdout.fnmatch_lines(expected)


def test_setup_failure(testdir):
    """A failure in test setup is marked as an error.

    See https://github.com/python-tap/pytest-tap/issues/39.
    """
    testdir.makepyfile(
        """
        import pytest

        @pytest.fixture
        def bad_fixture():
            raise Exception('boom')

        def test_with_bad_fixture(bad_fixture):
            assert True
    """
    )
    result = testdir.runpytest_subprocess("--tap")

    result.stdout.fnmatch_lines(
        ["1..1", "not ok 1 test_setup_failure.py::test_with_bad_fixture"]
    )
