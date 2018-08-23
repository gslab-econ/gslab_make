#! /usr/bin/env python

import sys
import os
import datetime
import re

import messages as messages
import metadata as metadata

from exceptionclasses import *

#== Logging ===============================================
def start_logging(log, logtype):
    try:
        LOGFILE = open(log, 'wb') 
    except:
        raise CustomError.crit(messages.crit_error_log % log)

    time_begin = datetime.datetime.now().replace(microsecond = 0)
    orig_stderr = sys.stderr
    sys.stderr = LOGFILE
    working_dir = os.getcwd()
    print >> LOGFILE, messages.note_logstart % logtype, time_begin, working_dir
    return LOGFILE


def end_logging(LOGFILE, makelog, logtype):
    time_end = datetime.datetime.now().replace(microsecond=0)
    print >> LOGFILE, messages.note_logend % logtype,time_end
    LOGFILE.close()
    if not makelog: return
    if not (metadata.makelog_started and os.path.isfile(makelog)):
        raise CritError(messages.crit_error_nomakelog % makelog)
    MAKE_LOGFILE = open(makelog, 'ab')
    MAKE_LOGFILE.write( open(LOGFILE.name, 'rU').read() )
    MAKE_LOGFILE.close()
    os.remove(LOGFILE.name)


def norm_path(path):
    path = re.split('[/\\\\]+', path)
    path = os.path.join(*path)
    path = os.path.abspath(path)

    return(path)


def glob_recursive(path, recur):
    path = norm_path(output_dir)
    path_files = []

    i = 0 
    while i <= recur_lim:          
        path = os.join(path, "*")
        glob_files = glob.glob(path)
        if glob_files:
            path_files.append(glob.glob(path)) 
            i += 1
        else:
            break

    return(path_files)

def file_to_array(file_name):
    # Import file
    if not os.path.isfile(file_name)
        raise CritError(messages.crit_error_file % file_name)        

    with open(file_name, 'rb') as f:
        array = [line for line in f if not re.match('\s*\#',line)]
        return (array)

