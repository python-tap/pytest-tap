Releases
========

Version 2.4, To Be Released
---------------------------

* Handle failures that occur from setup.
  This will catch errors that may happen in fixtures.
* Drop support for Python 3.4 (it is end-of-life).
* Add support for Python 3.7.

Version 2.3, September 16, 2018
-------------------------------

* Improve xfail handling.
  Honor strict xfail mode.
  Use TODO instead of SKIP directive to better align with TAP specification.
* Output the plan line (``1..N``) first.

Version 2.2, January 9, 2018
----------------------------

* Update output format to match closer to pytest styling.
* Drop support for Python 3.3 (it is end-of-life).

Version 2.1, August 12, 2017
----------------------------

* Add support for Python 3.6.
* Fix crash when running with pytest-xdist (#27).

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
