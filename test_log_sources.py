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

    @func_set_timeout(60)
    def test_log_output_depth_recursive(self):    
        """
        Note
        ----
        For some reason, recursive symlinks don't actually break as expected.
        Python just stops walking the recursive directory at a certain point.
        Investigate when time allows.
        """ 
        with no_stderrout():
            paths = self.make_paths()
            inputs = link_inputs(paths, ['test/raw/log_sources/move_recursion.txt'])
            write_source_logs(paths, inputs)

    def tear_Down(self):
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()