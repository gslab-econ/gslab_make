#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make.write_logs import start_makelog
from gslab_make.dir_mod import clear_dir
from gslab_make.run_program import run_stata
from nostderrout import nostderrout
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError
    

class testRunStata(unittest.TestCase):

    def setUp(self):
        with nostderrout():
            clear_dir(['../output/', '../log'])

    def test_default_log(self):
        default_makelog = {'makelog' : '../log/make.log'}
        with nostderrout():
            start_makelog(default_makelog)
            run_stata(default_makelog, program = 'gslab_make/tests/input/stata_test_script.do')
        self.assertIn('end of do-file', open(default_makelog['makelog']).read())
        
    def test_custom_log(self):
        makelog_file = {'makelog' : '../log/custom.log'}
        with nostderrout():
            start_makelog(makelog_file)
            run_stata(makelog_file, program = 'gslab_make/tests/input/stata_test_script.do')
        self.assertIn('end of do-file', open(makelog_file['makelog']).read())

    def test_independent_log(self):
        default_makelog = {'makelog' : '../log/make.log'}
        independent_log = {'makelog' : '../log/stata.log'}
        with nostderrout():
            start_makelog(independent_log)
            run_stata(independent_log, program = 'gslab_make/tests/input/stata_test_script.do')
        #self.assertIn('end of do-file', open(default_makelog['makelog']).read())
        self.assertTrue(os.path.isfile('../log/stata.log'))
        self.assertIn('end of do-file', open(independent_log['makelog']).read())
        
    def test_executable(self):
        default_makelog = {'makelog' : '../log/make.log'}
        with nostderrout():
            start_makelog(default_makelog)
            run_stata(default_makelog, program = 'gslab_make/tests/input/stata_test_script.do', executable = metadata.default_executables[os.name]['stata']) 
        self.assertIn('end of do-file', open(default_makelog['makelog']).read())
        
    def test_bad_executable(self):
        default_makelog = {'makelog' : '../log/make.log'}
        with nostderrout():
            start_makelog(default_makelog)
        with self.assertRaises(CritError):
            run_stata(default_makelog, program = 'gslab_make/tests/input/stata_test_script.do', executable = 'nonexistent_stata_executable')
        self.assertNotIn('end of do-file', open(default_makelog['makelog']).read())
    
    def test_no_program(self):
        default_makelog = {'makelog' : '../log/make.log'}
        with nostderrout():
            start_makelog(default_makelog)
        with self.assertRaises(Exception):
            run_stata(default_makelog, program = 'gslab_make/tests/input/nonexistent_stata_script.do')
        self.assertNotIn('end of do-file', open(default_makelog['makelog']).read())
    
    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isdir('../log/'):
            shutil.rmtree('../log/')
        if os.path.isfile('output.txt'):
            os.remove('output.txt')
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()