# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import re
import sys
import shutil
import unittest
from test.utility import no_stderrout, redirect_stdout, read_file

import gslab_make.private.metadata as metadata
from gslab_make import start_makelog, clear_dir
from gslab_make.private.exceptionclasses import CritError, ProgramError
    
from gslab_make import run_python as run_function

class TestRunPython(unittest.TestCase):

    def setup_directories(self):
        with no_stderrout():
            clear_dir(['test/output/', 'test/log/'])
        
        if not os.path.isdir('test/raw/run_program/program/'):
            os.makedirs('test/raw/run_program/program/')     

    def setUp(self):
        self.setup_directories()

        self.app = 'python'
        self.ext = 'py'
        self.executable = metadata.default_executables[os.name][self.app]
        self.option = metadata.default_options[os.name][self.app]
        self.arg = 'arg'

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
            program_name = 'test/raw/run_program/%s_script_arg.%s' % (self.app, self.ext)
            run_function(paths, program = program_name, args = self.arg)
        
        self.check_output(paths)
        output = read_file('test/output/output.csv')
        self.assertTrue(re.search('arg', output))

    def test_error_bad_paths(self):      
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = {}
                program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
                run_function(paths, program = program_name)    

    def test_error_bad_os(self):      
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
                run_function(paths, program = program_name, osname = 'bad_os')              

    def test_error_program_dir(self):      
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/program/'
                run_function(paths, program = program_name)           

    def test_error_bad_program(self):      
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_script_error.%s' % (self.app, self.ext)
                run_function(paths, program = program_name)          

    def test_error_program_missing(self):      
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_script_missing.%s' % (self.app, self.ext)
                run_function(paths, program = program_name)           

    def test_error_program_wrong_extension(self):      
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/wrong_extension.txt'
                run_function(paths, program = program_name)           

    def test_error_bad_arg(self):      
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                program_name = 'test/raw/run_program/%s_script.%s' % (self.app, self.ext)
                run_function(paths, program = program_name, arg = [])    

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')
                
if __name__ == '__main__':
    unittest.main()