import unittest
import sys
import os
import shutil
import zipfile
from utility import no_stderrout, create_file

from gslab_make.modify_dir import zip_dir, unzip

class TestZip(unittest.TestCase):

    def set_up(self):
        # Create output directory
        self.assertFalse(os.path.isdir('output/'))
        os.makedirs('output/')

        # Create test file
        create_file('output/file.txt') 

        # Create test zip
        with zipfile.ZipFile('output/unzip.zip', 'w', zipfile.ZIP_DEFLATED) as z:
            z.write('output/file.txt', arcname = 'file.txt')

    def test_unzip_to_not_exist_dir(self):
        unzip('output/unzip.zip', 'output/unzipped/')
        self.assertTrue(os.path.isfile('output/unzipped/file.txt'))

    def test_unzip_to_exist_dir(self):        
        os.makedirs('output/unzipped')
        create_file('output/exist.txt') 
        
        unzip('output/unzip.zip', 'output/unzipped/')
        self.assertTrue(os.path.isfile('output/unzipped/file.txt'))
        self.assertTrue(os.path.isfile('output/unzipped/exist.txt'))

    def test_unzip_to_not_exist_file(self):
        unzip('output/unzip.zip', 'output/unzipped.txt')
        self.assertTrue(os.path.isfile('output/unzipped.txt/file.txt'))
  
    def test_error_unzip_to_exist_file(self):
        create_file('output/unzipped.txt') 

        with Exception as e:
            unzip('output/unzip.zip', 'output/unzipped.txt')
            self.assertRaises(Exception, e)
        
    def test_zip_to_not_exist_file(self):        
        with no_stderrout():
            zip_dir('output/', 'output/zipped.zip')
        self.assertTrue(os.path.isfile('output/zipped.zip'))

    def test_zip_to_exist_file(self):        
        create_file('output/zipped.zip')
            
        with no_stderrout():
            zip_dir('output/', 'output/zipped.zip')
        self.assertTrue(os.path.isfile('output/zipped.zip'))
        
        unzip('output/unzip.zip', 'output/unzipped/')
        self.assertTrue(os.path.isfile('output/unzipped/file.txt'))

    def test_error_zip_to_dir(self):
        with Exception as e:
            with no_stderrout():
                zip_dir('output/', 'output/')
            self.assertRaises(Exception, e)
        
    def tear_down(self):
        if os.path.isdir('output/'):
            shutil.rmtree('output/')

if __name__ == '__main__':
    unittest.main()
