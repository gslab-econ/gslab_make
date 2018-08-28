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

def start_log(log, log_type):
    log = norm_path(log)

    try:
        LOG = open(log, 'w') 
    except:
        raise CustomError.crit(messages.crit_error_log % log)

    time_start = str(datetime.datetime.now().replace(microsecond = 0))
    working_dir = os.getcwd()
    print(messages.note_dash_separator + '\n', file = LOG)
    print(messages.note_log_start % log_type + time_start + '\n', file = LOG)
    print(messages.note_working_directory + working_dir + '\n', file = LOG)
    print(messages.note_dash_separator + '\n', file = LOG)

    return LOG


def end_log(LOG, log_type, makelog):    
    makelog = norm_path(makelog)

    time_end = str(datetime.datetime.now().replace(microsecond = 0))
    working_dir = os.getcwd()
    print(messages.note_dash_separator + '\n', file = LOG)
    print(messages.note_log_end % log_type + time_end + '\n', file = LOG)
    print(messages.note_working_directory + working_dir + '\n', file = LOG)
    print(messages.note_dash_separator + '\n', file = LOG)
    
    LOG.close()
    
    if makelog: 
        if not (metadata.makelog_started and os.path.isfile(makelog)):
            raise CritError(messages.crit_error_no_makelog % makelog)

        with open(makelog, 'a') as MAKELOG:
            with open(LOG.name, 'r') as LOG:
                MAKELOG.write(LOG.read())
        
        os.remove(LOG.name)


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

