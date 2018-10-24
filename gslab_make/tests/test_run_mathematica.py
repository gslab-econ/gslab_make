#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make.write_logs import start_makelog
from gslab_make.dir_mod import clear_dir
from gslab_make.run_program import run_mathematica
from nostderrout import nostderrout
import gslab_make.private.metadata as metadata


class testRunMathematica(unittest.TestCase):

    def setUp(self):
        makelog_file = {'makelog' : '../log/make.log'}
        log_dir = '../log/'
        output_dir = '../output/'
        with nostderrout():
            clear_dir([output_dir, log_dir])
            start_makelog(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_mathematica(program = 'gslab_make/tests/input/mathematica_test_script.m')       
        self.assertIn('mathematica test ended', open('../log/make.log', 'rU').read())        
        self.assertTrue(os.path.isfile('output_plot.eps'))
        
    def test_custom_log(self):
        os.remove('../log/make.log')
        makelog_file = {'makelog' : '../log/custom_make.log'}
        with nostderrout():
            start_makelog(makelog_file)
            run_mathematica(program = 'gslab_make/tests/input/mathematica_test_script.m', makelog = makelog_file)   
        self.assertIn('mathematica test ended', open('../log/custom_make.log', 'rU').read())   
        self.assertTrue(os.path.isfile('output_plot.eps'))
        
    def test_independent_log(self):
        with nostderrout():
            run_mathematica(program = 'gslab_make/tests/input/mathematica_test_script.m', log = '../log/mathematica.log')        
        self.assertIn('mathematica test ended', open('../log/make.log', 'rU').read())   
        self.assertTrue(os.path.isfile('../log/mathematica.log'))    
        self.assertIn('mathematica test ended',  open('../log/mathematica.log', 'rU').read())   
        self.assertTrue(os.path.isfile('output_plot.eps')) 
        
    def test_executable(self):
        with nostderrout():
            run_mathematica(program = 'gslab_make/tests/input/mathematica_test_script.m', executable = metadata.default_executables[os.name]['math'])       
        self.assertIn('mathematica test ended', open('../log/make.log', 'rU').read()     )  
        self.assertTrue(os.path.isfile('output_plot.eps'))
        
    def test_bad_executable(self):
        with nostderrout():
            run_mathematica(program = 'gslab_make/tests/input/mathematica_test_script.m', executable = 'nonexistent_mathematica_executable')
        self.assertNotIn('mathematica test ended', open('../log/make.log', 'rU').read()) 

    def test_no_program(self):
        with self.assertRaises(Exception):
            run_mathematica(program = 'gslab_make/tests/input/nonexistent_mathematica_script.m')
        self.assertNotIn('mathematica test ended', open('../log/make.log').read())
    
    def test_option(self):
        with nostderrout():
            run_mathematica(program = 'gslab_make/tests/input/mathematica_test_script.m', option = '-initfile gslab_make/tests/input/mathematica_init_script.m')     
        self.assertIn('mathematica test ended', open('../log/make.log', 'rU').read()) 
    
    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isdir('../log/'):
            shutil.rmtree('../log/')
        if os.path.isfile('output_plot.eps'):
            os.remove('output_plot.eps')
        if os.path.isfile('gslab_make/tests/input/output_plot.eps'):
            os.remove('gslab_make/tests/input/output_plot.eps')
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
