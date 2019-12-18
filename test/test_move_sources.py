import unittest
import sys
import os
import shutil
from test.utility import no_stderrout, redirect_stdout

from gslab_make import start_makelog, remove_dir, clear_dir
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ProgramError
    
from gslab_make import link_inputs, copy_inputs, link_externals, copy_externals

class TestMoveSources(unittest.TestCase):

    def setUp(self):
        with no_stderrout():
            clear_dir(['test/output/', 'test/log/'])
            remove_dir(['test/external/', 'test/input/'])

    def make_paths(self, move_path = 'test/log/make.log', input_path = 'test/input/'):
        paths = {'makelog': move_path, 
                 'input_dir': input_path}

        with no_stderrout():
            start_makelog(paths)
            
        return(paths)
        
    def check_move(self, paths):
        self.assertIn('Input links successfully created!', open(paths['makelog']).read())
        self.assertTrue(os.path.isfile('test/input/file.txt'))

    def test_move_file(self):        
        with no_stderrout():
            paths = self.make_paths()
            link_inputs(paths, ['test/raw/move_source/move_file.txt'])
            self.check_move(paths)

    def test_move_dir(self):        
        with no_stderrout():
            paths = self.make_paths()
            link_inputs(paths, ['test/raw/move_source/move_dir.txt'])
            self.assertIn('Input links successfully created!', open(paths['makelog']).read())
            self.assertTrue(os.path.isdir('test/input/program/'))

    def test_move_wildcard(self):        
        with no_stderrout():
            paths = self.make_paths()
            link_inputs(paths, ['test/raw/move_source/move_wildcar*.txt'])
            self.check_move(paths)

    def test_move_character(self):        
        with no_stderrout():
            paths = self.make_paths()
            link_inputs(paths, ['test/raw/move_source/move_β.txt'])
            self.check_move(paths)

    def test_move_empty_file(self):        
        with no_stderrout():
            paths = self.make_paths()
            link_inputs(paths, [])
            self.check_move(paths)

    def test_move_empty_command(self):        
        with no_stderrout():
            paths = self.make_paths()
            link_inputs(paths, ['test/raw/move_source/move_empty.txt'])
            self.assertIn('Input links successfully created!', open(paths['makelog']).read())

    def test_move_space(self):        
        with no_stderrout():
            paths = self.make_paths()
            link_inputs(paths, ['test/raw/move_source/move space.txt'])
            self.check_move(paths)

    def test_error_bad_os(self):        
        try:
            with no_stderrout():
                # Change OS
                paths = self.make_paths()
                link_inputs(paths, ['test/raw/move_source/move_file.txt'])
                self.check_move(paths)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_move(self):        
        try:
            with no_stderrout():
                paths = self.make_paths()
                link_inputs(paths, ['test/raw/move_source/move_bad.txt'])
                self.check_move(paths)
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_not_exist_command(self):        
        try:
            with no_stderrout():
                paths = self.make_paths()
                link_inputs(paths, ['test/raw/move_source/move_nonexist.txt'])
                self.check_move(paths)
        except Exception as e:
            self.assertRaises(Exception, e)


    def test_error_not_exist_move(self):        
        try:
            with no_stderrout():
                paths = self.make_paths()
                link_inputs(paths, ['test/raw/move_source/move_nonexistent.txt'])
                self.check_move(paths)
        except Exception as e:
            self.assertRaises(Exception, e)


    def test_error_bad_wildcard(self):        
        try:
            with no_stderrout():
                paths = self.make_paths()
                link_inputs(paths, ['test/raw/move_source/move_bad_wildcard.txt'])
                self.check_move(paths)
        except Exception as e:
            self.assertRaises(Exception, e)


    def test_error_bad_key(self):        
        try:
            with no_stderrout():
                paths = self.make_paths()
                link_inputs(paths, ['test/raw/move_source/move_bad_key.txt'])
                self.check_move(paths)
        except Exception as e:
            self.assertRaises(Exception, e)


    def test_error_bad_paths(self):        
        try:
            with no_stderrout():
                paths = {}
                link_inputs(paths, ['test/raw/move_source/move_file.txt'])
                self.check_move(paths)
        except Exception as e:
            self.assertRaises(Exception, e)


    def test_error_corrupt_paths(self):        
        try:
            with no_stderrout():
                paths = {'makelog': move_path, 
                         'input': input_path, 
                         'bad': []}
                link_inputs(paths, ['test/raw/move_source/move_bad_paths.txt'])
                self.check_move(paths)
        except Exception as e:
            self.assertRaises(Exception, e)


    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')
        if os.path.isdir('test/input/'):
            shutil.rmtree('test/input/')
        if os.path.isdir('test/external/'):
            shutil.rmtree('test/external/')

if __name__ == '__main__':
    unittest.main()