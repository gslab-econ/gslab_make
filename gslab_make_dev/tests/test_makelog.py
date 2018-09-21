# #! /usr/bin/env python
# import unittest, sys, os, shutil
# from gslab_make_dev.write_logs import start_makelog, end_makelog, write_to_makelog
# from gslab_make_dev.dir_mod import clear_dir
# from gslab_make_dev.tests.nostderrout import nostderrout
# from gslab_make_dev.private.utility import norm_path
# import gslab_make_dev.private.metadata as metadata
# import gslab_make_dev.private.messages as messages
# from gslab_make_dev.private.exceptionclasses import CritError

# class testMakeLog(unittest.TestCase):

#     def setUp(self):
#         with nostderrout():
#             clear_dir(['../log'])

#     def test_default(self):
#         self.assertFalse(metadata.makelog_started)
#         with nostderrout():
#             start_makelog()
#         self.assertIn(norm_path('.'), open('../log/make.log').read())
#         self.assertTrue(metadata.makelog_started)
#         self.assertIn(messages.note_makelog_start, open('../log/make.log').read())
#         self.assertIn(messages.note_working_directory, open('../log/make.log').read())
#         self.assertNotIn("Testing write", open('../log/make.log').read())
#         with nostderrout():
#             write_to_makelog(u"Testing write")
#         self.assertIn("Testing write", open('../log/make.log').read())
#         self.assertNotIn(messages.note_makelog_end, open('../log/make.log').read())
#         with nostderrout():
#             end_makelog()
#         self.assertIn(messages.note_makelog_end, open('../log/make.log').read())

#     def test_newlog(self):
#         newlog = '../log/new_log.log'
#         self.assertFalse(metadata.makelog_started)
#         with nostderrout():
#             start_makelog(makelog=newlog)
#         self.assertIn(norm_path('.'), open(newlog).read())
#         self.assertTrue(metadata.makelog_started)
#         self.assertIn(messages.note_makelog_start, open(newlog).read())
#         self.assertIn(messages.note_working_directory, open(newlog).read())
#         self.assertNotIn("Testing write", open(newlog).read())
#         with nostderrout():
#             write_to_makelog(u"Testing write", makelog=newlog)
#         self.assertIn("Testing write", open(newlog).read())
#         self.assertNotIn(messages.note_makelog_end, open(newlog).read())
#         with nostderrout():
#             end_makelog(makelog=newlog)
#         self.assertIn(messages.note_makelog_end, open(newlog).read())
#         self.assertFalse(os.path.isfile('../log/make.log'))

#     def test_not_started(self):
#         self.assertFalse(metadata.makelog_started)
#         with self.assertRaises(CritError):
#             write_to_makelog(u"Testing write")
#         with self.assertRaises(CritError):
#             end_makelog()

#     def test_log_deleted(self):
#         self.assertFalse(metadata.makelog_started)
#         with nostderrout():
#             start_makelog()
#             os.remove('../log/make.log')
#         self.assertTrue(metadata.makelog_started)
#         with self.assertRaises(CritError):
#             write_to_makelog(u"Testing write")

#     def tearDown(self):
#         if os.path.isdir('../log/'):
#            shutil.rmtree('../log/')
#         metadata.makelog_started = False

# if __name__ == '__main__':
#     os.getcwd()
#     unittest.main()