# -- Path setup --------------------------------------------------------------

import os
import sys
from datetime import datetime
import sphinx_rtd_theme
from sphinx.ext.napoleon.docstring import GoogleDocstring

sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------

project = 'GSLab Make'
copyright = '%s, Matthew Gentzkow' % datetime.today().year
author = 'Matthew Gentzkow'
release = '2.0.0'

# -- General configuration ---------------------------------------------------

extensions = ['sphinx.ext.autodoc', 
              'sphinx.ext.napoleon', 
              'sphinx_rtd_theme']

# -- Extensions to Napoleon --------------------------------------------------

def parse_keys_section(self, section):
    return self._format_fields('Path Keys', self._consume_fields())

GoogleDocstring._parse_keys_section = parse_keys_section

def patched_parse(self):
    self._sections['path keys'] = self._parse_keys_section
    self._unpatched_parse()

GoogleDocstring._unpatched_parse = GoogleDocstring._parse
GoogleDocstring._parse = patched_parse

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = []

add_module_names = False
autodoc_default_options = {
    'member-order': 'bysource'
}