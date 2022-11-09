# -*- coding: utf-8 -*-
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import sys
import os
import io
import datetime
import traceback
import subprocess

from termcolor import colored
import colorama
colorama.init()

import gslab_make.private.messages as messages
import gslab_make.private.metadata as metadata
from gslab_make.private.exceptionclasses import ColoredError
from gslab_make.private.utility import norm_path, get_path, glob_recursive, format_message
from gslab_make.write_logs import write_to_makelog, _write_heads_log

def write_version_logs(paths):
    """.. Makes sure that the repository is being run with conda and is up to date.
    Checks that conda is activated. 
    Produces warning if it is not. 
    Produces warning if setup/conda_env.yaml has been altered more recently than the .
    Parameters
    ----------
    root : str 
        Directory of root.
    Returns
    -------
    None 
    """
    try:
        versions_log = get_path(paths, 'versions_log')
        python_executable = sys.executable
     # Check if currently in a conda env
        if 'conda' in python_executable:
            if "active environment : None" not in str(subprocess.run(['conda', 'info'], capture_output=True)):  
                conda_list= subprocess.run(['conda', 'list'], capture_output=True, text=True).stdout
                versions_log = norm_path(versions_log)

                with io.open(versions_log, 'w', encoding = 'utf8', errors = 'ignore') as CONDALOG:
                    time_start = str(datetime.datetime.now().replace(microsecond = 0))
                    print(messages.note_dash_line, file = CONDALOG)
                    print("Versions log started: " + time_start, file = CONDALOG)
                    print(messages.note_dash_line, file = CONDALOG)
                    print(conda_list, file = CONDALOG)

                message = 'Version logs successfully written!'
                write_to_makelog(paths, message)  
                print(colored(message, metadata.color_success)) 
            else:
                message = 'Conda environment is not activated. Please activate the environment'
                raise ColoredError(message)

    except:
        error_message = 'Error with `write_version_logs`. Traceback can be found below.' 
        error_message = format_message(error_message) 
        write_to_makelog(paths, error_message + '\n\n' + traceback.format_exc())
        raise ColoredError(error_message, traceback.format_exc())             
             
__all__ = ['write_version_logs']