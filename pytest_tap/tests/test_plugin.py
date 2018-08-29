# Copyright (c) 2018, Matt Layman

# try:
#     from unittest import mock
# except ImportError:
#     import mock
# import tempfile
# import unittest

import pytest

# from tap.tracker import Tracker

# from pytest_tap import plugin


@pytest.fixture
def sample_test_file(testdir):
    testdir.makepyfile(
        """
        import pytest

        def test_ok():
            assert True

        def test_not_ok():
            assert False

        @pytest.mark.skip(reason='some reason')
        def test_skipped():
            assert False

        @pytest.mark.xfail
        def test_broken():
            assert False
    """
    )


def test_includes_options(testdir):
    """All options are present in the help."""
    result = testdir.runpytest("--help")

    result.stdout.fnmatch_lines(
        ["*--tap-stream*", "*--tap-files*", "*--tap-combined*", "*--tap-outdir=path*"]
    )


def test_stream(testdir, sample_test_file):
    """Results are streamed to stdout."""
    result = testdir.runpytest_subprocess("--tap-stream")

    result.stdout.fnmatch_lines(
        [
            "ok 1 test_stream.py::test_ok",
            "not ok 2 test_stream.py::test_not_ok",
            "ok 3 test_stream.py::test_skipped # SKIP some reason",
            "ok 4 test_stream.py::test_broken # SKIP ",
            "1..4",
        ]
    )


def test_combined(testdir, sample_test_file):
    """Tests are combined into a single output file."""
    testdir.runpytest_subprocess("--tap-combined")

    testresults = testdir.tmpdir.join("testresults.tap")
    assert testresults.check()


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
