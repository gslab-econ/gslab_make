#! /usr/bin/env python

import os
import re
import glob
from itertools import chain
import subprocess

from exceptionclasses import CritError, SyntaxError
import messages as messages
import metadata as metadata
from utility import norm_path, file_to_array

class LinkDirective(object):

    def __init__(self, line, link_dir):
        self.osname    = os.name
        self.line      = line
        self.link_dir  = link_dir
        self.check_os()
        self.get_paths()
        self.check_paths()
        self.get_link_list()

    def check_os(self):
        if (self.osname != 'posix') & (self.osname != 'nt'):
            raise CritError(messages.crit_error_unknown_system % self.osname)

    def get_paths(self):
        try:
            self.line = self.line.strip().split('\t')
            self.line = [l.strip() for l in self.line]
            self.symlink, self.target = self.line
        except:
            raise CritError(messages.crit_error_bad_link % self.line)

        self.target = norm_path(self.target)
        self.symlink = norm_path(os.join(self.link_dir, self.symlink))

    def check_paths(self):
        if re.findall('\*', self.target)!= re.findall('\*', self.symlink):
            raise SyntaxError(messages.syn_error_wildcard)
        
        if re.search('\*', self.target):
            if not glob.glob(self.target):
                raise CritError(messages.crit_error_no_file_wildcard % self.target)
        else:
            if not os.path.isfile(self.target):
                raise CritError(messages.crit_error_no_file % self.target)   

    def get_link_list(self):
        """
        Convert wildcard paths to list of absolute paths that meet wildcard criteria
        """
    
        if re.match('\*', self.target):
            self.target_list  = glob.glob(self.target)

            self.symlink_list = [parse_wildcards(t) for t in self.target_list]
            self.symlink_list = [fill_in_wildcards(s) for s in self.symlink_list]

        else:
            self.target_list  = list(self.target)
            self.symlink_list = list(self.symlink)

        self.link_list = zip(self.target_list, self.symlink_list)

    def parse_wildcards(self, f):
        regex = self.target.split('*')
        regex = '(.*)'.join(regex) 

        wildcards = re.findall(regex, f)
        wildcards = [(w, ) if isinstance(w, str) else w for w in wildcards]
        wildcards = chain(*wildcards)

        return(wildcards)

    def fill_in_wildcards(self, wildcards):
        f = self.symlink
        for wild in wildcards:
            f = re.sub('\*', wild, f, 1)

        return(f)

    def create_symlinks(self):
        if self.osname == 'posix':
            self.create_symlinks_posix()
        elif self.osname == 'nt':
            self.create_symlinks_nt()

        return(self.link_list)
   
    def create_symlinks_posix(self):   
        for target, symlink in self.link_list:
            command = metadata.commands[self.osname]['makelink'] % (target, symlink)
            subprocess.Popen(command.split())

    def create_symlinks_nt(self):   
        for target, symlink in self.link_list:
            if os.path.isdir(target):
                directory = '/d'
            else:
                directory = ''

            command = metadata.commands[self.osname]['makelink'] % (directory, target, symlink)
            subprocess.Popen(command.split())


class LinksList(object):

    def __init__(self, 
                 file_list, 
                 link_dir = metadata.settings['link_dir']):
        
        self.file_list
        self.link_dir = link_dir
        self.parse_file_list()
        self.get_paths()
        self.get_link_directive_list()
        self.make_symlinks()

    def parse_file_list(self):    
        if type(self.file_list) is list:
            self.file_list = [f for file in self.file_list for f in glob.glob(file)]
        else:
            raise SyntaxError(messages.syn_error_file_list)
    
    def get_paths(self):    
        self.links_dir  = norm_path(self.links_dir)
        self.files_list = [norm_path(f) for f in self.files_list]
         
    def get_link_directive_list(self):
        self.link_directive_list = []

        for f in self.links_files:
            lines = file_to_array(f)
            for line in lines:
                directive = LinkDirectives(line, self.links_dir)
                self.linkdirectives_list.append(directive)

    def make_symlinks(self):        
        link_map = []
        for link in self.linkdirectives_list:
            link_map.append(link.create_symlinks())
            
        return(link_map)
        
        