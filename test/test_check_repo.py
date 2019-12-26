import unittest
import sys
import os
import shutil
from test.utility import no_stderrout, redirect_stdout, read_file

from gslab_make import start_makelog, clear_dir
    
from gslab_make import check_module_size

class TestCheckModuleSize(unittest.TestCase):

    def setUp(self):
        with no_stderrout():
            clear_dir(['test/output/', 'test/log'])

    def make_paths(self, 
                   makelog_path = 'test/log/make.log', 
                   config_path = 'test/raw/config/config.yaml'):
    
        paths = {'makelog': makelog_path, 
                 'config': config_path}

        with no_stderrout():
            start_makelog(paths)
            
        return(paths)
    
    def test_module_size(self):     
        paths = self.make_paths()
        check_module_size(paths)

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()