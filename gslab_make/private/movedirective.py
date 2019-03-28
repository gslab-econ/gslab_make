#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import traceback
import re
import glob
from itertools import chain
import subprocess

from gslab_make.private.exceptionclasses import CritError
import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.utility import norm_path, file_to_array, check_duplicate


class MoveDirective(object):
    """ 
    Directive for creating symbolic link or copy of data.
    
    Notes
    -----
    Parse line of text containing linking/copying instructions and represent as directive.
    Takes glob-style wildcards.
    
    Parameters
    ----------
    line_raw : str
        Raw text of linking/copying instructions (used for error messaging).
    line : str
        Line of text containing linking/copying instructions.
    move_dir : str
        Directory to write symlink/copy.
    osname : str, optional
        Name of OS. Defaults to `os.name`.

    Attributes
    ----------
    source : list
        List of sources parsed from line.
    destination : list
        List of destinations parsed from line.
    move_list : list
        List of (source, destination) mappings parsed from line.
    """
    
    def __init__(self, raw, line, move_dir, osname = os.name):
        self.raw      = raw
        self.line     = line
        self.move_dir = move_dir
        self.osname   = osname
        self.check_os()
        self.get_paths()
        self.check_paths()
        self.get_move_list()

    def check_os(self):
        """ Check OS is either POSIX or NT.  
                
        Returns
        -------
        None
        """      
        
        if self.osname not in {'posix', 'nt'}:
            raise CritError(messages.crit_error_unknown_system % self.osname)

    def get_paths(self):
        """ Parse sources and destinations from line. 
                
        Returns
        -------
        None
        """
        
        try:
            self.line = self.line.strip().split('|')
            self.line = [l.strip() for l in self.line]
            self.line = [l.strip('"\'') for l in self.line]
            self.destination, self.source = self.line
        except:
            error_message = messages.crit_error_bad_link % self.line_raw
            error_message = error_message + '\n' + traceback.format_exc().splitlines()[-1]
            raise CritError(error_message)

        self.source = norm_path(self.source)
        self.destination = norm_path(os.path.join(self.move_dir, self.destination))

    def check_paths(self):
        """ Check sources and destination exist and have same number of wildcards. 
                
        Returns
        -------
        None
        """
    
        if re.findall('\*', self.source) != re.findall('\*', self.destination):
            raise SyntaxError(messages.syn_error_wildcard)
        
        if re.search('\*', self.source):
            if not glob.glob(self.source):
                raise CritError(messages.crit_error_no_path_wildcard % self.source)
        else:
            if not os.path.exists(self.source):
                raise CritError(messages.crit_error_no_path % self.source)   

    def get_move_list(self):
        """ Interpret wildcards to get list of paths that meet criteria. 
                
        Returns
        -------
        None
        """
    
        if re.match('\*', self.source):
            self.source_list  = glob.glob(self.source)
            self.destination_list = [extract_wildcards(t) for t in self.source_list]
            self.destination_list = [fill_in_wildcards(s) for s in self.destination_list]
        else:
            self.source_list  = [self.source]
            self.destination_list = [self.destination]

        self.move_list = list(zip(self.source_list, self.destination_list))

    def extract_wildcards(self, f):
        """ Extract wildcard characters from source path.
    
        Notes
        -----
        Suppose path `foo.py` and glob pattern `*.py`. 
        The wildcard characters would therefore be `foo`.
        
        Parameters
        ----------
        f : str
           Source path from which to extract wildcard characters.
           
        Returns
        -------
        wildcards : iter
           Iterator of extracted wildcard characters.
        """
        
        regex = self.source.split('*')
        regex = '(.*)'.join(regex) 

        wildcards = re.findall(regex, f)
        wildcards = [(w, ) if isinstance(w, str) else w for w in wildcards]
        wildcards = chain(*wildcards)

        return wildcards

    def fill_in_wildcards(self, wildcards):
        """ Fill in wildcards for destination path.
        
        Notes
        -----
        Use extracted wildcard characters from a source path to create 
        corresponding destination path.
    
        Parameters
        ----------
        wildcards: iterator
           Extracted wildcard characters (returned from `extract_wildcards`).
        
        Returns
        -------
        f : str
           Destination path 
        """
        
        f = self.destination
        for wild in wildcards:
            f = re.sub('\*', wild, f, 1)

        return f

    def create_symlinks(self):
        """ Create symlinks. 
                
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        
        if self.osname == 'posix':
            self.move_posix(type = 'link')
        elif self.osname == 'nt':
            self.move_nt(type = 'link')

        return(self.move_list)

    def create_copies(self):
        """ Create copies. 
                
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        
        if self.osname == 'posix':
            self.move_posix(type = 'copy')
        elif self.osname == 'nt':
            self.move_nt(type = 'copy')

        return(self.move_list)

    def move_posix(self, movetype):   
        """ Create symlinks/copies using POSIX shell command specified in metadata.  
        
        Parameters
        ----------
    	movetype : str
        	Type of file movement. Takes either `copy` or `symlink`. 

        Returns
        -------
        None
        """
    
        for source, destination in self.move_list:
            if movetype == 'copy':
                duplicate = check_duplicate(source, destination)
                if not duplicate:
                    command = metadata.commands[self.osname]['makecopy'] % (source, destination)
            elif movetype == 'symlink':
                command = metadata.commands[self.osname]['makelink'] % (source, destination)
            subprocess.Popen(command, shell = True)

    def move_nt(self, movetype):   
        """ Create symlinks/copies using NT shell command specified in metadata. 
        
        Parameters
        ----------
    	movetype : str
        	Type of file movement. Takes either `copy` or `symlink`. 

        Returns
        -------
        None
        """
        for source, destination in self.move_list:
            if os.path.isdir(source):
                directory = '/d'
            else:
                directory = ''

            if movetype == 'copy':
                duplicate = check_duplicate(source, destination)
                if not duplicate:
                    command = metadata.commands[self.osname]['makecopy'] % (source, destination)
            elif movetype == 'symlink':
                command = metadata.commands[self.osname]['makelink'] % (directory, destination, source)
            subprocess.Popen(command, shell = True)


