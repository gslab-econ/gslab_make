# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import raise_from
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

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
        with self.assertRaises(Exception):
            tablefill(template = 'test/raw/tablefill/tablefill_template_missing_input.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill.txt'], 
                      output   = 'test/output/tablefill.lyx')

    def test_error_duplicate(self):
        with self.assertRaises(Exception):
            tablefill(template = 'test/raw/tablefill/tablefill_template.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill.txt', 
                                  'test/raw/tablefill/tablefill_duplicate.txt'], 
                      output   = 'test/output/tablefill.lyx')

    def test_error_no_tag(self):
        with self.assertRaises(Exception):
            tablefill(template = 'test/raw/tablefill/tablefill_template.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill_no_tag.txt'], 
                      output   = 'test/output/tablefill.lyx')

    def test_error_too_many_values(self):
        with self.assertRaises(Exception):
            tablefill(template = 'test/raw/tablefill/tablefill_template_too_many_values.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill.txt'], 
                      output   = 'test/output/tablefill.lyx')

    def test_error_not_enough_values(self):
        with self.assertRaises(Exception):
            tablefill(template = 'test/raw/tablefill/tablefill_template_not_enough_values.lyx', 
                      inputs   = ['test/raw/tablefill/tablefill.txt'], 
                      output   = 'test/output/tablefill.lyx')

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')

if __name__ == '__main__':
    unittest.main()
