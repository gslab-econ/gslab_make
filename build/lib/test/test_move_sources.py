# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import sys
import shutil
import unittest
from test.utility import no_stderrout, redirect_stdout, read_file

import gslab_make.private.metadata as metadata
from gslab_make import start_makelog, remove_dir, clear_dir
from gslab_make.private.exceptionclasses import CritError, ProgramError
    
from gslab_make import link_inputs, copy_inputs, link_externals, copy_externals

class TestLinkInputs(unittest.TestCase):

    def setup_directories(self):
        with no_stderrout():
            remove_dir(['test/external/', 'test/input/'])
            clear_dir(['test/output/', 'test/log/'])

        if not os.path.isdir('test/raw/move_sources/dir/'):
            os.makedirs('test/raw/move_sources/dir/')     

    def setUp(self):
        self.setup_directories()
        self.move_type = 'input'

    def move_function(self, *args):
        link_inputs(*args)

    def make_paths(self, 
                   makelog_path = 'test/log/make.log', 
                   input_path = 'test/input/', 
                   external_path = 'test/external/'):
    
        paths = {'makelog': makelog_path, 
                 'input_dir': input_path,
                 'external_dir': external_path}

        with no_stderrout():
            start_makelog(paths)
            
        return(paths)
        
    def check_makelog(self, paths):
        message = 'Input links successfully created!'
        self.assertIn(message, read_file(paths['makelog']))

    def check_move(self, paths):
        self.check_makelog(paths)
        self.assertTrue(os.path.isfile('test/%s/file.txt' % self.move_type))

    def test_move_file(self):        
        with no_stderrout():
            paths = self.make_paths()
            self.move_function(paths, ['test/raw/move_sources/move_file.txt'])
            self.check_move(paths)

    def test_move_non_list(self):        
        with no_stderrout():
            paths = self.make_paths()
            self.move_function(paths, 'test/raw/move_sources/move_file.txt')
            self.check_move(paths)

    def test_move_dir(self):        
        with no_stderrout():
            paths = self.make_paths()
            self.move_function(paths, ['test/raw/move_sources/move_dir.txt'])
            self.check_makelog(paths)
            self.assertTrue(os.path.isdir('test/%s/dir/' % self.move_type))

    def test_move_wildcard(self):        
        with no_stderrout():
            paths = self.make_paths()
            self.move_function(paths, ['test/raw/move_sources/move_wildcar*.txt'])
            self.check_move(paths)

    def test_move_space(self):        
        with no_stderrout():
            paths = self.make_paths(makelog_path = 'test/log/make space.log')
            self.move_function(paths, ['test/raw/move_sources/move space.txt'])
            self.check_makelog(paths)
            self.assertTrue(os.path.isfile('test/%s/file space.txt' % self.move_type))

    def test_move_no_move(self):        
        with no_stderrout():
            paths = self.make_paths()
            self.move_function(paths, [])
            self.check_makelog(paths)

    def test_move_empty_command(self):        
        with no_stderrout():
            paths = self.make_paths()
            self.move_function(paths, ['test/raw/move_sources/move_empty.txt'])
            self.check_makelog(paths)

    def test_error_bad_move(self):        
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                self.move_function(paths, ['test/raw/move_sources/move_bad.txt'])
                self.check_move(paths)

    def test_error_missing_target(self):        
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                self.move_function(paths, ['test/raw/move_sources/move_missing.txt'])
                self.check_move(paths)

    def test_error_missing_move(self):        
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                self.move_function(paths, ['test/raw/move_sources/move_nonexistent.txt'])
                self.check_move(paths)

    def test_error_bad_wildcard(self):        
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                self.move_function(paths, ['test/raw/move_sources/move_bad_wildcard.txt'])
                self.check_move(paths)

    def test_error_bad_key(self):        
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = self.make_paths()
                self.move_function(paths, ['test/raw/move_sources/move_bad_key.txt'])
                self.check_move(paths)

    def test_error_bad_paths(self):        
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = {}
                self.move_function(paths, ['test/raw/move_sources/move_file.txt'])
                self.check_move(paths)

    def test_error_corrupt_paths(self):        
        with self.assertRaises(Exception):
            with no_stderrout():
                paths = {'makelog': 'test/log/make.log', 
                         'input_dir': 'test/input/', 
                         'external_dir': 'test/external/',
                         'bad_key': []}

                self.move_function(paths, ['test/raw/move_sources/move_file.txt'])
                self.check_move(paths)

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')
        if os.path.isdir('test/input/'):
            remove_dir(['test/input/'], quiet = True)
        if os.path.isdir('test/external/'):
            shutil.rmtree('test/external/')

class TestLinkExternals(TestLinkInputs):      

    def setUp(self):
        self.setup_directories()
        self.move_type = 'external'

    def move_function(self, *args):
        link_externals(*args)

    def check_makelog(self, paths):
        message = 'External links successfully created!'
        self.assertIn(message, read_file(paths['makelog']))

class TestCopyInputs(TestLinkInputs):      

    def setUp(self):
        self.setup_directories()
        self.move_type = 'input'

    def move_function(self, *args):
        copy_inputs(*args)

    def check_makelog(self, paths):
        message = 'Input copies successfully created!'
        self.assertIn(message, read_file(paths['makelog']))

class TestCopyExternals(TestLinkInputs):      

    def setUp(self):
        self.setup_directories()
        self.move_type = 'external'

    def move_function(self, *args):
        copy_externals(*args)

    def check_makelog(self, paths):
        message = 'External copies successfully created!'
        self.assertIn(message, read_file(paths['makelog']))

if __name__ == '__main__':
    unittest.main()