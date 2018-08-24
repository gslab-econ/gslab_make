#! /usr/bin/env python
import os
import datetime
import re
import string

import private.messages as messages
import private.metadata as metadata
from private.exceptionclasses import CritError, SyntaxError
from private.utility import norm_path, glob_recursive

def set_option(**kwargs):
    kwargs = {re.sub('_file$|_dir$', '', k):v for k, v in kwargs.items()}

    if len(kwargs.keys()) != len(set(kwargs.keys())):
        raise SyntaxError(messages.syn_error_options)      

    for key in metadata.settings.keys():
        root = re.sub('_file$|_dir$', '', key) 
        if root in kwargs.keys():
            metadata.settings[key] = kwargs[root]


def start_makelog(makelog = metadata.settings['makelog']):
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


def end_makelog(makelog = metadata.settings['makelog']):
    makelog = norm_path(makelog)
    print('Ending makelog file at: "%s"' % makelog)

    if not (metadata.makelog_started and os.path.isfile(makelog)):
        raise CritError(messages.crit_error_no_makelog % makelog)

    try:
        MAKELOG = open(makelog, 'ab')
    except Exception as error:
        raise CritError((messages.crit_error_log % makelog) + '\n' + str(error))
       
    time_end = datetime.datetime.now().replace(microsecond = 0)
    working_dir = os.getcwd()
    print >> MAKELOG, messages.note_dash_separator + '\n'
    print >> MAKELOG, messages.note_makelog_end, time_end + '\n'
    print >> MAKELOG, messages.note_working_directory, working_dir, '\n'
    print >> MAKELOG, messages.note_dash_separator + '\n'
    MAKELOG.close()

def make_output_logs(output_dir = metadata.settings['output_dir'],
                     output_statslog = metadata.settings['output_statslog'], 
                     output_headslog = metadata.settings['output_headslog'],
                     recur = float('inf')):

    output_files = glob_recursive(output_dir, recur)

    if output_statslog:
        output_statslog = norm_path(output_statslog)
        write_stats_log(output_statslog, output_files)
    
    if output_headslog:
        output_headslog = norm_path(output_headslog)
        write_heads_log(output_headslog, output_files)
    

def write_stats_log (statslog_file, output_files):
    header = "file name\tlast modified\tfile size"
    
    with open(statslog_file, 'wb') as STATSLOG:
        print >> STATSLOG, header        

        for file_name in output_files:
            stats = os.stat(file_name)
            last_mod = datetime.datetime.utcfromtimestamp(round(stats.st_mtime))
            file_size = stats.st_size

            print >> STATSLOG, "%s\t%s\t%s" % (file_name, last_mod, file_size)


def write_heads_log(headslog_file, output_files, num_lines = 10):
    header = "File headers"

    with open(headslog_file, 'wb') as HEADSLOG:      
        print >> HEADSLOG, header
        print >> HEADSLOG, '\n' + messages.note_dash_separator + '\n'
        
        for file_name in output_files:
            print >> HEADSLOG, "%s\n" % file_name
            
            try:
                with open(file_name, 'wb') as f:
                    for i in range(num_lines):
                        line = f.next().strip()
                        cleaned_line = filter(lambda x: x in string.printable, line)
                        print >> HEADSLOG, cleaned_line
            except:
                print >> HEADSLOG, "Head not readable"

            print >> HEADSLOG, '\n' + messages.note_dash_separator + '\n'
