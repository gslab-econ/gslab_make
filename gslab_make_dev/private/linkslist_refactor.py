#! /usr/bin/env python

import os
import glob
import re

from linkdirectives import *
from preliminaries import *
import metadata as metadata

class LinksList(object):

    def __init__(self, 
                 files_list, 
                 links_dir = metadata.settings['links_dir']):
        
        self.links_dir = links_dir
        self.files_list
        self.parse_files_list()
        self.get_paths()

    def parse_files_list(self):    
        if type(file_list) is list:
            self.files_list = [f for files in self.files_list for f in glob.glob(files)]
        else:
            "RAISE LIST ERROR"
    
    def get_paths(self):    
        self.links_dir  = os.path.abspath(self.links_dir)
        self.files_list = [os.path.abspath(f) for f in self.files_list]

'''
                
        self.linkdirectives_list = []
        for f in self.links_files:
            lines = input_to_array(f)
            for line in lines:
                directive = LinkDirectives(line, self.links_dir)
                self.linkdirectives_list.append(directive)
    


    def issue_sys_command(self, logfile, quiet):        
        for link in self.linkdirectives_list:
            try:
                link.issue_sys_command(logfile, quiet)
            except:
                print_error(logfile)
    
    def link_files_and_dict(self, recur_lim):
        links_dict = {}
        for link in self.linkdirectives_list:
            links_dict = link.add_to_dict(links_dict)
        
        links = links_dict.values()
        sorted_files = [ f for f in links if os.path.isfile(f) ]
        if recur_lim > 1:
            dirs = [ d for d in links if os.path.isdir(d) ]
            for d in dirs:
                new_files = files_list(d, recur_lim - 1)
                sorted_files = sorted_files + new_files
        elif not recur_lim:
            dirs = [ d for d in links if os.path.isdir(d) ]
            for d in dirs:
                new_files = files_list(d, recur_lim)
                sorted_files = sorted_files + new_files
        sorted_files.sort()
            
        return sorted_files, links_dict
            
'''
      
    

