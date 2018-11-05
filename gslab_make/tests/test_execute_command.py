#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make.write_logs import start_makelog
from gslab_make import clear_dir
from gslab_make import execute_command
import gslab_make.private.metadata as metadata
from gslab_make.tests      import nostderrout
    

class testExecuteCommand(unittest.TestCase):

    def setUp(self):
    	self.assertIn(os.name, ['posix', 'nt'])
    	self.assertFalse(os.path.isfile('test_data.txt'))
        # default_makelog = metadata.settings['makelog']
        with nostderrout():
            clear_dir(['../log/'])  

    def test_default_log(self):
    	default_makelog = {'makelog' : '../log/make.log'}
    	start_makelog(default_makelog)
        self.assertFalse(os.path.isfile('test_data.txt'))
        if os.name=='posix':
            our_unzip = 'unzip gslab_make/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make/tests/input/zip_test_file.zip'
        with nostderrout():
            execute_command(default_makelog, our_unzip) 
        self.assertIn('test_data.txt', open(default_makelog['makelog']).read())
        self.assertTrue(os.path.isfile('test_data.txt'))
        
    def test_custom_log(self):
        makelog_file = {'makelog' : '../log/custom_make.log'}
        start_makelog(makelog_file)
        if os.name=='posix':
            our_unzip = 'unzip gslab_make/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make/tests/input/zip_test_file.zip'
        with nostderrout():
            execute_command(makelog_file, our_unzip)
        self.assertIn('test_data.txt', open(makelog_file['makelog']).read())
        self.assertTrue(os.path.isfile('test_data.txt'))
        
    def test_independent_log(self):
    	default_makelog = {'makelog' : '../log/make.log'}
    	independent_log = {'makelog' : '../log/command.log'}
    	start_makelog(independent_log)
        if os.name=='posix':
            our_unzip = 'unzip gslab_make/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make/tests/input/zip_test_file.zip'     
        with nostderrout():
            execute_command(independent_log, our_unzip)
        self.assertIn('test_data.txt', open(independent_log['makelog']).read())
        self.assertTrue(os.path.isfile('test_data.txt'))
   
    def tearDown(self):
        if os.path.isdir('../log/'):
            shutil.rmtree('../log/')
        if os.path.isfile('test_data.txt'):
            os.remove('test_data.txt')
    
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
