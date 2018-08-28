#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import subprocess
import zipfile
import time

import gslab_make_dev.private.metadata as metadata
import gslab_make_dev.private.messages as messages

from gslab_make_dev.private.exceptionclasses import CustomError, CritError, SyntaxError, LogicError
from gslab_make_dev.private.utility import norm_path


def remove_path(path, option = '', quiet = False):
    path = norm_path(path)
    if not option:
        option = metadata.default_options[os.name]['rmdir']

    command = metadata.commands[os.name]['rmdir'] % (option, path)
    subprocess.Popen(command, shell = True)

    if not quiet:
        print('\nDeleted: "%s"' % path)
    

def clear_dir(dir_list):
    if type(dir_list) is list:
        dir_list = [norm_path(dir_path) for dir_path in dir_list]
    else:
        raise SyntaxError(messages.syn_error_file_list)
    
    for dir_path in dir_list:
        if os.path.isdir(dir_path):
            remove_path(dir_path, quiet = True)
        elif os.path.isfile(dir_path): 
            raise CritError(messages.crit_not_dir % dir_path)
        
    time.sleep(0.25) # Allow file manager to recognize files no longer exist
    
    for dir_path in dir_list:
        os.makedirs(dir_path)
        print('Cleared: "%s"' % dir_path) 
        

def unzip(zip_path, output_dir):
    with zipfile.ZipFile(zip_path, allowZip64 = True) as z:
        z.extractall(output_dir)


def zip_dir(source_dir, zip_dest):
    with zipfile.ZipFile('%s' % (zip_dest), 'w', zipfile.ZIP_DEFLATED, allowZip64 = True) as z:
        source_dir = norm_path(source_dir)

        for root, dirs, files in os.walk(source_dir):
            for f in files:
                file_path = os.path.join(root, f)
                file_name = os.path.basename(file_path)
                
                print('Zipped: "%s" as "%s"' % (file_path, file_name))
                z.write(file_path, file_name)