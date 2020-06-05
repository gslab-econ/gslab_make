Testing instructions
--------------------
From the root directory of the repository, use the following shell command:
```
python -m unittest discover
```

`unittest` will automatically run any scripts that begin with `test`. To exclude a test script, append a non-test prefix.

Currently, certain test scripts have been excluded with the prefix `EXCLUDE_` in order to implement continuous integration testing with Github Actions. To run the full suite of tests, include these test scripts by removing the `EXCLUDE_` prefix.

Todo
----
- Test `test_matlab.py` with a machine that has the latest version of Matlab
- Finish `test_latex.py` to include additional tests for TeX
- Add `test_jupyter.py` to contain tests for Jupyter Notebooks
- Refactor exception checks in unit tests to be more specific in type of exception to confirm
