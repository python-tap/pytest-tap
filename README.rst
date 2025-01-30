pytest-tap
==========

|version| |license| |coverage|

.. |version| image:: https://img.shields.io/pypi/v/pytest-tap.svg
    :target: https://pypi.python.org/pypi/pytest-tap
    :alt: PyPI version
.. |license| image:: https://img.shields.io/pypi/l/pytest-tap.svg
    :target: https://raw.githubusercontent.com/python-tap/pytest-tap/master/LICENSE
    :alt: BSD license

Test Anything Protocol (TAP) reporting plugin for
`pytest <http://pytest.org/latest/>`_

The plugin outputs test results as TAP data in a variety of formats.
See the `tappy documentation <http://tappy.readthedocs.io/en/latest/producers.html#pytest-tap-plugin>`_
for more information on usage.

Install
-------

.. code-block:: console

   $ pip install pytest-tap

Usage
-----

This is an example usage from the plugin's test suite.

.. code-block:: console

   $ pytest --tap
   1..12
   ok 1 tests/test_help.py::test_includes_options
   ok 2 tests/test_help.py::test_handle_help_with_stream
   ok 3 tests/test_plugin.py::test_stream
   ok 4 tests/test_plugin.py::test_stream_simple_flag
   ok 5 tests/test_plugin.py::test_combined
   ok 6 tests/test_plugin.py::test_files
   ok 7 tests/test_plugin.py::test_outdir
   ok 8 tests/test_plugin.py::test_xfail_no_reason
   ok 9 tests/test_plugin.py::test_xfail_nonstrict
   ok 10 tests/test_plugin.py::test_xfail_strict
   ok 11 tests/test_plugin.py::test_unittest_expected_failure
   ok 12 tests/test_plugin.py::test_setup_failure

Contributing
------------

The project welcomes contributions of all kinds.
Check out the `contributing guidelines <https://github.com/python-tap/pytest-tap/blob/master/.github/contributing.md>`_
for tips on how to get started.
