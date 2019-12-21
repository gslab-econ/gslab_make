import unittest
import sys
import os
import shutil
from test.utility import no_stderrout, redirect_stdout, create_file
from gslab_make import clear_dir

from gslab_make import update_executables, update_paths, copy_output

class TestUpdateExecutables(unittest.TestCase):

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
        if os.path.isdir('log/'):
            shutil.rmtree('log/')

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

if __name__ == '__main__':
    unittest.main()