# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import io
import re
import sys
import codecs
import contextlib

class Devnull(object):
    def write(self, _): pass

@contextlib.contextmanager
def no_stderrout():
    savestderr = sys.stderr
    savestdout = sys.stdout
    sys.stderr = Devnull()    
    sys.stdout = Devnull()
    try:
        yield
    finally:
        sys.stderr = savestderr
        sys.stdout = savestdout

@contextlib.contextmanager
def redirect_stdout(file):
    save_stdout = sys.stdout
    sys.stdout = file
    try:
        yield
    finally:
        sys.stdout = save_stdout

def norm_path(path):
    """Normalize path to be OS-compatible."""

    if path:
        path = re.split('[/\\\\]+', path)
        path = os.path.sep.join(path)
        path = os.path.expanduser(path)
        path = os.path.abspath(path)

    return(path)

def create_file(path):
    """Create file."""
    
    path = norm_path(path)

    with io.open(path, 'w', encoding = 'utf-8') as f:
        f.write('')

def read_file(path):
    """Read file."""

    path = norm_path(path)

    with io.open(path, 'r', encoding = 'utf-8') as f:
        content = f.read()

    return(content)