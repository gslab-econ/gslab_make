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
        with nostderrout():
            clear_dir(['../log/'])  

    def test_log(self):
    	makelog = {'makelog' : '../log/make.log'}
    	start_makelog(makelog)
        self.assertFalse(os.path.isfile('test_data.txt'))
        if os.name=='posix':
            our_unzip = 'unzip gslab_make/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make/tests/input/zip_test_file.zip'
        with nostderrout():
            execute_command(makelog, our_unzip) 
        self.assertIn('test_data.txt', open(makelog['makelog']).read())
        self.assertTrue(os.path.isfile('test_data.txt'))
   
    def tearDown(self):
        if os.path.isdir('../log/'):
            shutil.rmtree('../log/')
        if os.path.isfile('test_data.txt'):
            os.remove('test_data.txt')
    
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
