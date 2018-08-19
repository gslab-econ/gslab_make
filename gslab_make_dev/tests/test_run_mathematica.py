# #! /usr/bin/env python

# import unittest, sys, os, shutil, contextlib
# from gslab_make_dev.make_log import start_make_logging
# from gslab_make_dev.dir_mod import clear_dirs
# from gslab_make_dev.run_program import run_mathematica
# from nostderrout import nostderrout
# import gslab_make_dev.private.metadata as metadata


# class testRunMathematica(unittest.TestCase):

#     def setUp(self):
#         makelog_file = '../output/make.log'
#         output_dir = '../output/'
#         with nostderrout():
#             clear_dirs(output_dir)
#             start_make_logging(makelog_file)

#     def test_default_log(self):
#         with nostderrout():
#             run_mathematica(program = 'gslab_make_dev/tests/input/mathematica_test_script.m')       
#         self.assertIn('mathematica test ended', open('../output/make.log', 'rU').read())        
#         self.assertTrue(os.path.isfile('output_plot.eps'))
        
#     def test_custom_log(self):
#         os.remove('../output/make.log')
#         makelog_file = '../output/custom_make.log'
#         output_dir = '../output/'
#         with nostderrout():
#             clear_dirs(output_dir)
#             start_make_logging(makelog_file)
#             run_mathematica(program = 'gslab_make_dev/tests/input/mathematica_test_script.m', makelog = '../output/custom_make.log')   
#         self.assertIn('mathematica test ended', open('../output/custom_make.log', 'rU').read())   
#         self.assertTrue(os.path.isfile('output_plot.eps'))
        
#     def test_independent_log(self):
#         with nostderrout():
#             run_mathematica(program = 'gslab_make_dev/tests/input/mathematica_test_script.m', log = '../output/mathematica.log')        
#         self.assertIn('mathematica test ended', open('../output/make.log', 'rU').read())   
#         self.assertTrue(os.path.isfile('../output/mathematica.log'))    
#         self.assertIn('mathematica test ended',  open('../output/mathematica.log', 'rU').read())   
#         self.assertTrue(os.path.isfile('output_plot.eps')) 

#     def test_no_extension(self):
#         with nostderrout():
#             run_mathematica(program = 'gslab_make_dev/tests/input/mathematica_test_script')       
#         self.assertIn('mathematica test ended', open('../output/make.log', 'rU').read()  ) 
#         self.assertTrue(os.path.isfile('output_plot.eps'))
        
#     def test_executable(self):
#         with nostderrout():
#             run_mathematica(program = 'gslab_make_dev/tests/input/mathematica_test_script.m', executable = metadata.default_executables[os.name]['math'])       
#         self.assertIn('mathematica test ended', open('../output/make.log', 'rU').read()     )  
#         self.assertTrue(os.path.isfile('output_plot.eps'))
        
#     def test_bad_executable(self):
#         with nostderrout():
#             run_mathematica(program = 'gslab_make_dev/tests/input/mathematica_test_script.m', executable = 'nonexistent_mathematica_executable')
#         self.assertNotIn('mathematica test ended', open('../output/make.log', 'rU').read()) 

#     def test_no_program(self):
#         with nostderrout():
#             run_mathematica(program = 'gslab_make_dev/tests/input/nonexistent_mathematica_script.m')
#         self.assertNotIn('mathematica test ended', open('../output/make.log', 'rU').read()) 
    
#     def test_option(self):
#         with nostderrout():
#             run_mathematica(program = 'gslab_make_dev/tests/input/mathematica_test_script.m', option = '-initfile gslab_make_dev/tests/input/mathematica_init_script.m')     
#         self.assertIn('mathematica test ended', open('../output/make.log', 'rU').read()) 
    
#     def tearDown(self):
#         if os.path.isdir('../output/'):
#             shutil.rmtree('../output/')
#         if os.path.isfile('output_plot.eps'):
#             os.remove('output_plot.eps')
#         if os.path.isfile('gslab_make_dev/tests/input/output_plot.eps'):
#             os.remove('gslab_make_dev/tests/input/output_plot.eps')
                
# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()
