#! /usr/bin/env python

import unittest, sys, os, shutil, contextlib
@contextlib.contextmanager
def redirect_stdout(target):
    original = sys.stdout
    sys.stdout = target
    yield
    sys.stdout = original
from gslab_make.dir_mod import remove_path
from nostderrout import nostderrout
import time
    

class testRemovePath(unittest.TestCase):

    def setUp(self):
        self.assertFalse(os.path.isdir('./output_local/'))
        os.makedirs('./output_local/')
        newfile = open('./output_local/text.txt', 'w+')
        newfile.write('test')
        newfile.close()

    def test_default(self):
        self.assertTrue(os.path.isdir('./output_local/'))
        with nostderrout():
        	remove_path('./output_local/')
        	time.sleep(0.1)
        self.assertFalse(os.path.isfile('./output_local/text.txt'))
        self.assertFalse(os.path.isdir('./output_local/'))

    def test_default_noisy(self):
        self.assertTrue(os.path.isfile('./output_local/text.txt'))
        with open('stdout.txt', 'w') as f:
        	with redirect_stdout(f):
        		remove_path('./output_local/')
        time.sleep(0.1)
        self.assertIn('Deleted:', open('stdout.txt').read())

    def test_options(self):
        self.assertTrue(os.path.isfile('./output_local/text.txt'))
        os.makedirs('./output_local/temp_dir/')     
        with nostderrout():
            remove_path('./output_local', option='-v')
            time.sleep(0.1)
        self.assertTrue(os.path.isdir('./output_local/')) #Shouldn't have been able to remove nonempty directory
        with nostderrout():
            remove_path('./output_local/')
            time.sleep(0.1)
        self.assertFalse(os.path.isdir('./output_local/'))

    def test_quiet(self):
        self.assertTrue(os.path.isfile('./output_local/text.txt'))
        with open('stdout.txt', 'w') as f:
        	with redirect_stdout(f):
        		remove_path('./output_local', quiet=True)
		time.sleep(0.1)
		self.assertNotIn('Deleted:', open('stdout.txt').read())

            
    def tearDown(self):
        if os.path.isdir('./output_local/'):
            shutil.rmtree('./output_local/')
        if os.path.isfile('stdout.txt'):
        	os.remove('stdout.txt')  

if __name__ == '__main__':
    os.getcwd()
    unittest.main()