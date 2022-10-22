# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import sys
import shutil
import unittest
from func_timeout import func_set_timeout
from test.utility import no_stderrout, redirect_stdout, read_file

from gslab_make import clear_dir, start_makelog, remove_dir

from gslab_make import log_files_in_output, link_inputs

class TestOutputLog(unittest.TestCase):
            
    def setUp(self):
        with no_stderrout():
            clear_dir(['test/log/'])

    def make_paths(self, 
                   output_path, 
                   output_local_path = [], 
                   makelog_path = 'test/log/make.log', 
                   output_statslog = 'test/log/output_stats.log'):

        paths = {'makelog': makelog_path, 
                 'output_dir': output_path, 
                 'output_local_dir': output_local_path,
                 'output_statslog' : output_statslog}
            
        with no_stderrout():
            start_makelog(paths)

        return(paths)

    def check_makelog(self, paths):
        self.assertIn('Output logs successfully written!', read_file(paths['makelog']))

    def check_logs(self, paths):
        self.check_makelog(paths)
        self.assertIn('file.txt', read_file(paths['output_statslog']))

    def test_log_output(self):     
        with no_stderrout():
            paths = self.make_paths(output_path = 'test/raw/log_outputs/dir')
            log_files_in_output(paths)
            self.check_logs(paths)

    def test_log_output_space(self):     
        with no_stderrout():
            paths = self.make_paths(output_path = 'test/raw/log_outputs/dir space')
            log_files_in_output(paths)
            self.check_makelog(paths)
            self.assertIn('file space.txt', read_file(paths['output_statslog']))

    def test_log_output_no_log(self):     
        with no_stderrout():
            paths = self.make_paths(output_path = 'test/raw/log_outputs/dir', 
                                    output_statslog = '')
            log_files_in_output(paths)
            self.check_makelog(paths)
            self.assertFalse(os.path.isfile(paths['output_statslog']))

    def test_log_output_local(self):     
        with no_stderrout():
            paths = self.make_paths(output_path = 'test/raw/log_outputs/dir', 
                                    output_local_path = ['test/raw/log_outputs/dir_local'])
            log_files_in_output(paths)
            self.check_logs(paths)
            self.assertIn('file_local.txt', read_file(paths['output_statslog']))

    def test_log_output_local_string(self):     
        with no_stderrout():
            paths = self.make_paths(output_path = 'test/raw/log_outputs/dir', 
                                    output_local_path = 'test/raw/log_outputs/dir_local')
            log_files_in_output(paths)
            self.check_logs(paths)
            self.assertIn('file_local.txt', read_file(paths['output_statslog']))

    def test_log_output_depth_zero(self):     
        with no_stderrout():
            paths = self.make_paths(output_path = 'test/raw/log_outputs/dir_depth')
            log_files_in_output(paths, depth = 0)
            self.assertIn('depth_1.txt', read_file(paths['output_statslog']))
            self.assertNotIn('depth_2.txt', read_file(paths['output_statslog']))

    def test_log_output_depth_one(self):     
        with no_stderrout():
            paths = self.make_paths(output_path = 'test/raw/log_outputs/dir_depth')
            log_files_in_output(paths, depth = 1)
            self.assertIn('depth_1.txt', read_file(paths['output_statslog']))
            self.assertIn('depth_2.txt', read_file(paths['output_statslog']))

    @func_set_timeout(60)
    def test_log_output_depth_recursive(self):  
        """
        Note
        ----
        For some reason, recursive symlinks don't actually break as expected.
        Python just stops walking the recursive directory at a certain point.
        """    
        with no_stderrout():
            paths = {'makelog': 'test/log/make.log', 
                     'input_dir': 'test/input',
                     'output_dir': 'test/input',  
                     'output_statslog': 'test/log/output_stats.log'}

            start_makelog(paths)
            link_inputs(paths, ['test/raw/log_outputs/recursion.txt'])
            log_files_in_output(paths)

    def test_error_bad_path(self):     
        with no_stderrout():
            try:
                paths = {}
                log_files_in_output(paths)
                self.check_logs(paths)
            except Exception as e:
                self.assertRaises(Exception, e)
                
    def tearDown(self):
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')
        if os.path.isdir('test/input/'):
            remove_dir(['test/input/'], quiet = True)

if __name__ == '__main__':
    unittest.main()