#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make.write_logs import start_makelog
from gslab_make.dir_mod import clear_dir
from gslab_make.run_program import run_r
from nostderrout import nostderrout
    

class testRunR(unittest.TestCase):

    def setUp(self):
        makelog = {'makelog' : 'log/make.log'}
        log_dir = 'log/'
        output_dir = 'output/'
        with nostderrout():
            clear_dir([output_dir, log_dir])
            start_makelog(makelog)

    def test_log(self):
        makelog = {'makelog' : 'log/make.log'}
        with nostderrout():
            run_r(makelog, program = 'gslab_make/tests/input/R_test_script.R')      
        logfile_data = open('log/make.log', 'rU').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_independent_log(self):
        makelog = {'makelog' : 'log/make.log'}
        independent_log = {'makelog' : 'log/R.log'}
        with nostderrout():
            start_makelog(makelog)
            run_r(makelog, program = 'gslab_make/tests/input/R_test_script.R', log=independent_log['makelog'])
        self.assertIn('Test script complete', open(makelog['makelog'], 'rU').read())
        self.assertTrue(os.path.isfile('log/R.log'))
        self.assertIn('Test script complete', open(independent_log['makelog'], 'rU').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_executable(self):
        makelog = {'makelog' : 'log/make.log'}
        with nostderrout():
            run_r(makelog, program = 'gslab_make/tests/input/R_test_script.R', executable = 'R CMD BATCH') 
        self.assertNotIn('Test script complete', open(makelog['makelog'], 'rU').read()) # check this
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_bad_executable(self):
        makelog = {'makelog' : 'log/make.log'}
        with self.assertRaises(Exception):
            run_r(makelog, program = 'gslab_make/tests/input/R_test_script.R', executable = 'nonexistent_R_executable')
        self.assertNotIn('Test script complete', open(makelog['makelog'], 'rU').read()) # check this
   
    def test_no_program(self):
        makelog = {'makelog' : 'log/make.log'}
    	with self.assertRaises(Exception):
             run_r(makelog, program = 'gslab_make/tests/input/nonexistent_R_script.R')
        logfile_data = open('log/make.log', 'rU').readlines()
        self.assertNotIn('Test script complete', open(makelog['makelog'], 'rU').read())
    
    def test_option(self):
        makelog = {'makelog' : 'log/make.log'}
        with nostderrout():
            run_r(makelog, program = 'gslab_make/tests/input/R_test_script.R', option = '--slave')
        logfile_data = open(makelog['makelog'], 'rU').read()
        self.assertIn('Test script complete', logfile_data)      
        self.assertTrue(os.path.isfile('output.txt'))
    
    def test_r_error(self):
        makelog = {'makelog' : 'log/make.log'}
        with self.assertRaises(Exception):
            run_r(makelog, program = 'gslab_make/tests/input/R_test_script_error.R')
        self.assertIn('executed with errors', open(makelog['makelog'], 'rU').read())
        
    def tearDown(self):
        if os.path.isdir('output/'):
            shutil.rmtree('output/')
        if os.path.isdir('log/'):
            shutil.rmtree('log/')
        if os.path.isfile('output.txt'):
            os.remove('output.txt')
        if os.path.isfile('gslab_make/tests/input/output.txt'):
            os.remove('gslab_make/tests/input/output.txt')                
        if os.path.isfile('.RData'):
            os.remove('.RData')
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
