import unittest
import sys
import os
import shutil
from test.utility import no_stderrout, redirect_stdout, create_file, read_file

from gslab_make.modify_dir import clear_dir

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
        try:
            with no_stderrout:
            	clear_dir(['test/output/text.txt'])
        except Exception as e:
            self.assertRaises(Exception, e)

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')         
        if os.path.isfile('test/stdout.txt'):
            os.remove('test/stdout.txt') 

if __name__ == '__main__':
    unittest.main()