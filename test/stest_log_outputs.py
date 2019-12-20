import unittest
import sys
import os
import shutil
from test.utility import no_stderrout, redirect_stdout, read_file
from gslab_make import clear_dir, start_makelog

from gslab_make.write_logs import log_files_in_output

class TestMakeLog(unittest.TestCase):
            
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

    def check_log(self, paths):
        self.assertIn('Output logs successfully written!', read_file(paths['makelog']))
        self.assertIn('file.txt', read_file(paths['output_statslog']))

    def test_log_output(self):     
        with no_stderrout():
            paths = self.make_paths('test/raw/log_outputs/dir')
            log_files_in_output(paths)
            self.check_log(paths)

    def tear_Down(self):
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()