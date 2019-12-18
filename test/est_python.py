import unittest
import sys
import os
import shutil
from test.utility import no_stderrout, redirect_stdout

from gslab_make import start_makelog, clear_dir
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import CritError, ProgramError
    
from gslab_make import run_python as run_function
app = 'python'
ext = 'py'
executable = metadata.default_executables[os.name][app]
option = metadata.default_options[os.name][app]
arg = ''

class TestRunPython(unittest.TestCase):

    def setUp(self):
        with no_stderrout():
            clear_dir(['test/output/', 'test/log/'])

    def make_paths(self, makelog_path = 'test/log/make.log'):
        paths = {'makelog': makelog_path}
        
        with no_stderrout():
            start_makelog(paths)
            
        return(paths)
        
    def test_makelog(self):        
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext))
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_makelog_space(self):        
        with no_stderrout():
            paths = self.make_paths(makelog_path = 'test/log/make space.log')
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext))
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_makelog_character(self):        
        with no_stderrout():
            paths = self.make_paths(makelog_path = 'test/log/make_β.log')
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext))
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_no_makelog(self):        
        with no_stderrout():
            paths = self.make_paths(makelog_path = '')
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext))
            
        self.assertFalse(os.path.isfile(paths['makelog']))
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_log(self):      
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), log = 'test/output/log.log')
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertIn('Test script complete', open('test/output/log.log').read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_log_space(self):      
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), log = 'test/output/log space.log')
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertIn('Test script complete', open('test/output/log space.log').read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_log_character(self):      
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), log = 'test/output/log_β.log')
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertIn('Test script complete', open('test/output/log_β.log').read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_no_log(self):      
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), log = '')
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertFalse(os.path.isfile('test/output/log.log'))
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_program_space(self):      
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/python_script space.py')
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_program_character(self):      
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/python_script_β.py')
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_program_executable(self):      
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), executable = executable)
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_program_option(self):      
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), option = option)
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_program_arg(self):      
        with no_stderrout():
            paths = self.make_paths()
            run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), arg = arg)
            
        self.assertIn('Test script complete', open(paths['makelog']).read())
        self.assertTrue(os.path.isfile('test/output/output.csv'))

    def test_error_bad_paths(self):      
        try:
            with no_stderrout():
                paths = {}
                run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext))
        
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_os(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), osname = 'bad_os')
                
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_program_dir(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                run_function(paths, program = 'test/raw/run_program/program/')
                
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_program(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                run_function(paths, program = 'test/raw/run_program/%s_script_error.%s' % (app, ext))
                
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_program_missing(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                run_function(paths, program = 'test/raw/run_program/missing.%s' % ext)
                
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_program_wrong_extension(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                run_function(paths, program = 'test/raw/run_program/wrong_extension.txt')
                
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_executable(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), executable = [])          
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_option(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), option = [])               
        except Exception as e:
            self.assertRaises(Exception, e)

    def test_error_bad_arg(self):      
        try:
            with no_stderrout():
                paths = self.make_paths()
                run_function(paths, program = 'test/raw/run_program/%s_script.%s' % (app, ext), arg = [])              
        except Exception as e:
            self.assertRaises(Exception, e)

    def tearDown(self):
        if os.path.isdir('test/output/'):
            shutil.rmtree('test/output/')
        if os.path.isdir('test/log/'):
            shutil.rmtree('test/log/')
                
if __name__ == '__main__':
    unittest.main()