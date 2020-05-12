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
From the `docs/sphinx` directory, use the following shell command:

```
make html
```

Copy over the files in `docs/sphinx/build/html` to `docs`.