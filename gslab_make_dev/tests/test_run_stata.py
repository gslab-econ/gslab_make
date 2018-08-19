#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make_dev.make_log import start_make_logging
from gslab_make_dev.dir_mod import clear_dirs
from gslab_make_dev.run_program import run_stata
from nostderrout import nostderrout
import gslab_make_dev.private.metadata as metadata
    

class testRunStata(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_dirs(output_dir)
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do')
        self.assertIn('end of do-file', open('../output/make.log').read())
        
    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():    
            clear_dirs(output_dir)
            start_make_logging(makelog_file)
            run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do', makelog = '../output/custom_make.log')
        self.assertIn('end of do-file', open('../output/custom_make.log').read())

    def test_independent_log(self):
        with nostderrout():
            run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do', log = '../output/stata.log')
        self.assertIn('end of do-file', open('../output/make.log').read())
        self.assertTrue(os.path.isfile('../output/stata.log'))
        self.assertIn('end of do-file', open('../output/stata.log').read())
        
    def test_no_extension(self):
        with nostderrout():
            run_stata(program = 'gslab_make_dev/tests/input/stata_test_script')
        self.assertIn('end of do-file', open('../output/make.log').read())
        
    def test_executable(self):
        with nostderrout():
			run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do', executable = metadata.default_executables[os.name]['stata']) 
        self.assertIn('end of do-file', open('../output/make.log').read())
        
    def test_bad_executable(self):
        with nostderrout():
            run_stata(program = 'gslab_make_dev/tests/input/stata_test_script.do', executable = 'nonexistent_stata_executable')
        self.assertFalse('end of do-file' in open('../output/make.log').read())
    
    def test_no_program(self):
        with nostderrout():
            run_stata(program = 'gslab_make_dev/tests/input/nonexistent_stata_script.do')
        self.assertFalse('end of do-file' in open('../output/make.log').read())
    
    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isdir('./output/'):
            shutil.rmtree('./output/')    
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
