import unittest
import sys
import os
import shutil
import zipfile
from test.utility import no_stderrout, create_file

from gslab_make.modify_dir import zip_dir, unzip

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

        try:
            # Unzip zip
            unzip('test/output/unzip.zip', 'test/output/unzipped.txt')
        except Exception as e:
            # Check unzip
            self.assertRaises(Exception, e)
        
    def test_zip_to_not_exist_file(self):        
        # Zip directory
        with no_stderrout():
            zip_dir('test/output/', 'test/output/zipped.zip')
        
        # Check zip
        self.assertTrue(os.path.isfile('test/output/zipped.zip'))

    def test_zip_to_exist_file(self):        
        create_file('test/output/zipped.zip')    
        
        # Zip directory
        with no_stderrout():
            zip_dir('test/output/', 'test/output/zipped.zip')
        
        # Check zip
        self.assertTrue(os.path.isfile('test/output/zipped.zip'))
        unzip('test/output/unzip.zip', 'test/output/unzipped/')
        self.assertTrue(os.path.isfile('test/output/unzipped/file.txt'))

    def test_error_zip_to_dir(self):
        try:
            # Zip directory
            with no_stderrout():
                zip_dir('test/output/', 'test/output/')
        except Exception as e:
            # Check zip
            self.assertRaises(Exception, e)
        
    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')

if __name__ == '__main__':
    unittest.main()
