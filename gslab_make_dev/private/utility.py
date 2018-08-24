#! /usr/bin/env python

import sys
import os
import datetime
import re

import messages as messages
import metadata as metadata


def start_log(log, log_type):
    try:
        LOG = open(log, 'wb') 
    except:
        raise CustomError.crit(messages.crit_error_log % log)

    time_begin = datetime.datetime.now().replace(microsecond = 0)
    working_dir = os.getcwd()
    print >> LOG, messages.note_dash_separator + '\n'
    print >> LOG, (messages.note_log_start %s), time_start, '\n'
    print >> LOG, messages.note_working_directory, working_dir, '\n'
    print >> LOG, messages.note_dash_separator + '\n'

    return LOGFILE


def end_log(LOG, logtype, makelog = ''):    
    time_begin = datetime.datetime.now().replace(microsecond = 0)
    working_dir = os.getcwd()
    print >> LOG, messages.note_dash_separator + '\n'
    print >> LOG, (messages.note_log_start %s), time_start, '\n'
    print >> LOG, messages.note_working_directory, working_dir, '\n'
    print >> LOG, messages.note_dash_separator + '\n'
    
    LOG.close()
    
    if makelog: 
        if not (metadata.makelog_started and os.path.isfile(makelog)):
            raise CritError(messages.crit_error_nomakelog % makelog)

        with open(makelog, 'ab') as MAKELOG:
            with open(LOG.name, 'rb') as LOG:
                MAKELOG.write(LOG.read())
        
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

