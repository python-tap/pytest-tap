Releases
========

Version 2.0, August 1, 2016
---------------------------

* Update to tap.py 2.0.
  This update drops the indirect dependencies on nose and pygments.
* Improve handling of skips and xfails.
* Suppress ``# TAP results for TestCase`` for streaming.
  This header makes little sense for pytest's test function paradigm.
  Including the header generated extra noise for each function.
* Drop support for Python 2.6

Version 1.9, Released June 11, 2016
-----------------------------------

* Initial release as stand-alone plugin.
  The version number aligns with tappy.
