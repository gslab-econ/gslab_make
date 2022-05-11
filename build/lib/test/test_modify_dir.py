# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import sys
import os
import shutil
import zipfile
import unittest
from test.utility import no_stderrout, redirect_stdout, create_file, read_file

from gslab_make import clear_dir, remove_dir, zip_dir, unzip

class TestClearDir(unittest.TestCase):
            
    def make_output(self, contain_file = False):
        # Create output directory
        self.assertFalse(os.path.exists('test/output/'))
        os.makedirs('test/output/')

        # Create test file
        if contain_file:
            create_file('test/output/file.txt')

    def check_output(self):
        # Check output directory exists
        self.assertTrue(os.path.exists('test/output/'))
        
        # Check output directory empty
        file_list = os.listdir('test/output/')
        self.assertEqual(len(file_list), 0)
          
        # Check status message printed
        self.assertIn('Cleared:', read_file('test/stdout.txt'))

    def clear_output(self, output_list):
        with open('test/stdout.txt', 'w') as f:
            with redirect_stdout(f):
                clear_dir(output_list) 

    def test_dir_not_exist(self):
        self.assertFalse(os.path.exists('test/output/'))
        self.clear_output(['test/output/'])
        self.check_output()
        
    def test_dir(self):
        self.make_output()      
        self.clear_output(['test/output/']) 
        self.check_output()
            
    def test_dir_with_files(self):
        self.make_output(contain_file = True) 
        self.clear_output(['test/output/'])   
        self.check_output()          
  
    def test_wildcard(self):
        self.make_output() 
        self.clear_output(['test/outpu*/'])   
        self.check_output()  

    def test_non_list(self):                   
        self.make_output() 
        self.clear_output('test/output/')
        self.check_output()

    def test_error_file(self):                   
        self.make_output(contain_file = True)
        with self.assertRaises(Exception):
            with no_stderrout:
            	clear_dir(['test/output/text.txt'])

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')         
        if os.path.isfile('test/stdout.txt'):
            os.remove('test/stdout.txt') 

class TestRemoveDir(unittest.TestCase):
            
    def make_output(self, contain_file = False):
        # Create output directory
        self.assertFalse(os.path.exists('test/output/'))
        os.makedirs('test/output/')

        # Create test file
        if contain_file:
            create_file('test/output/file.txt')

    def check_output(self):
        self.assertFalse(os.path.exists('test/output/'))

    def test_quiet(self):
        self.make_output()
        
        # Redirect stdout
        with open('test/stdout.txt', 'w') as f:
            with redirect_stdout(f):
                remove_dir(['test/output/'], quiet = True)
                
        # Check stdout
        self.assertNotIn('Removed:', read_file('test/stdout.txt'))
        
    def test_not_quiet(self):
        self.make_output()
             
        # Redirect stdout 
        with open('test/stdout.txt', 'w') as f:
            with redirect_stdout(f):
                remove_dir(['test/output/'], quiet = False)
        
        # Check stdout      
        self.assertIn('Removed:', read_file('test/stdout.txt'))
            
    def test_dir_not_exist(self):
        """
        Note
        ----
        When removing a directory that does not exist, nothing
        is ever printed.
        """

        self.assertFalse(os.path.exists('test/output/'))
                
        # Redirect stdout
        with open('test/stdout.txt', 'w') as f:
            with redirect_stdout(f):
                remove_dir(['test/output/'], quiet = False)
         
        # Check stdout      
        self.assertNotIn('Removed:', read_file('test/stdout.txt'))
            
        self.check_output()
        
    def test_dir(self):
        self.make_output()       
        remove_dir(['test/output/'], quiet = True)
        self.check_output()
            
    def test_dir_with_files(self):
        self.make_output(contain_file = True)
        remove_dir(['test/output/'], quiet = True)
        self.check_output()          
  
    def test_wildcard(self):
        self.make_output()
        remove_dir(['test/outpu*/'], quiet = True)
        self.check_output()  

    def test_non_list(self):                   
        self.make_output()     
        remove_dir('test/output/', quiet = True)
        self.check_output()

    def test_error_file(self):    
        self.make_output(contain_file = True)      
        with self.assertRaises(Exception):
            remove_dir(['test/output/file.txt'], quiet = True)       

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')  
        if os.path.isfile('test/stdout.txt'):
            os.remove('test/stdout.txt') 

class TestZip(unittest.TestCase):

    def setUp(self):
        # Create output directory
        self.assertFalse(os.path.isdir('test/output/'))
        os.makedirs('test/output/')

        # Create test file
        create_file('test/output/file.txt') 

        # Create test zip
        with zipfile.ZipFile('test/output/unzip.zip', 'w', zipfile.ZIP_DEFLATED) as z:
            z.write('test/output/file.txt', arcname = 'file.txt')

    def test_unzip_to_not_exist_dir(self):
        # Unzip zip
        unzip('test/output/unzip.zip', 'test/output/unzipped/')
        
        # Check unzip
        self.assertTrue(os.path.isfile('test/output/unzipped/file.txt'))

    def test_unzip_to_exist_dir(self):        
        os.makedirs('test/output/unzipped')
        create_file('test/output/unzipped/exist.txt') 
        
        # Unzip zip
        unzip('test/output/unzip.zip', 'test/output/unzipped/')
        
        # Check unzip and existing
        self.assertTrue(os.path.isfile('test/output/unzipped/file.txt'))
        self.assertTrue(os.path.isfile('test/output/unzipped/exist.txt'))

    def test_unzip_to_not_exist_file(self):
        # Unzip zip
        unzip('test/output/unzip.zip', 'test/output/unzipped.txt')
        
        # Check unzip
        self.assertTrue(os.path.isfile('test/output/unzipped.txt/file.txt'))
  
    def test_error_unzip_to_exist_file(self):
        create_file('test/output/unzipped.txt') 
        
        with self.assertRaises(Exception):
            unzip('test/output/unzip.zip', 'test/output/unzipped.txt')
        
    def test_zip_to_not_exist_file(self):        
        # Zip directory
        with no_stderrout():
            zip_dir('test/output/', 'test/output/zipped.zip')
        
        # Check zip
        self.assertTrue(os.path.isfile('test/output/zipped.zip'))

    def test_zip_to_exist_file(self):        
        create_file('test/output/zipped.zip')    
        
        with no_stderrout():
            zip_dir('test/output/', 'test/output/zipped.zip')
        
        # Check zip
        self.assertTrue(os.path.isfile('test/output/zipped.zip'))
        unzip('test/output/unzip.zip', 'test/output/unzipped/')
        self.assertTrue(os.path.isfile('test/output/unzipped/file.txt'))

    def test_error_zip_to_dir(self):
        with self.assertRaises(Exception):
            with no_stderrout():
                zip_dir('test/output/', 'test/output/')
        
    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
            
if __name__ == '__main__':
    unittest.main()