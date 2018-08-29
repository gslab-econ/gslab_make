#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import datetime
import re
import glob

from gslab_make_dev.private.exceptionclasses import CustomError, CritError
import gslab_make_dev.private.messages as messages
import gslab_make_dev.private.metadata as metadata


def norm_path(path):
    path = re.split('[/\\\\]+', path)
    path = os.path.sep.join(path)
    path = path.rstrip(os.path.sep)
    path = os.path.abspath(path)

    return path


def glob_recursive(path, recur_lim):
    path = norm_path(path)
    path_files = []

    i = 0 
    while i <= recur_lim:          
        path = os.path.join(path, "*")
        glob_files = glob.glob(path)
        if glob_files:
            path_files.extend(glob.glob(path)) 
            i += 1
        else:
            break

    return path_files

 
def file_to_array(file_name):
    if not os.path.isfile(file_name):
        raise CritError(messages.crit_error_file % file_name)        

    with open(file_name, 'r') as f:
        array = [line for line in f if not re.match('\s*\#',line)]
        return array

