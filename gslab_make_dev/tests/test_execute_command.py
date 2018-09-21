# #! /usr/bin/env python

# import unittest, sys, os, shutil, contextlib
# from gslab_make_dev.write_logs import start_makelog
# from gslab_make_dev import clear_dir
# from gslab_make_dev import execute_command
# import gslab_make_dev.private.metadata as metadata
# from gslab_make_dev.tests      import nostderrout
    

# class testExecuteCommand(unittest.TestCase):

#     def setUp(self):
#     	self.assertIn(os.name, ['posix', 'nt'])
#     	self.assertFalse(os.path.isfile('test_data.txt'))
#         default_makelog = metadata.settings['makelog']
#         with nostderrout():
#             clear_dir(['../log/'])  

#     def test_default_log(self):
#     	default_makelog = metadata.settings['makelog']
#     	start_makelog(default_makelog)
#         self.assertFalse(os.path.isfile('test_data.txt'))
#         if os.name=='posix':
#             our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
#         else:
#             our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'
#         with nostderrout():
#             execute_command(command = our_unzip) 
#         self.assertIn('test_data.txt', open(default_makelog).read())
#         self.assertTrue(os.path.isfile('test_data.txt'))
        
#     def test_custom_log(self):
#         makelog_file = '../log/custom_make.log'
#         start_makelog(makelog_file)
#         if os.name=='posix':
#             our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
#         else:
#             our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'
#         with nostderrout():
#             execute_command(command = our_unzip, makelog = makelog_file)
#         self.assertIn('test_data.txt', open(makelog_file).read())
#         self.assertTrue(os.path.isfile('test_data.txt'))
        
#     def test_independent_log(self):
#     	default_makelog = metadata.settings['makelog']
#     	independent_log = '../log/command.log'
#     	start_makelog(default_makelog)
#         if os.name=='posix':
#             our_unzip = 'unzip gslab_make_dev/tests/input/zip_test_file.zip'
#         else:
#             our_unzip = 'wzunzip gslab_make_dev/tests/input/zip_test_file.zip'     
#         with nostderrout():
#             execute_command(command = our_unzip, log = independent_log)
#         self.assertIn('test_data.txt', open(default_makelog).read())
#         self.assertIn('test_data.txt', open(independent_log).read())
#         self.assertTrue(os.path.isfile('test_data.txt'))
   
#     def tearDown(self):
#         if os.path.isdir('../log/'):
#             shutil.rmtree('../log/')
#         if os.path.isfile('test_data.txt'):
#             os.remove('test_data.txt')
    
# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()
