import re
import os
import io
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

def encode(string):
    """Clean string for encoding."""

    if (sys.version_info < (3, 0)):
        string = codecs.encode(string, 'utf-8') 

    return(string)

def norm_path(path):
    """Normalize path to be OS-compatible."""

    if path:
        path = re.split('[/\\\\]+', path)
        path = os.path.sep.join(path)
        path = os.path.expanduser(path)
        path = os.path.abspath(path)

    path = encode(path)

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