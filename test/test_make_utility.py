# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import sys
import mock
import copy
import shutil
import unittest
from test.utility import no_stderrout, redirect_stdout, create_file

import gslab_make.private.metadata as metadata
from gslab_make import clear_dir

from gslab_make import update_executables, update_paths, copy_output

class TestUpdateExecutables(unittest.TestCase):

    def setUp(self):
        self.default = copy.deepcopy(metadata.default_executables)

    def test_config(self):     
        PATHS = {'config_user': 'test/raw/config/config_user.yaml'}
        update_executables(PATHS)

    def test_config_character(self):     
        PATHS = {'config_user': 'test/raw/config/config_user_╬▓.yaml'}
        update_executables(PATHS)

    def test_config_empty(self):     
        PATHS = {'config_user': 'test/raw/config/config_user_empty.yaml'}
        update_executables(PATHS)

    def test_error_config_bad(self):     
        try:
            PATHS = {'config_user': 'test/raw/config/config_user_bad.yaml'}
            update_executables(PATHS)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_config_missing(self):     
        try:
            PATHS = {'config_user': 'test/raw/config/config_missing.yaml'}
            update_executables(PATHS)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_paths(self):     
        try:
            PATHS = {}
            update_executables(PATHS)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_os(self):     
        try:
            PATHS = {'config_user': 'test/raw/config/config_user.yaml'}
            update_executables(PATHS, osname = 'bad_os')
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_executables(self):     
        try:
            PATHS = {'config_user': 'test/raw/config/config_bad_executables.yaml'}
        except Exception as e:
            self.assertRaises(Exception, e)

    def tearDown(self):
        # Delete log directory
        if os.path.isdir('log/'):
            shutil.rmtree('log/')

        # Reset executables to default
        metadata.default_executables = copy.deepcopy(self.default)

class TestUpdateMappings(unittest.TestCase):

    def test_config(self):     
        PATHS = {'config_user': 'test/raw/config/config_user.yaml'}
        PATH_MAPPINGS = update_paths(PATHS)

    def test_config_character(self):     
        PATHS = {'config_user': 'test/raw/config/config_user_╬▓.yaml'}
        PATH_MAPPINGS = update_paths(PATHS)

    def test_config_empty(self):     
        PATHS = {'config_user': 'test/raw/config/config_user_empty.yaml'}
        PATH_MAPPINGS = update_paths(PATHS)

    def test_error_config_bad(self):     
        try:
            PATHS = {'config_user': 'test/raw/config/config_user_bad.yaml'}
            PATH_MAPPINGS = update_paths(PATHS)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_config_missing(self):     
        try:
            PATHS = {'config_user': 'test/raw/config/config_missing.yaml'}
            PATH_MAPPINGS = update_paths(PATHS)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_paths(self):     
        try:
            PATHS = {}
            PATH_MAPPINGS = update_paths(PATHS)
        except Exception as e:
            self.assertRaises(Exception, e)
            
    def tearDown(self):
        if os.path.isdir('log/'):
            shutil.rmtree('log/')

class TestCopyOutput(unittest.TestCase):

    def setUp(self):
        # Create output directory
        self.assertFalse(os.path.exists('test/output/'))
        os.makedirs('test/output/')

        self.assertFalse(os.path.exists('test/copy/'))
        os.makedirs('test/copy/')

        # Create test file
        create_file('test/output/file.txt')

    @mock.patch('gslab_make.make_utility.input', return_value = 'Yes')
    def test_copy(self, mocked_input):  
        copy_output('test/output/file.txt', 'test/copy/')
        self.assertTrue(os.path.isfile('test/copy/file.txt'))

    @mock.patch('gslab_make.make_utility.input', return_value = 'No')
    def test_not_copy(self, mocked_input):  
        copy_output('test/output/file.txt', 'test/copy/')
        self.assertFalse(os.path.isfile('test/copy/file.txt'))

    @mock.patch('gslab_make.make_utility.input', return_value = 'Yes')
    def test_error_no_file(self, mocked_input):  
        try:
            copy_output('test/output/file_missing.txt', 'test/copy/')
        except Exception as e:
            self.assertRaises(Exception, e)

    @mock.patch('gslab_make.make_utility.input', return_value = 'Yes')
    def test_error_no_dir(self, mocked_input):  
        try:
            copy_output('test/output/file.txt', 'test/output/dir_missing/')
        except Exception as e:
            self.assertRaises(Exception, e)

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
        if os.path.isdir('test/copy/'):
            shutil.rmtree('test/copy/')

if __name__ == '__main__':
    unittest.main()