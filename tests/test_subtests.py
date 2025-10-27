import pytest
from tap.tracker import ENABLE_VERSION_13


@pytest.mark.subtests
def test_log_subtests_stream(testdir):
    """Subtests are added individually to stream."""
    testdir.makepyfile(
        """
        import pytest

        def test_subtests(subtests):
            for i in range(2):
                with subtests.test(msg="sub_msg", i=i):
                    assert i % 2 == 0
    """
    )
    result = testdir.runpytest_subprocess("--tap")

    result.stdout.fnmatch_lines(
        [
            "ok 1 test_log_subtests_stream.py::test_subtests[sub_msg] (i=0)",
            "not ok 2 test_log_subtests_stream.py::test_subtests[sub_msg] (i=1)",
            "ok 3 test_log_subtests_stream.py::test_subtests",
            "1..3",
        ]
    )


@pytest.mark.subtests
def test_log_subtests_combined(testdir):
    """Subtests are added individually to combined."""
    testdir.makepyfile(
        """
        import pytest

        def test_subtests(subtests):
            for i in range(2):
                with subtests.test(msg="sub_msg", i=i):
                    assert i % 2 == 0
    """
    )
    testdir.runpytest_subprocess("--tap-combined")
    testresults = testdir.tmpdir.join("testresults.tap")
    assert testresults.check()
    actual_results = [
        line.strip() for line in testresults.readlines() if not line.startswith("#")
    ]

    expected_results = [
        "1..3",
        "ok 1 test_log_subtests_combined.py::test_subtests[sub_msg] (i=0)",
        "not ok 2 test_log_subtests_combined.py::test_subtests[sub_msg] (i=1)",
        "ok 3 test_log_subtests_combined.py::test_subtests",
    ]

    # If the dependencies for version 13 happen to be installed, tweak the output.
    if ENABLE_VERSION_13:
        expected_results.insert(0, "TAP version 13")
    assert actual_results == expected_results
