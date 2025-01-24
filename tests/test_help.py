def test_includes_options(testdir):
    """All options are present in the help."""
    result = testdir.runpytest("--help")

    expected_option_flags = [
        "*--tap *",
        "*--tap-files*",
        "*--tap-combined*",
        "*--tap-outdir=path*",
        "*--tap-logging*",
    ]
    result.stdout.fnmatch_lines(expected_option_flags)


def test_handle_help_with_stream(testdir):
    """The help prints when the stream option is given.

    This demonstrates behavior reported in:
    https://github.com/python-tap/pytest-tap/issues/59
    """
    result = testdir.runpytest("--tap", "-h")

    expected_option_flags = ["*--tap *"]
    result.stdout.fnmatch_lines(expected_option_flags)
