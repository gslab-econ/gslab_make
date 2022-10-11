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

from gslab_make import clear_dir, remove_dir, start_makelog

from gslab_make import write_source_logs, link_inputs

class TestMakeLog(unittest.TestCase):
            
    def setUp(self):
        with no_stderrout():
            remove_dir(['test/input/'])
            clear_dir(['test/log/'])

    def make_paths(self, 
                   makelog_path = 'test/log/make.log', 
                   input_path = 'test/input/', 
                   source_maplog_path = 'test/log/source_map.log',  
                   source_statslog_path = 'test/log/source_stats.log'):
    
        paths = {'makelog': makelog_path, 
                 'input_dir': input_path,
                 'source_maplog': source_maplog_path,  
                 'source_statslog': source_statslog_path}
            
        with no_stderrout():
            start_makelog(paths)

        return(paths)

    def check_makelog(self, paths):
        self.assertIn('Source logs successfully written!', read_file(paths['makelog']))

    def check_logs(self, paths):
        self.check_makelog(paths)
        self.assertIn('dir', read_file(paths['source_maplog']))
        self.assertIn('file.txt', read_file(paths['source_statslog']))

    def test_log_output(self):     
        with no_stderrout():
            paths = self.make_paths()
            inputs = link_inputs(paths, ['test/raw/log_sources/move.txt'])
            write_source_logs(paths, inputs)
            self.check_logs(paths)

    def test_log_output_space(self):     
        with no_stderrout():
            paths = self.make_paths()
            inputs = link_inputs(paths, ['test/raw/log_sources/move space.txt'])
            write_source_logs(paths, inputs)
            self.check_makelog(paths)
            self.assertIn('dir space', read_file(paths['source_maplog']))
            self.assertIn('file space.txt', read_file(paths['source_statslog']))

    def test_log_output_no_log(self):     
        with no_stderrout():
            paths = self.make_paths(source_maplog_path = '', 
                                    source_statslog_path = '')
            inputs = link_inputs(paths, ['test/raw/log_sources/move space.txt'])
            write_source_logs(paths, inputs)
            self.check_makelog(paths)
            self.assertFalse(os.path.isfile(paths['source_maplog']))
            self.assertFalse(os.path.isfile(paths['source_statslog']))

    def test_log_output_depth_zero(self):     
        with no_stderrout():
            paths = self.make_paths()
            inputs = link_inputs(paths, ['test/raw/log_sources/move_depth.txt'])
            write_source_logs(paths, inputs, depth = 0)
            self.assertIn('depth_1.txt', read_file(paths['source_statslog']))
            self.assertNotIn('depth_2.txt', read_file(paths['source_statslog']))

    def test_log_output_depth_one(self):     
        with no_stderrout():
            paths = self.make_paths()
            inputs = link_inputs(paths, ['test/raw/log_sources/move_depth.txt'])
            write_source_logs(paths, inputs, depth = 1)
            self.assertIn('depth_1.txt', read_file(paths['source_statslog']))
            self.assertIn('depth_2.txt', read_file(paths['source_statslog']))

    @func_set_timeout(60)
    def test_log_output_depth_recursive(self):    
        """
        Note
        ----
        For some reason, recursive symlinks don't actually break as expected.
        Python just stops walking the recursive directory at a certain point.
        """ 
        with no_stderrout():
            paths = self.make_paths()
            inputs = link_inputs(paths, ['test/raw/log_sources/move_recursion.txt'])
            write_source_logs(paths, inputs)

    def test_error_bad_path(self):     
        with no_stderrout():
            try:
                paths = {}
                inputs = link_inputs(paths, ['test/raw/log_sources/move space.txt'])
                write_source_logs(paths, inputs)
            except Exception as e:
                self.assertRaises(Exception, e)

    def tear_Down(self):
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()