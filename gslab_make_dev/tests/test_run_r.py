#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
sys.path.append('../..')
from gslab_make_dev.make_log import start_make_logging
from gslab_make_dev.dir_mod import clear_dirs
from gslab_make_dev.run_program import run_r
from nostderrout import nostderrout
    

class testRunR(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_dirs(output_dir)
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_r(program = './input/R_test_script.R')      
        logfile_data = open('../output/make.log', 'rU').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertIn('> proc.time()', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_default_log_install(self):
        with nostderrout():
            run_r(package = './input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz')
        self.assertTrue(self.last_line_equals('../output/make.log', '* DONE (Ecdat)\n'))   
        
    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_dirs(output_dir)
            start_make_logging(makelog_file)
            run_r(program = './input/R_test_script.R', makelog = '../output/custom_make.log')
        logfile_data = open('../output/custom_make.log', 'rU').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_independent_log(self):
        with nostderrout():
            run_r(program = './input/R_test_script.R', log = '../output/R.log')
        makelog_data = open('../output/make.log', 'rU').read()
        self.assertIn('Test script complete', makelog_data)
        self.assertTrue(os.path.isfile('../output/R.log'))
        Rlog_data = open('../output/R.log', 'rU').read()
        self.assertIn('Test script complete', Rlog_data)
        self.assertTrue(os.path.isfile('output.txt'))

    def test_no_extension(self):
        with nostderrout():
            run_r(program = './input/R_test_script')
        logfile_data = open('../output/make.log', 'rU').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_executable(self):
        with nostderrout():
            run_r(program = './input/R_test_script.R', executable = 'R CMD BATCH') 
        logfile_data = open('../output/make.log', 'rU').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_bad_executable(self):
        with nostderrout():
            run_r(program = './input/R_test_script.R', executable = 'nonexistent_R_executable')
        logfile_data = open('../output/make.log', 'rU').read()
        if os.name == 'posix':
            self.assertIn('/bin/sh: nonexistent_R_executable: command not found', logfile_data)
        else:
            self.assertIn('\'nonexistent_R_executable\' is not recognized as an internal or external command', logfile_data)
    
    def test_no_program(self):
        with nostderrout():
            run_r(program = './input/nonexistent_R_script.R')
        logfile_data = open('../output/make.log', 'rU').readlines()
        self.assertTrue(logfile_data[-1].startswith('CritError:'))

    def test_no_package(self):
        with nostderrout():
            run_r(package = 'nonexistent_R_package')
        logfile_data = open('../output/make.log', 'rU').readlines()
        self.assertTrue(logfile_data[-1].startswith('CritError:'))
    
    def test_option(self):
        with nostderrout():
            run_r(program = './input/R_test_script.R', option = '--no-timing')
        logfile_data = open('../output/make.log', 'rU').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertIn('R version', logfile_data)        
        self.assertNotIn('> proc.time()', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_two_option(self):
        with nostderrout():
            run_r(program = './input/R_test_script.R', option = '--no-timing --slave')
        logfile_data = open('../output/make.log', 'rU').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertNotIn('R version', logfile_data)        
        self.assertNotIn('> proc.time()', logfile_data)
        self.assertTrue(os.path.isfile('output.txt'))   

    def test_option_install(self):
        self.assertFalse(os.path.isdir('../output/Ecdat/'))
        self.assertFalse(os.path.isfile('../output/Ecdat/INDEX'))       
        with nostderrout():
            run_r(package = './input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz', lib = '../output/', option = '--no-data')
        self.assertTrue(os.path.isdir('../output/Ecdat/'))
        self.assertTrue(os.path.isfile('../output/Ecdat/INDEX'))   
        self.assertFalse(os.path.isdir('../output/Ecdat/data/'))     
    
    def test_r_error(self):
        with nostderrout():
            run_r(program = './input/R_test_script_error.R')
        logfile_data = open('../output/make.log', 'rU').read()
        self.assertIn('executed with errors', logfile_data)
        
    def test_change_dir(self):        
        with nostderrout():
            run_r(program = './input/R_test_script.R', changedir = True)      
        logfile_data = open('../output/make.log', 'rU').read()
        self.assertIn('Test script complete', logfile_data)
        self.assertIn('> proc.time()', logfile_data)
        self.assertTrue(os.path.isfile('./input/output.txt'))

    def test_specify_lib(self):
        self.assertFalse(os.path.isdir('../output/Ecdat/'))
        self.assertFalse(os.path.isfile('../output/Ecdat/INDEX'))       
        with nostderrout():
            run_r(package = './input/rinstall_test_package/Ecdat_0.1-6.1.tar.gz', lib = '../output/')
        self.assertTrue(self.last_line_equals('../output/make.log', '* DONE (Ecdat)\n'))
        self.assertTrue(os.path.isdir('../output/Ecdat/'))
        self.assertTrue(os.path.isfile('../output/Ecdat/INDEX'))    

    def last_line_equals(self, filename, string):
        file_data = open(filename, 'rU')
        file_data.seek(-2, 2)
        file_data.read(2)
        string_len = len(string)
        if file_data.newlines == '\n' or file_data.newlines == '\r' :
            file_data.seek(-string_len, 2)
        elif file_data.newlines == '\r\n':
            file_data.seek(-string_len -1, 2)
        return string == file_data.read(string_len)  
        
    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isfile('output.txt'):
            os.remove('output.txt')
        if os.path.isfile('./input/output.txt'):
            os.remove('./input/output.txt')                
        if os.path.isfile('.RData'):
            os.remove('.RData')
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()