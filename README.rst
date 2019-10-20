pytest-tap
==========

|version| |license| |travis| |travismac| |appveyor| |coverage|

.. |version| image:: https://img.shields.io/pypi/v/pytest-tap.svg
    :target: https://pypi.python.org/pypi/pytest-tap
    :alt: PyPI version
.. |license| image:: https://img.shields.io/pypi/l/pytest-tap.svg
    :target: https://raw.githubusercontent.com/python-tap/pytest-tap/master/LICENSE
    :alt: BSD license
.. |downloads| image:: https://img.shields.io/pypi/dm/pytest-tap.svg
    :target: https://pypi.python.org/pypi/pytest-tap
    :alt: Downloads
.. |travis| image:: https://img.shields.io/travis/python-tap/pytest-tap/master.svg?label=linux+build
    :target: https://travis-ci.org/python-tap/pytest-tap
    :alt: Linux status
.. |travismac| image:: https://img.shields.io/travis/python-tap/pytest-tap/master.svg?label=macOS+build
    :target: https://travis-ci.org/python-tap/pytest-tap
    :alt: macOS status
.. |appveyor| image:: https://img.shields.io/appveyor/ci/mblayman/pytest-tap/master.svg?label=windows+build
    :target: https://ci.appveyor.com/project/mblayman/pytest-tap
    :alt: Windows status
.. |coverage| image:: https://img.shields.io/codecov/c/github/python-tap/pytest-tap.svg
    :target: https://codecov.io/github/python-tap/pytest-tap
    :alt: Coverage

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

   $ pytest --tap-stream
   1..12
   ok 1 - TestPlugin.test_generates_reports_for_combined
   ok 2 - TestPlugin.test_generates_reports_for_files
   ok 3 - TestPlugin.test_generates_reports_for_stream
   ok 4 - TestPlugin.test_includes_options
   ok 5 - TestPlugin.test_skips_reporting_with_no_output_option
   ok 6 - TestPlugin.test_track_when_call_report
   ok 7 - TestPlugin.test_tracker_combined_set
   ok 8 - TestPlugin.test_tracker_outdir_set
   ok 9 - TestPlugin.test_tracker_stream_set
   ok 10 - TestPlugin.test_tracks_not_ok
   ok 11 - TestPlugin.test_tracks_ok
   ok 12 - TestPlugin.test_tracks_skip

Contributing
------------

The project welcomes contributions of all kinds.
Check out the `contributing guidelines <https://github.com/python-tap/pytest-tap/blob/master/.github/contributing.md>`_
for tips on how to get started.
