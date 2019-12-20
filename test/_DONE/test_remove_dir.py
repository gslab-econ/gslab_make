import unittest
import sys
import os
import shutil
from test.utility import no_stderrout, redirect_stdout, create_file, read_file

from gslab_make.modify_dir import remove_dir

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
        try:   
            remove_dir(['test/output/text.txt'], quiet = True)       
        except Exception as e:
            self.assertRaises(Exception, e)

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')  
        if os.path.isfile('test/stdout.txt'):
            os.remove('test/stdout.txt') 
        
if __name__ == '__main__':
    unittest.main()