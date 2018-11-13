#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib

from gslab_make.write_logs import start_makelog
from gslab_make.dir_mod import clear_dir
from gslab_make.run_program import run_lyx
from gslab_make.tests import nostderrout
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError
    

class testRunLyx(unittest.TestCase):

    def setUp(self):
        with nostderrout():
            clear_dir(['../log', '../output/', '../temp'])

    def test_default_log(self):
        makelog = {'makelog' : '../log/make.log', 'pdf_dir' : '../output'}
        with nostderrout():    
            start_makelog(makelog)
            run_lyx(makelog, program = 'gslab_make/tests/input/lyx_test_file.lyx')
        logfile_data = open(makelog['makelog'], 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))
        
    def test_independent_log(self):
        makelog = {'makelog' : '../log/make.log', 'pdf_dir' : '../output'}
        independent_log = {'makelog' : '../log/lyx.log', 'pdf_dir' : '../output'}
        with nostderrout():  
            start_makelog(makelog)  
            start_makelog(independent_log)
            run_lyx(independent_log, program = 'gslab_make/tests/input/lyx_test_file.lyx', log=independent_log['makelog'])
        self.assertTrue(os.path.isfile('../log/lyx.log'))
        makelog_data = open(makelog['makelog'], 'rU').read()
        lyxlog_data = open(independent_log['makelog'], 'rU').read()
        self.assertIn('LaTeX', lyxlog_data)
        self.assertIn(lyxlog_data, makelog_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))    
        
    def test_executable(self):
        makelog = {'makelog' : '../log/make.log', 'pdf_dir' : '../output'}
        with nostderrout():    
            start_makelog(makelog)
            run_lyx(makelog, program = 'gslab_make/tests/input/lyx_test_file.lyx', executable = metadata.default_executables[os.name]['lyx']) 
        logfile_data = open(makelog['makelog'], 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))
        
    def test_bad_executable(self):
        makelog = {'makelog' : '../log/make.log', 'pdf_dir' : '../output'}
        with nostderrout():    
            start_makelog(makelog)
        with self.assertRaises(CritError):
            run_lyx(makelog, program = 'gslab_make/tests/input/lyx_test_file.lyx', executable = 'nonexistent_lyx_executable')
        logfile_data = open(makelog['makelog'], 'rU').read()
        self.assertIn('CritError', logfile_data)
        self.assertIn('nonexistent_lyx_executable', logfile_data)

    def test_no_program(self):
        makelog = {'makelog' : '../log/make.log', 'pdf_dir' : '../output'}
        with nostderrout():    
            start_makelog(makelog)
        with self.assertRaises(Exception):
            run_lyx(makelog, 'gslab_make/tests/input/nonexistent_lyx_file.lyx')
        self.assertFalse(os.path.isfile('../output/lyx_test_file.pdf'))
    
    def test_option(self):
        makelog = {'makelog' : '../log/make.log', 'pdf_dir' : '../output'}
        with nostderrout():
            start_makelog(makelog)
            run_lyx(makelog, program = 'gslab_make/tests/input/lyx_test_file.lyx', option = '-e pdf')
        logfile_data = open(makelog['makelog'], 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))
        
    def test_pdfout(self):
        makelog = {'makelog' : '../log/make.log', 'pdf_dir' : '../log'}
        with nostderrout():
            start_makelog(makelog)
            run_lyx(makelog, program = 'gslab_make/tests/input/lyx_test_file.lyx')
        logfile_data = open(makelog['makelog'], 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../log/lyx_test_file.pdf'))
        self.assertFalse(os.path.isfile('../output/lyx_test_file.pdf'))

    def test_comments(self):
        makelog = {'makelog' : '../log/make.log', 'pdf_dir' : '../output'}
        with nostderrout():    
            start_makelog(makelog)
            run_lyx(makelog, program = 'gslab_make/tests/input/lyx_test_file.lyx', doctype = 'comments')
        logfile_data = open(makelog['makelog'], 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../temp/lyx_test_file.pdf'))
        self.assertFalse(os.path.isfile('../output/lyx_test_file_comments.pdf'))

    def test_handout_pdfout(self):
    	makelog = {'makelog' : '../log/make.log', 'pdf_dir' : '../output'}
        with nostderrout():    
            start_makelog(makelog)
            run_lyx(makelog, program = 'gslab_make/tests/input/lyx_test_file.lyx', doctype = 'handout')
        logfile_data = open(makelog['makelog'], 'rU').read()
        self.assertIn('LaTeX', logfile_data)
        self.assertTrue(os.path.isfile('../output/lyx_test_file.pdf'))
        self.assertFalse(os.path.isfile('../temp/lyx_test_file.pdf'))
        
    def tearDown(self):
        if os.path.isdir('../output/'):
            shutil.rmtree('../output/')
        if os.path.isdir('../log/'):
            shutil.rmtree('../log/')
        if os.path.isdir('../temp/'):
            shutil.rmtree('../temp/')
    
if __name__ == '__main__':
    os.getcwd()
    unittest.main()
