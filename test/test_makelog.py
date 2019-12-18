import unittest
import sys
import os
import shutil
from test.utility import no_stderrout, redirect_stdout, create_file
from gslab_make import clear_dir

from gslab_make.write_logs import start_makelog, end_makelog, write_to_makelog

class TestMakeLog(unittest.TestCase):
            
    def setUp(self):
        with no_stderrout():
            clear_dir(['test/log/'])

    def make_paths(self, makelog_path = 'test/log/make.log'):
        paths = {'makelog': makelog_path}
            
        return(paths)

    def check_makelog(self, paths):
        self.assertIn('Makelog started: ', open(paths['makelog']).read())
        self.assertIn('Hello, World!', open(paths['makelog']).read())
        self.assertIn('Makelog ended: ', open(paths['makelog']).read())

    def test_makelog(self):     
        with no_stderrout():
            paths = self.make_paths()
            start_makelog(paths)
            write_to_makelog(paths, 'Hello, World!')
            end_makelog(paths)
            self.check_makelog(paths)

    def test_makelog_character(self):     
        with no_stderrout():
            paths = self.make_paths(makelog_path = 'test/log/make_β.log')
            start_makelog(paths)
            write_to_makelog(paths, 'Hello, World! β')
            end_makelog(paths)
            self.check_makelog(paths)

    def test_error_bad_paths(self):     
        try:
            with no_stderrout():
                paths = {}
                start_makelog(paths)
                write_to_makelog(paths, 'Hello, World!')
                end_makelog(paths)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_no_makelog(self):     
        try:
            with no_stderrout():
                paths = self.make_paths()
                write_to_makelog(paths, 'Hello, World!')
                end_makelog(paths)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_makelog_not_started(self):     
        try:
            with no_stderrout():
                paths = self.make_paths()
                create_file('test/log/make.log')
                write_to_makelog(paths, 'Hello, World!')
                end_makelog(paths)
        except Exception as e:
            self.assertRaises(Exception, e)

    def tearDown(self):
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()