'''
This directory contains the `gslab_python_lite` library's unit tests. 
These tests can be run using
`python -m unittest discover`
or 
`python run_all_tests.py`
from `gslab_python_lite/tests/`. The latter command stores the test 
results in `gslab_python_lite/tests/log/make.log`.

The following inputs of these tests were created by running logs_for_textfill.do,
a Stata do file that is now stored in the subdirectory.
- legal.log
- alternative_prefix.log
- tags_not_closed.log
- tags_incorrectly_named.log
- tags_dont_match.log
'''

from nostderrout import nostderrout
