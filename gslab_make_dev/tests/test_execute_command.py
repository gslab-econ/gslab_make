#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
from gslab_make_dev import start_make_logging
from gslab_make_dev import clear_dirs
from gslab_make_dev import execute_command
from gslab_make_dev.tests      import nostderrout
    

class testRunCommand(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        if os.name == 'posix':
            our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
        elif os.name == 'nt':
            our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'
        else:
            raise CritError(messages.crit_error_unknown_system % os.name)

        with nostderrout():
            clear_dirs(output_dir)  
            start_make_logging(makelog_file)

    def test_default_log(self):
        self.assertFalse(os.path.isfile('test_data.txt'))
        if os.name=='posix':
            our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'
        with nostderrout():
            execute_command(command = our_unzip) 
        logfile_data = open('../output/make.log', 'rU').readlines()
        search_str1 = 'Unzipping test_data.txt.'
        search_str2 = 'Extracting test_data.txt.'
        search_str3 = 'extracting: test_data.txt'
        found1 = logfile_data[-1].find(search_str1) != -1
        found2 = logfile_data[-1].find(search_str2) != -1
        found3 = logfile_data[-2].find(search_str3) != -1
        self.assertTrue(found1 | found2 | found3)
        self.assertTrue(os.path.isfile('test_data.txt'))
        
    def test_custom_log(self):
        self.assertFalse(os.path.isfile('test_data.txt'))    
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        if os.name=='posix':
            our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'
        with nostderrout():
            clear_dirs(output_dir)  
            start_make_logging(makelog_file)
            execute_command(command = our_unzip, makelog = '../output/custom_make.log')
        logfile_data = open('../output/custom_make.log', 'rU').readlines()
        search_str1 = 'Unzipping test_data.txt.'
        search_str2 = 'Extracting test_data.txt.'
        search_str3 = 'extracting: test_data.txt'
        found1 = logfile_data[-1].find(search_str1) != -1
        found2 = logfile_data[-1].find(search_str2) != -1
        found3 = logfile_data[-2].find(search_str3) != -1
        self.assertTrue(found1 | found2 | found3)
        self.assertTrue(os.path.isfile('test_data.txt'))
        
    def test_independent_log(self):
        self.assertFalse(os.path.isfile('test_data.txt'))
        if os.name=='posix':
            our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
        else:
            our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'     
        with nostderrout():
            execute_command(command = our_unzip, log = '../output/command.log')
        makelog_data = open('../output/make.log', 'rU').readlines()
        search_str1 = 'Unzipping test_data.txt.'
        search_str2 = 'Extracting test_data.txt.'
        search_str3 = 'extracting: test_data.txt'
        found1 = makelog_data[-1].find(search_str1) != -1
        found2 = makelog_data[-1].find(search_str2) != -1
        found3 = makelog_data[-2].find(search_str3) != -1
        self.assertTrue(found1 | found2 | found3)
        self.assertTrue(os.path.isfile('../output/command.log'))
        commandlog_data = open('../output/command.log', 'rU').readlines()
        found1 = commandlog_data[-1].find(search_str1) != -1
        found2 = commandlog_data[-1].find(search_str2) != -1
        found3 = commandlog_data[-2].find(search_str3) != -1
        self.assertTrue(found1 | found2 | found3)
        self.assertTrue(os.path.isfile('test_data.txt'))
   
    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isfile('test_data.txt'):
            os.remove('test_data.txt')
    
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
