#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import datetime
import re
import glob

from private.exceptionclasses import CustomError, CritError
import private.messages as messages
import private.metadata as metadata


def norm_path(path):
    """ Normalizes path to be OS-compatible. """

    path = re.split('[/\\\\]+', path)
    path = os.path.sep.join(path)
    path = path.rstrip(os.path.sep)
    path = os.path.abspath(path)

    return path


def glob_recursive(path, recursive):
    """ Walks through path. 
    
    Notes
    -----
    Takes glob-style wildcards.

    Parameters
    ----------
    path : str
        Path to walk through.
    recursive : int
        Level of depth when walking through path.

    Returns
    -------
    path_files : list
        List of files contained in path.
    """

    path = norm_path(path)
    path_files = []

    i = 0 
    while i <= recursive:          
        path = os.path.join(path, "*")
        glob_files = glob.glob(path)
        if glob_files:
            path_files.extend(glob.glob(path)) 
            i += 1
        else:
            break

    return path_files

 
def file_to_array(file_name):
    """ Read file and extract lines to list. 

    Parameters
    ----------
    file_name : str
        Path of file to read.

    Returns
    -------
    array : list
        List of lines contained in file.
    """
    
    
    if not os.path.isfile(file_name):
        raise CritError(messages.crit_error_file % file_name)        

    with open(file_name, 'r') as f:
        array = [line for line in f if not re.match('\s*\#',line)]
                                                    
    return array

