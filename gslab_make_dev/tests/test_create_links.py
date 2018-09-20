# #! /usr/bin/env python
# import unittest, sys, os, shutil
# from gslab_make_dev.write_logs import start_makelog, end_makelog
# from gslab_make_dev.create_links import create_links
# from gslab_make_dev.private.utility import norm_path
# from gslab_make_dev.dir_mod import clear_dir
# from nostderrout import nostderrout
# import time
    

# class testCreateLinks(unittest.TestCase):

#     def setUp(self):
#         with nostderrout():
#             clear_dir(['../input', '../log'])  
#             start_makelog()

#     def test_default(self):
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/test_file_list.txt'))
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/lyx_test_file.lyx'))
#         with nostderrout():
#             link_map = create_links(['gslab_make_dev/tests/input/test_file_list.txt'])
#         time.sleep(.1)
#         self.assertTrue(len(link_map)==2)
#         expected_entry = (unicode(norm_path('gslab_make_dev/tests/input/lyx_test_file.lyx'),'utf-8'), \
#         	unicode(norm_path('../input/linked_lyx_file'),'utf-8'))
#         self.assertTrue(expected_entry==link_map[0])
#         self.assertTrue(os.path.isfile('../input/linked_lyx_file'))
#         self.assertTrue(os.path.isdir('../input/linked_folder'))
#         with nostderrout():
#             os.remove('../input/linked_lyx_file')
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/lyx_test_file.lyx'))

#     def test_bad_list(self):
#         with nostderrout():
#             create_links(['nonexistent_list'])
#         self.assertIn('An error was encountered with `create_links`', open('../log/make.log').read())

#     def test_wildcard(self):
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/test_file_list_w_wildcard.txt'))
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/matlab_test_script_wait1.m'))
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/matlab_test_script_wait2.m'))
#         with nostderrout():
#             create_links(['gslab_make_dev/tests/input/test_file_list_w_wildcard.txt'])
#         time.sleep(.1)
#         self.assertTrue(os.path.isfile('../input/matlab_link1.m'))
#         self.assertTrue(os.path.isfile('../input/matlab_link2.m'))

#     def test_multiple_lists(self):
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/test_file_list.txt'))
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/test_file_list_w_wildcard.txt'))
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/matlab_test_script_wait1.m'))
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/matlab_test_script_wait2.m'))
#         with nostderrout():
#             create_links(['gslab_make_dev/tests/input/test_file_list.txt', \
#                             'gslab_make_dev/tests/input/test_file_list_w_wildcard.txt'])
#         time.sleep(.1)
#         self.assertTrue(os.path.isfile('../input/linked_lyx_file'))
#         self.assertTrue(os.path.isdir('../input/linked_folder'))
#         self.assertTrue(os.path.isfile('../input/matlab_link1.m'))
#         self.assertTrue(os.path.isfile('../input/matlab_link2.m'))

#     def test_change_log(self):
#         with nostderrout():
#             end_makelog()
#             newlog = '../input/new_log'
#             start_makelog(makelog = newlog)
#             create_links(['nonexistent_list'], makelog = newlog)
#         self.assertIn('An error was encountered with `create_links`', open(newlog).read())

#     def test_change_linkdir(self):
#         with nostderrout():
#             create_links(['gslab_make_dev/tests/input/test_file_list.txt'], link_dir='../log/')
#             time.sleep(.1)
#         self.assertTrue(os.path.isfile('../log/linked_lyx_file'))

#     def tearDown(self):
#         if os.path.isdir('../input/'):
#            shutil.rmtree('../input/')
#         if os.path.isdir('../log/'):
#            shutil.rmtree('../log/')

# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()