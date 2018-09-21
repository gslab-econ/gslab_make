# #! /usr/bin/env python
# import unittest, sys, os, shutil
# from gslab_make_dev.write_logs import write_heads_log, write_stats_log, write_output_logs, start_makelog
# from gslab_make_dev.dir_mod import clear_dir
# from gslab_make_dev.create_links import create_links
# from nostderrout import nostderrout
# from gslab_make_dev.private.utility import norm_path
# import gslab_make_dev.private.metadata as metadata
# import datetime
# import time
    

# class testOutputLogs(unittest.TestCase):

#     def setUp(self):
#         with nostderrout():
#             clear_dir(['../log', '../output'])  

#     def test_heads_log_default(self):
#     	default_log = metadata.settings['output_headslog']
#     	file1 = 'gslab_make_dev/tests/input/lyx_test_file.lyx'
#     	file2 = 'gslab_make_dev/tests/input/perl_test_script.pl'
#     	self.assertFalse(os.path.isfile(default_log))
#     	with nostderrout():
#     		write_heads_log(headslog_file=default_log, output_files=[file1, file2])
#     	lines = open(default_log).read().split('\n')
#     	self.assertTrue(lines[0]=='File headers')
#     	self.assertTrue(lines[2]==file1)
#     	self.assertTrue(lines[4]=='#LyX 2.1 created this file. For more info see http://www.lyx.org/')
#     	self.assertTrue(lines[15]==file2)
#     	self.assertTrue(lines[17]=='#! /usr/bin/env perl')
#     	self.assertTrue(lines[26]=='Head not readable or less than 10 lines')

#     def test_heads_log_2lines(self):
#     	default_log = metadata.settings['output_headslog']
#     	file1 = 'gslab_make_dev/tests/input/lyx_test_file.lyx'
#     	file2 = 'gslab_make_dev/tests/input/perl_test_script.pl'
#     	self.assertFalse(os.path.isfile(default_log))
#     	with nostderrout():
#     		write_heads_log(headslog_file=default_log, output_files=[file1, file2], \
#     			num_lines=2)
#     	lines = open(default_log).read().split('\n')
#     	self.assertTrue(lines[0]=='File headers')
#     	self.assertTrue(lines[2]==file1)
#     	self.assertTrue(lines[4]=='#LyX 2.1 created this file. For more info see http://www.lyx.org/')
#     	self.assertTrue(lines[7]==file2)
#     	self.assertTrue(lines[9]=='#! /usr/bin/env perl')

#     def test_heads_log_changelog(self):
#     	new_log = '../log/new_log.log'
#     	file1 = 'gslab_make_dev/tests/input/lyx_test_file.lyx'
#     	file2 = 'gslab_make_dev/tests/input/perl_test_script.pl'
#     	self.assertFalse(os.path.isfile(new_log))
#     	with nostderrout():
#     		write_heads_log(headslog_file=new_log, output_files=[file1, file2])
#     	lines = open(new_log).read().split('\n')
#     	self.assertTrue(lines[0]=='File headers')
#     	self.assertTrue(lines[2]==file1)
#     	self.assertTrue(lines[4]=='#LyX 2.1 created this file. For more info see http://www.lyx.org/')
#     	self.assertTrue(lines[15]==file2)
#     	self.assertTrue(lines[17]=='#! /usr/bin/env perl')
#     	self.assertTrue(lines[26]=='Head not readable or less than 10 lines')

#     def test_stats_log_default(self):
#     	default_log = metadata.settings['output_statslog']
#     	file1 = 'gslab_make_dev/tests/input/lyx_test_file.lyx'
#     	file2 = 'gslab_make_dev/tests/input/perl_test_script.pl'
#     	self.assertFalse(os.path.isfile(default_log))
#     	with nostderrout():
#     		write_stats_log(statslog_file=default_log, output_files=[file1, file2])
#     	lines = open(default_log).read().split('\n')
#     	self.assertTrue(len(lines)==4)
#     	self.assertTrue(lines[0]=='file name\tlast modified\tfile size')
#         stats = os.stat(file2)
#         last_mod = datetime.datetime.utcfromtimestamp(round(stats.st_mtime))
#         file_size = stats.st_size
#         self.assertTrue(lines[2]=='\t'.join((file2, str(last_mod), str(file_size))))

#     def test_stats_log_changelog(self):
#     	new_log = '../log/new_log.log'
#     	file1 = 'gslab_make_dev/tests/input/lyx_test_file.lyx'
#     	file2 = 'gslab_make_dev/tests/input/perl_test_script.pl'
#     	self.assertFalse(os.path.isfile(new_log))
#     	with nostderrout():
#     		write_stats_log(statslog_file=new_log, output_files=[file1, file2])
#     	lines = open(new_log).read().split('\n')
#     	self.assertTrue(len(lines)==4)
#     	self.assertTrue(lines[0]=='file name\tlast modified\tfile size')
#         stats = os.stat(file2)
#         last_mod = datetime.datetime.utcfromtimestamp(round(stats.st_mtime))
#         file_size = stats.st_size
#         self.assertTrue(lines[2]=='\t'.join((file2, str(last_mod), str(file_size))))

