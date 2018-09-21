# #! /usr/bin/env python
# import unittest, sys, os, shutil
# from gslab_make_dev.write_logs import start_makelog, set_option
# from gslab_make_dev.dir_mod import clear_dir
# from gslab_make_dev.private.utility import norm_path
# from gslab_make_dev.tests.nostderrout import nostderrout
# import gslab_make_dev.private.metadata as metadata

# class testSetOption(unittest.TestCase):

#     def setUp(self):
#         with nostderrout():
#             clear_dir(['../log'])
#         self.assertTrue(metadata.settings['link_dir']=='../input/')
#         self.assertTrue(metadata.settings['temp_dir']=='../temp/')
#         self.assertTrue(metadata.settings['output_dir']=='../output/')
#         self.assertTrue(metadata.settings['makelog']=='../log/make.log')
#         self.assertTrue(metadata.settings['output_statslog']=='../log/output_stats.log')
#         self.assertTrue(metadata.settings['output_headslog']=='../log/output_heads.log')
#         self.assertTrue(metadata.settings['link_maplog']=='../log/link_map.log')
#         self.assertTrue(metadata.settings['link_statslog']=='../log/link_stats.log')
#         self.assertTrue(metadata.settings['link_headslog'] =='../log/link_heads.log')


# 	def test_metadata_changes(self):
# 		set_option(link_dir='new_link_dir', \
# 			temp_dir='new_temp_dir', \
# 			output_dir='new_output_dir', \
# 			makelog='new_makelog', \
# 			output_stats_log='new_output_statslog', \
# 			output_headslog='new_output_headslog', \
# 			link_maplog='new_link_maplog', \
# 			link_statslog='new_link_statslog', \
# 			link_headslog='new_link_headslog')

# 		self.assertTrue(metadata.settings.link_dir=='new_link_dir')
# 		self.assertTrue(metadata.settings.temp_dir=='new_temp_dir')
# 		self.assertTrue(metadata.settings.output_dir=='new_output_dir')
# 		self.assertTrue(metadata.settings.makelog=='new_makelog')
# 		self.assertTrue(metadata.settings.output_statslog=='new_output_statslog')
# 		self.assertTrue(metadata.settings.output_headslog=='new_output_headslog')
# 		self.assertTrue(metadata.settings.link_maplog=='new_link_maplog')
# 		self.assertTrue(metadata.settings.link_statslog=='new_link_statslog')
# 		self.assertTrue(metadata.settings.link_headslog=='new_link_headslog')

#     def test_new_makelog(self):
#     	newlog = '../log/new_log.log'
#         set_option(makelog=newlog)
#         self.assertFalse(metadata.makelog_started)
#         with nostderrout():
#             start_makelog()
#         self.assertTrue(metadata.makelog_started)
#         self.assertTrue(os.path.isfile(newlog))
#         self.assertIn(norm_path('.'), open(newlog).read())
#         self.assertTrue(metadata.makelog_started)
#         self.assertIn(messages.note_makelog_start, open(newlog).read())
#         self.assertIn(messages.note_working_directory, open(newlog).read())
#         self.assertNotIn("Testing write", open(newlog).read())
#         with nostderrout():
#             write_to_makelog(u"Testing write")
#         self.assertIn("Testing write", open(newlog).read())
#         self.assertNotIn(messages.note_makelog_end, open(newlog).read())
#         with nostderrout():
#             end_makelog()
#         self.assertIn(messages.note_makelog_end, open(newlog).read())
#         self.assertFalse(os.path.isfile('../log/make.log'))

# 	def tearDown(self):
# 		if os.path.isdir('../log/'):
# 			shutil.rmtree('../log/')
# 		set_option(link_dir='../input/', \
# 			temp_dir='../temp/', \
# 			output_dir='../output/', \
# 			makelog='../log/make.log', \
# 			output_stats_log='../log/output_stats.log', \
# 			output_headslog='../log/output_heads.log', \
# 			link_maplog= '../log/link_map.log', \
# 			link_statslog='../log/link_stats.log', \
# 			link_headslog='../log/link_heads.log')



# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()