
# Sphinx 

Sphinx is a tool that allows you to easily create formatted Python documentation. Sphinx also imports docstrings to create autodocumentation. See here for further [detail](http://www.sphinx-doc.org/en/master/).

Requirements
------------
- Python 3

```
pip install sphinx
pip install sphinx_rtd_theme
pip install sphinx-automodapi
```

Compiling instructions
----------------------
1. Delete all files/directories in `docs` except `README.md` and `docs/sphinx`.

2. From the `docs/sphinx` directory, use the following shell command:

```
make html
```

3. Copy over the files in `docs/sphinx/build/html` to `docs`.

Notes
-----
- `audodoc` only documents functions in the package that are public. See [here](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) for more detail.

- `docs/sphinx/source/pages/dummy.rst` is just a dummy page so that `sphinx_automodapi.automodapi` can automatically generate individual pages for each function in the package.
- These individual pages can be found in `docs/sphinx/source/pages/api`. This allows us to add links for each function to the sidebar table of contents.
- `sphinx.ext.autosectionlabel` allows us to properly reference the page for a function.