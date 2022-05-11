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
    
from gslab_make import run_latex as run_function

class TestRunLaTeX(unittest.TestCase):

    def setup_directories(self):
        with no_stderrout():
            clear_dir(['test/output/', 'test/log/'])
        
        if not os.path.isdir('test/raw/run_program/program/'):
            os.makedirs('test/raw/run_program/program/')     

    def setUp(self):
        self.setup_directories()

        self.app = 'latex'
        self.ext = 'tex'
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

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')

if __name__ == '__main__':
    unittest.main()