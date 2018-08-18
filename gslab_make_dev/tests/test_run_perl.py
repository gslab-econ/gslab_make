#! /usr/bin/env perl

import unittest, sys, os, shutil, contextlib
sys.path.append('../..')
from gslab_make_dev.make_log import start_make_logging
from gslab_make_dev.dir_mod import clear_dirs
from gslab_make_dev.run_program import run_perl
from nostderrout import nostderrout
    

class testRunPerl(unittest.TestCase):

    def setUp(self):
        makelog_file = '../output/make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_dirs(output_dir)
            start_make_logging(makelog_file)

    def test_default_log(self):
        with nostderrout():
            run_perl(program = './input/perl_test_script.pl')
        self.assertTrue(self.last_line_equals('../output/make.log', 'Test script complete\n'))
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_custom_log(self):
        os.remove('../output/make.log')
        makelog_file = '../output/custom_make.log'
        output_dir = '../output/'
        with nostderrout():
            clear_dirs(output_dir)
            start_make_logging(makelog_file)
            run_perl(program = './input/perl_test_script.pl', makelog = '../output/custom_make.log')
        self.assertTrue(self.last_line_equals('../output/custom_make.log', 'Test script complete\n'))
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_independent_log(self):
        with nostderrout():
            run_perl(program = './input/perl_test_script.pl', log = '../output/perl.log')
        self.assertTrue(self.last_line_equals('../output/make.log', 'Test script complete\n'))
        self.assertTrue(os.path.isfile('../output/perl.log'))
        self.assertTrue(self.last_line_equals('../output/perl.log', 'Test script complete\n'))
        self.assertTrue(os.path.isfile('output.txt'))

    def test_no_extension(self):
        with nostderrout():
            run_perl(program = './input/perl_test_script')
        self.assertTrue(self.last_line_equals('../output/make.log', 'Test script complete\n'))
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_executable(self):
        with nostderrout():
            run_perl(program = './input/perl_test_script.pl', executable = 'perl') 
        self.assertTrue(self.last_line_equals('../output/make.log', 'Test script complete\n'))
        self.assertTrue(os.path.isfile('output.txt'))
        
    def test_bad_executable(self):
        with nostderrout():
            run_perl(program = './input/perl_test_script.pl', executable = 'nonexistent_perl_executable')
        logfile_data = open('../output/make.log', 'rU').read()
        if os.name == 'posix':
            self.assertIn('/bin/sh: nonexistent_perl_executable: command not found', logfile_data)
        else:
            self.assertIn('\'nonexistent_perl_executable\' is not recognized as an internal or external command', logfile_data)
    
    def test_no_program(self):
        with nostderrout():
            run_perl(program = './input/nonexistent_perl_script.pl')
        logfile_data = open('../output/make.log', 'rU').readlines()
        self.assertTrue(logfile_data[-1].startswith('CritError:'))
    
    def test_options(self):
        with nostderrout():
            run_perl(program = './input/perl_test_script.pl', option = '-h')
        logfile_data = open('../output/make.log', 'rU').read()
        self.assertIn('Options and arguments (and corresponding environment variables):', logfile_data)
    
    def test_args(self):
        with nostderrout():
            run_perl(program = './input/perl_test_script.pl', args = '-i \'Input\'')
        output_data = open('output.txt', 'rU').read()
        self.assertIn('Input', output_data)
        
    def test_change_dir(self):        
        with nostderrout():
            run_perl(program = './input/perl_test_script.pl', changedir = True)
        self.assertTrue(self.last_line_equals('../output/make.log', 'Test script complete\n'))
        self.assertTrue(os.path.isfile('./input/output.txt'))    
    
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
                
if __name__ == '__main__':
    os.getcwd()
    unittest.main()