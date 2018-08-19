#! /usr/bin/env perl

import unittest, sys, os, shutil, contextlib
from gslab_make_dev.make_log import start_make_logging
from gslab_make_dev.dir_mod import clear_dirs
from gslab_make_dev.run_program import run_perl
from nostderrout import nostderrout
import gslab_make_dev.private.metadata as metadata
    

class testRunPerl(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_dirs(output_dir)
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl')
        self.assertIn('Test script complete', open('../output/make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_dirs(output_dir)
            start_make_logging(makelog_file)
            run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl', makelog = '../output/custom_make.log')
        self.assertIn('Test script complete', open('../output/custom_make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_independent_log(self):
        with nostderrout():
            run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl', log = '../output/perl.log')
        self.assertIn('Test script complete', open('../output/make.log').read())
        self.assertTrue(os.path.isfile('../output/perl.log'))
        self.assertIn('Test script complete', open('../output/perl.log').read())        
        self.assertTrue(os.path.isfile('output.txt'))

    def test_no_extension(self):
        with nostderrout():
            run_perl(program = 'gslab_make_dev/tests/input/perl_test_script')
        self.assertIn('Test script complete', open('../output/make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_executable(self):
        with nostderrout():
            run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl', executable = metadata.default_executables[os.name]['perl']) 
        self.assertIn('Test script complete', open('../output/make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_bad_executable(self):
        with nostderrout():
            run_perl(program = 'gslab_make_dev/tests/input/perl_test_script.pl', executable = 'nonexistent_perl_executable')
        self.assertNotIn('Test script complete', open('../output/make.log').read())

    def test_no_program(self):
        with nostderrout():
            run_perl(program = 'gslab_make_dev/tests/input/nonexistent_perl_script.pl')
        self.assertNotIn('Test script complete', open('../output/make.log').read())
    
    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isfile('output.txt'):
            os.remove('output.txt')
        if os.path.isfile('gslab_make_dev/tests/input/output.txt'):
            os.remove('gslab_make_dev/tests/input/output.txt')  
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()