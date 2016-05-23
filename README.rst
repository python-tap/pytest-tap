pytest-tap
==========

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

   $ py.test --tap-stream
   # TAP results for TestPlugin
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
   1..12
