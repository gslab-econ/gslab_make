# -*- coding: utf-8 -*-
import unittest
import sys
import os
import shutil
import zipfile
from test.utility import no_stderrout

from gslab_make import tablefill

class TestTablefill(unittest.TestCase):

    def setUp(self):
        # Create output directory
        self.assertFalse(os.path.isdir('test/output/'))
        os.makedirs('test/output/')

    def test_tablefill(self):
        tablefill(template = 'test/raw/tablefill/tablefill_template.lyx', 
                  inputs   = ['test/raw/tablefill/tablefill.txt'], 
                  output   = 'test/output/tablefill.lyx')

        self.assertTrue(os.path.isfile('test/output/tablefill.lyx'))
    
    def test_tablefill_character(self):
        tablefill(template = 'test/raw/tablefill/tablefill_template_╬▓.lyx', 
                  inputs   = ['test/raw/tablefill/tablefill_╬▓.txt'], 
                  output   = 'test/output/tablefill_╬▓.lyx')

        self.assertTrue(os.path.isfile('test/output/tablefill_╬▓.lyx'))

    def test_tablefill_space(self):
        tablefill(template = 'test/raw/tablefill/tablefill_template space.lyx', 
                  inputs   = ['test/raw/tablefill/tablefill space.txt'], 
                  output   = 'test/output/tablefill space.lyx')

        self.assertTrue(os.path.isfile('test/output/tablefill space.lyx'))

    def test_tablefill_string(self):
        tablefill(template = 'test/raw/tablefill/tablefill_template.lyx', 
                  inputs   = 'test/raw/tablefill/tablefill.txt', 
                  output   = 'test/output/tablefill.lyx')

        self.assertTrue(os.path.isfile('test/output/tablefill.lyx'))

    def test_extra_input(self):
        tablefill(template = 'test/raw/tablefill/tablefill_template_extra_input.lyx', 
                  inputs   = ['test/raw/tablefill/tablefill.txt'], 
                  output   = 'test/output/tablefill.lyx')

        self.assertTrue(os.path.isfile('test/output/tablefill.lyx'))

    def test_null(self):
        tablefill(template = 'test/raw/tablefill/tablefill_template.lyx', 
                  inputs   = ['test/raw/tablefill/tablefill.txt'], 
                  output   = 'test/output/tablefill.lyx', 
                  null     = '0')

        self.assertTrue(os.path.isfile('test/output/tablefill.lyx'))

    def test_latex(self):
        tablefill(template = 'test/raw/tablefill/tablefill_template.tex', 
                  inputs   = ['test/raw/tablefill/tablefill.txt'], 
                  output   = 'test/output/tablefill.tex')

        self.assertTrue(os.path.isfile('test/output/tablefill.tex'))

    def test_error_missing_input(self):
        try:
            tablefill(template = 'test/raw/tablefill/tablefill_template_missing_input.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill.txt'], 
                      output   = 'test/output/tablefill.lyx')
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_duplicate(self):
        try:
            tablefill(template = 'test/raw/tablefill/tablefill_template.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill.txt', 
                                  'test/raw/tablefill/tablefill_duplicate.txt'], 
                      output   = 'test/output/tablefill.lyx')
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_no_tag(self):
        try:
            tablefill(template = 'test/raw/tablefill/tablefill_template.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill_no_tag.txt'], 
                      output   = 'test/output/tablefill.lyx')
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_too_many_values(self):
        try:
            tablefill(template = 'test/raw/tablefill/tablefill_template_too_many_values.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill.txt'], 
                      output   = 'test/output/tablefill.lyx')
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_not_enough_values(self):
        try:
            tablefill(template = 'test/raw/tablefill/tablefill_template_not_enough_values.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill.txt'], 
                      output   = 'test/output/tablefill.lyx')
        except Exception as e:
            self.assertRaises(Exception, e)

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')

if __name__ == '__main__':
    unittest.main()
