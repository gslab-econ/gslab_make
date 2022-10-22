# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
                      
import os
import re
import sys
import shutil
import unittest
from test.utility import no_stderrout, redirect_stdout, create_file, read_file

from gslab_make import clear_dir

from gslab_make import start_makelog, end_makelog, write_to_makelog

class TestMakeLog(unittest.TestCase):
            
    def setUp(self):
        with no_stderrout():
            clear_dir(['test/log/'])

    def make_paths(self, makelog_path = 'test/log/make.log'):
        paths = {'makelog': makelog_path}
            
        return(paths)

    def check_makelog(self, paths):
        makelog = read_file(paths['makelog'])
        self.assertTrue(re.search('Makelog started: ', makelog))
        self.assertTrue(re.search('Hello, World!', makelog))
        self.assertTrue(re.search('Makelog ended: ', makelog))

    def test_makelog(self):     
        with no_stderrout():
            paths = self.make_paths()
            start_makelog(paths)
            write_to_makelog(paths, 'Hello, World!')
            end_makelog(paths)
            self.check_makelog(paths)

    def test_makelog_space(self):     
        with no_stderrout():
            paths = self.make_paths(makelog_path = 'test/log/make space.log')
            start_makelog(paths)
            write_to_makelog(paths, 'Hello, World!')
            end_makelog(paths)
            self.check_makelog(paths)

    def test_error_bad_paths(self):     
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = {}
                start_makelog(paths)
                write_to_makelog(paths, 'Hello, World!')
                end_makelog(paths)

    def test_error_no_makelog(self):     
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                write_to_makelog(paths, 'Hello, World!')
                end_makelog(paths)

    def tearDown(self):
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()