import contextlib
import sys

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

def create_file(path):
    with open(path, 'w') as f:
            f.write('')