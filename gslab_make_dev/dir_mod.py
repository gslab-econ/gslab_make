#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import subprocess
import zipfile
import time

import private.metadata as metadata
import private.messages as messages

from private.exceptionclasses import CustomError, CritError, SyntaxError, LogicError
from private.utility import norm_path


def check_os():
    """ Check OS is either POSIX or NT. 
    
    Returns
    -------
    None
    """

    if (os.name != 'posix') & (os.name != 'nt'):
        raise CritError(messages.crit_error_unknown_system % os.name)


def remove_path(path, option = '', quiet = False):
    """ Remove path using shell command specified in metadata.
    
    Parameters
    ----------
    path : str
        Path to remove.
    option : str, optional
        Options for shell command. Defaults to options specified in metadata.
    quiet : bool, optional
        Suppress printing of paths removed. Defaults to False. 

    Returns
    -------
    None
    """

    path = norm_path(path)
    if not option:
        option = metadata.default_options[os.name]['rmdir']

    command = metadata.commands[os.name]['rmdir'] % (option, path)
    subprocess.Popen(command, shell = True)

    if not quiet:
        print('\nDeleted: "%s"' % path)
    

def clear_dir(dir_list):
    """ Remove everything in directory. Create directory if nonexistent.
    
    Parameters
    ----------
    dir_list : list
        List of directories to clear.

    Returns
    -------
    None
    """

    if type(dir_list) is list:
        dir_list = [norm_path(dir_path) for dir_path in dir_list]
    else:
        raise TypeError(messages.syn_error_file_list)
    
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
    """ Unzip file to directory.
    
    Parameters
    ----------
    zip_path : str
        Path of file to unzip.
    output_dir : str
        Directory to write outputs of unzipped file.

    Returns
    -------
    None
    """

    with zipfile.ZipFile(zip_path, allowZip64 = True) as z:
        z.extractall(output_dir)


def zip_dir(source_dir, zip_dest):
    """ Zip directory to file.
    
    Parameters
    ----------
    source_dir : str
        Path of directory to zip.
    zip_dest : str
        Destination of zip file.

    Returns
    -------
    None
    """

    with zipfile.ZipFile('%s' % (zip_dest), 'w', zipfile.ZIP_DEFLATED, allowZip64 = True) as z:
        source_dir = norm_path(source_dir)

        for root, dirs, files in os.walk(source_dir):
            for f in files:
                file_path = os.path.join(root, f)
                file_name = os.path.basename(file_path)
                
                print('Zipped: "%s" as "%s"' % (file_path, file_name))
                z.write(file_path, file_name)