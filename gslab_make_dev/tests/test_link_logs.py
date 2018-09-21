# #! /usr/bin/env python
# import unittest, sys, os, shutil
# from gslab_make_dev.write_logs import start_makelog
# from gslab_make_dev.write_link_logs import write_link_maplog, write_link_logs
# from gslab_make_dev.dir_mod import clear_dir
# from gslab_make_dev.create_links import create_links
# from nostderrout import nostderrout
# from gslab_make_dev.private.utility import norm_path
# import gslab_make_dev.private.metadata as metadata
# import datetime
# import time
    

# class testLinkLogs(unittest.TestCase):

#     def setUp(self):
#         with nostderrout():
#             clear_dir(['../log', '../input'])  

#     def test_link_maplog_default(self):        
#         default_maplog = metadata.settings['link_maplog']
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/test_file_list.txt'))
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/lyx_test_file.lyx'))
#         with nostderrout():
#             start_makelog()
#             link_map = create_links(['gslab_make_dev/tests/input/test_file_list.txt'])
#             time.sleep(.1)
#             write_link_maplog(link_maplog = default_maplog, link_map = link_map)

#         lines = open(default_maplog).read().split('\n')
#         self.assertTrue(len(lines)==4)
#         self.assertTrue(lines[0]=='target\tsymlink')
#         self.assertTrue(lines[1]=='\t'.join((norm_path('gslab_make_dev/tests/input/lyx_test_file.lyx'), \
#             norm_path('../input/linked_lyx_file'))))

#     def test_link_maplog_newlog(self):        
#         new_maplog = '../log/new_maplog.log'
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/test_file_list.txt'))
#         self.assertTrue(os.path.isfile('gslab_make_dev/tests/input/lyx_test_file.lyx'))
#         with nostderrout():
#             start_makelog()
#             link_map = create_links(['gslab_make_dev/tests/input/test_file_list.txt'])
#             time.sleep(.1)
#             write_link_maplog(link_maplog = new_maplog, link_map = link_map)

#         lines = open(new_maplog).read().split('\n')
#         self.assertTrue(len(lines)==4)
#         self.assertTrue(lines[0]=='target\tsymlink')
#         self.assertTrue(lines[1]=='\t'.join((norm_path('gslab_make_dev/tests/input/lyx_test_file.lyx'), \
#             norm_path('../input/linked_lyx_file'))))


#     def test_write_link_logs_default(self):
#         default_makelog = metadata.settings['makelog']
#         default_headslog = metadata.settings['link_headslog']
#         default_statslog = metadata.settings['link_statslog']
#         default_maplog = metadata.settings['link_maplog']
#         with nostderrout():
#             start_makelog()
#             link_map = create_links(['gslab_make_dev/tests/input/test_file_list.txt'])
#             time.sleep(.1)
#             write_link_logs(link_map)
#         self.assertTrue(os.path.isfile('../input/linked_lyx_file'))
#         self.assertTrue(os.path.isdir('../input/linked_folder'))
#         self.assertTrue(os.path.isfile(default_makelog))
#         self.assertTrue(os.path.isfile(default_headslog))
#         self.assertTrue(os.path.isfile(default_statslog))
#         self.assertTrue(os.path.isfile(default_maplog))
#         for log in [default_headslog, default_statslog]:      
#             self.assertIn(norm_path('gslab_make_dev/tests/input/lyx_beamer_test_file.lyx'), open(log).read())
#         self.assertIn('Link logs successfully written!', open(default_makelog).read())
#         maplog_lines = open(default_maplog).read().split('\n')
#         self.assertTrue(len(maplog_lines)==4)
#         self.assertTrue(maplog_lines[0]=='target\tsymlink')
#         self.assertTrue(maplog_lines[1]=='\t'.join((norm_path('gslab_make_dev/tests/input/lyx_test_file.lyx'), \
#             norm_path('../input/linked_lyx_file'))))

#     def test_write_link_logs_recursive(self):
#         default_makelog = metadata.settings['makelog']
#         default_headslog = metadata.settings['link_headslog']
#         default_statslog = metadata.settings['link_statslog']
#         default_maplog = metadata.settings['link_maplog']
#         with nostderrout():
#             start_makelog()
#             link_map = create_links(['gslab_make_dev/tests/input/test_file_list.txt'])
#             time.sleep(.1)
#             write_link_logs(link_map, recursive=0)
#         self.assertTrue(os.path.isfile('../input/linked_lyx_file'))
#         self.assertTrue(os.path.isdir('../input/linked_folder'))
#         self.assertTrue(os.path.isfile(default_makelog))
#         self.assertTrue(os.path.isfile(default_headslog))
#         self.assertTrue(os.path.isfile(default_statslog))
#         self.assertTrue(os.path.isfile(default_maplog))
#         for log in [default_headslog, default_statslog]:      
#             self.assertNotIn(norm_path('gslab_make_dev/tests/input/lyx_beamer_test_file.lyx'), open(log).read())
#             self.assertIn(norm_path('gslab_make_dev/tests/__init__.py'), open(log).read())
#         self.assertIn('Link logs successfully written!', open(default_makelog).read())
#         maplog_lines = open(default_maplog).read().split('\n')
#         self.assertTrue(len(maplog_lines)==4)
#         self.assertTrue(maplog_lines[0]=='target\tsymlink')
#         self.assertTrue(maplog_lines[1]=='\t'.join((norm_path('gslab_make_dev/tests/input/lyx_test_file.lyx'), \
#             norm_path('../input/linked_lyx_file'))))

#     def test_write_link_logs_changelog(self):
#         new_makelog = '../log/new_makelog.log'
#         new_headslog = '../log/new_headslog.log'
#         new_statslog = '../log/new_statslog.log'
#         new_maplog = '../log/new_maplog.log'
#         with nostderrout():
#             start_makelog(makelog=new_makelog)
#             link_map = create_links(['gslab_make_dev/tests/input/test_file_list.txt'], \
#                 makelog=new_makelog)
#             time.sleep(.1)
#             write_link_logs(link_map, makelog=new_makelog, link_headslog=new_headslog, \
#                 link_statslog=new_statslog, link_maplog=new_maplog)
#         self.assertTrue(os.path.isfile('../input/linked_lyx_file'))
#         self.assertTrue(os.path.isdir('../input/linked_folder'))
#         self.assertTrue(os.path.isfile(new_makelog))
#         self.assertTrue(os.path.isfile(new_headslog))
#         self.assertTrue(os.path.isfile(new_statslog))
#         self.assertTrue(os.path.isfile(new_maplog))
#         for log in [new_headslog, new_statslog]:      
#             self.assertIn(norm_path('gslab_make_dev/tests/input/lyx_beamer_test_file.lyx'), open(log).read())
#         self.assertIn('Link logs successfully written!', open(new_makelog).read())
#         maplog_lines = open(new_maplog).read().split('\n')
#         self.assertTrue(len(maplog_lines)==4)
#         self.assertTrue(maplog_lines[0]=='target\tsymlink')
#         self.assertTrue(maplog_lines[1]=='\t'.join((norm_path('gslab_make_dev/tests/input/lyx_test_file.lyx'), \
#             norm_path('../input/linked_lyx_file'))))

#     def tearDown(self):
#         if os.path.isdir('../log/'):
#            shutil.rmtree('../log/')
#         if os.path.isdir('../input/'):
#            shutil.rmtree('../input/')

# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()