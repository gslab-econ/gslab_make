#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make.write_logs import start_makelog
from gslab_make.dir_mod import clear_dir
from gslab_make.run_program import run_perl
from nostderrout import nostderrout
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError
    

class testRunPerl(unittest.TestCase):

    def setUp(self):
        with nostderrout():
            clear_dir(['../output/', '../log'])

    def test_default_log(self):
    	default_makelog = {'makelog' : '../log/make.log'}
        with nostderrout():
            start_makelog(default_makelog)
            run_perl(default_makelog, program = 'gslab_make/tests/input/perl_test_script.pl')
        self.assertIn('Test script complete', open(default_makelog['makelog']).read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_custom_log(self):
        makelog_file = {'makelog' : '../log/custom_make.log'}
        with nostderrout():
            start_makelog(makelog_file)
            run_perl(makelog_file, program = 'gslab_make/tests/input/perl_test_script.pl')
        self.assertIn('Test script complete', open(makelog_file['makelog']).read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_independent_log(self):
    	default_makelog = {'makelog' : '../log/make.log'}
    	independent_log = {'makelog' : '../log/perl.log'}
        with nostderrout():
            start_makelog(independent_log)
            run_perl(independent_log, program = 'gslab_make/tests/input/perl_test_script.pl')
        # self.assertIn('Test script complete', open(default_makelog['makelog']).read())
        self.assertIn('Test script complete', open(independent_log['makelog']).read())        
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_executable(self):
    	default_makelog = {'makelog' : '../log/make.log'}
        with nostderrout():
            start_makelog(default_makelog)
            run_perl(default_makelog, program = 'gslab_make/tests/input/perl_test_script.pl', executable = metadata.default_executables[os.name]['perl']) 
        self.assertIn('Test script complete', open(default_makelog['makelog']).read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_bad_executable(self):
    	default_makelog = {'makelog' : '../log/make.log'}
        with nostderrout():
            start_makelog(default_makelog)
        with self.assertRaises(CritError):
            run_perl(default_makelog, program = 'gslab_make/tests/input/perl_test_script.pl', executable = 'nonexistent_perl_executable')
        self.assertNotIn('Test script complete', open(default_makelog['makelog']).read())

    def test_no_program(self):
    	default_makelog = {'makelog' : '../log/make.log'}
        with nostderrout():
            start_makelog(default_makelog)
        with self.assertRaises(Exception):
            run_perl(default_makelog, program = 'gslab_make/tests/input/nonexistent_perl_script.pl')
        self.assertNotIn('Test script complete', open(default_makelog['makelog']).read())
    
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
