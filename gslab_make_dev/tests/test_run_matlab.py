# #! /usr/bin/env python

# import unittest, sys, os, shutil, contextlib
# sys.path.append('../..')
# from gslab_make_dev.make_log import start_make_logging
# from gslab_make_dev.dir_mod import clear_dirs
# from gslab_make_dev.run_program import run_matlab
# from nostderrout import nostderrout
# import gslab_make_dev.private.metadata as metadata

# class testRunMatlab(unittest.TestCase):

#     def setUp(self):
#         makelog_file = '../output/make.log'
#         output_dir = '../output/'
#         with nostderrout():
#             clear_dirs(output_dir)
#             start_make_logging(makelog_file)

#     def test_default_log(self):
#         run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m')
#         self.assert_proper_output('../output/make.log')
#         self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        
#     def test_custom_log(self):
#         os.remove('../output/make.log')
#         makelog_file = '../output/custom_make.log'
#         output_dir = '../output/'
#         with nostderrout():
#             clear_dirs(output_dir)
#             start_make_logging(makelog_file)
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', makelog = '../output/custom_make.log')
#         self.assert_proper_output('../output/custom_make.log')
#         self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        
#     def test_independent_log(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', log = '../output/matlab.log')
#         self.assert_proper_output('../output/make.log')
#         self.assertTrue(os.path.isfile('../output/matlab.log'))
#         self.assert_proper_output('../output/matlab.log')
#         self.assertTrue(os.path.isfile('../output/matlab_test.mat'))

#     def test_no_extension(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script')
#         self.assert_proper_output('../output/make.log')
#         self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        
#     def test_executable(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', executable = metadata.default_executables[os.name]['matlab']) 
#         self.assert_proper_output('../output/make.log')
#         self.assertTrue(os.path.isfile('../output/matlab_test.mat'))
        
#     def test_bad_executable(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', executable = 'nonexistent_matlab_executable')
#         self.assertNotIn('1.716', open('../output/make.log', 'rU').read())
    
#     def test_no_program(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/nonexistent_matlab_script.m')
#         self.assertNotIn('1.716', open('../output/make.log', 'rU').read())
    
#     def test_option(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script.m', option = '-h')
#         logfile_data = open('../output/make.log', 'rU').read()
#         if os.name == 'posix':
#             self.assertIn('matlab [-h|-help]', logfile_data)
#         else:
#             self.assertIn('matlab [-? ^| -h ^| -help]', logfile_data)
            
#     def test_wait(self):
#         with nostderrout():
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script_wait1.m')
#             run_matlab(program = 'gslab_make_dev/tests/input/matlab_test_script_wait2.m')
#         file_data = open('../output/make.log', 'rU').read()
#         self.assertIn('1.716', file_data)
#         self.assertNotIn('Error', file_data)

#     def assert_proper_output(self, filename):
#         file_data = open(filename, 'rU').read()
#         self.assertIn('0.8147', file_data)
#         self.assertNotIn('Error', file_data)

#     def tearDown(self):
#         if os.path.isdir('../output/'):
#             shutil.rmtree('../output/')
    
# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()
