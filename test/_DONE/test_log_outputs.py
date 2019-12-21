import unittest
import sys
import os
import shutil
from test.utility import no_stderrout, redirect_stdout, read_file
from gslab_make import clear_dir, start_makelog

from gslab_make.write_logs import log_files_in_output

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

    def test_log_output_character(self):     
        with no_stderrout():
            paths = self.make_paths(output_path = 'test/raw/log_outputs/dir_╬▓')
            log_files_in_output(paths)
            self.check_makelog(paths)
            self.assertIn('file_╬▓.txt', read_file(paths['output_statslog']))

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

    def test_log_output_string(self):     
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

    def test_error_bad_path(self):     
        with no_stderrout():
            try:
                paths = {}
                log_files_in_output(paths)
                self.check_logs(paths)
            except Exception as e:
                self.assertRaises(Exception, e)
                
    def tear_Down(self):
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()