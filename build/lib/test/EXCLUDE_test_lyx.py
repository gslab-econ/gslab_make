# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import unittest
import sys
import os
import shutil
import re
from test.utility import no_stderrout, redirect_stdout, read_file

from gslab_make import start_makelog, clear_dir
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ProgramError
    
from gslab_make import run_lyx as run_function

class TestRunLyX(unittest.TestCase):

    def setup_directories(self):
        with no_stderrout():
            clear_dir(['test/output/', 'test/log/'])
        
        if not os.path.isdir('test/raw/run_program/program/'):
            os.makedirs('test/raw/run_program/program/')     

    def setUp(self):
        self.setup_directories()

        self.app = 'lyx'
        self.ext = 'lyx'
        self.executable = metadata.default_executables[os.name][self.app]
        self.option = metadata.default_options[os.name][self.app]
        self.arg = ''

    def check_output(self, 
                     paths, 
                     pdf_name = ''):

        pdf_name = pdf_name if pdf_name else ('%s_file.pdf' % self.app)
        makelog = read_file(paths['makelog'])
        self.assertTrue(os.path.isfile('test/output/%s' % pdf_name))

    def make_paths(self, 
    	           makelog_path = 'test/log/make.log', 
    	           output_dir = 'test/output'):
        paths = {'makelog': makelog_path, 
                 'output_dir': output_dir}
        
        with no_stderrout():
            start_makelog(paths)
            
        return(paths)
        
    def test_program(self):        
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
            run_function(paths, program = program_name)
            
        self.check_output(paths)

    def test_program_beamer(self):        
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_file_beamer.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, doctype = 'beamer')
            
        self.check_output(paths, '%s_file_beamer.pdf' % self.app)

    def test_program_comments(self):        
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_file_comments.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, doctype = 'comments')
            
        self.check_output(paths, '%s_file_comments.pdf' % self.app)

    def test_program_handout(self):        
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_file_handout.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, doctype = 'handout')
            
        self.check_output(paths, '%s_file_handout.pdf' % self.app)

    def test_program_space(self):        
        with no_stderrout():
            paths = self.make_paths(makelog_path = 'test/log/make space.log')
            program_name = 'test/raw/run_program/%s_file space.%s' % (self.app, self.ext)
            run_function(paths, program = program_name)
            
        self.check_output(paths, '%s_file space.pdf' % self.app)

    def test_log(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, log = 'test/output/log.log')
            
        self.check_output(paths)
        self.assertIn('Executing command', read_file('test/output/log.log'))

    def test_log_space(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, log = 'test/output/log space.log')
            
        self.check_output(paths)
        self.assertIn('Executing command', read_file('test/output/log space.log'))

    def test_no_log(self):        
        with no_stderrout():
            paths = self.make_paths(makelog_path = '')
            program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, log = '')

        self.assertFalse(os.path.isfile(paths['makelog']))
        self.assertFalse(os.path.isfile('test/output/log.log'))
        self.assertTrue(os.path.isfile('test/output/%s_file.pdf' % self.app))
        
    def test_program_executable(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, executable = self.executable)
            
        self.check_output(paths)

    def test_program_option(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, option = self.option)
            
        self.check_output(paths)

    def test_program_arg(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, args = self.arg)
        
        self.check_output(paths)

    def test_error_bad_paths(self):      
        try:
            with no_stderrout():
                paths = {}
                program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
                run_function(paths, program = program_name)    
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_os(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
                run_function(paths, program = program_name, osname = 'bad_os')              
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_program_dir(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/program/'
                run_function(paths, program = program_name)           
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_program(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_file_error.%s' % (self.app, self.ext)
                run_function(paths, program = program_name)          
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_program_missing(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_file_missing.%s' % (self.app, self.ext)
                run_function(paths, program = program_name)           
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_program_wrong_extension(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/wrong_extension.txt'
                run_function(paths, program = program_name)           
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_executable(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
                run_function(paths, program = program_name, executable = []) 
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_option(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
                run_function(paths, program = program_name, option = [])   
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_arg(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_file.%s' % (self.app, self.ext)
                run_function(paths, program = program_name, arg = [])    
        except Exception as e:
            self.assertRaises(Exception, e)

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()