#! /usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import os
import datetime
import re
import string
import traceback

import gslab_make_dev.private.messages as messages
import gslab_make_dev.private.metadata as metadata
from gslab_make_dev.private.exceptionclasses import CritError
from gslab_make_dev.private.utility import norm_path, glob_recursive, format_error


def set_option(**kwargs):
    """ Set global options. See metadata for default options. 
    
    Returns
    -------
    None
    """

    options = {re.sub('_file$|_dir$', '', k):v for k, v in kwargs.items()}

    if len(options.keys()) != len(kwargs.keys()):
        error = format_error(messages.syn_error_options)
        raise SyntaxError(error)      

    for key in metadata.settings.keys():
        root = re.sub('_file$|_dir$', '', key) 
        if root in options.keys():
            metadata.settings[key] = options[root]


def start_makelog(makelog = metadata.settings['makelog']):
    """ Start make log. Record start time.

    Notes
    -----
    The make log start condition is needed by other functions to confirm a 
    make log exists.

    Parameters
    ----------
    makelog : str, optional
        Path to write make log. Defaults to path specified in metadata.

    Returns
    -------
    None
    """

    metadata.makelog_started = True
    makelog = norm_path(makelog)
    print('Starting makelog file at: "%s"' % makelog)
    
    try:
        MAKELOG = open(makelog, 'w')
    except:
        error = (messages.crit_error_log % makelog) + '\n' + traceback.format_exc()
        error = format_error(error)
        raise CritError(error)
        
    time_start = str(datetime.datetime.now().replace(microsecond = 0))
    working_dir = os.getcwd()
    print(messages.note_dash_line, file = MAKELOG)
    print(messages.note_makelog_start + time_start, file = MAKELOG)
    print(messages.note_working_directory + working_dir, file = MAKELOG)
    print(messages.note_dash_line, file = MAKELOG)
    MAKELOG.close()


def end_makelog(makelog = metadata.settings['makelog']):
    """ End make log. Record end time.

    Parameters
    ----------
    makelog : str, optional
        Path of started make log. Defaults to path specified in metadata.

    Returns
    -------
    None
    """
 
    makelog = norm_path(makelog)
    print('Ending makelog file at: "%s"' % makelog)

    if not (metadata.makelog_started and os.path.isfile(makelog)):
        error = format_error(messages.crit_error_no_makelog % makelog)
        raise CritError(error)

    try:
        MAKELOG = open(makelog, 'a')
    except:
        error = (messages.crit_error_log % makelog) + '\n' + traceback.format_exc()
        error = format_error(error)
        raise CritError(error)
       
    time_end = str(datetime.datetime.now().replace(microsecond = 0))
    working_dir = os.getcwd()
    print(messages.note_dash_line, file = MAKELOG)
    print(messages.note_makelog_end + time_end, file = MAKELOG)
    print(messages.note_working_directory + working_dir, file = MAKELOG)
    print(messages.note_dash_line, file = MAKELOG)
    MAKELOG.close()
    
    
def write_to_makelog(message, makelog = metadata.settings['makelog']):
    """ Append message to make log.

    Parameters
    ----------
    message : str
        Message to append.
    makelog : str, optional
        Path of started make log. Defaults to path specified in metadata.

    Returns
    -------
    None
    """

    makelog = norm_path(makelog)

    if not (metadata.makelog_started and os.path.isfile(makelog)):
        error = format_error(messages.crit_error_no_makelog % makelog)
        raise CritError(error)

    try:
        MAKELOG = open(makelog, 'a')
    except:
        error = (messages.crit_error_log % makelog) + '\n' + traceback.format_exc()
        error = format_error(error)
        raise CritError(error)
        
    print(message, file = MAKELOG)
    MAKELOG.close()
    
    
def write_output_logs(output_dir = metadata.settings['output_dir'],
                      output_statslog = metadata.settings['output_statslog'], 
                      output_headslog = metadata.settings['output_headslog'],
                      recursive = float('inf')
                      makelog = makelog = metadata.settings['makelog']):
    """ Write output logs.

    Notes
    -----
    The following information is logged of all files contained in output directory:
        * File name (output statistics log)
        * Last modified (output statistics log)
        * File size (output statistics log)
        * File head (output headers log)
    * When walking through output directory, recursive determines depth.

    Parameters
    ----------
    output_dir : str, optional
        Path of output directory. Defaults to path specified in metadata.
    output_statslog : str, optional
        Path to write output statistics log. Defaults to path specified in metadata.
    output_headslog : str, optional
        Path to write output headers log. Defaults to path specified in metadata.
    recursive : int, optional
        Level of depth when walking through output directory.
    makelog : str, optional
        Path of makelog. Defaults to path specified in metadata.

    Returns
    -------
    None
    """

    output_files = glob_recursive(output_dir, recursive)

    if output_statslog:
        output_statslog = norm_path(output_statslog)
        write_stats_log(output_statslog, output_files)
    
    if output_headslog:
        output_headslog = norm_path(output_headslog)
        write_heads_log(output_headslog, output_files)
    
    write_to_makelog('Output logs successfully written!', makelog)  
        
    s
def write_stats_log (statslog_file, output_files):
    """ Write statistics log.
   
    Notes
    -----
    The following information is logged of all output files:
        * File name 
        * Last modified 
        * File size

    Parameters
    ----------
    statslog_file : str
        Path to write statistics log. 

    output_files : list
        List of output files to log statistics.

    Returns
    -------
    None
    """

    header = "file name\tlast modified\tfile size"
    
    with open(statslog_file, 'w') as STATSLOG:
        print(header, file = STATSLOG)      

        for file_name in output_files:
            stats = os.stat(file_name)
            last_mod = datetime.datetime.utcfromtimestamp(round(stats.st_mtime))
            file_size = stats.st_size

            print("%s\t%s\t%s" % (file_name, last_mod, file_size), file = STATSLOG)


def write_heads_log(headslog_file, output_files, num_lines = 10):
    """ Write headers log.

    Parameters
    ----------
    headslog_file : str
        Path to write headers log. 

    output_files : list
        List of output files to log headers.

    num_lines: int, optional
        Number of lines for headers. Default is 10.

    Returns
    -------
    None
    """

    header = "File headers"

    with open(headslog_file, 'w') as HEADSLOG:      
        print(header, file = HEADSLOG)
        print(messages.note_dash_line, file = HEADSLOG)
        
        for file_name in output_files:
            print("%s" % file_name, file = HEADSLOG)
            print(messages.note_dash_line, file = HEADSLOG)
            
            try:
                with open(file_name, 'r') as f:
                    for i in range(num_lines):
                        line = f.next().strip()
                        cleaned_line = filter(lambda x: x in string.printable, line)
                        print(cleaned_line, file = HEADSLOG)
            except:
                print("Head not readable or less than %s lines" % num_lines, file = HEADSLOG)

            print(messages.note_dash_line, file = HEADSLOG)