class MoveList(object):
    """ 
    List of move directives.
    
    Notes
    -----
    Parse files containing linking/copying instructions and represent as move directives.
    
    Parameters
    ----------
    file_list : list
        List of files from which to parse linking/copying instructions.
    move_dir : str
        Directory to write symlink/copy.
    mapping_dict : dict, optional
        Dictionary of path mappings used to parse linking/copying instructions. 
        Defaults to no mappings.
        
    Attributes
    ----------
    move_directive_list : list
        List of move directives.   
    """
    
    def __init__(self, 
                 file_list, 
                 move_dir, 
                 mapping_dict = {}):
        
        self.file_list    = file_list
        self.move_dir     = move_dir
        self.mapping_dict = mapping_dict
        self.move_type    = move_type
        self.parse_file_list()
        self.get_paths()
        self.get_move_directive_list()

    def parse_file_list(self): 
        """ Parse wildcards in list of files. 
                
        Returns
        -------
        None
        """
        
        if type(self.file_list) is not list:
            raise TypeError(messages.type_error_file_list % self.file_list)

        file_list_parsed = [f for file in self.file_list for f in glob.glob(file)]   
        if file_list_parsed:
            self.file_list = file_list_parsed
        else:
            error_list = [str(f) for f in self.file_list]
            raise CritError(messages.crit_error_no_files % error_list) 

    def get_paths(self):    
        """ Normalize paths. 
                
        Returns
        -------
        None
        """
        
        self.move_dir  = norm_path(self.move_dir)
        self.file_list = [norm_path(f) for f in self.file_list]

    def get_move_directive_list(self):
        """ Parse list of files to create symlink directives. 
                
        Returns
        -------
        None
        """
        
        lines = [line for file in self.file_list for line in file_to_array(file)]
        lines = [(l, l) for l in lines]
        try:
            lines = [(raw, str(line).format(**self.mapping_dict)) for (raw, line) in lines]
        except KeyError as e:
            error_message = messages.crit_error_bad_move % messages.crit_error_path_mapping % str(e).strip("'")
            error_message = error_message + '\n' + traceback.format_exc().splitlines()[-1]
            raise CritError(error_message)
			
        self.move_directive_list = [MoveDirective(raw, line, self.move_dir) for (raw, line) in lines]

    def create_symlinks(self):       
        """ Create symlinks according to directives. 
        
        Returns
        -------
        move_map : list
            List of (source, destination) for each symlink created.
        """
        
        move_map = []
        for move in self.move_directive_list:
            move_map.extend(move.create_symlinks)
            
        return move_map

    def create_copies(self):       
        """ Create copies according to directives. 
        
        Returns
        -------
        move_map : list
            List of (source, destination) for each copy created.
        """
        
        move_map = []
        for move in self.move_directive_list:
            move_map.extend(move.create_copies)
            
        return move_map