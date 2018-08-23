#! /usr/bin/env python
import sys
import subprocess
import shutil
import os
import datetime
import re
import string

import private.messages as messages
import private.metadata as metadata
from private.preliminaries import print_error, files_list
from dir_mod import delete_files, list_directory
from private.exceptionclasses import CustomError, CritError, SyntaxError, LogicError


def set_option(**kwargs):\
    kwargs = {re.sub('_file$|_dir$', '', k):v for k, v in kwargs.items()}

    if len(kwargs.keys()) != len(set(kwargs.keys())):
        raise SyntaxError(messages.syn_error_options)      

    for key in metadata.settings.keys():
        root = re.sub('_file$|_dir$', '', k) 
        if root in kwargs.keys():
            metadata.settings[key] = kwargs[root]


def start_makelog(makelog = metadata.settings['makelog_file']):
    metadata.makelog_started = True
    makelog = norm_path(makelog)
    print('Starting makelog file at: "%s"' % makelog)
    
    try:
        MAKELOG = open(makelog, 'wb')
    except Exception as error:
        raise CritError((messages.crit_error_log % makelog) + '\n' + str(error))
        
    time_start = datetime.datetime.now().replace(microsecond = 0)
    working_dir = os.getcwd()
    print >> MAKELOG, messages.note_dash_separator + '\n'
    print >> MAKELOG, messages.note_makelog_start, time_start, '\n'
    print >> MAKELOG, messages.note_working_directory, working_dir, '\n'
    print >> MAKELOG, messages.note_dash_separator + '\n'
    MAKELOG.close()


def end_makelog(makelog = metadata.settings['makelog_file']):
    makelog = norm_path(makelog)
    print('Ending makelog file at: "%s"' % makelog)

    if not (metadata.makelog_started and os.path.isfile(makelog)):
        raise CritError(messages.crit_error_no_makelog % makelog)

    try:
        MAKELOG = open(makelog, 'ab')
    except Exception as errmsg:
        raise CritError((messages.crit_error_log % makelog) + '\n' + str(error))
       
    time_end = datetime.datetime.now().replace(microsecond = 0)
    working_dir = os.getcwd()
    print >> MAKELOG, messages.note_dash_separator + '\n'
    print >> MAKELOG, messages.note_makelog_end, time_end + '\n'
    print >> MAKELOG, messages.note_working_directory, working_dir, '\n'
    print >> MAKELOG, messages.note_dash_separator + '\n'
    MAKELOG.close()

def make_output_logs(output_dir = metadata.settings['output_file'],
                     statslog_file = metadata.settings['statslog_file'], 
                     headslog_file = metadata.settings['headslog_file'],
                     recur = float('inf')):

    output_files = glob_recur(output_dir, recur)

    if statslog_file:
        statslog_file = norm_path(statslog_file)
        write_stats_log(statslog_file, output_files)
    
    if headslog_file:
        headslog_file = norm_path(headslog_file)
        write_heads_log(headslog_file, output_files)
    

def write_stats_log (stats_file, output_files):
    header = "file name\tlast modified\tfile size"
    
    with open(stats_path, 'wb') as STATSLOG:
        print >> STATSFILE, header        

        for file_name in output_files:
            stats = os.stat(file_name)
            last_mod = datetime.datetime.utcfromtimestamp(round(stats.st_mtime))
            file_size = stats.st_size

            print >> STATSFILE, "%s\t%s\t%s" % (file_name, last_mod, file_size)


def write_heads_log(headslog_file, output_files, num_lines = 10):
    header = "File headers"

    with open(headslog_path, 'wb') as HEADSLOG:      
        print >> HEADSLOG, header
        print >> HEADSLOG, '\n' + messages.note_dash_separator + '\n'
        
        for file_name in output_files:
            print >> HEADSLOG, "%s\n" % file_name
            
            try:
                with open(file_name, 'wb') as f:
                    for i in range(num_lines):
                        line = f.next().strip()
                        cleaned_line = filter(lambda x: x in string.printable, line)
                        print >> HEADSFILE, cleaned_line
            except:
                print >> HEADSLOG, "Head not readable"

            print >> HEADSFILE, '\n' + messages.note_dash_separator + '\n'
