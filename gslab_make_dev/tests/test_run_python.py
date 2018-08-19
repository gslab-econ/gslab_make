#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make_dev.make_log import start_make_logging
from gslab_make_dev.dir_mod import clear_dirs
from gslab_make_dev.run_program import run_python
from nostderrout import nostderrout
import gslab_make_dev.private.metadata as metadata
    

class testRunPython(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_dirs(output_dir)
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py')
        self.assertIn('Test script complete', open('../output/make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_dirs(output_dir)
            start_make_logging(makelog_file)
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', makelog = '../output/custom_make.log')
        self.assertIn('Test script complete', open('../output/custom_make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_independent_log(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', log = '../output/python.log')
        self.assertIn('Test script complete', open('../output/make.log').read())
        self.assertTrue(os.path.isfile('../output/python.log'))
        self.assertIn('Test script complete', open('../output/python.log').read())        
        self.assertTrue(os.path.isfile('output.txt'))

    def test_no_extension(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script')
        self.assertIn('Test script complete', open('../output/make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_executable(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', executable = metadata.default_executables[os.name]['python']) 
        self.assertIn('Test script complete', open('../output/make.log').read())
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_bad_executable(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', executable = 'nonexistent_python_executable')
        self.assertNotIn('Test script complete', open('../output/make.log').read())

    def test_no_program(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/nonexistent_python_script.py')
        self.assertNotIn('Test script complete', open('../output/make.log').read())
    
    def test_options(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', option = '-h')
        logfile_data = open('../output/make.log', 'rU').read()
        self.assertIn('Options and arguments (and corresponding environment variables):', logfile_data)
    
    def test_args(self):
        with nostderrout():
            run_python(program = 'gslab_make_dev/tests/input/python_test_script.py', args = '-i \'Input\'')
        output_data = open('output.txt', 'rU').read()
        self.assertIn('Input', output_data)
    
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