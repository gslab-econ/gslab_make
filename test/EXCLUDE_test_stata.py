# -*- coding: UTF-8 -*-
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
    
from gslab_make import run_stata as run_function

class TestRunStata(unittest.TestCase):

    def setup_directories(self):
        with no_stderrout():
            clear_dir(['test/output/', 'test/log/'])
        
        if not os.path.isdir('test/raw/run_program/program/'):
            os.makedirs('test/raw/run_program/program/')     

    def setUp(self):
        self.setup_directories()

        self.app = 'stata'
        self.ext = 'do'
        self.executable = metadata.default_executables[os.name][self.app]
        self.option = metadata.default_options[os.name][self.app]
        self.arg = ''

    def check_output(self, paths):
        makelog = read_file(paths['makelog'])
        self.assertTrue(re.search('Test script complete', makelog))
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def make_paths(self, makelog_path = 'test/log/make.log'):
        paths = {'makelog': makelog_path}
        
        with no_stderrout():
            start_makelog(paths)
            
        return(paths)
        
    def test_program(self):        
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
            run_function(paths, program = program_name)
                        
        self.check_output(paths)

    def test_program_space(self):        
        with no_stderrout():
            paths = self.make_paths(makelog_path = 'test/log/make space.log')
            program_name = 'test/raw/run_program/%s_script space.%s' % (self.app, self.ext)
            run_function(paths, program = program_name)
            
        self.check_output(paths)

    def test_log(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, log = 'test/output/log.log')
            
        self.check_output(paths)
        self.assertIn('Test script complete', read_file('test/output/log.log'))

    def test_log_space(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, log = 'test/output/log space.log')
            
        self.check_output(paths)
        self.assertIn('Test script complete', read_file('test/output/log space.log'))

    def test_no_log(self):        
        with no_stderrout():
            paths = self.make_paths(makelog_path = '')
            program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, log = '')

        self.assertFalse(os.path.isfile(paths['makelog']))
        self.assertFalse(os.path.isfile('test/output/log.log'))
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_program_executable(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, executable = self.executable)
            
        self.check_output(paths)

    def test_program_option(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, option = self.option)
            
        self.check_output(paths)

    def test_program_arg(self):      
        with no_stderrout():
            paths = self.make_paths()
            program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, args = self.arg)
        
        self.check_output(paths)

    def test_error_bad_paths(self):      
        try:
            with no_stderrout():
                paths = {}
                program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
                run_function(paths, program = program_name)    
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_os(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
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
                program_name = 'test/raw/run_program/%s_script_error.%s' % (self.app, self.ext)
                run_function(paths, program = program_name)          
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_program_missing(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_script_missing.%s' % (self.app, self.ext)
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
                program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
                run_function(paths, program = program_name, executable = []) 
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_option(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
                run_function(paths, program = program_name, option = [])   
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_arg(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
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