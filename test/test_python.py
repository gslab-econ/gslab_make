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
        
        start_makelog(paths)
            
        return(paths)

    def test_program_character(self):        
        paths = self.make_paths(makelog_path = 'test/log/make_╬▓.log')
        program_name = 'test/raw/run_program/%s_script_╬▓.%s' % (self.app, self.ext)
        run_function(paths, program = program_name)
            
        self.check_output(paths)

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')
                
if __name__ == '__main__':
    unittest.main()