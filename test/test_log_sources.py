import unittest
import sys
import os
import shutil
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

    def check_log(self, paths):
        self.assertIn('Source logs successfully written!', read_file(paths['makelog']))
        self.assertIn('dir', read_file(paths['source_maplog']))
        self.assertIn('file.txt', read_file(paths['source_statslog']))

    def test_log_output(self):     
        with no_stderrout():
            paths = self.make_paths()
            inputs = link_inputs(paths, ['test/raw/log_sources/move.txt'])
            write_source_logs(paths, inputs)
            self.check_log(paths)

    def tear_Down(self):
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()