#     def test_write_output_logs_from_cwd(self):
#     	default_makelog = metadata.settings['makelog']
#     	default_headslog = metadata.settings['output_headslog']
#     	default_statslog = metadata.settings['output_statslog']
#     	with nostderrout():
#     		start_makelog()
#     		write_output_logs(output_dir='.')

# 	    	self.assertTrue(os.path.isfile(default_makelog))
# 	    	self.assertTrue(os.path.isfile(default_headslog))
# 	    	self.assertTrue(os.path.isfile(default_statslog))
# 	    	self.assertIn(norm_path('gslab_make_dev/tests/input/lyx_beamer_test_file.lyx'), \
# 	    		open(default_headslog).read())
# 	    	self.assertIn(norm_path('gslab_make_dev/tests/input/lyx_beamer_test_file.lyx'), \
# 	    		open(default_statslog).read())
# 	    	self.assertIn('Output logs successfully written!', open(default_makelog).read())

#     def test_write_output_changelog(self):
#     	new_makelog = '../log/new_log.log'
#     	new_headslog = '../log/new_headslog.log'
#     	new_statslog = '../log/new_statslog.log'
#     	with nostderrout():
#     		start_makelog(makelog=new_makelog)
#     		write_output_logs(output_dir='.', makelog=new_makelog, \
#     			output_headslog=new_headslog, output_statslog=new_statslog)

# 	    	self.assertTrue(os.path.isfile(new_makelog))
# 	    	self.assertTrue(os.path.isfile(new_headslog))
# 	    	self.assertTrue(os.path.isfile(new_statslog))
# 	    	self.assertIn(norm_path('gslab_make_dev/tests/input/lyx_beamer_test_file.lyx'), \
# 	    		open(new_headslog).read())
# 	    	self.assertIn(norm_path('gslab_make_dev/tests/input/lyx_beamer_test_file.lyx'), \
# 	    		open(new_statslog).read())
# 	    	self.assertIn('Output logs successfully written!', open(new_makelog).read())

#     def test_write_output_recursion(self):
#     	default_makelog = metadata.settings['makelog']
#     	default_headslog = metadata.settings['output_headslog']
#     	default_statslog = metadata.settings['output_statslog']
#     	with nostderrout():
#     		start_makelog()
#     		write_output_logs(output_dir='.', recursive=0)

# 	    	self.assertTrue(os.path.isfile(default_makelog))
# 	    	self.assertTrue(os.path.isfile(default_headslog))
# 	    	self.assertTrue(os.path.isfile(default_statslog))
# 	    	self.assertIn(norm_path('LICENSE.txt'), \
# 	    		open(default_headslog).read())
# 	    	self.assertIn(norm_path('LICENSE.tx'), \
# 	    		open(default_statslog).read())
# 	    	self.assertNotIn(norm_path('gslab_make_dev'), \
# 	    		open(default_headslog).read())
# 	    	self.assertNotIn(norm_path('gslab_make_dev'), \
# 	    		open(default_statslog).read())
# 	    	self.assertIn('Output logs successfully written!', open(default_makelog).read())

#     def test_write_output_logs_via_symlink(self):
#     	default_makelog = metadata.settings['makelog']
#     	default_headslog = metadata.settings['output_headslog']
#     	default_statslog = metadata.settings['output_statslog']
#     	with nostderrout():
#     		start_makelog()
#     		link_map = create_links(['gslab_make_dev/tests/input/test_file_list.txt'], link_dir='../output/')
#     		time.sleep(.1)
#     		write_output_logs(output_dir='.')
# 	    	self.assertTrue(os.path.isfile('../output/linked_lyx_file'))
# 	    	self.assertTrue(os.path.isdir('../output/linked_folder'))
# 	    	self.assertTrue(os.path.isfile(default_makelog))
# 	    	self.assertTrue(os.path.isfile(default_headslog))
# 	    	self.assertTrue(os.path.isfile(default_statslog))
# 	    	self.assertIn(norm_path('gslab_make_dev/tests/input/lyx_beamer_test_file.lyx'), \
# 	    		open(default_headslog).read())
# 	    	self.assertIn(norm_path('gslab_make_dev/tests/input/lyx_beamer_test_file.lyx'), \
# 	    		open(default_statslog).read())
# 	    	self.assertIn('Output logs successfully written!', open(default_makelog).read())

#     def tearDown(self):
#         if os.path.isdir('../log/'):
#            shutil.rmtree('../log/')
#         if os.path.isdir('../output/'):
#            shutil.rmtree('../output/')

# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()