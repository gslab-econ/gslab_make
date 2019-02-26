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
            clear_dir(['output/', 'log'])

    def test_log(self):
        makelog = {'makelog' : 'log/make.log'}
        with nostderrout():
            start_makelog(makelog)
            run_stata(makelog, program = 'gslab_make/tests/input/stata_test_script.do')
        self.assertIn('end of do-file', open(makelog['makelog']).read())

    def test_independent_log(self):
        makelog = {'makelog' : 'log/make.log'}
        independent_log = {'makelog' : 'log/stata.log'}
        with nostderrout():
            start_makelog(makelog)
            run_stata(makelog, program = 'gslab_make/tests/input/stata_test_script.do', log=independent_log['makelog'])
        self.assertIn('end of do-file', open(makelog['makelog']).read())
        self.assertTrue(os.path.isfile('log/stata.log'))
        self.assertIn('end of do-file', open(independent_log['makelog']).read())
        
    def test_executable(self):
        makelog = {'makelog' : 'log/make.log'}
        with nostderrout():
            start_makelog(makelog)
            run_stata(makelog, program = 'gslab_make/tests/input/stata_test_script.do', executable = metadata.default_executables[os.name]['stata']) 
        self.assertIn('end of do-file', open(makelog['makelog']).read())
    
    def test_path_with_space(self):
        makelog = {'makelog' : 'log/make.log'}
        with nostderrout():
            start_makelog(makelog)
            run_stata(makelog, program = 'gslab_make/tests/input/stata_test_script copy.do', executable = metadata.default_executables[os.name]['stata']) 
        self.assertIn('end of do-file', open(makelog['makelog']).read())

    def test_bad_executable(self):
        makelog = {'makelog' : 'log/make.log'}
        with nostderrout():
            start_makelog(makelog)
        with self.assertRaises(CritError):
            run_stata(makelog, program = 'gslab_make/tests/input/stata_test_script.do', executable = 'nonexistent_stata_executable')
        self.assertNotIn('end of do-file', open(makelog['makelog']).read())
    
    def test_no_program(self):
        makelog = {'makelog' : 'log/make.log'}
        with nostderrout():
            start_makelog(makelog)
        with self.assertRaises(Exception):
            run_stata(makelog, program = 'gslab_make/tests/input/nonexistent_stata_script.do')
        self.assertNotIn('end of do-file', open(makelog['makelog']).read())
    
    def tearDown(self):
        if os.path.isdir('output/'):
            shutil.rmtree('output/')
        if os.path.isdir('log/'):
            shutil.rmtree('log/')
        if os.path.isfile('output.txt'):
            os.remove('output.txt')
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()